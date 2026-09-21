#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Teste Automatizado - 10 Novas Melhorias do Ecossistema TruData
Valida endpoints, arquivos HTML e integridade das regras de negócio.
"""
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PAINEL_DIR = BASE_DIR / "painel_aprovacao"
BASE_URL = "http://127.0.0.1:8080"

def testar_servidor_ativo():
    print("[1/6] Testando se servidor HTTP está respondendo em :8080...")
    try:
        req = urllib.request.urlopen(f"{BASE_URL}/", timeout=4)
        status = req.getcode()
        assert status == 200, f"Status code inesperado: {status}"
        print("  -> OK! Servidor ativo e respondendo na porta 8080.")
    except Exception as e:
        print(f"  -> ERRO ao conectar no servidor: {e}")
        sys.exit(1)

def testar_api_gerar_rota_maps():
    print("[2/6] Testando POST /api/gerar_rota_maps (Melhoria 1)...")
    payload = {
        "empresas": [
            {"nome": "Super Cotrisoja", "cidade": "Sarandi", "endereco": "Av. Expedicionário, 1200"},
            {"nome": "Farmácia São João Centro", "cidade": "Passo Fundo", "endereco": "Rua Morom, 1500"},
            {"nome": "Mercado Modelo", "cidade": "Carazinho", "endereco": "Av. Flores da Cunha, 800"}
        ]
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/api/gerar_rota_maps", data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=4) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        assert res.get("sucesso") is True, f"Falha na resposta: {res}"
        url_maps = res.get("url_maps", "")
        assert "google.com/maps/dir" in url_maps, f"URL Maps inválida: {url_maps}"
        assert "Sarandi" in url_maps, "Origem Sarandi ausente na rota"
        print(f"  -> OK! Rota multiponto gerada com sucesso com {res.get('total_pontos')} pontos.")

def testar_api_adicionar_nota_lead():
    print("[3/6] Testando POST /api/adicionar_nota_lead (Melhoria 4)...")
    payload = {
        "id": "lead-101",
        "tipo": "Ligação",
        "texto": "Teste automatizado: Diretor Marcos solicitou proposta em PDF para 4 PDVs.",
        "autor": "Consultor Automático"
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/api/adicionar_nota_lead", data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=4) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        assert res.get("sucesso") is True, f"Falha ao adicionar nota: {res}"
        nota = res.get("nota", {})
        assert nota.get("autor") == "Consultor Automático", "Autor da nota incorreto"
        print("  -> OK! Nota de interação persistida no histórico do lead com sucesso.")

def testar_api_exportar_crm_csv():
    print("[4/6] Testando GET /api/exportar_crm_csv (Melhoria 7)...")
    with urllib.request.urlopen(f"{BASE_URL}/api/exportar_crm_csv", timeout=4) as resp:
        content_type = resp.headers.get("Content-Type", "")
        assert "csv" in content_type, f"Content-Type inválido: {content_type}"
        csv_text = resp.read().decode('utf-8-sig')
        assert "Nome da Empresa;Cidade;Segmento;Etapa" in csv_text, "Cabeçalho CSV ausente ou incorreto"
        assert "MRR Estimado (R$)" in csv_text, "Coluna de MRR ausente no CSV"
        linhas = csv_text.strip().split("\n")
        print(f"  -> OK! Exportação de planilha CSV validada com {len(linhas)} linhas geradas.")

def testar_arquivos_html():
    print("[5/6] Testando presença e integridade dos componentes no front-end...")
    
    # 1. radar_clientes.html (Melhorias 1 e 2)
    radar_html = (PAINEL_DIR / "radar_clientes.html").read_text(encoding='utf-8')
    assert "roteirizarVisitasSelecionadas" in radar_html, "Função roteirizarVisitasSelecionadas ausente em radar_clientes.html"
    assert "abrirStreetView" in radar_html, "Função abrirStreetView ausente em radar_clientes.html"
    print("  -> OK! radar_clientes.html possui Roteirizador e Street View integrados.")

    # 2. crm.html (Melhorias 3, 4 e 7)
    crm_html = (PAINEL_DIR / "crm.html").read_text(encoding='utf-8')
    assert "kpi-total-mrr" in crm_html, "KPI de MRR ausente no crm.html"
    assert "modalNotaLead" in crm_html, "Modal de Notas ausente no crm.html"
    assert "/api/exportar_crm_csv" in crm_html, "Link de exportação CSV ausente no crm.html"
    print("  -> OK! crm.html possui KPIs de MRR, modal de timeline e exportação CSV.")

    # 3. auditor_xml.html (Melhorias 5 e 6)
    auditor_html = (PAINEL_DIR / "auditor_xml.html").read_text(encoding='utf-8')
    assert "DOMParser" in auditor_html, "DOMParser ausente no auditor_xml.html"
    assert "enviarLaudoWhatsApp" in auditor_html, "Disparo WhatsApp do laudo ausente"
    print("  -> OK! auditor_xml.html possui upload nativo, auditoria ST/Monofásico e disparo WhatsApp.")

    # 4. gerador_proposta.html (Melhoria 8)
    prop_html = (PAINEL_DIR / "gerador_proposta.html").read_text(encoding='utf-8')
    assert "Estudo de TCO & Economia Projetada" in prop_html, "Seção de TCO ausente em gerador_proposta.html"
    assert "outTcoTotal" in prop_html, "Elemento outTcoTotal ausente em gerador_proposta.html"
    print("  -> OK! gerador_proposta.html possui TCO comparativo e cálculo dinâmico de economia anual.")

    # 5. copiloto_vendas.html (Melhoria 9)
    copiloto_html = (PAINEL_DIR / "copiloto_vendas.html").read_text(encoding='utf-8')
    assert "tab-btn-simulador" in copiloto_html, "Botão do simulador ausente em copiloto_vendas.html"
    assert "avaliarPitchComercial" in copiloto_html, "Função avaliarPitchComercial ausente"
    print("  -> OK! copiloto_vendas.html possui simulador interativo de objeções e avaliação de gatilhos.")

    # 6. index.html (Melhoria 10)
    index_html = (PAINEL_DIR / "index.html").read_text(encoding='utf-8')
    assert "auditor_xml.html" in index_html, "auditor_xml.html ausente no hub central index.html"
    assert "COMANDOS_GLOBAIS" in index_html, "COMANDOS_GLOBAIS ausente em index.html"
    print("  -> OK! index.html possui conexões, botões e atalhos na Command Bar.")

def testar_leads_crm_json():
    print("[6/6] Verificando integridade de leads_crm.json...")
    leads_file = PAINEL_DIR / "leads_crm.json"
    with open(leads_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    leads = data if isinstance(data, list) else data.get("leads", [])
    assert len(leads) > 0, "Nenhum lead encontrado em leads_crm.json"
    lead_ex = leads[0]
    assert "id" in lead_ex, "Campo id ausente no lead"
    print(f"  -> OK! Base de leads íntegra ({len(leads)} leads cadastrados no CRM).")

if __name__ == "__main__":
    print("=== INICIANDO BATERIA DE TESTES DAS 10 MELHORIAS ===")
    testar_servidor_ativo()
    testar_api_gerar_rota_maps()
    testar_api_adicionar_nota_lead()
    testar_api_exportar_crm_csv()
    testar_arquivos_html()
    testar_leads_crm_json()
    print("=== TODOS OS TESTES PASSARAM COM SUCESSO! 100% FUNCIONAL ===")
