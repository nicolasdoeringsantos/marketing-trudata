import json
import os
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRM_JSON = os.path.join(PROJECT_ROOT, "painel_aprovacao", "leads_crm.json")
ALVOS_JSON = os.path.join(PROJECT_ROOT, "painel_aprovacao", "alvos_prioritarios_piloto.json")

with open(ALVOS_JSON, 'r', encoding='utf-8') as f:
    alvos = json.load(f)

leads_existentes = []
if os.path.exists(CRM_JSON):
    with open(CRM_JSON, 'r', encoding='utf-8') as f:
        leads_existentes = json.load(f)

cnpjs_existentes = {l.get('cnpj', '').strip() for l in leads_existentes if l.get('cnpj')}
empresas_existentes = {l.get('empresa', '').strip().lower() for l in leads_existentes if l.get('empresa')}

adicionados = 0
for a in alvos:
    cnpj = a.get('cnpj', '').strip()
    empresa = a.get('nome', '').strip()
    if cnpj in cnpjs_existentes or empresa.lower() in empresas_existentes:
        continue
    
    pdvs = int(a.get('pdvs_estimados', 2))
    mrr = 180 + (pdvs - 1) * 60
    setup = 350 + (pdvs - 1) * 150
    
    novo_lead = {
        "id": f"lead-piloto-{a.get('id', '')}",
        "nome": a.get('decisor', 'Diretoria'),
        "empresa": empresa,
        "cidade": f"{a.get('cidade', 'Sarandi')} - RS",
        "segmento": a.get('segmento', 'Varejo'),
        "telefone": a.get('whatsapp', a.get('telefone', '')).replace('(', '').replace(')', '').replace('-', '').replace(' ', ''),
        "email": a.get('email', ''),
        "site": a.get('site', 'Não possui site'),
        "tem_site": a.get('tem_site', False),
        "endereco": f"{a.get('endereco', '')}, {a.get('bairro', '')} - {a.get('cidade', '')}/RS",
        "cnpj": cnpj,
        "origem": f"Operação Piloto Raio 30km ({a.get('distancia_km', 0)}km de Sarandi)",
        "fase": "novo",
        "caixas": str(pdvs),
        "mrr_estimado": mrr,
        "setup_estimado": setup,
        "data": datetime.now().strftime("%d/%m/%Y"),
        "notas": f"Lead prioritário da Operação Piloto TruData. Decisor(a): {a.get('decisor', 'A confirmar')}. {pdvs} PDVs estimados.",
        "historico_notas": [
            {
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "autor": "Inteligência B2B",
                "tipo": "Mapeamento",
                "texto": f"Mapeado na Operação Piloto como alvo de alta prioridade. Distância da matriz: {a.get('distancia_km', 0)} km."
            }
        ]
    }
    leads_existentes.append(novo_lead)
    adicionados += 1

with open(CRM_JSON, 'w', encoding='utf-8') as f:
    json.dump(leads_existentes, f, indent=2, ensure_ascii=False)

print(f"Total de novos leads adicionados ao CRM Kanban: {adicionados}")
print(f"Total geral no pipeline CRM: {len(leads_existentes)} leads.")
