#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compilador do Relatório Executivo Semanal de Marketing & Vendas — TruData ERP
Gera mensagem formatada para WhatsApp destinada à diretoria da Hansen Software.
"""

import sys
import os
import json
from datetime import datetime

if sys.platform == "win32":
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAINEL_DIR = os.path.join(BASE_DIR, "painel_aprovacao")
STATUS_FILE = os.path.join(PAINEL_DIR, "status_aprovacoes.json")
METRICAS_FILE = os.path.join(PAINEL_DIR, "metricas_posts.json")

def carregar_dados():
    status = {}
    metricas = {}
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                status = json.load(f)
        except Exception:
            pass

    if os.path.exists(METRICAS_FILE):
        try:
            with open(METRICAS_FILE, "r", encoding="utf-8") as f:
                metricas = json.load(f)
        except Exception:
            pass

    return status, metricas

def gerar_relatorio_whatsapp():
    status, metricas = carregar_dados()
    hoje = datetime.now().strftime("%d/%m/%Y")

    total_aprovados = sum(1 for s in status.values() if s.get("status") == "aprovado")
    total_rejeitados = sum(1 for s in status.values() if s.get("status") == "rejeitado")
    
    total_alcance = sum(int(m.get("alcance", 0)) for m in metricas.values())
    total_curtidas = sum(int(m.get("curtidas", 0)) for m in metricas.values())
    total_cliques = sum(int(m.get("cliques", 0)) for m in metricas.values())

    msg = f"""📊 *RELATÓRIO EXECUTIVO SEMANAL — TRUDATA MARKETING*
📅 Data: {hoje}
🏢 Hansen Software LTDA · Sarandi - RS

━━━━━━━━━━━━━━━━━━━━━
📈 *1. ESTEIRA DE CONTEÚDO & APROVAÇÕES*
• Posts Aprovados para Publicação: *{total_aprovados}*
• Posts com Ajuste Solicitado: *{total_rejeitados}*
• Total de Artes Prontas no Ecossistema: *17 cards HD*

━━━━━━━━━━━━━━━━━━━━━
🎯 *2. PERFORMANCE & ENGAJAMENTO ACUMULADO*
• Alcance Estimado: *{total_alcance:,} visualizações*
• Interações / Curtidas: *{total_curtidas}*
• Cliques Direcionados para WhatsApp: *{total_cliques} potenciais leads*

━━━━━━━━━━━━━━━━━━━━━
🗓️ *3. DESTAQUES DA SEMANA & PAUTAS PRIORITÁRIAS*
✅ *Sábado de Loja Cheia & PDV Veloz:* Reforço de contingência offline para mercados.
✅ *Campanha Reforma Tributária:* Divulgação do simulador interativo de CBS/IBS.
✅ *Selo Escritório Parceiro:* Abordagem direta com contabilidades de Sarandi e Passo Fundo.
✅ *Módulo Moda & Grade:* Prospecção de confecções e sapatarias locais.

━━━━━━━━━━━━━━━━━━━━━
💡 *4. FERRAMENTAS & NOVOS RECURSOS DISPONÍVEIS*
• 4 Novas Landing Pages Ativas: `/mercados`, `/moda`, `/farmacias` e `/reforma-tributaria`
• Gerador de Propostas Comerciais B2B em 1 página PDF
• Teleprompter no painel para gravação de Reels da equipe
• Calculadora de Retrabalho com botão WhatsApp

🔗 *Acesso ao Painel Central:* http://192.168.0.157:8080/index.html
━━━━━━━━━━━━━━━━━━━━━
_Gerado automaticamente pelo Agente de Marketing TruData_"""

    return msg

def main():
    relatorio = gerar_relatorio_whatsapp()
    print("=" * 65)
    print("  TRUDATA ERP — RELATÓRIO EXECUTIVO PARA WHATSAPP")
    print("=" * 65)
    print(relatorio)
    print("=" * 65)

if __name__ == "__main__":
    main()
