"""Valida componentes de endereços; não comprova ocupação ou funcionamento da empresa."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'base_clientes_regional.json'
CONFLICTS = {'CLI-REAL-0019', 'CLI-REAL-0023', 'CLI-REAL-0208', 'CLI-REAL-0471'}

def norm(value):
    return ' '.join(re.sub(r'[^a-z0-9]', ' ', unicodedata.normalize('NFKD', str(value or '')).encode('ascii', 'ignore').decode().lower()).split())

def street(value):
    value = norm(value)
    aliases = {'avenida': 'av', 'rua': 'r', 'rodovia': 'rod', 'doutor': 'dr', 'general': 'gen', 'sete': '7', 'quinze': '15', 'vinte e cinco': '25'}
    for a, b in aliases.items():
        value = re.sub(r'\b' + a + r'\b', b, value)
    return value

def parts(client):
    match = re.match(r'^(.+?),\s*(\d+[a-zA-Z]?)\b', client.get('endereco', ''))
    return (match[1], match[2].lstrip('0') or '0') if match else ('', '')

def reason(client, result):
    road, number = parts(client)
    if not road or number == '0':
        return 'Endereço sem número identificável; requer conferência.'
    if result.get('result_type') != 'building':
        return 'A resposta não identifica um prédio.'
    rank = result.get('rank', {})
    try:
        levels = [float(rank.get(k) or 0) for k in ('confidence', 'confidence_city_level', 'confidence_street_level', 'confidence_building_level')]
    except (TypeError, ValueError):
        return 'Confiança inválida na resposta.'
    if any(not math.isfinite(v) or v < .95 or v > 1 for v in levels):
        return 'Confiança insuficiente na posição do prédio ou no endereço.'
    if result.get('country_code') != 'br' or 'RS' not in (result.get('state_code'), result.get('county_code')):
        return 'País ou estado divergente.'
    if norm(client.get('cidade')) != norm(result.get('city')):
        return 'Município divergente.'
    if street(road) != street(result.get('street')):
        return 'Rua divergente ou grafia que exige conferência.'
    if norm(number) != (norm(result.get('housenumber')).lstrip('0') or '0'):
        return 'Número divergente.'
    original_zip = re.sub(r'\D', '', client.get('cep', ''))
    found_zip = re.sub(r'\D', '', result.get('postcode', ''))
    if len(original_zip) == 8 and not original_zip.endswith('000') and found_zip and original_zip != found_zip:
        return 'CEP específico divergente; confira o cadastro.'
    try:
        lat, lon = float(result['lat']), float(result['lon'])
        if not (math.isfinite(lat) and math.isfinite(lon) and -34 <= lat <= -27 and -58 <= lon <= -49):
            return 'Coordenadas incompatíveis com o Rio Grande do Sul.'
    except (KeyError, TypeError, ValueError):
        return 'Coordenadas inválidas.'
    return None

def review(client, entry):
    address = ', '.join(str(client.get(k) or '').strip() for k in ('endereco', 'cidade', 'uf', 'cep')) + ', Brasil'
    if entry.get('endereco_hash') != hashlib.sha256(address.encode()).hexdigest():
        return None, 'Endereço alterado após a consulta; consulte novamente.'
    if client['id'] in CONFLICTS:
        return None, 'Há divergência conhecida de endereço ou filial; confirme onde a empresa funciona.'
    candidates = entry.get('resultados', [])
    accepted = [r for r in candidates if reason(client, r) is None]
    if len(accepted) > 1 and len({(round(r['lat'], 5), round(r['lon'], 5)) for r in accepted}) > 1:
        return None, 'Mais de uma posição compatível; requer revisão.'
    if accepted:
        return accepted[0], None
    return None, reason(client, candidates[0]) if candidates else 'Nenhum endereço encontrado pela API.'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--aplicar', action='store_true')
    args = parser.parse_args()
    raw = BASE.read_bytes()
    clients = json.loads(raw)
    cache = json.loads((ROOT / 'geoapify-candidatos.json').read_text(encoding='utf-8'))
    report = []
    for client in clients:
        if client.get('geolocalizacao', {}).get('status') == 'localizado' and (client.get('geolocalizacao', {}).get('provedor') != 'geoapify' or client.get('geolocalizacao', {}).get('revisado_usuario')):
            continue
        entry = cache.get(client['id'])
        if not entry:
            continue
        result, failure = review(client, entry)
        geo = {'status': 'pendente', 'consultado_em': entry['consultado_em'][:10], 'provedor': 'geoapify', 'observacao': failure}
        if result:
            client.setdefault('coordenadas_anteriores', {'lat': client.get('lat'), 'lon': client.get('lon')})
            client['lat'], client['lon'] = result['lat'], result['lon']
            geo.update(status='localizado', precisao='endereco', endereco_fonte=result.get('formatted'), fonte_url='https://www.geoapify.com/', place_id=result.get('place_id'), confianca=result['rank'], fonte=result.get('datasource', {}), observacao='Rua, número, município e posição do prédio conferidos pela API. Endereço do cadastro localizado; funcionamento da empresa e entrada não confirmados.')
        client['geolocalizacao'] = geo
        report.append({'id': client['id'], 'nome': client['nome'], 'status': geo['status'], 'motivo': failure, 'endereco_fonte': geo.get('endereco_fonte'), 'lat': result['lat'] if result else None, 'lon': result['lon'] if result else None})
    summary = dict(Counter(x['status'] for x in report))
    output = {'consultas_em_cache': len(cache), 'resumo': summary, 'criterio': 'Prédio, confiança >= 0.95 nos quatro níveis; rua, número, município e UF compatíveis; sem CEP específico divergente ou conflito conhecido.', 'itens': report}
    (ROOT / 'relatorio-geoapify.json').write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary))
    if args.aplicar:
        if BASE.read_bytes() != raw:
            raise RuntimeError('A base mudou durante a validação. Execute novamente.')
        backup = ROOT / ('base-antes-geoapify-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '.json')
        backup.write_bytes(raw)
        temp = BASE.with_suffix('.tmp')
        temp.write_text(json.dumps(clients, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        temp.replace(BASE)
        print('Resultados aplicados; dados comerciais preservados.')

if __name__ == '__main__':
    main()
