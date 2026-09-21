import json
import socket
import urllib.request
import urllib.error

with open('agente/base_clientes_regional.json', 'r', encoding='utf-8') as f:
    leads = json.load(f)

contabilidades = [
    l for l in leads 
    if 'contab' in l.get('segmento', '').lower() 
    or 'contábil' in l.get('nome', '').lower() 
    or 'contabilidade' in l.get('nome', '').lower()
]

print(f"Total de contabilidades na base: {len(contabilidades)}")

com_site = []
for c in contabilidades:
    site = c.get('site')
    tem_site = c.get('tem_site')
    if tem_site or (site and site not in ['Não possui site', 'null', None, '-', '']):
        com_site.append((c.get('id'), c.get('nome'), c.get('cidade'), site))

print(f"Contabilidades com site preenchido: {len(com_site)}")
print("-" * 60)
for cid, nome, cidade, site in com_site:
    print(f"[{cid}] {nome} ({cidade}) -> {site}")

