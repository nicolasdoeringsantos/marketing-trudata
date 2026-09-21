import json, os, sys
sys.path.append(os.path.abspath('agente'))
import prospector_clientes

crm_file = os.path.abspath('painel_aprovacao/leads_crm.json')
base_file = os.path.abspath('agente/base_clientes_regional.json')

with open(base_file, 'r', encoding='utf-8') as f:
    base = json.load(f)

contabilidades = [b for b in base if 'contabil' in (b.get('segmento') or '').lower() or 'contabilidade' in (b.get('segmento') or '').lower()]
print(f"Total contabilidades auditadas: {len(contabilidades)}")

adicionados = 0
for c in contabilidades:
    cli_est = c.get('clientes_estimados', 70)
    lead_payload = {
        'empresa': c['nome'],
        'nome': c.get('decisor') or 'Diretoria Contábil',
        'cidade': f"{c['cidade']} - RS",
        'segmento': 'Escritórios de Contabilidade',
        'telefone': c.get('whatsapp') or c.get('telefone') or '',
        'email': c.get('email') or '',
        'caixas': 1,
        'origem': 'Canal Parceiro Contábil (150km)',
        'fase': 'novo',
        'notas': f"Escritório Parceiro (carteira estimada: {cli_est} empresas). CNPJ: {c['cnpj']}. Endereço: {c['endereco']}"
    }
    suc, res = prospector_clientes.enviar_para_crm_json(lead_payload, crm_file)
    if suc:
        adicionados += 1

print(f"Novos escritórios contábeis adicionados ao CRM: {adicionados}")
with open(crm_file, 'r', encoding='utf-8') as f:
    total_crm = json.load(f)
print(f"Total geral de leads no CRM agora: {len(total_crm)}")
