"""Aplica somente correspondências revisadas; não promove candidatos por similaridade."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / 'base_clientes_regional.json'

def main():
    raw = BASE.read_text(encoding='utf-8')
    data = json.loads(raw)
    backup = ROOT / 'base-antes-validacao.json'
    if not backup.exists():
        backup.write_text(raw, encoding='utf-8')
    osm = json.loads((ROOT / 'osm-regional.json').read_text(encoding='utf-8-sig'))
    elements = {(x['type'], x['id']): x for x in osm['elements']}
    approved = {
        'CLI-REAL-0381': ('node', 7969535885, 'Nome, rua e número coincidem com o ponto do estabelecimento no OpenStreetMap.'),
        'CLI-REAL-0211': ('way', 548424422, 'Nome e endereço rodoviário coincidem. Ponto no centro da área do posto; entrada não confirmada.'),
    }
    conflicts = {
        'CLI-REAL-0001': 'Endereço ainda não confirmado.',
        'CLI-REAL-0023': 'Foram encontrados estabelecimentos com o mesmo nome e endereços diferentes. Confirme a filial.',
        'CLI-REAL-0208': 'O ponto encontrado está na Avenida Flores da Cunha, diferente do endereço rodoviário cadastrado.',
        'CLI-REAL-0471': 'O mapa identifica este endereço como antigo hospital. Confirme o endereço atual.',
    }
    for p in data:
        geo = {'status': 'pendente', 'observacao': conflicts.get(p['id'], 'Endereço sem correspondência cartográfica suficiente. Confirme rua, número e filial para localizar.'), 'consultado_em': '2026-09-21'}
        if p['id'] in approved:
            typ, ident, reason = approved[p['id']]
            item = elements[(typ, ident)]
            coord = item.get('center', item)
            p.setdefault('coordenadas_anteriores', {'lat': p.get('lat'), 'lon': p.get('lon')})
            p['lat'], p['lon'] = coord['lat'], coord['lon']
            geo.update(status='localizado', fonte_url=f'https://www.openstreetmap.org/{typ}/{ident}', observacao=reason, precisao='estabelecimento' if typ == 'node' else 'centro_da_area')
        p['geolocalizacao'] = geo
    BASE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(approved)} estabelecimentos localizados; {len(data)-len(approved)} pendentes.')

if __name__ == '__main__':
    main()
