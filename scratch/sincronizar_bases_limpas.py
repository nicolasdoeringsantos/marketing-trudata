import json
import csv
import os
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# 1. Carrega base oficial limpa
with open('agente/base_clientes_regional.json', 'r', encoding='utf-8') as f:
    leads = json.load(f)

print(f"Total de registros na base regional: {len(leads)}")

# Mapeamento rápido por CNPJ e Nome
mapa_limpo_cnpj = {}
mapa_limpo_nome = {}
for l in leads:
    cnpj_limpo = (l.get('cnpj') or '').replace('\D', '').strip()
    if cnpj_limpo:
        mapa_limpo_cnpj[cnpj_limpo] = l
    mapa_limpo_nome[l.get('nome', '').strip().lower()] = l

# 2. Atualiza painel_aprovacao/leads_crm.json se existir
crm_path = 'painel_aprovacao/leads_crm.json'
if os.path.exists(crm_path):
    with open(crm_path, 'r', encoding='utf-8') as f:
        crm_data = json.load(f)
    
    atualizados = 0
    for lead in crm_data:
        cnpj = (lead.get('cnpj') or '').replace('\D', '').strip()
        nome = lead.get('empresa', '').strip().lower()
        ref = mapa_limpo_cnpj.get(cnpj) or mapa_limpo_nome.get(nome)
        if ref:
            lead['site'] = ref.get('site', 'Não possui site')
            lead['tem_site'] = ref.get('tem_site', False)
            atualizados += 1
            
    with open(crm_path, 'w', encoding='utf-8') as f:
        json.dump(crm_data, f, indent=2, ensure_ascii=False)
    print(f"leads_crm.json atualizado: {atualizados} leads sincronizados com dados limpos.")

# 3. Exporta clientes_prospeccao_real.csv
csv_path = 'painel_aprovacao/clientes_prospeccao_real.csv'
colunas = [
    "ID", "Nome Fantasia", "Razão Social", "CNPJ", "Status Sintegra-RS", "Segmento", 
    "CNAE Fiscal", "Cidade", "Endereço Completo", "Bairro", "CEP", 
    "Distância (km)", "Telefone", "WhatsApp", "E-mail", 
    "Possui Site?", "Site / Website URL", "Decisor", "Porte", "PDVs Estimados", "Lead Score", "Observações"
]

with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=colunas, delimiter=';')
    writer.writeheader()
    for l in leads:
        writer.writerow({
            "ID": l.get("id", ""),
            "Nome Fantasia": l.get("nome", ""),
            "Razão Social": l.get("razao_social", ""),
            "CNPJ": l.get("cnpj", ""),
            "Status Sintegra-RS": l.get("status_sintegra", "Ativa"),
            "Segmento": l.get("segmento", ""),
            "CNAE Fiscal": l.get("cnae", ""),
            "Cidade": l.get("cidade", ""),
            "Endereço Completo": l.get("endereco", ""),
            "Bairro": l.get("bairro", ""),
            "CEP": l.get("cep", ""),
            "Distância (km)": l.get("distancia_km", ""),
            "Telefone": l.get("telefone", ""),
            "WhatsApp": l.get("whatsapp", ""),
            "E-mail": l.get("email", ""),
            "Possui Site?": "SIM" if l.get("tem_site") else "NÃO",
            "Site / Website URL": l.get("site", "Não possui site"),
            "Decisor": l.get("decisor", ""),
            "Porte": l.get("porte", "ME"),
            "PDVs Estimados": l.get("pdvs_estimados", 1),
            "Lead Score": l.get("lead_score", 70),
            "Observações": l.get("notas", "")
        })

print(f"CSV oficial atualizado com sucesso em {csv_path}!")
