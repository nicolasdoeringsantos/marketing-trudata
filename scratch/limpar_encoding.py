# -*- coding: utf-8 -*-
import json
import re

with open('agente/base_clientes_regional.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean_txt(t):
    if not isinstance(t, str):
        return t
    t = t.replace('Autope\ufffdas', 'Autopeças')
    t = t.replace('Constru\ufffdo', 'Construção')
    t = t.replace('Bebidas & G\ufffds', 'Bebidas & Gás')
    t = t.replace('Escrit\ufffdrios', 'Escritórios')
    t = t.replace('Farm\ufffdcias', 'Farmácias')
    t = t.replace('Ind\ufffdstrias', 'Indústrias')
    t = t.replace('Metal\ufffdrgicas', 'Metalúrgicas')
    t = t.replace('Cal\ufffdados', 'Calçados')
    t = t.replace('M\ufffdveis', 'Móveis')
    t = t.replace('Decora\ufffdo', 'Decoração')
    t = t.replace('Presta\ufffdo', 'Prestação')
    t = t.replace('Servi\ufffdos', 'Serviços')
    t = t.replace('Log\ufffdstica', 'Logística')
    t = t.replace('Inform\ufffdtica', 'Informática')
    t = t.replace('\ufffdticas', 'Óticas')
    return t

for d in data:
    for k, v in d.items():
        if isinstance(v, str):
            d[k] = clean_txt(v)

with open('agente/base_clientes_regional.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Segmentos agora:")
print(set(d['segmento'] for d in data))
