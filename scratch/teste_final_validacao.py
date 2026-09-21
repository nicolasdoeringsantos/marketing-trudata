# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json

# 1. Teste HTML do Radar
res_html = urllib.request.urlopen('http://127.0.0.1:8080/radar_clientes.html')
assert res_html.status == 200
html_content = res_html.read().decode('utf-8')
assert 'Sintegra-RS: Ativa' in html_content
print('[1/3] radar_clientes.html servido com status 200 e selo Sintegra-RS presente.')

# 2. Teste API de prospecção com filtros
for seg in ['Supermercados & Mercearias', 'Autopeças & Oficinas', 'Farmácias & Drogarias']:
    url = f'http://127.0.0.1:8080/api/prospectar?raio=100&origem=Sarandi&segmento={urllib.parse.quote(seg)}'
    res_api = urllib.request.urlopen(url)
    data = json.loads(res_api.read().decode('utf-8'))
    assert data['sucesso'] == True
    print(f'[2/3] Filtro segmento "{seg}": {data["total"]} estabelecimentos reais retornados.')

# 3. Teste Rota Exportar CSV
res_csv = urllib.request.urlopen('http://127.0.0.1:8080/api/exportar_prospects_csv?raio=50&origem=Sarandi')
assert res_csv.status == 200
csv_lines = res_csv.read().decode('utf-8-sig').splitlines()
assert len(csv_lines) > 10
assert 'Status Sintegra-RS' in csv_lines[0]
print(f'[3/3] /api/exportar_prospects_csv gerou com sucesso {len(csv_lines)} linhas de clientes reais.')

print('\nTODOS OS TESTES DE VALIDAÇÃO PASSARAM COM 100% DE SUCESSO!')
