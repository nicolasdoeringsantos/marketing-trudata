"""Configuração local e consulta controlada de endereços via Geoapify.

A chave fica fora do projeto e da pasta servida por HTTP.
Resultados são candidatos para revisão, nunca aprovação automática de empresas.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from collections import deque
from threading import Lock
from datetime import datetime, timezone
from getpass import getpass
import hashlib
import json
import os
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
CONFIG = Path(os.environ.get('LOCALAPPDATA', Path.home() / '.config')) / 'TruData' / 'geolocalizacao.json'
CACHE = ROOT / 'geodata' / 'geoapify-candidatos.json'

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    for attempt in range(5):
        try:
            temp.replace(path)
            break
        except PermissionError:
            if attempt == 4:
                raise RuntimeError('O arquivo de resultados está em uso. Feche o programa que o mantém aberto e retome a consulta.') from None
            time.sleep(0.2 * (attempt + 1))

def api_key():
    value = os.environ.get('GEOAPIFY_API_KEY', '').strip()
    if value:
        return value
    if CONFIG.exists():
        return json.loads(CONFIG.read_text(encoding='utf-8')).get('api_key', '').strip()
    return ''

def query_address(client):
    # Não envia contatos, CNPJ, decisores, notas comerciais ou dados do CRM.
    return ', '.join(str(client.get(k) or '').strip() for k in ('endereco', 'cidade', 'uf', 'cep')) + ', Brasil'

def fetch(address, key):
    params = urlencode({'text': address, 'filter': 'countrycode:br', 'lang': 'pt', 'format': 'json', 'limit': 3, 'apiKey': key})
    request = Request('https://api.geoapify.com/v1/geocode/search?' + params, headers={'User-Agent': 'TruData-Location-Review/1.0'})
    try:
        with urlopen(request, timeout=30) as response:
            payload = json.load(response)
        if not isinstance(payload.get('results'), list):
            raise RuntimeError('Resposta inesperada do serviço. A base não foi alterada.')
        return payload['results']
    except HTTPError as exc:
        messages = {401: 'Chave recusada. Configure uma chave válida.', 403: 'Acesso recusado. Confira a chave e as restrições do projeto Geoapify.', 429: 'Limite de consultas atingido. Retome após a renovação da cota.'}
        raise RuntimeError(messages.get(exc.code, f'Serviço indisponível (HTTP {exc.code}). Retome mais tarde.')) from None
    except (OSError, ValueError):
        # Nunca imprima exceções de rede: elas podem incluir a URL com a chave.
        raise RuntimeError('Não foi possível consultar o serviço. Confira a conexão e retome mais tarde.') from None

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('acao', choices=['configurar', 'status', 'consultar'])
    parser.add_argument('--limite', type=int, default=25, help='Máximo de novas consultas nesta execução (1 a 663).')
    args = parser.parse_args()
    if args.acao == 'configurar':
        if not sys.stdin.isatty():
            raise RuntimeError('Execute configurar em um terminal interativo para inserir a chave sem exibi-la.')
        key = getpass('Cole a chave Geoapify (entrada oculta): ').strip()
        if not key or any(c.isspace() for c in key):
            raise RuntimeError('Chave vazia ou com espaços. Copie novamente no painel Geoapify.')
        write_json(CONFIG, {'provider': 'geoapify', 'api_key': key})
        print('Chave salva fora do projeto. Use consultar para testar o acesso.')
        return
    key = api_key()
    if args.acao == 'status':
        print('Chave configurada; acesso ainda depende de uma consulta.' if key else 'Geoapify ainda não configurado. Execute configurar em um terminal.')
        return
    if not 1 <= args.limite <= 663:
        raise RuntimeError('Use --limite entre 1 e 663.')
    if not key:
        raise RuntimeError('Configure a chave antes de consultar.')
    clients = json.loads((ROOT / 'base_clientes_regional.json').read_text(encoding='utf-8'))
    cache = json.loads(CACHE.read_text(encoding='utf-8')) if CACHE.exists() else {}
    pending = []
    for client in clients:
        if client.get('geolocalizacao', {}).get('status') == 'localizado':
            continue
        address = query_address(client)
        fingerprint = hashlib.sha256(address.encode('utf-8')).hexdigest()
        if cache.get(client['id'], {}).get('endereco_hash') != fingerprint:
            pending.append((client, address, fingerprint))
    pending = iter(pending[:args.limite])
    rate_lock = Lock()
    last_start = [0.0]
    def consult(item):
        with rate_lock:
            time.sleep(max(0, 0.5 - (time.monotonic() - last_start[0])))
            last_start[0] = time.monotonic()
        return item, fetch(item[1], key)
    count = 0
    # Até 3 consultas em andamento, no máximo 2 novas requisições/segundo.
    # Escrita do cache permanece serial; falhas não disparam a fila inteira.
    with ThreadPoolExecutor(max_workers=3) as pool:
        running = deque(pool.submit(consult, item) for _, item in zip(range(3), pending))
        while running:
            (client, address, fingerprint), results = running.popleft().result()
            cache[client['id']] = {'endereco_hash': fingerprint, 'endereco_consultado': address, 'consultado_em': datetime.now(timezone.utc).isoformat(), 'status': 'aguarda_revisao' if results else 'nao_encontrado', 'resultados': results, 'atribuicao': 'Powered by Geoapify', 'fontes': list({r.get('datasource', {}).get('attribution', '') for r in results})}
            write_json(CACHE, cache)
            count += 1
            print(f'{count}/{args.limite}: {client["id"]} — {len(results)} candidato(s).', flush=True)
            item = next(pending, None)
            if item is not None:
                running.append(pool.submit(consult, item))
    print(f'{count} novas consultas salvas. Resultados aguardam revisão; os pontos do radar foram preservados.')

if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError) as exc:
        # Apenas mensagens próprias; erros de arquivo não devem revelar conteúdo.
        print(str(exc) if isinstance(exc, RuntimeError) else 'Falha ao ler ou salvar a configuração local. Confira o arquivo e tente novamente.', file=sys.stderr)
        sys.exit(1)
