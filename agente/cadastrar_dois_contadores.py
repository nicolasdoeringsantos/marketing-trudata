#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de cadastro das duas contabilidades no TruData CRM Enterprise e leads_crm.json:
1. Assiscon Assistência Contábil (Leonardo Portolan e Vilson Cesar Barichello)
2. Delmir Ganassini Assessoria Contábil (Delmir Ganassini)
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

def cadastrar():
    with open(ENTERPRISE_DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. EMPRESA 1: Assiscon Assistência Contábil
    emp_assiscon_id = f"emp-{uuid.uuid4().hex[:8]}"
    emp_assiscon = {
        "id": emp_assiscon_id,
        "tipo": "PJ",
        "razao_social": "PORTOLAN & BARICHELLO SS LTDA - ME",
        "nome_fantasia": "Assiscon Assistência Contábil",
        "documento": "05.416.782/0001-68",
        "inscricao_estadual": "",
        "telefone": "(54) 3361-3146",
        "whatsapp": "(54) 3361-3146",
        "email": "",
        "cidade": "Sarandi",
        "uf": "RS",
        "endereco": "Sarandi - RS",
        "segmento": "Escritórios de Contabilidade",
        "pdvs_estimados": 1,
        "campos_customizados": {
            "telefone_publico_adicional": "(54) 3613-302",
            "tipo_parceria": "Escritório Contábil Indicador B2B2B"
        },
        "consentimento_lgpd": {
            "autorizado": True,
            "data_consentimento": datetime.now().isoformat(),
            "base_legal": "Art. 7º V/IX da LGPD (Relação Comercial B2B)"
        },
        "criado_em": datetime.now().strftime("%d/%m/%Y"),
        "origem": "Indicação / Prospecção Manual"
    }

    # Contatos Assiscon
    ctt_leonardo_id = f"ctt-{uuid.uuid4().hex[:8]}"
    ctt_leonardo = {
        "id": ctt_leonardo_id,
        "empresa_id": emp_assiscon_id,
        "nome": "Leonardo Portolan",
        "cargo": "Sócio / Contador",
        "telefone": "(54) 3361-3146",
        "whatsapp": "(54) 3361-3146",
        "email": "",
        "decisor": True,
        "campos_customizados": {},
        "consentimento_lgpd": {
            "autorizado": True,
            "data_consentimento": datetime.now().isoformat()
        }
    }

    ctt_vilson_id = f"ctt-{uuid.uuid4().hex[:8]}"
    ctt_vilson = {
        "id": ctt_vilson_id,
        "empresa_id": emp_assiscon_id,
        "nome": "Vilson Cesar Barichello",
        "cargo": "Sócio / Contador",
        "telefone": "(54) 3613-302",
        "whatsapp": "(54) 3613-302",
        "email": "",
        "decisor": True,
        "campos_customizados": {},
        "consentimento_lgpd": {
            "autorizado": True,
            "data_consentimento": datetime.now().isoformat()
        }
    }

    # Deal Assiscon no Kanban
    deal_assiscon_id = f"deal-{uuid.uuid4().hex[:8]}"
    deal_assiscon = {
        "id": deal_assiscon_id,
        "funil_id": "funil-vendas-novas",
        "etapa_id": "etapa-lead",
        "empresa_id": emp_assiscon_id,
        "contato_id": ctt_leonardo_id,
        "responsavel_id": "usr-admin",
        "titulo": "Parceria Contábil & Migração - Assiscon Assistência Contábil",
        "valor_mrr": 750.0,
        "valor_setup_produtos": 0.0,
        "desconto": 0.0,
        "probabilidade": 25,
        "data_prevista": (date.today() + timedelta(days=15)).isoformat(),
        "status": "aberto",
        "motivo_perda": "",
        "produtos": [],
        "tags": [
            "Escritórios de Contabilidade",
            "Parceria Contábil",
            "Multiplicador B2B2B"
        ],
        "criado_em": datetime.now().isoformat()
    }

    # Atividade Assiscon
    ativ_assiscon = {
        "id": f"ativ-{uuid.uuid4().hex[:8]}",
        "tipo": "ligacao",
        "deal_id": deal_assiscon_id,
        "contato_id": ctt_leonardo_id,
        "empresa_id": emp_assiscon_id,
        "responsavel_id": "usr-admin",
        "titulo": "Apresentar Parceria TruData ERP aos sócios Leonardo Portolan e Vilson Barichello",
        "data_hora": (datetime.now() + timedelta(hours=2)).isoformat(),
        "status": "pendente",
        "notas": "Ligar no (54) 3361-3146 / (54) 3613-302 para apresentar o Modo Escritório gratuito e comissão de 15% recorrente."
    }

    # 2. EMPRESA 2: Delmir Ganassini Assessoria Contábil
    emp_delmir_id = f"emp-{uuid.uuid4().hex[:8]}"
    emp_delmir = {
        "id": emp_delmir_id,
        "tipo": "PJ",
        "razao_social": "DELMIR GANASSINI ASSESSORIA CONTABIL - ME",
        "nome_fantasia": "Delmir Ganassini Assessoria Contábil - Escritório de Contabilidade em Sarandi",
        "documento": "22.276.845/0001-47",
        "inscricao_estadual": "",
        "telefone": "(54) 99104-6847",
        "whatsapp": "(54) 99104-6847",
        "email": "assessoria@dgassessoriacontabil.com.br",
        "cidade": "Sarandi",
        "uf": "RS",
        "endereco": "Rua Bórtolo de Marco, 1383, Sala 01, Centro",
        "segmento": "Escritórios de Contabilidade",
        "pdvs_estimados": 1,
        "campos_customizados": {
            "telefone_comercial_fixo": "(54) 3361-3508",
            "carteira_estimada": "~80 comércios potenciais",
            "tipo_parceria": "Escritório Contábil Indicador B2B2B"
        },
        "consentimento_lgpd": {
            "autorizado": True,
            "data_consentimento": datetime.now().isoformat(),
            "base_legal": "Art. 7º V/IX da LGPD (Relação Comercial B2B)"
        },
        "criado_em": datetime.now().strftime("%d/%m/%Y"),
        "origem": "Prospecção Manual / Radar"
    }

    # Contato Delmir Ganassini
    ctt_delmir_id = f"ctt-{uuid.uuid4().hex[:8]}"
    ctt_delmir = {
        "id": ctt_delmir_id,
        "empresa_id": emp_delmir_id,
        "nome": "Delmir Ganassini",
        "cargo": "Contador / Titular",
        "telefone": "(54) 99104-6847",
        "whatsapp": "(54) 99104-6847",
        "email": "assessoria@dgassessoriacontabil.com.br",
        "decisor": True,
        "campos_customizados": {},
        "consentimento_lgpd": {
            "autorizado": True,
            "data_consentimento": datetime.now().isoformat()
        }
    }

    # Deal Delmir Ganassini no Kanban
    deal_delmir_id = f"deal-{uuid.uuid4().hex[:8]}"
    deal_delmir = {
        "id": deal_delmir_id,
        "funil_id": "funil-vendas-novas",
        "etapa_id": "etapa-lead",
        "empresa_id": emp_delmir_id,
        "contato_id": ctt_delmir_id,
        "responsavel_id": "usr-admin",
        "titulo": "Parceria Contábil & Migração - Delmir Ganassini Assessoria Contábil",
        "valor_mrr": 750.0,
        "valor_setup_produtos": 0.0,
        "desconto": 0.0,
        "probabilidade": 25,
        "data_prevista": (date.today() + timedelta(days=15)).isoformat(),
        "status": "aberto",
        "motivo_perda": "",
        "produtos": [],
        "tags": [
            "Escritórios de Contabilidade",
            "Parceria Contábil",
            "Multiplicador B2B2B"
        ],
        "criado_em": datetime.now().isoformat()
    }

    # Atividade Delmir
    ativ_delmir = {
        "id": f"ativ-{uuid.uuid4().hex[:8]}",
        "tipo": "whatsapp",
        "deal_id": deal_delmir_id,
        "contato_id": ctt_delmir_id,
        "empresa_id": emp_delmir_id,
        "responsavel_id": "usr-admin",
        "titulo": "Contato WhatsApp com Delmir Ganassini (Parceria & Painel do Contador)",
        "data_hora": (datetime.now() + timedelta(hours=1)).isoformat(),
        "status": "pendente",
        "notas": "Disparar mensagem no WhatsApp (54) 99104-6847 com proposta de integração contábil e eliminação de retrabalho fiscal no SPED."
    }

    # Inserir no topo das coleções do CRM Enterprise
    data["empresas"].insert(0, emp_assiscon)
    data["empresas"].insert(1, emp_delmir)

    data["contatos"].insert(0, ctt_leonardo)
    data["contatos"].insert(1, ctt_vilson)
    data["contatos"].insert(2, ctt_delmir)

    data["negociacoes"].insert(0, deal_assiscon)
    data["negociacoes"].insert(1, deal_delmir)

    data["atividades"].insert(0, ativ_assiscon)
    data["atividades"].insert(1, ativ_delmir)

    # Salvar base CRM Enterprise
    with open(ENTERPRISE_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("[OK] crm_enterprise_data.json atualizado com sucesso!")

    # 3. Atualizar leads_crm.json
    leads = []
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            try:
                leads = json.load(f)
            except Exception:
                leads = []

    lead_assiscon = {
        "id": f"lead-assiscon-{uuid.uuid4().hex[:6]}",
        "nome": "Leonardo Portolan e Vilson Cesar Barichello",
        "empresa": "Assiscon Assistência Contábil",
        "cidade": "Sarandi - RS",
        "segmento": "Escritórios de Contabilidade",
        "telefone": "5433613146",
        "email": "",
        "site": "Não possui site",
        "tem_site": False,
        "endereco": "Sarandi - RS",
        "cnpj": "05.416.782/0001-68",
        "sintegra_status": "ATIVA / Regular na Receita Federal e Sintegra-RS",
        "cnae": "6920-2/01 - Atividades de contabilidade",
        "origem": "Prospecção Manual Contábil",
        "fase": "novo",
        "caixas": "1",
        "data": datetime.now().strftime("%d/%m/%Y"),
        "notas": "Cadastro público: (54) 3613-302; listagem local também mostra (54) 3361-3146. Sócios: Leonardo Portolan e Vilson Cesar Barichello."
    }

    lead_delmir = {
        "id": f"lead-delmir-{uuid.uuid4().hex[:6]}",
        "nome": "Delmir Ganassini",
        "empresa": "Delmir Ganassini Assessoria Contábil - Escritório de Contabilidade em Sarandi",
        "cidade": "Sarandi - RS",
        "segmento": "Escritórios de Contabilidade",
        "telefone": "54991046847",
        "email": "assessoria@dgassessoriacontabil.com.br",
        "site": "http://www.dgassessoriacontabil.com.br",
        "tem_site": True,
        "endereco": "Rua Bórtolo de Marco, 1383, Sala 01, Centro - Sarandi - RS",
        "cnpj": "22.276.845/0001-47",
        "sintegra_status": "ATIVA / Regular no Sintegra-RS",
        "cnae": "6920-2/01 - Atividades de contabilidade",
        "origem": "Prospecção Manual Contábil",
        "fase": "novo",
        "caixas": "1",
        "data": datetime.now().strftime("%d/%m/%Y"),
        "notas": "Escritório de Contabilidade auditado e ativo em Sarandi-RS. Decisor: Delmir Ganassini. Telefone: (54) 99104-6847 / (54) 3361-3508."
    }

    leads.insert(0, lead_assiscon)
    leads.insert(1, lead_delmir)

    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)
    print("[OK] leads_crm.json atualizado com sucesso!")

    # 4. Registrar em crm_audit_log.json
    audit_entries = []
    if os.path.exists(AUDIT_LOG_FILE):
        with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
            try:
                audit_entries = json.load(f)
            except Exception:
                audit_entries = []

    for emp_nome in ["Assiscon Assistência Contábil", "Delmir Ganassini Assessoria Contábil"]:
        audit_entries.insert(0, {
            "id": f"audit-{uuid.uuid4().hex[:8]}",
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "usuario": "Administrador",
            "acao": "CADASTRO_ENTIDADE_E_DEAL",
            "entidade": "empresa_deal",
            "entidade_id": emp_nome,
            "detalhe": f"Escritório contábil cadastrado e adicionado ao Kanban em '1. Lead / Qualificação'."
        })

    with open(AUDIT_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(audit_entries[:1000], f, indent=2, ensure_ascii=False)
    print("[OK] crm_audit_log.json atualizado com sucesso!")

if __name__ == "__main__":
    cadastrar()
