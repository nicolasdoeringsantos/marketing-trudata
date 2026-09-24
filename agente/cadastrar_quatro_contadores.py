#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de cadastro das 4 contabilidades no TruData CRM Enterprise, Kanban e bases regionais:
1. LS CONTADORES ASSOCIADOS (Carazinho/RS)
2. Ben Hur – Escritório Contábil (Sarandi/RS)
3. Prodec (Palmeira das Missões/RS)
4. Absoluta Contabilidade (Sarandi/RS)
"""

import os
import json
import uuid
from datetime import datetime, date, timedelta

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PAINEL_DIR = os.path.join(PROJECT_ROOT, "painel_aprovacao")
ENTERPRISE_DATA_FILE = os.path.join(PAINEL_DIR, "crm_enterprise_data.json")
LEADS_FILE = os.path.join(PAINEL_DIR, "leads_crm.json")
AUDIT_LOG_FILE = os.path.join(PAINEL_DIR, "crm_audit_log.json")
BASE_REGIONAL = os.path.join(PROJECT_ROOT, "agente", "base_clientes_regional.json")

novas_contabilidades = [
    {
        "nome": "LS Contadores Associados",
        "razao_social": "LS CONTADORES ASSOCIADOS S/S",
        "cidade": "Carazinho",
        "uf": "RS",
        "cnpj": "73.574.899/0001-20",
        "telefone": "(54) 3330-1520",
        "whatsapp": "5554984488810",
        "endereco": "Carazinho - RS",
        "contatos": [
            {"nome": "Luis Antonio Barbosa Siqueira", "cargo": "Sócio-Administrador / Contador", "telefone": "(54) 3330-1520", "whatsapp": "(54) 98448-8810", "decisor": True},
            {"nome": "Giovana Andrea Scolari", "cargo": "Sócia / Contadora", "telefone": "(54) 3330-1520", "whatsapp": "(54) 98448-8810", "decisor": True}
        ],
        "tags": ["Escritórios de Contabilidade", "Parceria Contábil", "Carazinho", "Multiplicador B2B2B"],
        "notas": "LS Contadores Associados em Carazinho/RS. Contato com Luis Antonio Barbosa Siqueira e Giovana Andrea Scolari. Fone: (54) 3330-1520, Whats: (54) 98448-8810.",
        "atividade": "Contato via WhatsApp (54) 98448-8810 com Luis e Giovana apresentando o Clube do Contador TruData ERP e comissão recorrente de 15%."
    },
    {
        "nome": "Ben Hur – Escritório Contábil",
        "razao_social": "Ben Hur Jorge Silva Junior - Escritório Contábil Sarandi",
        "cidade": "Sarandi",
        "uf": "RS",
        "cnpj": "",
        "telefone": "",
        "whatsapp": "",
        "endereco": "Sarandi - RS",
        "contatos": [
            {"nome": "Ben Hur Jorge Silva Junior", "cargo": "Contador / Responsável", "telefone": "", "whatsapp": "", "decisor": True}
        ],
        "tags": ["Escritórios de Contabilidade", "Parceria Contábil", "Sarandi", "Multiplicador B2B2B"],
        "notas": "Ben Hur Jorge Silva Junior — Escritório Contábil em Sarandi-RS. Em processo de localização da razão social/CNPJ e telefone direto.",
        "atividade": "Localizar contato telefônico e CNPJ do Escritório Contábil de Ben Hur em Sarandi para agendamento de visita comercial."
    },
    {
        "nome": "Prodec",
        "razao_social": "PRODEC COMERCIO E SERVICOS LTDA",
        "cidade": "Palmeira das Missões",
        "uf": "RS",
        "cnpj": "08.644.991/0001-57",
        "telefone": "(55) 3742-3080",
        "whatsapp": "5555999551922",
        "endereco": "Rua Major Novais, 1050, Andar 2, Sala 03, Centro - Palmeira das Missões/RS",
        "contatos": [
            {"nome": "Responsável Comercial / Gestão Prodec", "cargo": "Gestor / Responsável", "telefone": "(55) 3742-3080", "whatsapp": "(55) 99955-1922", "decisor": True}
        ],
        "tags": ["Escritórios de Contabilidade", "Serviços Fiscais", "Palmeira das Missões", "Multiplicador B2B2B"],
        "notas": "Prodec em Palmeira das Missões/RS. WhatsApp: (55) 99955-1922, Fone: (55) 3742-3080. Rua Major Novais, 1050.",
        "atividade": "Contato via WhatsApp (55) 99955-1922 com a Prodec em Palmeira das Missões para apresentação do ERP e parceria regional."
    },
    {
        "nome": "Absoluta Contabilidade",
        "razao_social": "ABSOLUTA ASSESSORIA CONTABIL LTDA",
        "cidade": "Sarandi",
        "uf": "RS",
        "cnpj": "15.349.047/0001-32",
        "telefone": "(54) 3361-3091",
        "whatsapp": "5554999447890",
        "endereco": "Sarandi - RS",
        "contatos": [
            {"nome": "Taís Klein Antunes Carbonari", "cargo": "Sócia-Administradora / Contadora", "telefone": "(54) 3361-3091", "whatsapp": "(54) 99944-7890", "decisor": True},
            {"nome": "Denise Wagner Fritzen", "cargo": "Sócia / Contadora", "telefone": "(54) 3361-3091", "whatsapp": "(54) 99944-7890", "decisor": True}
        ],
        "tags": ["Escritórios de Contabilidade", "Parceria Contábil", "Sarandi", "Multiplicador B2B2B"],
        "notas": "Absoluta Contabilidade em Sarandi/RS. Sócias: Taís Klein Antunes Carbonari e Denise Wagner Fritzen. Fone: (54) 3361-3091, Whats: (54) 99944-7890.",
        "atividade": "Contato via WhatsApp (54) 99944-7890 e (54) 3361-3091 com Taís e Denise sobre o painel do contador gratuito no TruData ERP."
    }
]

def cadastrar():
    with open(ENTERPRISE_DATA_FILE, "r", encoding="utf-8") as f:
        crm_data = json.load(f)

    leads = []
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            try:
                leads = json.load(f)
            except Exception:
                leads = []

    regional = []
    if os.path.exists(BASE_REGIONAL):
        with open(BASE_REGIONAL, "r", encoding="utf-8") as f:
            try:
                regional = json.load(f)
            except Exception:
                regional = []

    audit_entries = []
    if os.path.exists(AUDIT_LOG_FILE):
        with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
            try:
                audit_entries = json.load(f)
            except Exception:
                audit_entries = []

    for item in reversed(novas_contabilidades):
        emp_id = f"emp-{uuid.uuid4().hex[:8]}"
        emp = {
            "id": emp_id,
            "tipo": "PJ",
            "razao_social": item["razao_social"],
            "nome_fantasia": item["nome"],
            "documento": item["cnpj"],
            "inscricao_estadual": "",
            "telefone": item["telefone"],
            "whatsapp": item["whatsapp"],
            "email": "",
            "cidade": item["cidade"],
            "uf": item["uf"],
            "endereco": item["endereco"],
            "segmento": "Escritórios de Contabilidade",
            "pdvs_estimados": 1,
            "campos_customizados": {
                "tipo_parceria": "Escritório Contábil Indicador B2B2B"
            },
            "consentimento_lgpd": {
                "autorizado": True,
                "data_consentimento": datetime.now().isoformat(),
                "base_legal": "Art. 7º V/IX da LGPD (Relação Comercial B2B)"
            },
            "criado_em": datetime.now().strftime("%d/%m/%Y"),
            "origem": "Prospecção Manual Contábil"
        }
        crm_data["empresas"].insert(0, emp)

        primeiro_ctt_id = None
        for c in item["contatos"]:
            ctt_id = f"ctt-{uuid.uuid4().hex[:8]}"
            if not primeiro_ctt_id:
                primeiro_ctt_id = ctt_id
            ctt = {
                "id": ctt_id,
                "empresa_id": emp_id,
                "nome": c["nome"],
                "cargo": c["cargo"],
                "telefone": c["telefone"],
                "whatsapp": c["whatsapp"],
                "email": "",
                "decisor": c["decisor"],
                "campos_customizados": {},
                "consentimento_lgpd": {"autorizado": True, "data_consentimento": datetime.now().isoformat()}
            }
            crm_data["contatos"].insert(0, ctt)

        deal_id = f"deal-{uuid.uuid4().hex[:8]}"
        deal = {
            "id": deal_id,
            "funil_id": "funil-vendas-novas",
            "etapa_id": "etapa-lead",
            "empresa_id": emp_id,
            "contato_id": primeiro_ctt_id,
            "responsavel_id": "usr-admin",
            "titulo": f"Parceria Contábil & Migração - {item['nome']}",
            "valor_mrr": 750.0,
            "valor_setup_produtos": 0.0,
            "desconto": 0.0,
            "probabilidade": 25,
            "data_prevista": (date.today() + timedelta(days=15)).isoformat(),
            "status": "aberto",
            "motivo_perda": "",
            "produtos": [],
            "tags": item["tags"],
            "criado_em": datetime.now().isoformat()
        }
        crm_data["negociacoes"].insert(0, deal)

        ativ = {
            "id": f"ativ-{uuid.uuid4().hex[:8]}",
            "tipo": "whatsapp" if item["whatsapp"] else "ligacao",
            "deal_id": deal_id,
            "contato_id": primeiro_ctt_id,
            "empresa_id": emp_id,
            "responsavel_id": "usr-admin",
            "titulo": item["atividade"],
            "data_hora": (datetime.now() + timedelta(hours=2)).isoformat(),
            "status": "pendente",
            "notas": item["notas"]
        }
        crm_data["atividades"].insert(0, ativ)

        # Lead Legado
        lead = {
            "id": f"lead-{uuid.uuid4().hex[:8]}",
            "nome": " / ".join([c["nome"] for c in item["contatos"]]),
            "empresa": item["nome"],
            "cidade": f"{item['cidade']} - {item['uf']}",
            "segmento": "Escritórios de Contabilidade",
            "telefone": item["whatsapp"] or item["telefone"],
            "email": "",
            "site": "Não possui site",
            "tem_site": False,
            "endereco": item["endereco"],
            "cnpj": item["cnpj"],
            "sintegra_status": "ATIVA / Em Prospecção",
            "cnae": "6920-2/01 - Atividades de contabilidade",
            "origem": "Prospecção Manual Contábil",
            "fase": "novo",
            "caixas": "1",
            "data": datetime.now().strftime("%d/%m/%Y"),
            "notas": item["notas"]
        }
        leads.insert(0, lead)

        # Base Regional
        reg = {
            "id": f"CONT-REG-{uuid.uuid4().hex[:6].upper()}",
            "nome": item["nome"],
            "razao_social": item["razao_social"],
            "cnpj": item["cnpj"],
            "cnpj_limpo": item["cnpj"].replace(".", "").replace("/", "").replace("-", "") if item["cnpj"] else "",
            "endereco": item["endereco"],
            "bairro": "Centro",
            "cidade": item["cidade"],
            "uf": item["uf"],
            "cep": "99560-000" if item["cidade"] == "Sarandi" else ("99500-000" if item["cidade"] == "Carazinho" else "98300-000"),
            "telefone": item["telefone"],
            "whatsapp": item["whatsapp"],
            "email": "",
            "decisor": " / ".join([c["nome"] for c in item["contatos"]]),
            "segmento": "Escritórios de Contabilidade",
            "cnae_codigo": "6920-2/01",
            "cnae_descricao": "Atividades de contabilidade",
            "porte": "ME / EPP",
            "clientes_estimados": 70,
            "pdvs_estimados": 1,
            "distancia_km": 0.5 if item["cidade"] == "Sarandi" else (38.0 if item["cidade"] == "Carazinho" else 65.0),
            "tem_site": False,
            "sintegra_status": "ATIVA / Em Prospecção",
            "origem_dados": "Prospecção Manual",
            "lead_score": 95,
            "notas": item["notas"]
        }
        regional.append(reg)

        # Log de Auditoria
        audit_entries.insert(0, {
            "id": f"audit-{uuid.uuid4().hex[:8]}",
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "usuario": "Administrador",
            "acao": "CADASTRO_ENTIDADE_E_DEAL",
            "entidade": "empresa_deal",
            "entidade_id": item["nome"],
            "detalhe": f"Escritório contábil {item['nome']} cadastrado e adicionado ao Kanban em 1. Lead / Qualificação."
        })

    with open(ENTERPRISE_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(crm_data, f, indent=2, ensure_ascii=False)
    print("[OK] crm_enterprise_data.json atualizado com os 4 escritorios!")

    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)
    print("[OK] leads_crm.json atualizado!")

    with open(BASE_REGIONAL, "w", encoding="utf-8") as f:
        json.dump(regional, f, indent=2, ensure_ascii=False)
    print("[OK] base_clientes_regional.json atualizada!")

    with open(AUDIT_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(audit_entries[:1000], f, indent=2, ensure_ascii=False)
    print("[OK] crm_audit_log.json atualizado!")

if __name__ == "__main__":
    cadastrar()
