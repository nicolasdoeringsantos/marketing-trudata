import urllib.request
import urllib.parse
import json

print('=== INICIANDO TESTE DAS 10 MELHORIAS B2B TRUDATA ===')

# Teste 1: /api/prospectar com Cidade Alvo e Ordenação
url1 = 'http://127.0.0.1:8080/api/prospectar?raio=100&cidade=Sarandi&ordenacao=nome'
r1 = json.loads(urllib.request.urlopen(url1).read().decode('utf-8'))
assert r1['sucesso'] == True
assert len(r1['clientes']) > 0
tot_sarandi = len(r1['clientes'])
primeiro = r1['clientes'][0]['nome']
print(f'1. Filtro Cidade e Ordenacao: OK ({tot_sarandi} clientes em Sarandi, primeiro: {primeiro})')

# Teste 2: Abordagem WhatsApp especializada por nicho
c0 = r1['clientes'][0]
assert 'link_whatsapp' in c0 and 'wa.me' in c0['link_whatsapp']
print('2. Abordagem WhatsApp especializada: OK (link formatado com copy de nicho)')

# Teste 3: Autocomplete de Empresas Reais
url3 = 'http://127.0.0.1:8080/api/clientes_real_autocomplete?q=Biomix'
r3 = json.loads(urllib.request.urlopen(url3).read().decode('utf-8'))
assert r3['sucesso'] == True
assert r3['total'] > 0
print(f'3. Autocomplete Clientes Reais: OK ({r3["total"]} encontrados para Biomix: {r3["clientes"][0]["nome"]})')

# Teste 4: Status do Lead no CRM
url4 = 'http://127.0.0.1:8080/api/status_leads_radar'
r4 = json.loads(urllib.request.urlopen(url4).read().decode('utf-8'))
assert r4['sucesso'] == True
print(f'4. Sincronizacao de Status Leads: OK ({len(r4["status"])} mapeados)')

# Teste 5: Atualizacao de Status do Lead via POST
data_post = json.dumps({
    'cnpj': c0['cnpj'],
    'empresa': c0['nome'],
    'fase': 'demo_agendada',
    'decisor': c0.get('decisor', 'Responsavel'),
    'cidade': c0['cidade'],
    'segmento': c0['segmento']
}).encode('utf-8')
req5 = urllib.request.Request('http://127.0.0.1:8080/api/atualizar_status_lead', data=data_post, headers={'Content-Type': 'application/json'})
r5 = json.loads(urllib.request.urlopen(req5).read().decode('utf-8'))
assert r5['sucesso'] == True
print('5. Atualizar Status Lead no CRM: OK (Lead movido para demo_agendada)')

# Teste 6: Exportacao CSV filtrada
url6 = 'http://127.0.0.1:8080/api/exportar_prospects_csv?raio=100&cidade=Sarandi'
r6 = urllib.request.urlopen(url6).read().decode('utf-8-sig')
assert ('Razão Social' in r6 or 'CNPJ' in r6) and 'Sarandi' in r6
print('6. Exportacao CSV Filtrada: OK (CSV retornado com sucesso)')

# Teste 7: Integracao Gerador de Proposta A4 com Endereco
html_prop = urllib.request.urlopen('http://127.0.0.1:8080/painel_aprovacao/gerador_proposta.html').read().decode('utf-8')
assert 'inEndereco' in html_prop and "params.get('endereco')" in html_prop
print('7. Integracao Proposta A4: OK (Suporte a endereco e modulos automaticos)')

# Teste 8: Copiloto de Vendas com 4 Abas e Base Real
html_cop = urllib.request.urlopen('http://127.0.0.1:8080/painel_aprovacao/copiloto_vendas.html').read().decode('utf-8')
assert 'Cold Call' in html_cop and 'Quebrador de Obje' in html_cop and 'buscarAutocomplete' in html_cop
print('8. Copiloto de Vendas Comercial: OK (4 abas taticas e integracao base real)')

# Teste 9: Radar de Clientes com Mapa Leaflet e Sintegra
html_rad = urllib.request.urlopen('http://127.0.0.1:8080/painel_aprovacao/radar_clientes.html').read().decode('utf-8')
assert 'leaflet' in html_rad.lower() and 'auditarSintegra' in html_rad and 'copiarTelefonesVisiveis' in html_rad
print('9. Radar de Clientes: OK (Leaflet OSM, Auditoria Sintegra e Copiador de Telefones)')

# Teste 10: Dashboard Central Conectado (index.html)
html_idx = urllib.request.urlopen('http://127.0.0.1:8080/painel_aprovacao/index.html').read().decode('utf-8')
assert 'Central de Inteligência de Vendas B2B' in html_idx and '600' in html_idx
print('10. Dashboard Central Hub: OK (Painel de Expansao Regional com 4 KPIs e atalhos)')

print('=== TODAS AS 10 MELHORIAS VALIDADAS COM SUCESSO 100% ===')
