#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes Unitários Automatizados - TruData CRM Enterprise
Validação de Entidades (PF/PJ), Múltiplos Funis, Kanban, Atividades,
Automações, Deduplicação, Métricas, Logs e Conformidade LGPD.
"""

import unittest
import os
import io
import json
import shutil
import tempfile
import sys
from pathlib import Path

# Inserir caminho do painel
PROJECT_ROOT = Path(__file__).resolve().parent
PAINEL_DIR = PROJECT_ROOT / "painel_aprovacao"
sys.path.insert(0, str(PAINEL_DIR))

import crm_enterprise_api
from crm_enterprise_api import CRMEnterpriseService

class TestCRMEnterprise(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.test_data_file = os.path.join(cls.temp_dir, "test_crm_enterprise_data.json")
        cls.test_audit_file = os.path.join(cls.temp_dir, "test_crm_audit_log.json")
        cls.service = CRMEnterpriseService(data_file=cls.test_data_file, audit_file=cls.test_audit_file)
        cls.orig_service = crm_enterprise_api.crm_service
        crm_enterprise_api.crm_service = cls.service

    @classmethod
    def tearDownClass(cls):
        crm_enterprise_api.crm_service = cls.orig_service
        shutil.rmtree(cls.temp_dir, ignore_errors=True)

    def test_01_estado_inicial_e_metricas(self):
        estado = self.service.obter_estado_completo()
        self.assertIn("empresas", estado)
        self.assertIn("contatos", estado)
        self.assertIn("negociacoes", estado)
        self.assertIn("funis", estado)
        self.assertIn("metricas", estado)

        metricas = estado["metricas"]
        self.assertGreaterEqual(metricas["total_deals"], 0)
        self.assertIn("forecast_mrr_ponderado", metricas)
        self.assertIn("taxa_conversao", metricas)
        self.assertIn("ticket_medio", metricas)

    def test_02_salvar_empresa_pf_pj(self):
        # Teste Empresa PJ
        pj_payload = {
            "tipo": "PJ",
            "razao_social": "Supermercado Sul Ltda",
            "nome_fantasia": "Supermercado Sul",
            "documento": "12.345.678/0001-90",
            "telefone": "5433619999",
            "email": "contato@supersul.com.br",
            "cidade": "Sarandi - RS",
            "segmento": "Supermercados & Mercearias",
            "pdvs_estimados": 4
        }
        res_pj = self.service.salvar_empresa(pj_payload, usuario="Tester")
        self.assertTrue(res_pj["sucesso"])
        emp_id = res_pj["empresa"]["id"]

        # Teste Empresa / Produtor PF
        pf_payload = {
            "tipo": "PF",
            "razao_social": "João Agricultor e Comércio",
            "nome_fantasia": "João da Horta",
            "documento": "123.456.789-00",
            "telefone": "54999112233",
            "cidade": "Rondinha - RS",
            "segmento": "Comércio Geral"
        }
        res_pf = self.service.salvar_empresa(pf_payload, usuario="Tester")
        self.assertTrue(res_pf["sucesso"])

    def test_03_salvar_contato_e_deal(self):
        # Salvar Empresa
        res_emp = self.service.salvar_empresa({
            "tipo": "PJ",
            "razao_social": "Farmácia Vida & Saúde",
            "nome_fantasia": "Farmácia Vida",
            "documento": "98.765.432/0001-10",
            "telefone": "5433611122",
            "cidade": "Passo Fundo - RS",
            "segmento": "Farmácias & Drogarias",
            "pdvs_estimados": 2
        })
        emp_id = res_emp["empresa"]["id"]

        # Salvar Contato Decisor
        res_ctt = self.service.salvar_contato({
            "empresa_id": emp_id,
            "nome": "Dr. Fernando",
            "cargo": "Farmacêutico e Proprietário",
            "telefone": "5499887766",
            "email": "fernando@farmaciavida.com.br",
            "decisor": True
        })
        self.assertTrue(res_ctt["sucesso"])
        ctt_id = res_ctt["contato"]["id"]

        # Salvar Negociação (Deal) com Produtos
        res_deal = self.service.salvar_negociacao({
            "titulo": "Implantação ERP Farmácia Vida (2 PDVs)",
            "empresa_id": emp_id,
            "contato_id": ctt_id,
            "funil_id": "funil-vendas-novas",
            "etapa_id": "etapa-lead",
            "responsavel_id": "usr-vend1",
            "valor_mrr": 240.00,
            "valor_setup_produtos": 1000.00,
            "probabilidade": 20,
            "produtos": [
                {"produto_id": "prod-erp-base", "quantidade": 1, "valor_unitario": 180.00},
                {"produto_id": "prod-pdv-extra", "quantidade": 1, "valor_unitario": 60.00}
            ]
        })
        self.assertTrue(res_deal["sucesso"])
        deal_id = res_deal["deal"]["id"]

        # Teste 04: Mover etapa no Kanban e disparar automação
        res_mover = self.service.mover_etapa(deal_id, "etapa-proposta", usuario="Tester")
        self.assertTrue(res_mover["sucesso"])
        self.assertEqual(res_mover["deal"]["etapa_id"], "etapa-proposta")

        # Verificar se automação de follow-up foi acionada
        estado = self.service.obter_estado_completo()
        ativ_auto = next((a for a in estado["atividades"] if a.get("deal_id") == deal_id and a.get("tipo") == "follow_up"), None)
        self.assertIsNotNone(ativ_auto, "Automação deveria ter criado atividade de follow-up ao mover para 'etapa-proposta'")

    def test_04_motivo_perda_deal(self):
        res_deal = self.service.salvar_negociacao({
            "titulo": "Deal Concorrência Teste",
            "funil_id": "funil-vendas-novas",
            "etapa_id": "etapa-demo",
            "valor_mrr": 180.00
        })
        deal_id = res_deal["deal"]["id"]

        res_perda = self.service.mover_etapa(deal_id, "etapa-perdido", usuario="Tester", motivo_perda="Optou por concorrente com preço menor")
        self.assertTrue(res_perda["sucesso"])
        self.assertEqual(res_perda["deal"]["status"], "perdido")
        self.assertEqual(res_perda["deal"]["motivo_perda"], "Optou por concorrente com preço menor")

    def test_05_deduplicacao_e_mesclagem(self):
        # Cadastrar 2 empresas com mesmo CNPJ
        cnpj_duplicado = "44.555.666/0001-77"
        e1 = self.service.salvar_empresa({"tipo": "PJ", "razao_social": "Padaria Alpha", "nome_fantasia": "Padaria Alpha 1", "documento": cnpj_duplicado, "telefone": "5433618888"})
        e2 = self.service.salvar_empresa({"tipo": "PJ", "razao_social": "Padaria Alpha Filial", "nome_fantasia": "Padaria Alpha 2", "documento": cnpj_duplicado, "telefone": "5433618888"})

        dup_res = self.service.encontrar_duplicados()
        self.assertGreaterEqual(dup_res["total_grupos"], 1)

        # Mesclar
        id_primario = e1["empresa"]["id"]
        ids_sec = [e2["empresa"]["id"]]
        merge_res = self.service.mesclar_empresas(id_primario, ids_sec, usuario="Tester")
        self.assertTrue(merge_res["sucesso"])

    def test_06_atividades_e_conclusao(self):
        res_ativ = self.service.salvar_atividade({
            "tipo": "ligacao",
            "titulo": "Ligar para agendar demonstração técnica",
            "responsavel_id": "usr-vend1",
            "status": "pendente",
            "notas": "Falar sobre contingência offline."
        })
        self.assertTrue(res_ativ["sucesso"])
        ativ_id = res_ativ["atividade"]["id"]

        # Concluir
        res_ativ["atividade"]["status"] = "concluida"
        res_conc = self.service.salvar_atividade(res_ativ["atividade"], usuario="Tester")
        self.assertTrue(res_conc["sucesso"])
        self.assertEqual(res_conc["atividade"]["status"], "concluida")

    def test_07_conformidade_lgpd(self):
        doc_titular = "55.666.777/0001-88"
        res_emp = self.service.salvar_empresa({
            "tipo": "PJ",
            "razao_social": "Loja Moda Exclusiva",
            "nome_fantasia": "Moda Exclusiva",
            "documento": doc_titular,
            "email": "titular@modaexclusiva.com.br",
            "telefone": "54991234567"
        })
        emp_id = res_emp["empresa"]["id"]

        # Exportar Dossiê do Titular
        dossie = self.service.lgpd_exportar_titular(doc_titular)
        self.assertIn("relatorio_lgpd", dossie)
        self.assertGreaterEqual(len(dossie["relatorio_lgpd"]["empresas"]), 1)

        # Anonimizar sob demanda LGPD
        res_anon = self.service.lgpd_anonimizar_ou_excluir(emp_id, usuario="DPO")
        self.assertTrue(res_anon["sucesso"])

        estado = self.service.obter_estado_completo()
        emp_anon = next((e for e in estado["empresas"] if e["id"] == emp_id), None)
        self.assertEqual(emp_anon["nome_fantasia"], "[ANONIMIZADO LGPD]")
        self.assertFalse(emp_anon["consentimento_lgpd"]["autorizado"])

    def test_08_openapi_swagger_spec(self):
        spec = self.service.obter_openapi_spec()
        self.assertEqual(spec["openapi"], "3.0.3")
        self.assertIn("/estado", spec["paths"])
        self.assertIn("/mover_etapa", spec["paths"])
        self.assertIn("/deduplicar", spec["paths"])
        self.assertIn("/lgpd/exportar", spec["paths"])

    def test_09_exportacao_csv(self):
        csv_bytes = self.service.exportar_csv("leads")
        self.assertIsInstance(csv_bytes, bytes)
        self.assertIn(b"Empresa", csv_bytes)

    def test_10_gerar_e_rastrear_proposta_comercial(self):
        # 1. Cadastrar Deal para proposta
        res_deal = self.service.salvar_negociacao({
            "titulo": "Deal Proposta Rastreável Teste",
            "valor_mrr": 350.00,
            "valor_setup_produtos": 1200.00,
            "funil_id": "funil-vendas-novas",
            "etapa_id": "etapa-proposta"
        })
        deal_id = res_deal["deal"]["id"]

        # 2. Gerar proposta comercial rastreável (1-Click)
        res_prop = self.service.gerar_proposta_rastreavel(deal_id, usuario="ConsultorTest")
        self.assertTrue(res_prop["sucesso"])
        prop = res_prop["proposta"]
        hash_code = prop["hash"]
        self.assertTrue(hash_code.startswith("trudata-"))
        self.assertEqual(prop["status"], "aguardando_visualizacao")
        self.assertEqual(prop["total_visualizacoes"], 0)

        # 3. Obter proposta
        res_get = self.service.obter_proposta(hash_code)
        self.assertTrue(res_get["sucesso"])
        self.assertEqual(res_get["proposta"]["hash"], hash_code)

        # 4. Registrar Beacon de Visualização em Tempo Real (Abertura do cliente)
        res_track = self.service.registrar_visualizacao_proposta(hash_code, ip="189.100.20.10", user_agent="Mozilla/5.0 Safari")
        self.assertTrue(res_track["sucesso"])
        self.assertEqual(res_track["total_visualizacoes"], 1)
        self.assertEqual(res_track["status"], "visualizada")

        # Verificar se alerta foi registrado na timeline do Deal
        estado = self.service.obter_estado_completo()
        deal_atual = next((d for d in estado["negociacoes"] if d["id"] == deal_id), None)
        self.assertIsNotNone(deal_atual)
        self.assertIsNotNone(deal_atual.get("ultima_visualizacao_proposta"))

        alerta_hist = next((h for h in estado["historico_interacoes"] if h.get("deal_id") == deal_id and h.get("tipo") == "proposta_aberta"), None)
        self.assertIsNotNone(alerta_hist, "Alerta em tempo real de abertura da proposta deve estar no histórico")
        self.assertIn("189.100.20.10", alerta_hist["descricao"])

    def test_11_assinatura_digital_e_onboarding_tecnico(self):
        # 1. Criar negociação e proposta
        res_deal = self.service.salvar_negociacao({
            "titulo": "Deal Fechamento & Assinatura Digital",
            "valor_mrr": 480.00,
            "valor_setup_produtos": 1500.00,
            "funil_id": "funil-vendas-novas",
            "etapa_id": "etapa-negociacao"
        })
        deal_id = res_deal["deal"]["id"]
        res_prop = self.service.gerar_proposta_rastreavel(deal_id, usuario="VendedorTest")
        hash_prop = res_prop["proposta"]["hash"]

        # 2. Assinatura Digital com Validade Jurídica (SHA-256)
        res_sign = self.service.assinar_contrato_digital(
            hash_proposta=hash_prop,
            signatario_nome="Dr. Roberto Silva",
            signatario_cpf="111.222.333-44",
            signatario_email="roberto@farmacia.com.br",
            ip="201.80.15.2"
        )
        self.assertTrue(res_sign["sucesso"])
        contrato = res_sign["contrato"]
        self.assertEqual(len(contrato["hash_sha256"]), 64, "Hash SHA-256 deve ter 64 caracteres hex")
        self.assertEqual(contrato["signatario_cpf"], "111.222.333-44")

        # 3. Validar se o Deal virou Ganho e probabilidade 100%
        estado = self.service.obter_estado_completo()
        deal_fechado = next((d for d in estado["negociacoes"] if d["id"] == deal_id), None)
        self.assertEqual(deal_fechado["status"], "ganho")
        self.assertEqual(deal_fechado["probabilidade"], 100)

        # 4. Validar se o Checklist de Onboarding Técnico (6 etapas) foi disparado
        onboardings = self.service.obter_checklists_onboarding(deal_id=deal_id)
        self.assertGreaterEqual(len(onboardings), 1)
        onb = onboardings[0]
        self.assertEqual(len(onb["etapas"]), 6, "Onboarding deve conter exatamente 6 etapas técnicas")
        self.assertEqual(onb["progresso_pct"], 0)

        # 5. Atualizar etapa 1 e etapa 2 como concluídas
        res_et1 = self.service.atualizar_etapa_onboarding(onb["id"], "etapa-1", concluida=True, notas="PDVs validados com SAT", usuario="SuporteN1")
        self.assertTrue(res_et1["sucesso"])
        self.assertEqual(res_et1["onboarding"]["progresso_pct"], 17) # 1 de 6 = ~17%

        res_et2 = self.service.atualizar_etapa_onboarding(onb["id"], "etapa-2", concluida=True, notas="Agente TruData rodando", usuario="Implantação")
        self.assertEqual(res_et2["onboarding"]["progresso_pct"], 33) # 2 de 6 = 33%

    def test_12_metas_termometro_e_gamificacao(self):
        # 1. Configurar metas
        res_metas = self.service.salvar_metas({
            "meta_mrr_empresa": 20000.00,
            "meta_pdvs_empresa": 60,
            "mes_referencia": "Outubro/2026"
        }, usuario="DiretorComercial")
        self.assertTrue(res_metas["sucesso"])
        self.assertEqual(res_metas["metas"]["meta_mrr_empresa"], 20000.00)

        # 2. Obter métricas com termômetro e gamificação
        res_obter = self.service.obter_metas()
        self.assertTrue(res_obter["sucesso"])
        resumo = res_obter["resumo_painel"]
        self.assertIn("pct_meta_mrr", resumo)
        self.assertIn("pct_meta_pdvs", resumo)
        self.assertIn("projecao_run_rate_mrr", resumo)
        self.assertIn("ranking_vendedores", resumo)

        ranking = resumo["ranking_vendedores"]
        if ranking:
            self.assertIn("posicao", ranking[0])
            self.assertIn("comissao_estimada", ranking[0])

    def test_13_rotas_http_rest_v2(self):
        class MockHandler:
            def __init__(self, body_bytes=b""):
                self.rfile = io.BytesIO(body_bytes)
                self.wfile = io.BytesIO()
                self.headers = {"Content-Length": str(len(body_bytes)), "User-Agent": "UnitTests"}
                self.client_address = ("127.0.0.1", 12345)
                self.status_code = 200
                self.response_headers = {}

            def send_response(self, code):
                self.status_code = code

            def send_header(self, k, v):
                self.response_headers[k] = v

            def end_headers(self):
                pass

        # 1. Testar GET /api/crm/v2/metas/obter
        h1 = MockHandler()
        handled1 = crm_enterprise_api.handle_crm_v2(h1, "GET", "/api/crm/v2/metas/obter")
        self.assertTrue(handled1)
        self.assertEqual(h1.status_code, 200)
        res1 = json.loads(h1.wfile.getvalue().decode('utf-8'))
        self.assertTrue(res1["sucesso"])

        # 2. Testar POST /api/crm/v2/metas/salvar
        body2 = json.dumps({"meta_mrr_empresa": 25000, "mes_referencia": "Novembro/2026"}).encode('utf-8')
        h2 = MockHandler(body2)
        handled2 = crm_enterprise_api.handle_crm_v2(h2, "POST", "/api/crm/v2/metas/salvar")
        self.assertTrue(handled2)
        self.assertEqual(h2.status_code, 200)

        # 3. Testar GET /api/crm/v2/onboarding/listar
        h3 = MockHandler()
        handled3 = crm_enterprise_api.handle_crm_v2(h3, "GET", "/api/crm/v2/onboarding/listar")
        self.assertTrue(handled3)
        self.assertEqual(h3.status_code, 200)

    def test_14_salvar_novo_lead_completo(self):
        lead_payload = {
            "empresa": {
                "tipo": "PJ",
                "razao_social": "Auto Posto Rota Norte Ltda",
                "nome_fantasia": "Posto Rota Norte",
                "documento": "11.222.333/0001-44",
                "telefone": "5433615555",
                "cidade": "Sarandi - RS",
                "segmento": "Postos de Combustíveis & Conveniência",
                "pdvs_estimados": 3
            },
            "contato": {
                "nome": "Marcos Silveira",
                "cargo": "Gerente Geral",
                "telefone": "54999887766",
                "email": "marcos@rotanorte.com.br"
            },
            "negociacao": {
                "titulo": "Implantação TruData ERP + TEF (3 Caixas)",
                "valor_mrr": 300.0,
                "valor_setup_produtos": 500.0
            },
            "notas": "Cliente prospectado diretamente na rodovia RS-404."
        }
        res = self.service.salvar_novo_lead_completo(lead_payload, usuario="Tester")
        self.assertTrue(res["sucesso"])
        self.assertEqual(res["empresa"]["nome_fantasia"], "Posto Rota Norte")
        self.assertEqual(res["contato"]["nome"], "Marcos Silveira")
        self.assertEqual(res["negociacao"]["valor_mrr"], 300.0)

        # Validar no estado completo
        st = self.service.obter_estado_completo()
        deal_cadastrado = next((d for d in st["negociacoes"] if d["id"] == res["negociacao"]["id"]), None)
        self.assertIsNotNone(deal_cadastrado)

    def test_15_excluir_negociacao_kanban(self):
        # Criar negociação para teste de exclusão
        deal_res = self.service.salvar_negociacao({
            "titulo": "Deal Para Ser Excluído do Kanban",
            "valor_mrr": 250.0,
            "funil_id": "funil-vendas-novas",
            "etapa_id": "etapa-lead"
        }, usuario="Tester")
        self.assertTrue(deal_res["sucesso"])
        deal_id = deal_res["deal"]["id"]

        # Confirmar que está na base
        st = self.service.obter_estado_completo()
        deal_presente = next((d for d in st["negociacoes"] if d["id"] == deal_id), None)
        self.assertIsNotNone(deal_presente)

        # Excluir negociação
        del_res = self.service.excluir_negociacao(deal_id, usuario="Tester")
        self.assertTrue(del_res["sucesso"])

        # Verificar se foi removida do Kanban/negociações
        st_apos = self.service.obter_estado_completo()
        deal_removido = next((d for d in st_apos["negociacoes"] if d["id"] == deal_id), None)
        self.assertIsNone(deal_removido)

    def test_16_etapa_recontato_kanban(self):
        # 1. Verificar se a etapa existe no funil principal
        st = self.service.obter_estado_completo()
        funil = next(f for f in st["funis"] if f["id"] == "funil-vendas-novas")
        etapa_ids = [e["id"] for e in funil["etapas"]]
        self.assertIn("etapa-recontato", etapa_ids)

        # 2. Criar deal e mover para etapa-recontato
        deal_res = self.service.salvar_negociacao({
            "titulo": "Cliente Para Recontato 6 Meses",
            "valor_mrr": 200.0,
            "funil_id": "funil-vendas-novas",
            "etapa_id": "etapa-demo"
        }, usuario="Tester")
        deal_id = deal_res["deal"]["id"]

        # Mover para recontato com prazo de 6 meses
        mov_res = self.service.mover_etapa(deal_id, "etapa-recontato", usuario="Tester", motivo_perda="6 meses - Contrato com concorrente vence no fim do semestre")
        self.assertTrue(mov_res["sucesso"])
        self.assertEqual(mov_res["deal"]["status"], "recontato")
        self.assertEqual(mov_res["deal"]["probabilidade"], 15)
        self.assertTrue(mov_res["deal"]["data_prevista"])

        # Verificar se tarefa automática foi criada na agenda
        st_final = self.service.obter_estado_completo()
        ativ_recontato = next((a for a in st_final["atividades"] if a.get("deal_id") == deal_id), None)
        self.assertIsNotNone(ativ_recontato)
        self.assertIn("Recontatar", ativ_recontato["titulo"])
        self.assertEqual(ativ_recontato["status"], "pendente")

    def test_17_kanban_redesign_perda_modal_e_metricas_funil(self):
        # 1. Criar deal para perda estruturada com observações
        deal_res = self.service.salvar_negociacao({
            "titulo": "Deal Perdido para Concorrente",
            "valor_mrr": 350.0,
            "funil_id": "funil-vendas-novas",
            "etapa_id": "etapa-proposta"
        }, usuario="Tester")
        self.assertTrue(deal_res["sucesso"])
        deal_id = deal_res["deal"]["id"]

        # Mover para etapa-perdido com motivo estruturado e observações detalhadas
        mov_res = self.service.mover_etapa(
            deal_id, 
            "etapa-perdido", 
            usuario="Tester", 
            motivo_perda="Concorrente (Preço mais agressivo)",
            observacao_perda="Cliente optou por solução concorrente local com desconto de 40%."
        )
        self.assertTrue(mov_res["sucesso"])
        deal_perdido = mov_res["deal"]
        self.assertEqual(deal_perdido["status"], "perdido")
        self.assertEqual(deal_perdido["motivo_perda"], "Concorrente (Preço mais agressivo)")
        self.assertEqual(deal_perdido["observacao_perda"], "Cliente optou por solução concorrente local com desconto de 40%.")
        self.assertIn("etapa_atualizada_em", deal_perdido)
        self.assertTrue(deal_perdido["etapa_atualizada_em"])

        # 2. Validar cálculo e presença do Funil Resumido em métricas
        st = self.service.obter_estado_completo()
        metricas = st["metricas"]
        self.assertIn("funil_resumo", metricas)
        funil_resumo = metricas["funil_resumo"]
        
        self.assertIn("conversao_passos", funil_resumo)
        self.assertIn("motivos_perda_ranking", funil_resumo)
        self.assertIn("principal_motivo_perda", funil_resumo)
        self.assertIn("tempo_medio_dias_etapas", funil_resumo)

        # Conversão entre passos deve ser uma lista com taxas percentuais calculadas
        passos = funil_resumo["conversao_passos"]
        self.assertIsInstance(passos, list)
        self.assertGreater(len(passos), 0)
        primeiro_passo = passos[0]
        self.assertIn("de", primeiro_passo)
        self.assertIn("para", primeiro_passo)
        self.assertIn("taxa", primeiro_passo)

        # Motivos de perda devem conter o motivo registrado
        ranking = funil_resumo["motivos_perda_ranking"]
        self.assertIsInstance(ranking, list)
        motivos_encontrados = [r["motivo"] for r in ranking]
        self.assertIn("Concorrente (Preço mais agressivo)", motivos_encontrados)

        # Principal motivo de perda deve ter nome e percentual
        princ = funil_resumo["principal_motivo_perda"]
        self.assertIn("motivo", princ)
        self.assertIn("percentual", princ)

if __name__ == "__main__":
    unittest.main()

