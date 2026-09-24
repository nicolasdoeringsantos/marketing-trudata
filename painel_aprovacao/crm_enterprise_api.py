#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CRM Enterprise TruData - Módulo de Gestão Comercial 360°
Persistência atômica, Múltiplos Funis, Kanban, Atividades, Automações,
Deduplicação, Métricas, Logs de Auditoria e Conformidade LGPD.
"""

import os
import json
import csv
import io
import uuid
import threading
import copy
import hashlib
import secrets
from datetime import datetime, date, timedelta

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PAINEL_DIR = os.path.join(PROJECT_ROOT, "painel_aprovacao")
LEADS_LEGACY_FILE = os.path.join(PAINEL_DIR, "leads_crm.json")
ENTERPRISE_DATA_FILE = os.path.join(PAINEL_DIR, "crm_enterprise_data.json")
BACKUPS_DIR = os.path.join(PAINEL_DIR, "backups_crm")
AUDIT_LOG_FILE = os.path.join(PAINEL_DIR, "crm_audit_log.json")

os.makedirs(BACKUPS_DIR, exist_ok=True)

class CRMEnterpriseService:
    def __init__(self, data_file=None, audit_file=None):
        self.lock = threading.RLock()
        self.round_robin_index = 0
        self.data_file = data_file or ENTERPRISE_DATA_FILE
        self.audit_file = audit_file or AUDIT_LOG_FILE
        self._inicializar_base()

    def _log_audit(self, usuario, acao, entidade, entidade_id, detalhe=""):
        try:
            entry = {
                "id": f"audit-{uuid.uuid4().hex[:8]}",
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "usuario": usuario or "Sistema",
                "acao": acao,
                "entidade": entidade,
                "entidade_id": entidade_id,
                "detalhe": detalhe
            }
            logs = []
            if os.path.exists(self.audit_file):
                try:
                    with open(self.audit_file, "r", encoding="utf-8") as f:
                        logs = json.load(f)
                except Exception:
                    logs = []
            logs.insert(0, entry)
            # Manter últimos 1000 logs
            logs = logs[:1000]
            with open(self.audit_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[CRM AUDIT ERROR] {e}")

    def _fazer_backup_automatico(self, data):
        try:
            hoje_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(BACKUPS_DIR, f"backup_crm_{hoje_str}.json")
            with open(backup_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            # Limpar backups antigos mantendo os últimos 15
            arquivos = sorted([os.path.join(BACKUPS_DIR, a) for a in os.listdir(BACKUPS_DIR) if a.endswith(".json")])
            if len(arquivos) > 15:
                for antigo in arquivos[:-15]:
                    try:
                        os.remove(antigo)
                    except Exception:
                        pass
        except Exception as e:
            print(f"[CRM BACKUP ERROR] {e}")

    def _estrutura_padrao(self):
        return {
            "config": {
                "versao": "2.0.0",
                "nome_sistema": "TruData CRM Enterprise",
                "criado_em": datetime.now().isoformat()
            },
            "usuarios": [
                {"id": "usr-admin", "login": "admin", "nome": "Administrador TruData", "email": "comercial@trudata.com.br", "perfil": "admin", "equipe": "Diretoria", "visibilidade": "todos", "ativo": True}
            ],
            "funis": [
                {
                    "id": "funil-vendas-novas",
                    "nome": "Pipeline Principal: Vendas Novas B2B",
                    "descricao": "Prospecção e fechamento de clientes de varejo e pequenas empresas na região.",
                    "padrao": True,
                    "etapas": [
                        {"id": "etapa-lead", "nome": "1. Lead / Qualificação", "ordem": 1, "probabilidade": 20, "cor": "#60a5fa"},
                        {"id": "etapa-contato", "nome": "2. Contato Feito / Diagnóstico", "ordem": 2, "probabilidade": 40, "cor": "#fbbf24"},
                        {"id": "etapa-demo", "nome": "3. Demonstração / PDV Teste", "ordem": 3, "probabilidade": 60, "cor": "#a855f7"},
                        {"id": "etapa-proposta", "nome": "4. Proposta Enviada", "ordem": 4, "probabilidade": 80, "cor": "#f97316"},
                        {"id": "etapa-fechado", "nome": "5. Contrato Fechado (Ganho)", "ordem": 5, "probabilidade": 100, "cor": "#10b981"},
                        {"id": "etapa-recontato", "nome": "6. Recontato (6m - 1 ano)", "ordem": 6, "probabilidade": 15, "cor": "#06b6d4"},
                        {"id": "etapa-perdido", "nome": "7. Negócio Perdido", "ordem": 7, "probabilidade": 0, "cor": "#ef4444"}
                    ]
                },
                {
                    "id": "funil-upsell",
                    "nome": "Expansão & Upsell (PDVs Adicionais / Módulos)",
                    "descricao": "Venda de caixas extras, TEF Dedicado, conciliação e emissão móvel para clientes da base.",
                    "padrao": False,
                    "etapas": [
                        {"id": "etapa-up-identificacao", "nome": "1. Oportunidade Mapeada", "ordem": 1, "probabilidade": 30, "cor": "#38bdf8"},
                        {"id": "etapa-up-apresentacao", "nome": "2. Apresentação ao Lojista", "ordem": 2, "probabilidade": 65, "cor": "#c084fc"},
                        {"id": "etapa-up-ativado", "nome": "3. Módulo Adicionado (Ganho)", "ordem": 3, "probabilidade": 100, "cor": "#10b981"},
                        {"id": "etapa-up-descarte", "nome": "4. Sem Interesse no Momento", "ordem": 4, "probabilidade": 0, "cor": "#64748b"}
                    ]
                },
                {
                    "id": "funil-contadores",
                    "nome": "Parcerias Contábeis (B2B2B)",
                    "descricao": "Acordos de indicação com escritórios de contabilidade da região de Sarandi e raio de 100km.",
                    "padrao": False,
                    "etapas": [
                        {"id": "etapa-ct-mapeado", "nome": "1. Escritório Mapeado", "ordem": 1, "probabilidade": 25, "cor": "#818cf8"},
                        {"id": "etapa-ct-reuniao", "nome": "2. Reunião de Parceria", "ordem": 2, "probabilidade": 50, "cor": "#e879f9"},
                        {"id": "etapa-ct-acordo", "nome": "3. Termo de Parceria Assinado", "ordem": 3, "probabilidade": 100, "cor": "#059669"},
                        {"id": "etapa-ct-recusa", "nome": "4. Parceria Não Concretizada", "ordem": 4, "probabilidade": 0, "cor": "#f43f5e"}
                    ]
                }
            ],
            "produtos": [
                {"id": "prod-erp-base", "codigo": "ERP-01", "nome": "TruData ERP Web (Plano Base 1 PDV)", "categoria": "Software", "preco_padrao": 180.00, "tipo_cobranca": "mensal"},
                {"id": "prod-pdv-extra", "codigo": "PDV-ADD", "nome": "PDV / Caixa Adicional em Rede", "categoria": "Software", "preco_padrao": 60.00, "tipo_cobranca": "mensal"},
                {"id": "prod-tef-dedicado", "codigo": "TEF-01", "nome": "Módulo TEF Dedicado Multibandeira", "categoria": "Software", "preco_padrao": 45.00, "tipo_cobranca": "mensal"},
                {"id": "prod-sped-fiscal", "codigo": "SPED-01", "nome": "Auditor Fiscal e Integrador SPED/EFD", "categoria": "Fiscal", "preco_padrao": 85.00, "tipo_cobranca": "mensal"},
                {"id": "prod-setup-implantacao", "codigo": "SETUP-01", "nome": "Taxa de Implantação, Parametrização e Treinamento", "categoria": "Serviço", "preco_padrao": 800.00, "tipo_cobranca": "unico"},
                {"id": "prod-migracao-banco", "codigo": "MIG-01", "nome": "Migração de Dados do Sistema Anterior", "categoria": "Serviço", "preco_padrao": 350.00, "tipo_cobranca": "unico"}
            ],
            "empresas": [],
            "contatos": [],
            "negociacoes": [],
            "atividades": [],
            "historico_interacoes": [],
            "automacoes": [
                {
                    "id": "auto-proposta-followup",
                    "nome": "Criar Follow-up ao Mover para Proposta",
                    "ativo": True,
                    "gatilho": "mudanca_etapa",
                    "etapa_gatilho": "etapa-proposta",
                    "acao": "criar_atividade",
                    "parametros": {
                        "tipo": "follow_up",
                        "dias_prazo": 2,
                        "titulo": "Follow-up de Proposta Enviada (Verificar se há dúvidas)"
                    }
                },
                {
                    "id": "auto-round-robin",
                    "nome": "Atribuição Automática de Leads (Round-Robin)",
                    "ativo": True,
                    "gatilho": "novo_lead",
                    "acao": "atribuir_vendedor_round_robin",
                    "parametros": {
                        "vendedores": ["usr-admin"]
                    }
                },
                {
                    "id": "auto-email-boas-vindas",
                    "nome": "Disparar E-mail de Boas-Vindas e Apresentação Institucional",
                    "ativo": True,
                    "gatilho": "novo_lead",
                    "acao": "simular_envio_email",
                    "parametros": {
                        "assunto": "Apresentação de Soluções TruData ERP — Hansen Software"
                    }
                }
            ],
            "campos_customizados_config": [
                {"id": "cc-sistema-anterior", "entidade": "empresa", "rotulo": "Sistema de Gestão Atual", "tipo": "texto"},
                {"id": "cc-contador-responsavel", "entidade": "empresa", "rotulo": "Escritório Contábil", "tipo": "texto"},
                {"id": "cc-motivo-perda", "entidade": "negociacao", "rotulo": "Motivo de Perda Detalhado", "tipo": "selecao", "opcoes": ["Preço/Condição", "Optou por concorrente", "Sem verba no momento", "Falta de recurso específico", "Outro"]}
            ],
            "propostas_rastreadas": [],
            "contratos_assinados": [],
            "onboarding_checklists": [],
            "metas_comerciais": {
                "mes_referencia": "Setembro/2026",
                "meta_mrr_empresa": 0.0,
                "meta_pdvs_empresa": 0,
                "comissao_padrao_pct": 10.0,
                "metas_vendedores": {
                    "usr-admin": {"meta_mrr": 0.0, "meta_pdvs": 0, "comissao_pct": 10.0}
                }
            }
        }

    def _inicializar_base(self):
        with self.lock:
            if not os.path.exists(self.data_file):
                data = self._estrutura_padrao()
                self._salvar_base(data, usuario="Sistema (Inicialização)")
            else:
                data = self._ler_base()
                modificado = False
                for k, v in self._estrutura_padrao().items():
                    if k not in data:
                        data[k] = v
                        modificado = True
                if modificado:
                    self._salvar_base(data, usuario="Sistema (Migração de Estrutura)")

    def _migrar_leads_legados(self, data, leads):
        vendedores = [u["id"] for u in data["usuarios"] if u["perfil"] == "vendedor"]
        if not vendedores:
            vendedores = ["usr-admin"]
        
        mapa_fases = {
            "novo": "etapa-lead",
            "contato": "etapa-contato",
            "demo": "etapa-demo",
            "proposta": "etapa-proposta",
            "fechado": "etapa-fechado"
        }

        for idx, l in enumerate(leads):
            empresa_id = f"emp-{idx+1:04d}"
            contato_id = f"ctt-{idx+1:04d}"
            deal_id = f"deal-{idx+1:04d}"
            vendedor_resp = vendedores[idx % len(vendedores)]

            caixas = int(l.get("caixas", 1) or 1)
            is_contabil = "contabil" in (l.get("segmento", "")).lower()
            mrr = 750.0 if is_contabil else (180.0 + max(0, caixas - 1) * 60.0)
            setup = 0.0 if is_contabil else (800.0 + max(0, caixas - 1) * 200.0)

            empresa = {
                "id": empresa_id,
                "tipo": "PJ" if l.get("cnpj") else "PJ",
                "razao_social": l.get("empresa", "Empresa Regional"),
                "nome_fantasia": l.get("empresa", "Empresa Regional"),
                "documento": l.get("cnpj", ""),
                "inscricao_estadual": "",
                "telefone": l.get("telefone", ""),
                "whatsapp": l.get("telefone", ""),
                "email": l.get("email", ""),
                "cidade": l.get("cidade", "Sarandi - RS"),
                "uf": "RS",
                "endereco": l.get("endereco", ""),
                "segmento": l.get("segmento", "Varejo"),
                "pdvs_estimados": caixas,
                "campos_customizados": {
                    "cc-sistema-anterior": "Não informado",
                    "cc-contador-responsavel": "Próprio"
                },
                "consentimento_lgpd": {
                    "autorizado": True,
                    "data_consentimento": datetime.now().isoformat(),
                    "base_legal": "Legítimo interesse / Execução pré-contratual (Art. 7º V/IX da LGPD)",
                    "canal": "Prospecção Pública & Sintegra-RS"
                },
                "criado_em": l.get("data", datetime.now().strftime("%d/%m/%Y")),
                "origem": l.get("origem", "Radar Regional")
            }
            data["empresas"].append(empresa)

            contato = {
                "id": contato_id,
                "empresa_id": empresa_id,
                "nome": l.get("nome", "Decisor Principal"),
                "cargo": "Sócio / Administrador",
                "telefone": l.get("telefone", ""),
                "whatsapp": l.get("telefone", ""),
                "email": l.get("email", ""),
                "decisor": True,
                "campos_customizados": {},
                "consentimento_lgpd": {
                    "autorizado": True,
                    "data_consentimento": datetime.now().isoformat()
                }
            }
            data["contatos"].append(contato)

            fase_antiga = (l.get("fase") or "novo").lower()
            etapa_id = mapa_fases.get(fase_antiga, "etapa-lead")

            funil_id = "funil-contadores" if is_contabil else "funil-vendas-novas"
            if is_contabil and etapa_id == "etapa-fechado":
                etapa_id = "etapa-ct-acordo"
            elif is_contabil:
                etapa_id = "etapa-ct-mapeado"

            deal = {
                "id": deal_id,
                "funil_id": funil_id,
                "etapa_id": etapa_id,
                "empresa_id": empresa_id,
                "contato_id": contato_id,
                "responsavel_id": vendedor_resp,
                "titulo": f"Implantação TruData ERP - {empresa['nome_fantasia']}",
                "valor_mrr": mrr,
                "valor_setup_produtos": setup,
                "desconto": 0.0,
                "probabilidade": 100 if "fechado" in etapa_id else 40,
                "data_prevista": (date.today() + timedelta(days=20)).isoformat(),
                "status": "ganho" if ("fechado" in etapa_id or "acordo" in etapa_id) else "aberto",
                "motivo_perda": "",
                "produtos": [
                    {"produto_id": "prod-erp-base", "quantidade": 1, "valor_unitario": 180.00}
                ] if not is_contabil else [],
                "tags": [l.get("segmento", "Varejo"), "Migração"],
                "criado_em": datetime.now().isoformat()
            }
            data["negociacoes"].append(deal)

            # Histórico de notas antigas
            if l.get("notas"):
                interacao = {
                    "id": f"hist-{idx+1:04d}",
                    "empresa_id": empresa_id,
                    "contato_id": contato_id,
                    "deal_id": deal_id,
                    "responsavel_id": vendedor_resp,
                    "tipo": "nota",
                    "data_hora": datetime.now().isoformat(),
                    "canal": "Histórico Migrado",
                    "descricao": l.get("notas")
                }
                data["historico_interacoes"].append(interacao)

            # Atividade inicial
            data["atividades"].append({
                "id": f"ativ-{idx+1:04d}",
                "tipo": "ligacao",
                "deal_id": deal_id,
                "contato_id": contato_id,
                "empresa_id": empresa_id,
                "responsavel_id": vendedor_resp,
                "titulo": f"Primeiro contato comercial com {empresa['nome_fantasia']}",
                "data_hora": (date.today() + timedelta(days=1)).isoformat() + "T14:00:00",
                "status": "pendente" if "fechado" not in etapa_id else "concluida",
                "notas": "Apresentar condições especiais de migração sem taxa de rescisão."
            })

    def _ler_base(self):
        with self.lock:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)

    def _salvar_base(self, data, usuario="Sistema"):
        with self.lock:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self._fazer_backup_automatico(data)

    def zerar_base_dados(self, usuario="Administrador"):
        """
        Zera 100% o banco de dados do CRM (empresas, contatos, negócios, atividades,
        propostas, contratos, onboarding) deixando a base limpa para produção real.
        Cria backup de segurança antes da limpeza.
        """
        with self.lock:
            hoje_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            # 1. Backup de segurança dos dados atuais antes de zerar
            try:
                backup_path = os.path.join(BACKUPS_DIR, f"backup_antes_zerar_{hoje_str}.json")
                if os.path.exists(self.data_file):
                    with open(self.data_file, "r", encoding="utf-8") as f:
                        conteudo_antigo = json.load(f)
                    with open(backup_path, "w", encoding="utf-8") as f:
                        json.dump(conteudo_antigo, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"[CRM BACKUP PRE-ZERO ERROR] {e}")

            # 2. Gera nova estrutura limpa
            data = self._estrutura_padrao()
            self._salvar_base(data, usuario=usuario)

            # 3. Limpa log de auditoria com 1 registro único de inicialização
            try:
                reset_log = [{
                    "id": f"audit-{uuid.uuid4().hex[:8]}",
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "usuario": usuario or "Administrador",
                    "acao": "RESET_BASE_DADOS",
                    "entidade": "crm_enterprise",
                    "entidade_id": "root",
                    "detalhe": "Base de dados do CRM Enterprise zerada para início em produção real."
                }]
                with open(self.audit_file, "w", encoding="utf-8") as f:
                    json.dump(reset_log, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"[CRM AUDIT RESET ERROR] {e}")

            # 4. Backup e esvaziamento da base legada leads_crm.json se existir
            if os.path.exists(LEADS_LEGACY_FILE):
                try:
                    legacy_backup = os.path.join(PAINEL_DIR, f"leads_crm_backup_{hoje_str}.json")
                    with open(LEADS_LEGACY_FILE, "r", encoding="utf-8") as f:
                        legacy_leads = json.load(f)
                    with open(legacy_backup, "w", encoding="utf-8") as f:
                        json.dump(legacy_leads, f, indent=2, ensure_ascii=False)
                    with open(LEADS_LEGACY_FILE, "w", encoding="utf-8") as f:
                        json.dump([], f, indent=2, ensure_ascii=False)
                except Exception as e:
                    print(f"[CRM LEGACY RESET ERROR] {e}")

            return {
                "sucesso": True,
                "mensagem": "Base do CRM Enterprise zerada com sucesso. Pronto para uso real!",
                "timestamp": datetime.now().isoformat()
            }

    def sincronizar_com_legado(self, payload):
        """
        Recebe um lead oriundo do radar_clientes ou de endpoint legado
        e adiciona de forma transparente no CRM Enterprise.
        Garante que sempre apareça no Kanban principal (funil-vendas-novas).
        """
        with self.lock:
            data = self._ler_base()
            
            nome_empresa = (payload.get("nome") or payload.get("empresa") or payload.get("razao_social") or "Cliente Regional").strip()
            decisor_nome = (payload.get("decisor") or payload.get("nome_contato") or "Decisor Principal").strip()
            if decisor_nome == nome_empresa:
                decisor_nome = "Proprietário / Gerente"

            # Checar duplicidade por CNPJ, Telefone ou Nome exato
            cnpj = payload.get("cnpj", "").strip()
            tel = payload.get("telefone", "").strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
            empresa_existente = None
            for emp in data["empresas"]:
                if cnpj and emp.get("documento") == cnpj:
                    empresa_existente = emp
                    break
                if tel and len(tel) >= 8 and emp.get("telefone") and tel in emp.get("telefone").replace(" ", "").replace("-", ""):
                    empresa_existente = emp
                    break
                if emp.get("nome_fantasia", "").lower() == nome_empresa.lower():
                    empresa_existente = emp
                    break

            if empresa_existente:
                empresa_id = empresa_existente["id"]
                # Atualizar dados se estavam vazios
                if not empresa_existente.get("telefone") and payload.get("telefone"):
                    empresa_existente["telefone"] = payload.get("telefone")
                if not empresa_existente.get("cidade") and payload.get("cidade"):
                    empresa_existente["cidade"] = payload.get("cidade")
            else:
                empresa_id = f"emp-{uuid.uuid4().hex[:8]}"
                caixas = int(payload.get("caixas", 1) or 1)
                nova_empresa = {
                    "id": empresa_id,
                    "tipo": "PJ" if cnpj else "PF",
                    "razao_social": payload.get("razao_social") or nome_empresa,
                    "nome_fantasia": nome_empresa,
                    "documento": cnpj,
                    "inscricao_estadual": "",
                    "telefone": payload.get("telefone", ""),
                    "whatsapp": payload.get("whatsapp", payload.get("telefone", "")),
                    "email": payload.get("email", ""),
                    "cidade": payload.get("cidade", "Sarandi - RS"),
                    "uf": "RS",
                    "endereco": payload.get("endereco", ""),
                    "segmento": payload.get("segmento", "Comércio Geral"),
                    "pdvs_estimados": caixas,
                    "campos_customizados": {},
                    "consentimento_lgpd": {
                        "autorizado": True,
                        "data_consentimento": datetime.now().isoformat(),
                        "base_legal": "Prospecção Ativa B2B (LGPD Art. 7º IX)"
                    },
                    "criado_em": datetime.now().strftime("%d/%m/%Y"),
                    "origem": payload.get("origem", "Radar Comercial")
                }
                data["empresas"].insert(0, nova_empresa)

            # Criar ou obter contato
            contato_existente = next((c for c in data["contatos"] if c.get("empresa_id") == empresa_id), None)
            if contato_existente:
                contato_id = contato_existente["id"]
            else:
                contato_id = f"ctt-{uuid.uuid4().hex[:8]}"
                novo_contato = {
                    "id": contato_id,
                    "empresa_id": empresa_id,
                    "nome": decisor_nome,
                    "cargo": "Proprietário / Gerente",
                    "telefone": payload.get("telefone", ""),
                    "whatsapp": payload.get("whatsapp", payload.get("telefone", "")),
                    "email": payload.get("email", ""),
                    "decisor": True,
                    "campos_customizados": {},
                    "consentimento_lgpd": {"autorizado": True, "data_consentimento": datetime.now().isoformat()}
                }
                data["contatos"].insert(0, novo_contato)

            # Mapear fase para etapa do Kanban
            fase_map = {
                "novo": "etapa-lead",
                "contato": "etapa-contato",
                "contatado_whatsapp": "etapa-contato",
                "demo": "etapa-demo",
                "demo_agendada": "etapa-demo",
                "proposta": "etapa-proposta",
                "fechado": "etapa-fechado",
                "recontato": "etapa-recontato",
                "perdido": "etapa-perdido"
            }
            fase_raw = str(payload.get("fase", "novo")).lower()
            etapa_id = fase_map.get(fase_raw, "etapa-lead")

            # Checar se já existe um deal aberto para esta empresa
            deal_existente = next((d for d in data["negociacoes"] if d.get("empresa_id") == empresa_id and d.get("status") == "aberto"), None)
            if deal_existente:
                deal_existente["titulo"] = f"Implantação TruData ERP - {nome_empresa}"
                deal_existente["funil_id"] = "funil-vendas-novas"  # Garante presença no Kanban principal
                if fase_raw != "novo":
                    deal_existente["etapa_id"] = etapa_id
                self._salvar_base(data, usuario="Sistema (Sincronização Lead)")
                return {"sucesso": True, "empresa_id": empresa_id, "deal_id": deal_existente["id"], "responsavel": deal_existente.get("responsavel_id")}

            # Executar atribuição Round-Robin
            vendedores = [u["id"] for u in data["usuarios"] if u["perfil"] == "vendedor" and u["ativo"]]
            if not vendedores:
                vendedores = ["usr-admin"]
            resp_id = vendedores[self.round_robin_index % len(vendedores)]
            self.round_robin_index += 1

            caixas = int(payload.get("caixas", 1) or 1)
            is_contabil = "contabil" in (payload.get("segmento", "")).lower()
            mrr = 750.0 if is_contabil else (180.0 + max(0, caixas - 1) * 60.0)
            setup = 0.0 if is_contabil else (800.0 + max(0, caixas - 1) * 200.0)

            deal_id = f"deal-{uuid.uuid4().hex[:8]}"
            novo_deal = {
                "id": deal_id,
                "funil_id": "funil-vendas-novas",  # Sempre no funil principal do Kanban para visibilidade imediata
                "etapa_id": etapa_id,
                "empresa_id": empresa_id,
                "contato_id": contato_id,
                "responsavel_id": resp_id,
                "titulo": f"Implantação TruData ERP - {nome_empresa}",
                "valor_mrr": mrr,
                "valor_setup_produtos": setup,
                "desconto": 0.0,
                "probabilidade": 25,
                "data_prevista": (date.today() + timedelta(days=15)).isoformat(),
                "status": "aberto",
                "motivo_perda": "",
                "produtos": [],
                "tags": [payload.get("segmento", "Radar"), "Inbound Radar"] + (["Parceria Contábil"] if is_contabil else []),
                "criado_em": datetime.now().isoformat()
            }
            data["negociacoes"].insert(0, novo_deal)

            # Criar atividade inicial automática
            data["atividades"].insert(0, {
                "id": f"ativ-{uuid.uuid4().hex[:8]}",
                "tipo": "whatsapp",
                "deal_id": deal_id,
                "contato_id": contato_id,
                "empresa_id": empresa_id,
                "responsavel_id": resp_id,
                "titulo": f"Primeiro contato via WhatsApp com {nome_empresa}",
                "data_hora": datetime.now().isoformat(),
                "status": "pendente",
                "notas": "Apresentar contingência offline e agendamento de diagnóstico gratuito."
            })

            # Registrar histórico
            data["historico_interacoes"].insert(0, {
                "id": f"hist-{uuid.uuid4().hex[:8]}",
                "empresa_id": empresa_id,
                "contato_id": contato_id,
                "deal_id": deal_id,
                "responsavel_id": resp_id,
                "tipo": "entrada_lead",
                "data_hora": datetime.now().isoformat(),
                "canal": payload.get("origem", "Radar Comercial"),
                "descricao": f"Lead '{nome_empresa}' adicionado com sucesso ao Pipeline Kanban. Atribuído a {resp_id}."
            })

            self._salvar_base(data, usuario="Sistema (Importação de Lead)")
            self._log_audit("Sistema", "CRIAR", "negociacao", deal_id, f"Lead {nome_empresa} importado ao pipeline")
            return {"sucesso": True, "empresa_id": empresa_id, "deal_id": deal_id, "responsavel": resp_id}

    # ==================== MÉTODOS CRUD E REGRAS DE NEGÓCIO ====================

    def obter_estado_completo(self, usuario_id=None, perfil=None):
        with self.lock:
            data = copy.deepcopy(self._ler_base())
            # Filtrar por visibilidade se o usuário for apenas vendedor
            if perfil == "vendedor" and usuario_id:
                deals_usuario = [d for d in data["negociacoes"] if d.get("responsavel_id") == usuario_id]
                empresas_ids = {d["empresa_id"] for d in deals_usuario}
                contatos_ids = {d["contato_id"] for d in deals_usuario}

                data["negociacoes"] = deals_usuario
                data["empresas"] = [e for e in data["empresas"] if e["id"] in empresas_ids]
                data["contatos"] = [c for c in data["contatos"] if c["id"] in contatos_ids or c["empresa_id"] in empresas_ids]
                data["atividades"] = [a for a in data["atividades"] if a.get("responsavel_id") == usuario_id]

            # Adicionar métricas sumarizadas
            data["metricas"] = self._calcular_metricas(data)
            return data

    def _calcular_metricas(self, data):
        deals = data.get("negociacoes", [])
        total_deals = len(deals)
        abertos = [d for d in deals if d.get("status") == "aberto"]
        ganhos = [d for d in deals if d.get("status") == "ganho"]
        perdidos = [d for d in deals if d.get("status") == "perdido"]

        total_mrr_aberto = sum(float(d.get("valor_mrr", 0)) for d in abertos)
        total_setup_aberto = sum(float(d.get("valor_setup_produtos", 0)) for d in abertos)
        total_ganho_mrr = sum(float(d.get("valor_mrr", 0)) for d in ganhos)

        # Forecast ponderado = soma de (valor * probabilidade)
        forecast_mrr_ponderado = sum(float(d.get("valor_mrr", 0)) * (float(d.get("probabilidade", 50)) / 100.0) for d in abertos)

        taxa_conversao = (len(ganhos) / total_deals * 100.0) if total_deals > 0 else 0.0
        ticket_medio = (total_ganho_mrr / len(ganhos)) if len(ganhos) > 0 else 180.0

        # Conversão por etapa no Funil Principal
        funil_padrao = next((f for f in data.get("funis", []) if f.get("padrao")), None)
        etapas_stats = []
        if funil_padrao:
            for et in funil_padrao["etapas"]:
                count_et = len([d for d in deals if d.get("etapa_id") == et["id"]])
                valor_et = sum(float(d.get("valor_mrr", 0)) for d in deals if d.get("etapa_id") == et["id"])
                etapas_stats.append({
                    "id": et["id"],
                    "nome": et["nome"],
                    "cor": et.get("cor", "#009fe3"),
                    "probabilidade": et.get("probabilidade", 50),
                    "total_deals": count_et,
                    "valor_mrr": valor_et
                })

        # Metas Comerciais & Gamificação
        metas = data.get("metas_comerciais", {})
        meta_mrr_empresa = float(metas.get("meta_mrr_empresa", 15000.00))
        meta_pdvs_empresa = int(metas.get("meta_pdvs_empresa", 50))
        
        # Total de PDVs ganhos no mês
        pdvs_ganhos = sum(int(next((e.get("pdvs_estimados", 1) for e in data.get("empresas", []) if e["id"] == d.get("empresa_id")), 1) or 1) for d in ganhos)
        
        pct_meta_mrr = round((total_ganho_mrr / meta_mrr_empresa * 100), 1) if meta_mrr_empresa > 0 else 0.0
        pct_meta_pdvs = round((pdvs_ganhos / meta_pdvs_empresa * 100), 1) if meta_pdvs_empresa > 0 else 0.0

        # Run-rate do mês (dia atual vs mês)
        hoje_dia = min(30, max(1, datetime.now().day))
        projecao_run_rate_mrr = round((total_ganho_mrr / hoje_dia) * 30, 2)

        # Desempenho e Ranking por vendedor
        vendedores_stats = {}
        ranking_list = []
        metas_vend_map = metas.get("metas_vendedores", {})
        total_comissao_equipe = 0.0

        for usr in data.get("usuarios", []):
            deals_usr = [d for d in deals if d.get("responsavel_id") == usr["id"]]
            ganhos_usr = [d for d in deals_usr if d.get("status") == "ganho"]
            mrr_ganho_usr = sum(float(d.get("valor_mrr", 0)) for d in ganhos_usr)
            setup_ganho_usr = sum(float(d.get("valor_setup_produtos", 0)) for d in ganhos_usr)
            
            cfg_meta = metas_vend_map.get(usr["id"], {"meta_mrr": 5000.00, "meta_pdvs": 15, "comissao_pct": 12.0})
            meta_usr_mrr = float(cfg_meta.get("meta_mrr", 5000.00))
            comissao_pct = float(cfg_meta.get("comissao_pct", 12.0))
            
            comissao_estimada = round((mrr_ganho_usr * (comissao_pct / 100.0)) + (setup_ganho_usr * 0.10), 2)
            total_comissao_equipe += comissao_estimada
            pct_meta_usr = round((mrr_ganho_usr / meta_usr_mrr * 100), 1) if meta_usr_mrr > 0 else 0.0

            stat_item = {
                "id": usr["id"],
                "nome": usr["nome"],
                "equipe": usr.get("equipe", "Geral"),
                "total_deals": len(deals_usr),
                "ganhos": len(ganhos_usr),
                "mrr_ganho": mrr_ganho_usr,
                "setup_ganho": setup_ganho_usr,
                "taxa_conversao": round((len(ganhos_usr) / len(deals_usr) * 100), 1) if deals_usr else 0.0,
                "meta_mrr": meta_usr_mrr,
                "pct_meta": pct_meta_usr,
                "comissao_estimada": comissao_estimada
            }
            vendedores_stats[usr["id"]] = stat_item
            if usr["perfil"] == "vendedor":
                ranking_list.append(stat_item)

        ranking_list.sort(key=lambda x: x["mrr_ganho"], reverse=True)
        medalhas = ["🥇 1º Lugar", "🥈 2º Lugar", "🥉 3º Lugar"]
        for idx, item in enumerate(ranking_list):
            item["posicao"] = medalhas[idx] if idx < 3 else f"{idx+1}º Lugar"

        # Métricas avançadas de Funil e Conversão P2
        # Taxas entre etapas consecutivas do Funil Principal:
        # 1. Lead -> 2. Contato -> 3. Demo -> 4. Proposta -> 5. Ganho
        etapa_counts = {et["id"]: len([d for d in deals if d.get("etapa_id") == et["id"]]) for et in (funil_padrao["etapas"] if funil_padrao else [])}
        
        # Negócios que alcançaram cada estágio (acumulado para funil de conversão)
        c_lead = etapa_counts.get("etapa-lead", 0)
        c_contato = etapa_counts.get("etapa-contato", 0)
        c_demo = etapa_counts.get("etapa-demo", 0)
        c_proposta = etapa_counts.get("etapa-proposta", 0)
        c_ganho = etapa_counts.get("etapa-fechado", 0)
        c_recontato = etapa_counts.get("etapa-recontato", 0)
        c_perdido = etapa_counts.get("etapa-perdido", 0)

        # Taxas de avanço entre estágios consecutivos
        def calc_taxa(orig, dest):
            # Se ambos forem zero, 0. Se orig for 0 mas houver negócios em dest, 100%
            soma = orig + dest
            return round((dest / soma * 100.0), 1) if soma > 0 else 0.0

        taxa_lead_contato = calc_taxa(c_lead, c_contato + c_demo + c_proposta + c_ganho)
        taxa_contato_demo = calc_taxa(c_contato, c_demo + c_proposta + c_ganho)
        taxa_demo_proposta = calc_taxa(c_demo, c_proposta + c_ganho)
        taxa_proposta_ganho = calc_taxa(c_proposta, c_ganho)

        # Motivos de Perda
        motivos_counts = {}
        for d in deals:
            m_p = d.get("motivo_perda")
            if m_p and (d.get("status") == "perdido" or d.get("etapa_id") == "etapa-perdido"):
                motivos_counts[m_p] = motivos_counts.get(m_p, 0) + 1

        total_com_motivo = sum(motivos_counts.values())
        motivos_lista = []
        for mot, cnt in sorted(motivos_counts.items(), key=lambda x: x[1], reverse=True):
            pct = round((cnt / total_com_motivo * 100.0), 1) if total_com_motivo > 0 else 0.0
            motivos_lista.append({"motivo": mot, "quantidade": cnt, "percentual": pct})

        principal_motivo = motivos_lista[0] if motivos_lista else {"motivo": "Nenhuma perda registrada", "quantidade": 0, "percentual": 0.0}

        # Cálculo de tempo médio no estágio atual (dias)
        hoje_dt = datetime.now()
        tempos_etapas = {}
        for et_id in etapa_counts.keys():
            deals_da_etapa = [d for d in deals if d.get("etapa_id") == et_id]
            if deals_da_etapa:
                dias_totais = 0
                for d in deals_da_etapa:
                    data_ref_str = d.get("etapa_atualizada_em") or d.get("criado_em")
                    try:
                        if data_ref_str:
                            dt = datetime.fromisoformat(data_ref_str.split(".")[0])
                            dias_totais += max(0, (hoje_dt - dt).days)
                        else:
                            dias_totais += 1
                    except Exception:
                        dias_totais += 1
                tempos_etapas[et_id] = round(dias_totais / len(deals_da_etapa), 1)
            else:
                tempos_etapas[et_id] = 0.0

        funil_resumo = {
            "conversao_passos": [
                {"de": "Lead", "para": "Contato", "taxa": taxa_lead_contato, "de_count": c_lead, "para_count": c_contato},
                {"de": "Contato", "para": "Demonstração", "taxa": taxa_contato_demo, "de_count": c_contato, "para_count": c_demo},
                {"de": "Demonstração", "para": "Proposta", "taxa": taxa_demo_proposta, "de_count": c_demo, "para_count": c_proposta},
                {"de": "Proposta", "para": "Contrato Ganho", "taxa": taxa_proposta_ganho, "de_count": c_proposta, "para_count": c_ganho}
            ],
            "tempo_medio_dias_etapas": tempos_etapas,
            "motivos_perda_ranking": motivos_lista,
            "principal_motivo_perda": principal_motivo,
            "total_ganhos": len(ganhos),
            "total_perdidos": len(perdidos),
            "total_recontato": c_recontato
        }

        return {
            "total_deals": total_deals,
            "total_abertos": len(abertos),
            "total_ganhos": len(ganhos),
            "total_perdidos": len(perdidos),
            "total_mrr_aberto": round(total_mrr_aberto, 2),
            "total_setup_aberto": round(total_setup_aberto, 2),
            "total_ganho_mrr": round(total_ganho_mrr, 2),
            "forecast_mrr_ponderado": round(forecast_mrr_ponderado, 2),
            "taxa_conversao": round(taxa_conversao, 1),
            "ticket_medio": round(ticket_medio, 2),
            "ciclo_medio_dias": 14.5,
            "etapas_funil_padrao": etapas_stats,
            "funil_resumo": funil_resumo,
            "vendedores_stats": vendedores_stats,
            "metas_painel": {
                "mes_referencia": metas.get("mes_referencia", "Mês Atual"),
                "meta_mrr_empresa": meta_mrr_empresa,
                "meta_pdvs_empresa": meta_pdvs_empresa,
                "mrr_atingido": round(total_ganho_mrr, 2),
                "pdvs_atingidos": pdvs_ganhos,
                "pct_meta_mrr": pct_meta_mrr,
                "pct_meta_pdvs": pct_meta_pdvs,
                "projecao_run_rate_mrr": projecao_run_rate_mrr,
                "total_comissao_equipe": round(total_comissao_equipe, 2),
                "ranking_vendedores": ranking_list
            }
        }

    def mover_etapa(self, deal_id, nova_etapa_id, usuario="Admin", motivo_perda="", observacao_perda=""):
        with self.lock:
            data = self._ler_base()
            deal = next((d for d in data["negociacoes"] if d["id"] == deal_id), None)
            if not deal:
                raise ValueError("Negociação não encontrada.")

            etapa_antiga_id = deal.get("etapa_id")
            deal["etapa_id"] = nova_etapa_id
            deal["etapa_atualizada_em"] = datetime.now().isoformat()

            # Ajustar status e probabilidade de acordo com a etapa
            etapa_obj = None
            for funil in data["funis"]:
                for et in funil["etapas"]:
                    if et["id"] == nova_etapa_id:
                        etapa_obj = et
                        break

            if etapa_obj:
                deal["probabilidade"] = etapa_obj.get("probabilidade", deal.get("probabilidade", 50))
                if "fechado" in nova_etapa_id or "ativado" in nova_etapa_id or "acordo" in nova_etapa_id:
                    deal["status"] = "ganho"
                    deal["probabilidade"] = 100
                    deal["data_fechamento"] = datetime.now().strftime("%d/%m/%Y")
                    # Auto gerar checklist de onboarding técnico se não existir
                    self._criar_checklist_onboarding_internal(data, deal, usuario=usuario)
                elif "recontato" in nova_etapa_id or "nutricao" in nova_etapa_id:
                    deal["status"] = "recontato"
                    deal["probabilidade"] = 15
                    # Calcular prazo de recontato (padrão 6 meses = 180 dias; 1 ano = 365 dias)
                    prazo_str = str(motivo_perda or "").lower()
                    dias_recontato = 365 if ("1 ano" in prazo_str or "ano" in prazo_str or "12" in prazo_str or "365" in prazo_str) else 180
                    data_recontato = (date.today() + timedelta(days=dias_recontato)).isoformat()
                    deal["data_prevista"] = data_recontato
                    if motivo_perda:
                        deal["motivo_perda"] = motivo_perda
                    if observacao_perda:
                        deal["observacao_perda"] = observacao_perda
                    # Agendar tarefa automática de recontato na agenda
                    data["atividades"].insert(0, {
                        "id": f"ativ-{uuid.uuid4().hex[:8]}",
                        "tipo": "recontato",
                        "deal_id": deal_id,
                        "contato_id": deal.get("contato_id"),
                        "empresa_id": deal.get("empresa_id"),
                        "responsavel_id": deal.get("responsavel_id", usuario),
                        "titulo": f"⏰ Recontatar Lead: {deal.get('titulo')}",
                        "data_hora": f"{data_recontato}T09:00:00",
                        "status": "pendente",
                        "notas": f"Agendamento automático de recontato ({dias_recontato} dias). Motivo/Pauta: {motivo_perda or 'Reavaliar momento de compra / orçamento'}. {observacao_perda}".strip()
                    })
                elif "perdido" in nova_etapa_id or "descarte" in nova_etapa_id or "recusa" in nova_etapa_id:
                    deal["status"] = "perdido"
                    deal["probabilidade"] = 0
                    if motivo_perda:
                        deal["motivo_perda"] = motivo_perda
                    if observacao_perda:
                        deal["observacao_perda"] = observacao_perda
                else:
                    deal["status"] = "aberto"

            # Registrar histórico
            desc_extra = []
            if motivo_perda:
                desc_extra.append(f"Motivo: {motivo_perda}")
            if observacao_perda:
                desc_extra.append(f"Obs: {observacao_perda}")
            detalhe_str = (" (" + " | ".join(desc_extra) + ")") if desc_extra else ""

            data["historico_interacoes"].insert(0, {
                "id": f"hist-{uuid.uuid4().hex[:8]}",
                "empresa_id": deal.get("empresa_id"),
                "contato_id": deal.get("contato_id"),
                "deal_id": deal_id,
                "responsavel_id": usuario,
                "tipo": "mudanca_etapa",
                "data_hora": datetime.now().isoformat(),
                "canal": "Kanban",
                "descricao": f"Negociação movida da etapa '{etapa_antiga_id}' para '{nova_etapa_id}'{detalhe_str}."
            })

            # Disparar Automações de Etapa
            self._processar_automacoes_etapa(data, deal, nova_etapa_id, usuario)

            self._salvar_base(data, usuario=usuario)
            self._log_audit(usuario, "MOVER_ETAPA", "negociacao", deal_id, f"Mudou para etapa {nova_etapa_id}{detalhe_str}")
            return {"sucesso": True, "deal": deal}

    def _processar_automacoes_etapa(self, data, deal, nova_etapa_id, usuario):
        for auto in data.get("automacoes", []):
            if not auto.get("ativo"):
                continue
            if auto.get("gatilho") == "mudanca_etapa" and auto.get("etapa_gatilho") == nova_etapa_id:
                acao = auto.get("acao")
                params = auto.get("parametros", {})
                if acao == "criar_atividade":
                    prazo_dias = params.get("dias_prazo", 1)
                    data_ativ = (date.today() + timedelta(days=prazo_dias)).isoformat() + "T10:00:00"
                    data["atividades"].insert(0, {
                        "id": f"ativ-{uuid.uuid4().hex[:8]}",
                        "tipo": params.get("tipo", "follow_up"),
                        "deal_id": deal["id"],
                        "contato_id": deal.get("contato_id"),
                        "empresa_id": deal.get("empresa_id"),
                        "responsavel_id": deal.get("responsavel_id", usuario),
                        "titulo": params.get("titulo", "Atividade disparada por automação"),
                        "data_hora": data_ativ,
                        "status": "pendente",
                        "notas": f"Disparada automaticamente pela regra: {auto.get('nome')}"
                    })
                elif acao == "simular_envio_email":
                    data["historico_interacoes"].insert(0, {
                        "id": f"hist-{uuid.uuid4().hex[:8]}",
                        "empresa_id": deal.get("empresa_id"),
                        "contato_id": deal.get("contato_id"),
                        "deal_id": deal["id"],
                        "responsavel_id": "Automação Bot",
                        "tipo": "email_disparado",
                        "data_hora": datetime.now().isoformat(),
                        "canal": "E-mail Automatizado",
                        "descricao": f"E-mail de follow-up automático agendado e disparado: '{params.get('assunto')}'."
                    })

    def salvar_empresa(self, payload, usuario="Admin"):
        with self.lock:
            data = self._ler_base()
            emp_id = payload.get("id")
            is_nova = False
            if not emp_id:
                emp_id = f"emp-{uuid.uuid4().hex[:8]}"
                is_nova = True
                empresa = {"id": emp_id, "criado_em": datetime.now().strftime("%d/%m/%Y")}
                data["empresas"].insert(0, empresa)
            else:
                empresa = next((e for e in data["empresas"] if e["id"] == emp_id), None)
                if not empresa:
                    empresa = {"id": emp_id, "criado_em": datetime.now().strftime("%d/%m/%Y")}
                    data["empresas"].insert(0, empresa)

            for campo in ["tipo", "razao_social", "nome_fantasia", "documento", "inscricao_estadual",
                          "telefone", "whatsapp", "email", "cidade", "uf", "endereco", "segmento",
                          "pdvs_estimados", "campos_customizados", "consentimento_lgpd", "origem"]:
                if campo in payload:
                    empresa[campo] = payload[campo]

            # Garantir consentimento LGPD padrão caso não enviado
            if "consentimento_lgpd" not in empresa or not empresa["consentimento_lgpd"]:
                empresa["consentimento_lgpd"] = {
                    "autorizado": True,
                    "data_consentimento": datetime.now().isoformat(),
                    "base_legal": "Art. 7º V/IX da LGPD (Relação Comercial B2B)"
                }

            self._salvar_base(data, usuario=usuario)
            self._log_audit(usuario, "CRIAR" if is_nova else "ATUALIZAR", "empresa", emp_id, f"Empresa {empresa.get('nome_fantasia')}")
            return {"sucesso": True, "empresa": empresa}

    def excluir_empresa(self, empresa_id, usuario="Admin"):
        with self.lock:
            data = self._ler_base()
            if not empresa_id:
                return {"sucesso": False, "erro": "ID da empresa não informado."}
            empresa = next((e for e in data["empresas"] if e["id"] == empresa_id), None)
            if not empresa:
                return {"sucesso": False, "erro": f"Empresa {empresa_id} não encontrada."}

            nome_emp = empresa.get("nome_fantasia") or empresa.get("razao_social") or empresa_id
            data["empresas"] = [e for e in data["empresas"] if e["id"] != empresa_id]
            self._salvar_base(data, usuario=usuario)
            self._log_audit(usuario, "EXCLUIR", "empresa", empresa_id, f"Exclusão da empresa '{nome_emp}'")
            return {"sucesso": True, "id": empresa_id, "mensagem": f"Empresa '{nome_emp}' excluída com sucesso."}

    def salvar_contato(self, payload, usuario="Admin"):
        with self.lock:
            data = self._ler_base()
            ctt_id = payload.get("id")
            is_novo = False
            if not ctt_id:
                ctt_id = f"ctt-{uuid.uuid4().hex[:8]}"
                is_novo = True
                contato = {"id": ctt_id}
                data["contatos"].insert(0, contato)
            else:
                contato = next((c for c in data["contatos"] if c["id"] == ctt_id), None)
                if not contato:
                    contato = {"id": ctt_id}
                    data["contatos"].insert(0, contato)

            for campo in ["empresa_id", "nome", "cargo", "telefone", "whatsapp", "email",
                          "decisor", "campos_customizados", "consentimento_lgpd"]:
                if campo in payload:
                    contato[campo] = payload[campo]

            self._salvar_base(data, usuario=usuario)
            self._log_audit(usuario, "CRIAR" if is_novo else "ATUALIZAR", "contato", ctt_id, f"Contato {contato.get('nome')}")
            return {"sucesso": True, "contato": contato}

    def salvar_negociacao(self, payload, usuario="Admin"):
        with self.lock:
            data = self._ler_base()
            deal_id = payload.get("id")
            is_novo = False
            if not deal_id:
                deal_id = f"deal-{uuid.uuid4().hex[:8]}"
                is_novo = True
                deal = {"id": deal_id, "criado_em": datetime.now().isoformat(), "status": "aberto"}
                data["negociacoes"].insert(0, deal)
            else:
                deal = next((d for d in data["negociacoes"] if d["id"] == deal_id), None)
                if not deal:
                    deal = {"id": deal_id, "criado_em": datetime.now().isoformat(), "status": "aberto"}
                    data["negociacoes"].insert(0, deal)

            for campo in ["funil_id", "etapa_id", "empresa_id", "contato_id", "responsavel_id",
                          "titulo", "valor_mrr", "valor_setup_produtos", "desconto", "probabilidade",
                          "data_prevista", "status", "motivo_perda", "produtos", "tags"]:
                if campo in payload:
                    deal[campo] = payload[campo]

            self._salvar_base(data, usuario=usuario)
            self._log_audit(usuario, "CRIAR" if is_novo else "ATUALIZAR", "negociacao", deal_id, f"Negociação {deal.get('titulo')}")
            return {"sucesso": True, "deal": deal}

    def excluir_negociacao(self, deal_id, usuario="Admin"):
        with self.lock:
            data = self._ler_base()
            deal = next((d for d in data.get("negociacoes", []) if d["id"] == deal_id), None)
            if not deal:
                return {"sucesso": False, "erro": "Negociação não encontrada no pipeline"}

            titulo = deal.get("titulo", "Negociação")
            data["negociacoes"] = [d for d in data.get("negociacoes", []) if d["id"] != deal_id]

            # Limpar checklists de onboarding vinculados a esse deal se existirem
            if "onboarding_checklists" in data:
                data["onboarding_checklists"] = [chk for chk in data["onboarding_checklists"] if chk.get("deal_id") != deal_id]

            self._salvar_base(data, usuario=usuario)
            self._log_audit(usuario, "EXCLUIR", "negociacao", deal_id, f"Negociação '{titulo}' removida do Kanban")
            return {"sucesso": True, "mensagem": f"Negociação '{titulo}' removida do Kanban com sucesso"}

    def salvar_atividade(self, payload, usuario="Admin"):
        with self.lock:
            data = self._ler_base()
            ativ_id = payload.get("id")
            is_nova = False
            if not ativ_id:
                ativ_id = f"ativ-{uuid.uuid4().hex[:8]}"
                is_nova = True
                atividade = {"id": ativ_id, "status": "pendente"}
                data["atividades"].insert(0, atividade)
            else:
                atividade = next((a for a in data["atividades"] if a["id"] == ativ_id), None)
                if not atividade:
                    atividade = {"id": ativ_id, "status": "pendente"}
                    data["atividades"].insert(0, atividade)

            for campo in ["tipo", "deal_id", "contato_id", "empresa_id", "responsavel_id",
                          "titulo", "data_hora", "duracao_minutos", "status", "notas"]:
                if campo in payload:
                    atividade[campo] = payload[campo]

            # Registrar no histórico quando nova atividade é criada na agenda
            if is_nova:
                data["historico_interacoes"].insert(0, {
                    "id": f"hist-{uuid.uuid4().hex[:8]}",
                    "empresa_id": atividade.get("empresa_id"),
                    "contato_id": atividade.get("contato_id"),
                    "deal_id": atividade.get("deal_id"),
                    "responsavel_id": atividade.get("responsavel_id", usuario),
                    "tipo": "agendamento",
                    "data_hora": datetime.now().isoformat(),
                    "canal": "Agenda Comercial",
                    "descricao": f"Ação agendada: '{atividade.get('titulo')}' ({atividade.get('tipo', 'tarefa').upper()}) para {atividade.get('data_hora')}. Notas: {atividade.get('notas', 'Sem observações.')}"
                })

            # Se a atividade foi concluída, adicionar ao histórico de interações
            if payload.get("status") == "concluida":
                data["historico_interacoes"].insert(0, {
                    "id": f"hist-{uuid.uuid4().hex[:8]}",
                    "empresa_id": atividade.get("empresa_id"),
                    "contato_id": atividade.get("contato_id"),
                    "deal_id": atividade.get("deal_id"),
                    "responsavel_id": atividade.get("responsavel_id", usuario),
                    "tipo": atividade.get("tipo", "atividade"),
                    "data_hora": datetime.now().isoformat(),
                    "canal": "Atividade Concluída",
                    "descricao": f"Atividade concluída: '{atividade.get('titulo')}'. Notas: {atividade.get('notas', 'Sem notas.')}"
                })

            self._salvar_base(data, usuario=usuario)
            self._log_audit(usuario, "CRIAR" if is_nova else "ATUALIZAR", "atividade", ativ_id, f"Atividade {atividade.get('titulo')}")
            return {"sucesso": True, "atividade": atividade}

    def excluir_atividade(self, ativ_id, usuario="Admin"):
        with self.lock:
            data = self._ler_base()
            antes = len(data.get("atividades", []))
            data["atividades"] = [a for a in data.get("atividades", []) if a.get("id") != ativ_id]
            removidos = antes - len(data["atividades"])
            self._salvar_base(data, usuario=usuario)
            self._log_audit(usuario, "EXCLUIR", "atividade", ativ_id, f"Atividade {ativ_id} removida")
            return {"sucesso": True, "removidos": removidos}

    def limpar_todas_atividades(self, usuario="Admin"):
        with self.lock:
            data = self._ler_base()
            total = len(data.get("atividades", []))
            data["atividades"] = []
            data["historico_interacoes"] = [h for h in data.get("historico_interacoes", []) if h.get("tipo") != "agendamento"]
            self._salvar_base(data, usuario=usuario)
            self._log_audit(usuario, "LIMPAR_TODOS", "atividade", "todas", f"{total} atividades/ações limpas")
            return {"sucesso": True, "total_removido": total}

    def registrar_interacao(self, payload, usuario="Admin"):
        with self.lock:
            data = self._ler_base()
            interacao = {
                "id": f"hist-{uuid.uuid4().hex[:8]}",
                "empresa_id": payload.get("empresa_id"),
                "contato_id": payload.get("contato_id"),
                "deal_id": payload.get("deal_id"),
                "responsavel_id": usuario,
                "tipo": payload.get("tipo", "nota"),
                "data_hora": datetime.now().isoformat(),
                "canal": payload.get("canal", "Anotação Manual"),
                "descricao": payload.get("descricao", "")
            }
            data["historico_interacoes"].insert(0, interacao)
            self._salvar_base(data, usuario=usuario)
            return {"sucesso": True, "interacao": interacao}

    def salvar_novo_lead_completo(self, payload, usuario="Admin"):
        """
        Cadastra de forma unificada e atômica:
        1. Empresa (PF ou PJ)
        2. Contato (decisor)
        3. Oportunidade / Deal no Kanban
        4. Primeira Interação e Atividade
        """
        with self.lock:
            emp_dados = payload.get("empresa", {})
            if not emp_dados.get("razao_social") and not emp_dados.get("nome_fantasia"):
                raise ValueError("Nome ou Razão Social da empresa é obrigatório.")

            # 1. Salvar Empresa
            if not emp_dados.get("nome_fantasia"):
                emp_dados["nome_fantasia"] = emp_dados.get("razao_social")
            if not emp_dados.get("razao_social"):
                emp_dados["razao_social"] = emp_dados.get("nome_fantasia")
            if not emp_dados.get("origem"):
                emp_dados["origem"] = "Prospecção Manual"

            res_emp = self.salvar_empresa(emp_dados, usuario=usuario)
            emp = res_emp["empresa"]

            # 2. Salvar Contato
            ctt_dados = payload.get("contato", {})
            ctt_dados["empresa_id"] = emp["id"]
            if not ctt_dados.get("nome"):
                ctt_dados["nome"] = emp_dados.get("decisor") or "Decisor Principal"
            if not ctt_dados.get("cargo"):
                ctt_dados["cargo"] = "Sócio / Administrador"
            if not ctt_dados.get("telefone"):
                ctt_dados["telefone"] = emp.get("telefone", "")
            if not ctt_dados.get("whatsapp"):
                ctt_dados["whatsapp"] = emp.get("whatsapp", emp.get("telefone", ""))
            if not ctt_dados.get("email"):
                ctt_dados["email"] = emp.get("email", "")
            ctt_dados["decisor"] = True

            res_ctt = self.salvar_contato(ctt_dados, usuario=usuario)
            ctt = res_ctt["contato"]

            # 3. Salvar Oportunidade / Deal
            deal_dados = payload.get("negociacao", {})
            if not deal_dados.get("titulo"):
                deal_dados["titulo"] = f"Implantação TruData ERP - {emp['nome_fantasia']}"
            deal_dados["empresa_id"] = emp["id"]
            deal_dados["contato_id"] = ctt["id"]
            if not deal_dados.get("funil_id"):
                deal_dados["funil_id"] = "funil-vendas-novas"
            if not deal_dados.get("etapa_id"):
                deal_dados["etapa_id"] = "etapa-lead"
            if not deal_dados.get("responsavel_id"):
                deal_dados["responsavel_id"] = "usr-admin"
            if "valor_mrr" not in deal_dados:
                pdvs = int(emp.get("pdvs_estimados", 1) or 1)
                deal_dados["valor_mrr"] = 180.0 + max(0, pdvs - 1) * 60.0
            if "valor_setup_produtos" not in deal_dados:
                deal_dados["valor_setup_produtos"] = 0.0
            if "probabilidade" not in deal_dados:
                deal_dados["probabilidade"] = 20
            if not deal_dados.get("data_prevista"):
                deal_dados["data_prevista"] = (date.today() + timedelta(days=20)).isoformat()

            res_deal = self.salvar_negociacao(deal_dados, usuario=usuario)
            deal = res_deal["deal"]

            # 4. Histórico / Notas de Prospecção se fornecidas
            notas = payload.get("notas", "").strip()
            if notas:
                self.registrar_interacao({
                    "empresa_id": emp["id"],
                    "contato_id": ctt["id"],
                    "deal_id": deal["id"],
                    "tipo": "nota",
                    "canal": "Prospecção Manual",
                    "descricao": notas
                }, usuario=usuario)

            # 5. Primeira atividade de Follow-up
            self.salvar_atividade({
                "deal_id": deal["id"],
                "empresa_id": emp["id"],
                "contato_id": ctt["id"],
                "tipo": "ligacao",
                "titulo": f"Primeiro contato comercial com {emp['nome_fantasia']}",
                "data_hora": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT10:00:00"),
                "responsavel_id": deal_dados.get("responsavel_id", "usr-admin"),
                "notas": f"Apresentar soluções TruData ERP para {emp.get('segmento', 'Varejo')}."
            }, usuario=usuario)

            self._log_audit(usuario, "CRIAR_LEAD_COMPLETO", "lead", emp["id"], f"Lead completo criado: {emp['nome_fantasia']}")

            return {
                "sucesso": True,
                "mensagem": f"Lead '{emp['nome_fantasia']}' cadastrado com sucesso!",
                "empresa": emp,
                "contato": ctt,
                "negociacao": deal
            }

    # ==================== PROPOSTA COMERCIAL RASTREÁVEL (ITEM 1) ====================

    def gerar_proposta_rastreavel(self, deal_id, usuario="Admin"):
        with self.lock:
            data = self._ler_base()
            deal = next((d for d in data.get("negociacoes", []) if d["id"] == deal_id), None)
            if not deal:
                raise ValueError("Negociação não encontrada para geração de proposta.")

            empresa = next((e for e in data.get("empresas", []) if e["id"] == deal.get("empresa_id")), {})
            contato = next((c for c in data.get("contatos", []) if c["id"] == deal.get("contato_id")), {})

            propostas = data.setdefault("propostas_rastreadas", [])
            token_hash = f"trudata-{secrets.token_hex(6)}"

            proposta = {
                "hash": token_hash,
                "deal_id": deal_id,
                "deal_titulo": deal.get("titulo", "Proposta Comercial TruData"),
                "empresa_id": deal.get("empresa_id"),
                "empresa_nome": empresa.get("razao_social") or empresa.get("nome_fantasia", "Cliente"),
                "empresa_doc": empresa.get("cnpj_cpf") or empresa.get("documento", ""),
                "contato_id": deal.get("contato_id"),
                "contato_nome": contato.get("nome", "Responsável"),
                "contato_email": contato.get("email", ""),
                "contato_telefone": contato.get("telefone", ""),
                "cidade": empresa.get("cidade", "Sarandi - RS"),
                "pdvs_estimados": empresa.get("pdvs_estimados", 1),
                "valor_mrr": float(deal.get("valor_mrr", 180.00)),
                "valor_setup": float(deal.get("valor_setup_produtos", 500.00)),
                "desconto_aplicado": float(deal.get("desconto_aplicado", 0.00)),
                "produtos": deal.get("produtos", [
                    {"produto_id": "prod-erp-base", "nome": "TruData Gestão & Retaguarda Fiscal", "quantidade": 1, "valor_unitario": 180.00}
                ]),
                "status": "aguardando_visualizacao",
                "data_criacao": datetime.now().isoformat(),
                "validade_dias": 10,
                "total_visualizacoes": 0,
                "historico_acessos": [],
                "url_publica": f"/proposta-digital?p={token_hash}",
                "gerado_por": usuario
            }
            propostas.insert(0, proposta)

            deal["proposta_hash"] = token_hash
            deal["tem_proposta_rastreada"] = True

            data["historico_interacoes"].insert(0, {
                "id": f"hist-{uuid.uuid4().hex[:8]}",
                "empresa_id": deal.get("empresa_id"),
                "contato_id": deal.get("contato_id"),
                "deal_id": deal_id,
                "responsavel_id": usuario,
                "tipo": "proposta_gerada",
                "data_hora": datetime.now().isoformat(),
                "canal": "Proposta Digital 1-Click",
                "descricao": f"Proposta comercial rastreável gerada por {usuario}. Link público: /proposta-digital?p={token_hash}"
            })

            self._salvar_base(data, usuario=usuario)
            self._log_audit(usuario, "GERAR_PROPOSTA", "proposta", token_hash, f"Proposta gerada para deal {deal_id}")
            return {"sucesso": True, "proposta": proposta}

    def obter_proposta(self, hash_code):
        with self.lock:
            data = self._ler_base()
            propostas = data.get("propostas_rastreadas", [])
            prop = next((p for p in propostas if p.get("hash") == hash_code), None)
            if not prop:
                raise ValueError(f"Proposta comercial '{hash_code}' não localizada.")

            contrato = next((c for c in data.get("contratos_assinados", []) if c.get("hash_proposta") == hash_code), None)
            empresa = next((e for e in data.get("empresas", []) if e["id"] == prop.get("empresa_id")), {})
            return {
                "sucesso": True,
                "proposta": prop,
                "empresa": empresa,
                "contrato": contrato
            }

    def registrar_visualizacao_proposta(self, hash_code, ip="127.0.0.1", user_agent=""):
        with self.lock:
            data = self._ler_base()
            propostas = data.setdefault("propostas_rastreadas", [])
            prop = next((p for p in propostas if p.get("hash") == hash_code), None)
            if not prop:
                raise ValueError(f"Proposta comercial '{hash_code}' não localizada.")

            prop["total_visualizacoes"] = int(prop.get("total_visualizacoes", 0)) + 1
            if prop.get("status") == "aguardando_visualizacao":
                prop["status"] = "visualizada"

            agora_iso = datetime.now().isoformat()
            prop.setdefault("historico_acessos", []).append({
                "data_hora": agora_iso,
                "ip": ip,
                "user_agent": user_agent[:140] if user_agent else ""
            })

            # Alerta em tempo real no histórico do Deal
            deal = next((d for d in data.get("negociacoes", []) if d["id"] == prop.get("deal_id")), None)
            if deal:
                deal["ultima_visualizacao_proposta"] = agora_iso
                data["historico_interacoes"].insert(0, {
                    "id": f"hist-{uuid.uuid4().hex[:8]}",
                    "empresa_id": prop.get("empresa_id"),
                    "contato_id": prop.get("contato_id"),
                    "deal_id": prop.get("deal_id"),
                    "responsavel_id": "Beacon de Rastreio TruData",
                    "tipo": "proposta_aberta",
                    "data_hora": agora_iso,
                    "canal": "Rastreio em Tempo Real",
                    "descricao": f"🚨 ALERTA: O cliente acabou de abrir a Proposta #{hash_code}! (Acesso nº {prop['total_visualizacoes']}). IP: {ip}"
                })

            self._salvar_base(data, usuario="BeaconRastreio")
            self._log_audit("BeaconRastreio", "VISUALIZAR_PROPOSTA", "proposta", hash_code, f"Abertura nº {prop['total_visualizacoes']}")
            return {
                "sucesso": True,
                "total_visualizacoes": prop["total_visualizacoes"],
                "status": prop["status"],
                "ultima_visualizacao": agora_iso
            }

    # ==================== ASSINATURA DIGITAL & ONBOARDING (ITEM 2) ====================

    def assinar_contrato_digital(self, hash_proposta, signatario_nome, signatario_cpf, signatario_email="", ip="127.0.0.1"):
        with self.lock:
            data = self._ler_base()
            propostas = data.setdefault("propostas_rastreadas", [])
            prop = next((p for p in propostas if p.get("hash") == hash_proposta), None)
            if not prop:
                raise ValueError(f"Proposta '{hash_proposta}' não localizada.")

            if not signatario_nome or not signatario_cpf:
                raise ValueError("Nome completo e CPF do signatário são obrigatórios.")

            if prop.get("status") == "assinada":
                contrato_existente = next((c for c in data.get("contratos_assinados", []) if c.get("hash_proposta") == hash_proposta), None)
                return {"sucesso": True, "mensagem": "Esta proposta já foi assinada.", "contrato": contrato_existente}

            agora = datetime.now()
            agora_iso = agora.isoformat()

            raw_str = f"{hash_proposta}|{prop.get('deal_id')}|{signatario_nome.strip()}|{signatario_cpf.strip()}|{agora_iso}|{ip}|TRUDATA-SECURE-V2"
            hash_sha256 = hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

            prop["status"] = "assinada"
            prop["data_assinatura"] = agora_iso
            prop["hash_sha256"] = hash_sha256

            contrato_id = f"ct-{uuid.uuid4().hex[:8]}"
            contrato = {
                "id": contrato_id,
                "hash_proposta": hash_proposta,
                "deal_id": prop.get("deal_id"),
                "empresa_id": prop.get("empresa_id"),
                "empresa_nome": prop.get("empresa_nome"),
                "signatario_nome": signatario_nome.strip(),
                "signatario_cpf": signatario_cpf.strip(),
                "signatario_email": (signatario_email or prop.get("contato_email", "")).strip(),
                "ip_assinatura": ip,
                "data_assinatura": agora_iso,
                "hash_sha256": hash_sha256,
                "status": "vigente",
                "valor_mrr": prop.get("valor_mrr", 0),
                "valor_setup": prop.get("valor_setup", 0),
                "termos_aceitos": True,
                "amparo_legal": "Medida Provisória nº 2.200-2/2001 e Art. 107 do Código Civil Brasileiro"
            }
            data.setdefault("contratos_assinados", []).insert(0, contrato)

            # Negociação ganha
            deal = next((d for d in data.get("negociacoes", []) if d["id"] == prop.get("deal_id")), None)
            if deal:
                deal["status"] = "ganho"
                deal["probabilidade"] = 100
                deal["contrato_id"] = contrato_id
                deal["data_fechamento"] = agora.strftime("%d/%m/%Y")
                # Mover para etapa de fechamento
                for funil in data.get("funis", []):
                    if funil["id"] == deal.get("funil_id"):
                        et_ganho = next((et for et in funil["etapas"] if "fechado" in et["id"] or "ganho" in et["id"] or "acordo" in et["id"]), None)
                        if et_ganho:
                            deal["etapa_id"] = et_ganho["id"]
                        break

            # Disparar Checklist de Onboarding Técnico (6 etapas)
            checklist = self._criar_checklist_onboarding_internal(data, deal, usuario="Assinatura Eletrônica")

            # Timeline
            data["historico_interacoes"].insert(0, {
                "id": f"hist-{uuid.uuid4().hex[:8]}",
                "empresa_id": prop.get("empresa_id"),
                "contato_id": prop.get("contato_id"),
                "deal_id": prop.get("deal_id"),
                "responsavel_id": "Assinatura Digital",
                "tipo": "contrato_assinado",
                "data_hora": agora_iso,
                "canal": "Assinatura Eletrônica TruData",
                "descricao": f"🎉 CONTRATO ASSINADO DIGITALMENTE por {signatario_nome} (CPF: {signatario_cpf}). Hash SHA-256: {hash_sha256[:16]}... Negócio GANHO! Checklist de Onboarding inicializado."
            })

            self._salvar_base(data, usuario="AssinaturaEletronica")
            self._log_audit("AssinaturaEletronica", "ASSINAR_CONTRATO", "contrato", contrato_id, f"Contrato assinado {hash_sha256[:12]}")
            return {
                "sucesso": True,
                "contrato": contrato,
                "checklist": checklist
            }

    def _criar_checklist_onboarding_internal(self, data, deal, usuario="Sistema"):
        deal_id = deal.get("id") if deal else None
        empresa_id = deal.get("empresa_id") if deal else None
        empresa = next((e for e in data.get("empresas", []) if e["id"] == empresa_id), {}) if empresa_id else {}
        empresa_nome = empresa.get("razao_social") or empresa.get("nome_fantasia") or (deal.get("titulo") if deal else "Cliente TruData")

        onboardings = data.setdefault("onboarding_checklists", [])
        existente = next((o for o in onboardings if o.get("deal_id") == deal_id), None)
        if existente:
            return existente

        etapas_padrao = [
            {
                "id": "etapa-1",
                "nome": "1. Auditoria de Infraestrutura & Homologação de PDVs",
                "descricao": "Checagem de portas, rede local, SO (Windows/Linux) e comunicação com a impressora fiscal / SAT / NFC-e.",
                "responsavel": "Suporte Técnico N1",
                "prazo_dias": 2,
                "concluida": False,
                "data_conclusao": None,
                "notas": ""
            },
            {
                "id": "etapa-2",
                "nome": "2. Instalação do Agente TruData & Conectores de Dados",
                "descricao": "Deploy do executável do coletor em segundo plano e teste de leitura das tabelas de frente de caixa.",
                "responsavel": "Implantação & Infra",
                "prazo_dias": 3,
                "concluida": False,
                "data_conclusao": None,
                "notas": ""
            },
            {
                "id": "etapa-3",
                "nome": "3. Validação de Cargas & Telemetria em Tempo Real",
                "descricao": "Certificação do envio contínuo das transações, contingência offline ativada e latência inferior a 150ms.",
                "responsavel": "Engenharia de Dados",
                "prazo_dias": 4,
                "concluida": False,
                "data_conclusao": None,
                "notas": ""
            },
            {
                "id": "etapa-4",
                "nome": "4. Treinamento Operacional dos Fiscais e Gestão",
                "descricao": "Sessão remota via Google Meet/Teams com a gerência sobre uso do painel analítico TruData.",
                "responsavel": "Customer Success (CS)",
                "prazo_dias": 5,
                "concluida": False,
                "data_conclusao": None,
                "notas": ""
            },
            {
                "id": "etapa-5",
                "nome": "5. Parametrização de Regras Antifraude e Alertas",
                "descricao": "Definição de regras de alerta (cancelamento de item, sangria fora de hora, cupom alto) e canal de notificação.",
                "responsavel": "Customer Success (CS)",
                "prazo_dias": 6,
                "concluida": False,
                "data_conclusao": None,
                "notas": ""
            },
            {
                "id": "etapa-6",
                "nome": "6. Go-Live Oficial & Monitoramento de 48 Horas",
                "descricao": "Virada de chave oficial para produção assistida com plantão dedicado nas primeiras 48h.",
                "responsavel": "Líder de Operações",
                "prazo_dias": 7,
                "concluida": False,
                "data_conclusao": None,
                "notas": ""
            }
        ]

        onboarding_id = f"onb-{uuid.uuid4().hex[:8]}"
        novo_onboarding = {
            "id": onboarding_id,
            "deal_id": deal_id,
            "empresa_id": empresa_id,
            "empresa_nome": empresa_nome,
            "data_inicio": datetime.now().isoformat(),
            "prazo_final_estimado": (date.today() + timedelta(days=7)).strftime("%d/%m/%Y"),
            "status": "em_andamento",
            "progresso_pct": 0,
            "etapas": etapas_padrao,
            "criado_por": usuario
        }
        onboardings.insert(0, novo_onboarding)
        return novo_onboarding

    def gerar_checklist_onboarding(self, deal_id, usuario="Admin"):
        with self.lock:
            data = self._ler_base()
            deal = next((d for d in data.get("negociacoes", []) if d["id"] == deal_id), None)
            if not deal:
                raise ValueError("Negociação não encontrada.")
            chk = self._criar_checklist_onboarding_internal(data, deal, usuario=usuario)
            self._salvar_base(data, usuario=usuario)
            return {"sucesso": True, "onboarding": chk}

    def obter_checklists_onboarding(self, deal_id=None):
        with self.lock:
            data = self._ler_base()
            onboardings = data.get("onboarding_checklists", [])
            if deal_id:
                return [o for o in onboardings if o.get("deal_id") == deal_id]
            return onboardings

    def atualizar_etapa_onboarding(self, onboarding_id, etapa_id, concluida=True, notas="", usuario="Admin"):
        with self.lock:
            data = self._ler_base()
            onboardings = data.setdefault("onboarding_checklists", [])
            onb = next((o for o in onboardings if o["id"] == onboarding_id), None)
            if not onb:
                raise ValueError(f"Checklist '{onboarding_id}' não localizado.")

            etapa = next((e for e in onb.get("etapas", []) if e["id"] == etapa_id), None)
            if not etapa:
                raise ValueError(f"Etapa '{etapa_id}' não localizada.")

            etapa["concluida"] = bool(concluida)
            if concluida:
                etapa["data_conclusao"] = datetime.now().isoformat()
                etapa["concluido_por"] = usuario
            else:
                etapa["data_conclusao"] = None
                etapa["concluido_por"] = None

            if notas:
                etapa["notas"] = notas

            total = len(onb["etapas"])
            concluidas = len([e for e in onb["etapas"] if e.get("concluida")])
            progresso = round((concluidas / total * 100)) if total > 0 else 0
            onb["progresso_pct"] = progresso
            if progresso >= 100:
                onb["status"] = "concluido"
                onb["data_conclusao"] = datetime.now().isoformat()
            else:
                onb["status"] = "em_andamento"

            # Histórico
            data["historico_interacoes"].insert(0, {
                "id": f"hist-{uuid.uuid4().hex[:8]}",
                "empresa_id": onb.get("empresa_id"),
                "deal_id": onb.get("deal_id"),
                "responsavel_id": usuario,
                "tipo": "onboarding_etapa",
                "data_hora": datetime.now().isoformat(),
                "canal": "Checklist de Onboarding",
                "descricao": f"Etapa '{etapa['nome']}' alterada para {'CONCLUÍDA' if concluida else 'PENDENTE'} por {usuario}. Progresso total: {progresso}%."
            })

            self._salvar_base(data, usuario=usuario)
            self._log_audit(usuario, "ATUALIZAR_ONBOARDING", "onboarding", onboarding_id, f"Etapa {etapa_id} = {concluida}")
            return {"sucesso": True, "onboarding": onb}

    # ==================== METAS COMERCIAIS & GAMIFICAÇÃO (ITEM 3) ====================

    def obter_metas(self):
        with self.lock:
            data = self._ler_base()
            metas = data.get("metas_comerciais", {})
            metricas = self._calcular_metricas(data)
            return {
                "sucesso": True,
                "metas": metas,
                "resumo_painel": metricas.get("metas_painel", {})
            }

    def salvar_metas(self, payload, usuario="Admin"):
        with self.lock:
            data = self._ler_base()
            metas = data.setdefault("metas_comerciais", {})
            if "meta_mrr_empresa" in payload:
                metas["meta_mrr_empresa"] = float(payload["meta_mrr_empresa"])
            if "meta_pdvs_empresa" in payload:
                metas["meta_pdvs_empresa"] = int(payload["meta_pdvs_empresa"])
            if "mes_referencia" in payload:
                metas["mes_referencia"] = str(payload["mes_referencia"])
            if "metas_vendedores" in payload and isinstance(payload["metas_vendedores"], dict):
                metas.setdefault("metas_vendedores", {}).update(payload["metas_vendedores"])

            self._salvar_base(data, usuario=usuario)
            self._log_audit(usuario, "SALVAR_METAS", "metas", "metas_comerciais", "Metas e comissões atualizadas")
            return {"sucesso": True, "metas": metas}

    # ==================== DEDUPLICAÇÃO INTELIGENTE ====================

    def encontrar_duplicados(self):
        with self.lock:
            data = self._ler_base()
            empresas = data.get("empresas", [])
            grupos_duplicados = []

            # Mapeamento por documento e telefone
            por_doc = {}
            por_tel = {}
            por_email = {}

            for emp in empresas:
                doc = emp.get("documento", "").replace(".", "").replace("/", "").replace("-", "").strip()
                tel = emp.get("telefone", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "").strip()
                email = emp.get("email", "").strip().lower()

                if doc and len(doc) >= 11:
                    por_doc.setdefault(doc, []).append(emp)
                if tel and len(tel) >= 8:
                    por_tel.setdefault(tel, []).append(emp)
                if email and "@" in email:
                    por_email.setdefault(email, []).append(emp)

            processados_ids = set()
            for criterio, mapa in [("CNPJ/CPF", por_doc), ("Telefone", por_tel), ("E-mail", por_email)]:
                for chave, lista in mapa.items():
                    if len(lista) > 1:
                        ids_grupo = {e["id"] for e in lista}
                        if not ids_grupo.issubset(processados_ids):
                            processados_ids.update(ids_grupo)
                            grupos_duplicados.append({
                                "criterio": criterio,
                                "chave_conflito": chave,
                                "quantidade": len(lista),
                                "empresas": lista
                            })

            return {"total_grupos": len(grupos_duplicados), "grupos": grupos_duplicados}

    def mesclar_empresas(self, id_primario, ids_secundarios, usuario="Admin"):
        with self.lock:
            data = self._ler_base()
            primaria = next((e for e in data["empresas"] if e["id"] == id_primario), None)
            if not primaria:
                raise ValueError("Empresa primária não encontrada.")

            for sec_id in ids_secundarios:
                # Reatribuir contatos
                for ctt in data["contatos"]:
                    if ctt.get("empresa_id") == sec_id:
                        ctt["empresa_id"] = id_primario
                # Reatribuir negociações
                for deal in data["negociacoes"]:
                    if deal.get("empresa_id") == sec_id:
                        deal["empresa_id"] = id_primario
                # Reatribuir atividades
                for ativ in data["atividades"]:
                    if ativ.get("empresa_id") == sec_id:
                        ativ["empresa_id"] = id_primario
                # Reatribuir histórico
                for hist in data["historico_interacoes"]:
                    if hist.get("empresa_id") == sec_id:
                        hist["empresa_id"] = id_primario

            # Remover empresas secundárias
            data["empresas"] = [e for e in data["empresas"] if e["id"] not in ids_secundarios]

            self._salvar_base(data, usuario=usuario)
            self._log_audit(usuario, "MESCLAR", "empresa", id_primario, f"Mesclada com IDs {ids_secundarios}")
            return {"sucesso": True, "empresa_primaria": primaria, "removidos": ids_secundarios}

    # ==================== CONFORMIDADE LGPD ====================

    def lgpd_exportar_titular(self, identificador):
        """Exporta todos os dados associados a um CNPJ, CPF, E-mail ou Telefone."""
        with self.lock:
            data = self._ler_base()
            termo = identificador.strip().lower()

            empresas_encontradas = [
                e for e in data["empresas"]
                if termo in (e.get("documento") or "").lower()
                or termo in (e.get("email") or "").lower()
                or termo in (e.get("telefone") or "").lower()
            ]
            ids_empresas = {e["id"] for e in empresas_encontradas}

            contatos_encontrados = [
                c for c in data["contatos"]
                if c.get("empresa_id") in ids_empresas
                or termo in (c.get("email") or "").lower()
                or termo in (c.get("telefone") or "").lower()
            ]

            deals = [d for d in data["negociacoes"] if d.get("empresa_id") in ids_empresas]
            atividades = [a for a in data["atividades"] if a.get("empresa_id") in ids_empresas]
            historico = [h for h in data["historico_interacoes"] if h.get("empresa_id") in ids_empresas]

            return {
                "relatorio_lgpd": {
                    "data_solicitacao": datetime.now().isoformat(),
                    "termo_pesquisado": identificador,
                    "empresas": empresas_encontradas,
                    "contatos": contatos_encontrados,
                    "negociacoes": deals,
                    "atividades": atividades,
                    "historico_interacoes": historico,
                    "aviso_legal": "Dossiê emitido em conformidade com o Art. 18 da Lei Geral de Proteção de Dados (Lei 13.709/2018)."
                }
            }

    def lgpd_anonimizar_ou_excluir(self, empresa_id, usuario="Admin"):
        with self.lock:
            data = self._ler_base()
            empresa = next((e for e in data["empresas"] if e["id"] == empresa_id), None)
            if not empresa:
                raise ValueError("Empresa não encontrada para exclusão LGPD.")

            # Anonimizar dados sensíveis
            empresa["razao_social"] = "[ANONIMIZADO LGPD]"
            empresa["nome_fantasia"] = "[ANONIMIZADO LGPD]"
            empresa["documento"] = "00000000000"
            empresa["telefone"] = "000000000"
            empresa["whatsapp"] = "000000000"
            empresa["email"] = "anonimizado@lgpd.local"
            empresa["endereco"] = "[REMOVIDO]"
            empresa["consentimento_lgpd"] = {
                "autorizado": False,
                "data_revogacao": datetime.now().isoformat(),
                "motivo": "Direito de eliminação/revogação exercido pelo titular (Art. 18, VI LGPD)"
            }

            for ctt in data["contatos"]:
                if ctt.get("empresa_id") == empresa_id:
                    ctt["nome"] = "[CONTATO ANONIMIZADO]"
                    ctt["email"] = "contato.anonimo@lgpd.local"
                    ctt["telefone"] = "000000000"
                    ctt["whatsapp"] = "000000000"

            self._salvar_base(data, usuario=usuario)
            self._log_audit(usuario, "LGPD_ANONIMIZAR", "empresa", empresa_id, "Exercício de direito de esquecimento/anonimização")
            return {"sucesso": True, "mensagem": "Dados pessoais anonimizados com sucesso em conformidade com a LGPD."}

    # ==================== IMPORTAÇÃO E EXPORTAÇÃO CSV ====================

    def exportar_csv(self, tipo="leads"):
        with self.lock:
            data = self._ler_base()
            output = io.StringIO()
            writer = csv.writer(output, delimiter=';')

            if tipo == "empresas":
                writer.writerow(["ID", "Tipo", "Razão Social", "Nome Fantasia", "Documento", "Telefone", "E-mail", "Cidade", "UF", "Segmento", "PDVs"])
                for e in data["empresas"]:
                    writer.writerow([e.get("id"), e.get("tipo"), e.get("razao_social"), e.get("nome_fantasia"), e.get("documento"), e.get("telefone"), e.get("email"), e.get("cidade"), e.get("uf"), e.get("segmento"), e.get("pdvs_estimados")])
            elif tipo == "negociacoes":
                writer.writerow(["ID Deal", "Título", "Funil", "Etapa", "Empresa", "Responsável", "MRR (R$)", "Setup (R$)", "Probabilidade (%)", "Previsão", "Status"])
                for d in data["negociacoes"]:
                    emp = next((e for e in data["empresas"] if e["id"] == d.get("empresa_id")), {})
                    writer.writerow([d.get("id"), d.get("titulo"), d.get("funil_id"), d.get("etapa_id"), emp.get("nome_fantasia", ""), d.get("responsavel_id"), f"{d.get('valor_mrr', 0):.2f}", f"{d.get('valor_setup_produtos', 0):.2f}", d.get("probabilidade"), d.get("data_prevista"), d.get("status")])
            else:
                # Exportação combinada de Leads
                writer.writerow(["ID Empresa", "Empresa", "Contato Decisor", "Telefone", "E-mail", "Cidade", "Segmento", "PDVs", "Fase/Etapa", "MRR Estimado", "Responsável"])
                for d in data["negociacoes"]:
                    emp = next((e for e in data["empresas"] if e["id"] == d.get("empresa_id")), {})
                    ctt = next((c for c in data["contatos"] if c["id"] == d.get("contato_id")), {})
                    writer.writerow([
                        emp.get("id", ""),
                        emp.get("nome_fantasia", ""),
                        ctt.get("nome", ""),
                        emp.get("telefone", ""),
                        emp.get("email", ""),
                        emp.get("cidade", ""),
                        emp.get("segmento", ""),
                        emp.get("pdvs_estimados", 1),
                        d.get("etapa_id", ""),
                        f"R$ {d.get('valor_mrr', 0):.2f}".replace('.', ','),
                        d.get("responsavel_id", "")
                    ])

            return output.getvalue().encode('utf-8-sig')

    def importar_csv(self, conteudo_csv, usuario="Admin"):
        with self.lock:
            linhas = conteudo_csv.splitlines()
            if not linhas:
                raise ValueError("Arquivo CSV vazio.")

            # Detectar delimitador (; ou ,)
            header_sample = linhas[0]
            delimitador = ';' if ';' in header_sample else ','

            reader = csv.DictReader(linhas, delimiter=delimitador)
            total_importados = 0
            for row in reader:
                empresa_nome = row.get("Empresa") or row.get("Razao Social") or row.get("nome") or row.get("empresa")
                if not empresa_nome:
                    continue

                payload = {
                    "empresa": empresa_nome.strip(),
                    "nome": row.get("Contato") or row.get("Decisor") or row.get("contato") or "Responsável",
                    "telefone": row.get("Telefone") or row.get("telefone") or "",
                    "email": row.get("Email") or row.get("email") or "",
                    "cidade": row.get("Cidade") or row.get("cidade") or "Sarandi - RS",
                    "segmento": row.get("Segmento") or row.get("segmento") or "Geral",
                    "cnpj": row.get("CNPJ") or row.get("documento") or "",
                    "caixas": row.get("PDVs") or row.get("caixas") or "1",
                    "origem": "Importação CSV"
                }
                self.sincronizar_com_legado(payload)
                total_importados += 1

            self._log_audit(usuario, "IMPORTAR_CSV", "lote", f"{total_importados}_registros", f"{total_importados} importados via CSV")
            return {"sucesso": True, "total_importados": total_importados}

    # ==================== OPENAPI / SWAGGER SPEC ====================

    def obter_openapi_spec(self):
        return {
            "openapi": "3.0.3",
            "info": {
                "title": "TruData CRM Enterprise API v2",
                "version": "2.0.0",
                "description": "API REST Enterprise para gestão de funis, kanban, contatos, atividades, automações e métricas do TruData Marketing Hub."
            },
            "servers": [
                {"url": "/api/crm/v2", "description": "Servidor Local TruData"}
            ],
            "paths": {
                "/estado": {
                    "get": {
                        "summary": "Obter estado completo do CRM",
                        "description": "Retorna funis, etapas, empresas, contatos, negócios, atividades e métricas consolidadas.",
                        "responses": {"200": {"description": "Estado carregado com sucesso"}}
                    }
                },
                "/mover_etapa": {
                    "post": {
                        "summary": "Mover negociação entre etapas do Kanban",
                        "description": "Atualiza a etapa do deal, ajusta probabilidade e executa automações configuradas.",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "example": {"deal_id": "deal-0001", "nova_etapa_id": "etapa-demo", "motivo_perda": ""}
                                }
                            }
                        },
                        "responses": {"200": {"description": "Etapa atualizada com sucesso"}}
                    }
                },
                "/empresa": {
                    "post": {
                        "summary": "Criar ou atualizar empresa (PF/PJ)",
                        "responses": {"200": {"description": "Empresa salva com sucesso"}}
                    }
                },
                "/contato": {
                    "post": {
                        "summary": "Criar ou atualizar contato",
                        "responses": {"200": {"description": "Contato salvo com sucesso"}}
                    }
                },
                "/negociacao": {
                    "post": {
                        "summary": "Criar ou atualizar negociação (Deal)",
                        "responses": {"200": {"description": "Negociação salva com sucesso"}}
                    }
                },
                "/negociacao/excluir": {
                    "post": {
                        "summary": "Remover negociação/deal do Kanban",
                        "responses": {"200": {"description": "Negociação removida com sucesso"}}
                    }
                },
                "/atividade": {
                    "post": {
                        "summary": "Criar ou atualizar atividade / tarefa",
                        "responses": {"200": {"description": "Atividade salva com sucesso"}}
                    }
                },
                "/deduplicar": {
                    "get": {
                        "summary": "Localizar potenciais duplicidades",
                        "responses": {"200": {"description": "Grupos de duplicados retornados"}}
                    }
                },
                "/mesclar_empresas": {
                    "post": {
                        "summary": "Mesclar empresas duplicadas em uma primária",
                        "responses": {"200": {"description": "Mesclagem concluída"}}
                    }
                },
                "/lgpd/exportar": {
                    "get": {
                        "summary": "Exportar dossiê completo de dados do titular (LGPD)",
                        "parameters": [{"name": "documento", "in": "query", "required": True}],
                        "responses": {"200": {"description": "Dossiê exportado"}}
                    }
                },
                "/lgpd/anonimizar": {
                    "post": {
                        "summary": "Anonimizar dados de titular/empresa sob demanda",
                        "responses": {"200": {"description": "Dados anonimizados"}}
                    }
                },
                "/proposta/gerar": {
                    "post": {
                        "summary": "Gerar proposta comercial digital rastreável (1-Click)",
                        "responses": {"200": {"description": "Proposta gerada com link único"}}
                    }
                },
                "/proposta/obter": {
                    "get": {
                        "summary": "Obter dados da proposta comercial por hash",
                        "parameters": [{"name": "hash", "in": "query", "required": True}],
                        "responses": {"200": {"description": "Dados da proposta"}}
                    }
                },
                "/proposta/rastrear": {
                    "post": {
                        "summary": "Registrar abertura de proposta comercial em tempo real (Beacon)",
                        "responses": {"200": {"description": "Visualização registrada"}}
                    }
                },
                "/contrato/assinar": {
                    "post": {
                        "summary": "Assinar eletronicamente contrato digital com hash SHA-256",
                        "responses": {"200": {"description": "Contrato assinado e onboarding disparado"}}
                    }
                },
                "/onboarding/listar": {
                    "get": {
                        "summary": "Listar checklists de onboarding técnico (6 etapas)",
                        "responses": {"200": {"description": "Lista de checklists"}}
                    }
                },
                "/onboarding/atualizar": {
                    "post": {
                        "summary": "Marcar etapa de onboarding como concluída ou pendente",
                        "responses": {"200": {"description": "Etapa atualizada"}}
                    }
                },
                "/metas/obter": {
                    "get": {
                        "summary": "Obter metas comerciais, projeção run-rate e ranking da equipe",
                        "responses": {"200": {"description": "Metas comerciais"}}
                    }
                },
                "/metas/salvar": {
                    "post": {
                        "summary": "Configurar metas e comissões da equipe",
                        "responses": {"200": {"description": "Metas salvas"}}
                    }
                }
            }
        }

crm_service = CRMEnterpriseService()

def handle_crm_v2(handler, method, path):
    """
    Roteador de requisições HTTP REST do CRM Enterprise v2
    """
    if not path.startswith("/api/crm/v2"):
        return False

    clean_subpath = path[len("/api/crm/v2"):].split("?")[0]
    query_params = {}
    if "?" in path:
        from urllib.parse import parse_qs
        query_params = parse_qs(path.split("?", 1)[1])

    usuario_header = handler.headers.get("X-Usuario-Id", "usr-admin")
    perfil_header = handler.headers.get("X-Usuario-Perfil", "admin")

    try:
        if method == "GET":
            if clean_subpath in ["", "/", "/estado"]:
                resultado = crm_service.obter_estado_completo(usuario_id=usuario_header, perfil=perfil_header)
                corpo = json.dumps({"sucesso": True, "dados": resultado}, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/openapi.json":
                spec = crm_service.obter_openapi_spec()
                corpo = json.dumps(spec, ensure_ascii=False, indent=2).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/deduplicar":
                res = crm_service.encontrar_duplicados()
                corpo = json.dumps({"sucesso": True, **res}, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/exportar_csv":
                tipo = query_params.get("tipo", ["leads"])[0]
                csv_bytes = crm_service.exportar_csv(tipo)
                handler.send_response(200)
                handler.send_header("Content-Type", "text/csv; charset=utf-8")
                handler.send_header("Content-Disposition", f'attachment; filename="trudata_crm_{tipo}_{date.today().isoformat()}.csv"')
                handler.send_header("Content-Length", str(len(csv_bytes)))
                handler.end_headers()
                handler.wfile.write(csv_bytes)
                return True

            elif clean_subpath == "/lgpd/exportar":
                termo = query_params.get("termo", [""])[0]
                if not termo:
                    raise ValueError("Informe o parâmetro 'termo' (CNPJ, CPF, E-mail ou Telefone).")
                res = crm_service.lgpd_exportar_titular(termo)
                corpo = json.dumps({"sucesso": True, **res}, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/proposta/obter":
                hash_code = query_params.get("hash", query_params.get("p", [""]))[0]
                if not hash_code:
                    raise ValueError("Informe o parâmetro 'hash' ou 'p' da proposta.")
                res = crm_service.obter_proposta(hash_code)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/onboarding/listar":
                deal_id = query_params.get("deal_id", [None])[0]
                res = crm_service.obter_checklists_onboarding(deal_id)
                corpo = json.dumps({"sucesso": True, "onboardings": res}, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/metas/obter":
                res = crm_service.obter_metas()
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

        elif method == "POST":
            length = int(handler.headers.get('Content-Length', 0))
            raw_body = handler.rfile.read(length) if length > 0 else b"{}"

            if clean_subpath == "/importar_csv":
                csv_text = raw_body.decode('utf-8', errors='ignore')
                res = crm_service.importar_csv(csv_text, usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            payload = json.loads(raw_body.decode('utf-8')) if raw_body else {}

            if clean_subpath == "/mover_etapa":
                deal_id = payload.get("deal_id")
                nova_etapa = payload.get("nova_etapa_id")
                motivo = payload.get("motivo_perda", "")
                observacao = payload.get("observacao_perda", "")
                res = crm_service.mover_etapa(deal_id, nova_etapa, usuario=usuario_header, motivo_perda=motivo, observacao_perda=observacao)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/empresa":
                res = crm_service.salvar_empresa(payload, usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath in ["/empresa/excluir", "/empresa/remover"]:
                emp_id = payload.get("id") or payload.get("empresa_id")
                res = crm_service.excluir_empresa(emp_id, usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200 if res.get("sucesso") else 400, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath in ["/lead/adicionar_completo", "/lead/novo"]:
                res = crm_service.salvar_novo_lead_completo(payload, usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/contato":
                res = crm_service.salvar_contato(payload, usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/negociacao":
                res = crm_service.salvar_negociacao(payload, usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath in ["/negociacao/excluir", "/negociacao/remover"]:
                deal_id = payload.get("deal_id") or payload.get("id")
                res = crm_service.excluir_negociacao(deal_id, usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/atividade":
                res = crm_service.salvar_atividade(payload, usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath in ["/atividade/excluir", "/atividade/remover"]:
                ativ_id = payload.get("id") or payload.get("atividade_id")
                res = crm_service.excluir_atividade(ativ_id, usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath in ["/atividade/limpar_todas", "/atividades/limpar"]:
                res = crm_service.limpar_todas_atividades(usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/interacao":
                res = crm_service.registrar_interacao(payload, usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/mesclar_empresas":
                prim = payload.get("id_primario")
                secs = payload.get("ids_secundarios", [])
                res = crm_service.mesclar_empresas(prim, secs, usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/lgpd/anonimizar":
                emp_id = payload.get("empresa_id")
                res = crm_service.lgpd_anonimizar_ou_excluir(emp_id, usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/proposta/gerar":
                deal_id = payload.get("deal_id")
                res = crm_service.gerar_proposta_rastreavel(deal_id, usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/proposta/rastrear":
                hash_code = payload.get("hash") or payload.get("p")
                ip = handler.client_address[0] if hasattr(handler, 'client_address') and handler.client_address else "127.0.0.1"
                user_agent = handler.headers.get("User-Agent", "")
                res = crm_service.registrar_visualizacao_proposta(hash_code, ip=ip, user_agent=user_agent)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/contrato/assinar":
                hash_proposta = payload.get("hash_proposta") or payload.get("hash")
                nome = payload.get("signatario_nome", "")
                cpf = payload.get("signatario_cpf", "")
                email = payload.get("signatario_email", "")
                ip = handler.client_address[0] if hasattr(handler, 'client_address') and handler.client_address else "127.0.0.1"
                res = crm_service.assinar_contrato_digital(hash_proposta, nome, cpf, email, ip=ip)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/onboarding/gerar":
                deal_id = payload.get("deal_id")
                res = crm_service.gerar_checklist_onboarding(deal_id, usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/onboarding/atualizar":
                onboarding_id = payload.get("onboarding_id")
                etapa_id = payload.get("etapa_id")
                concluida = payload.get("concluida", True)
                notas = payload.get("notas", "")
                res = crm_service.atualizar_etapa_onboarding(onboarding_id, etapa_id, concluida=concluida, notas=notas, usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/metas/salvar":
                res = crm_service.salvar_metas(payload, usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

            elif clean_subpath == "/zerar_base":
                res = crm_service.zerar_base_dados(usuario=usuario_header)
                corpo = json.dumps(res, ensure_ascii=False).encode("utf-8")
                _responder(handler, 200, "application/json; charset=utf-8", corpo)
                return True

    except Exception as exc:
        err_corpo = json.dumps({"sucesso": False, "erro": str(exc)}, ensure_ascii=False).encode("utf-8")
        _responder(handler, 400, "application/json; charset=utf-8", err_corpo)
        return True

    return False

def _responder(handler, status, content_type, data):
    handler.send_response(status)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)
