"""Operações comerciais locais, com persistência e validação no servidor."""
import copy
from datetime import date, datetime
import hashlib
import json
import math
from pathlib import Path
import sys
import threading
import time
import uuid

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'agente'))
sys.path.insert(0, str(ROOT / 'agente' / 'geodata'))
from configurar_geolocalizacao import api_key, fetch, query_address, write_json
from validar_geoapify import reason


def text(value, maximum=3000):
    if not isinstance(value, str) or len(value) > maximum:
        raise ValueError('Texto inválido ou muito longo. Revise os campos.')
    return value.strip()


def day(value):
    date.fromisoformat(value)
    return value


def amount(value):
    n = float(value)
    if not math.isfinite(n) or not 0 <= n <= 100000000:
        raise ValueError('Informe um valor entre zero e 100 milhões.')
    return round(n, 2)


class Commercial:
    def __init__(self, root=ROOT):
        self.root = Path(root)
        self.base = self.root / 'agente/base_clientes_regional.json'
        self.crm = self.root / 'painel_aprovacao/leads_crm.json'
        self.file = self.root / 'painel_aprovacao/comercial_registros.json'
        self.lock = threading.RLock()
        self.geo_lock = threading.Lock()
        self.previews = {}

    def read(self, path, default):
        return json.loads(path.read_text(encoding='utf-8')) if path.exists() else copy.deepcopy(default)

    def state(self):
        return self.read(self.file, {'visitas': [], 'contatos': {}, 'eventos': [], 'propostas': []})

    def data(self):
        with self.lock:
            return {'clientes': self.read(self.base, []), 'leads': self.read(self.crm, []), 'registros': self.state()}

    def find(self, items, ident):
        item = next((x for x in items if x['id'] == ident), None)
        if item is None:
            raise ValueError('Cadastro não encontrado. Atualize a página.')
        return item

    def event(self, state, typ, ident, details=''):
        state['eventos'].append({'id': uuid.uuid4().hex, 'tipo': typ, 'cliente_id': ident, 'data': datetime.now().isoformat(timespec='seconds'), 'detalhes': details})

    def preview(self, body):
        with self.lock:
            original = self.find(self.read(self.base, []), body.get('id'))
            candidate = dict(original)
            for k in ('endereco', 'cidade', 'uf', 'cep'):
                candidate[k] = text(body.get(k, ''), 300)
            if not candidate['endereco'] or not candidate['cidade'] or candidate['uf'] != 'RS':
                raise ValueError('Informe endereço, cidade e UF RS para consultar.')
            fingerprint = hashlib.sha256(json.dumps(original, sort_keys=True).encode()).hexdigest()
        key = api_key()
        if not key:
            raise ValueError('Geoapify não configurado. Configure a chave no servidor e tente novamente.')
        with self.geo_lock:
            results = fetch(query_address(candidate), key)
            time.sleep(.5)
        checked = [{'endereco': r.get('formatted', ''), 'lat': r.get('lat'), 'lon': r.get('lon'), 'motivo': reason(candidate, r), 'tipo': r.get('result_type')} for r in results]
        token = uuid.uuid4().hex
        with self.lock:
            self.previews = {k: v for k, v in self.previews.items() if time.time() - v['time'] < 1800}
            self.previews[token] = {'time': time.time(), 'candidate': candidate, 'results': results, 'fingerprint': fingerprint}
        return {'token': token, 'resultados': checked}

    def mutate(self, action, body):
        if action == 'consultar-endereco':
            return self.preview(body)
        with self.lock:
            state = self.state()
            if action == 'aplicar-endereco':
                preview = self.previews.get(body.get('token'))
                if not preview or time.time() - preview['time'] > 1800:
                    raise ValueError('A consulta expirou. Consulte o endereço novamente.')
                index = int(body.get('indice', -1))
                if not 0 <= index < len(preview['results']):
                    raise ValueError('Selecione um resultado.')
                r = preview['results'][index]
                if reason(preview['candidate'], r):
                    raise ValueError('Este resultado não tem precisão suficiente. Corrija o endereço e consulte novamente.')
                if body.get('confirmado') is not True:
                    raise ValueError('Confirme que o endereço corresponde à empresa ou filial.')
                clients = self.read(self.base, [])
                current = self.find(clients, preview['candidate']['id'])
                if hashlib.sha256(json.dumps(current, sort_keys=True).encode()).hexdigest() != preview['fingerprint']:
                    raise ValueError('O cadastro mudou. Atualize e consulte novamente.')
                backup = self.base.parent / 'geodata' / ('base-revisao-' + uuid.uuid4().hex + '.json')
                write_json(backup, clients)
                current.setdefault('coordenadas_anteriores', {'lat': current.get('lat'), 'lon': current.get('lon')})
                for k in ('endereco', 'cidade', 'uf', 'cep'):
                    current[k] = preview['candidate'][k]
                current.update(lat=r['lat'], lon=r['lon'])
                current['geolocalizacao'] = {'status': 'localizado', 'precisao': 'endereco', 'provedor': 'geoapify', 'revisado_usuario': True, 'consultado_em': date.today().isoformat(), 'endereco_fonte': r.get('formatted'), 'fonte_url': 'https://www.geoapify.com/', 'fonte': r.get('datasource', {}), 'confianca': r.get('rank'), 'observacao': 'Endereço revisado pelo usuário e localizado pela API. Entrada não confirmada.'}
                write_json(self.base, clients)
                del self.previews[body['token']]
                return {'mensagem': 'Endereço atualizado'}
            if action == 'salvar-visita':
                clients = self.read(self.base, [])
                stops = body.get('paradas', [])
                if not isinstance(stops, list) or not 1 <= len(stops) <= 8 or len({s.get('id') for s in stops}) != len(stops):
                    raise ValueError('Escolha de uma a oito empresas diferentes.')
                previous = ''
                for stop in stops:
                    p = self.find(clients, stop.get('id'))
                    if p.get('geolocalizacao', {}).get('status') != 'localizado':
                        raise ValueError('Uma empresa está sem localização validada. Revise a seleção.')
                    hour = text(stop.get('hora', ''), 5)
                    datetime.strptime(hour, '%H:%M')
                    if previous and hour <= previous:
                        raise ValueError('Os horários devem seguir a ordem das visitas, sem repetição.')
                    previous = hour
                plan = {'id': uuid.uuid4().hex, 'data': day(body['data']), 'origem': text(body.get('origem', 'Sarandi, RS'), 300), 'paradas': [{'id': s['id'], 'hora': s['hora'], 'concluida': False} for s in stops], 'criado_em': datetime.now().isoformat()}
                state['visitas'].append(plan)
            elif action == 'concluir-visita':
                plan = self.find(state['visitas'], body.get('plano'))
                stop = self.find(plan['paradas'], body.get('id'))
                if not stop['concluida']:
                    stop['concluida'] = True
                    self.event(state, 'visita', stop['id'])
            elif action == 'salvar-contato':
                leads = self.read(self.crm, [])
                lead = self.find(leads, body.get('id'))
                next_day = body.get('data', '')
                if next_day:
                    day(next_day)
                action_text = text(body.get('acao', ''), 1000)
                if next_day and not action_text:
                    raise ValueError('Descreva a próxima ação combinada.')
                note = text(body.get('nota', ''), 3000)
                performed = body.get('realizado') is True
                if performed and not note:
                    raise ValueError('Registre o resultado da conversa antes de concluir.')
                rec = state['contatos'].get(lead['id'], {})
                rec.update(data=next_day, acao=action_text)
                if performed:
                    rec.update(ultima_data=date.today().isoformat(), ultima_nota=note)
                    self.event(state, 'contato', lead['id'], note)
                state['contatos'][lead['id']] = rec
            elif action == 'salvar-proposta':
                client = self.find(self.read(self.base, []), body.get('cliente_id'))
                items = body.get('itens', [])
                if not isinstance(items, list) or not 1 <= len(items) <= 20:
                    raise ValueError('Adicione de um a vinte serviços.')
                clean = []
                for item in items:
                    label = text(item.get('descricao', ''), 300)
                    if not label or item.get('tipo') not in ('mensal', 'unico'):
                        raise ValueError('Informe descrição e cobrança de cada serviço.')
                    clean.append({'descricao': label, 'tipo': item['tipo'], 'valor': amount(item['valor'])})
                conditions = text(body.get('condicoes', ''), 6000)
                if not conditions:
                    raise ValueError('Informe condições e prazos.')
                proposal = {'id': uuid.uuid4().hex, 'cliente_id': client['id'], 'empresa': client['nome'], 'cnpj': client.get('cnpj', ''), 'endereco': client.get('endereco', ''), 'itens': clean, 'condicoes': conditions, 'validade': day(body['validade']), 'criado_em': datetime.now().isoformat(), 'status': 'rascunho'}
                if body.get('id'):
                    saved = self.find(state['propostas'], body['id'])
                    if saved['status'] != 'rascunho':
                        raise ValueError('Uma proposta apresentada não pode ser editada. Crie outra proposta.')
                    proposal.update(id=saved['id'], criado_em=saved['criado_em'])
                    saved.update(proposal)
                else:
                    state['propostas'].append(proposal)
            elif action == 'status-proposta':
                proposal = self.find(state['propostas'], body.get('id'))
                status = body.get('status')
                allowed = {'rascunho': ['apresentada'], 'apresentada': ['aceita', 'recusada']}
                if status not in allowed.get(proposal['status'], []):
                    raise ValueError('A proposta mudou de status. Atualize a página.')
                proposal['status'] = status
                self.event(state, 'venda' if status == 'aceita' else 'proposta' if status == 'apresentada' else 'recusa', proposal['cliente_id'], proposal['id'])
            else:
                raise ValueError('Operação desconhecida.')
            write_json(self.file, state)
            return {'mensagem': 'Salvo'}


service = Commercial()


def handle(handler, method, path):
    if not path.startswith('/api/comercial/'):
        return False
    status = 200
    try:
        if method == 'GET' and path == '/api/comercial/dados':
            result = service.data()
        elif method == 'POST':
            from urllib.parse import urlparse
            origin = handler.headers.get('Origin')
            if origin and urlparse(origin).netloc != handler.headers.get('Host'):
                raise ValueError('Origem da requisição não permitida.')
            size = int(handler.headers.get('Content-Length', 0))
            if not 0 < size <= 65536 or 'application/json' not in handler.headers.get('Content-Type', ''):
                raise ValueError('Formato da requisição inválido.')
            body = json.loads(handler.rfile.read(size))
            if not isinstance(body, dict):
                raise ValueError('Dados inválidos.')
            result = service.mutate(path.rsplit('/', 1)[1], body)
        else:
            raise ValueError('Operação desconhecida.')
        result = {'sucesso': True, **result}
    except (ValueError, KeyError, TypeError, RuntimeError) as exc:
        status = 400
        result = {'sucesso': False, 'erro': str(exc) if isinstance(exc, (ValueError, RuntimeError)) else 'Confira os campos e tente novamente.'}
    except Exception:
        status = 500
        result = {'sucesso': False, 'erro': 'Não foi possível salvar ou consultar. Verifique o servidor e tente novamente.'}
    data = json.dumps(result, ensure_ascii=False).encode('utf-8')
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Content-Length', str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)
    return True
