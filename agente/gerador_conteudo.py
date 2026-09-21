#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Conteúdo e Assistente de Marketing V2.0 — TruData ERP (Hansen Software)
Equipado com 50 melhorias: Frameworks AIDA/PAS/BAB, Motor de 50 Ganchos,
Validador Fiscal, Exportação Direta para o Painel Web, e Gerador de Prompts de Imagem IA.
"""

import sys
import os
import json
import argparse
import re
from datetime import datetime

# Fix Windows console UTF-8 output
if sys.platform == "win32":
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass


# -------------------------------------------------------------------------
# CONSTANTES & ESTRUTURAS
# -------------------------------------------------------------------------

SEGMENTOS = {
    "1": "Comércio Geral & Varejo",
    "2": "Moda, Confecções & Calçados",
    "3": "Farmácias & Drogarias",
    "4": "Prestação de Serviços & Oficinas Mecânicas",
    "5": "Contabilidades & Parceiros Fiscais (Modo Escritório)",
    "6": "Supermercados & Mercados de Bairro"
}

FRAMEWORKS = {
    "AIDA": "Atenção (Gancho) -> Interesse (Dor/Cenário) -> Desejo (Solução TruData) -> Ação (CTA)",
    "PAS": "Problema (Gargalo) -> Agitação (Custo do problema) -> Solução (Trudata ERP)",
    "BAB": "Before (Vida sem ERP) -> After (Rotina organizada) -> Bridge (Como fazer a transição)"
}

HASHTAGS_SEGMENTADAS = {
    "geral": "#TrudataERP #HansenSoftware #GestaoEmpresarial #Varejo #ComercioGaucho #SarandiRS",
    "fiscal": "#ReformaTributaria #SefazRS #NFCe #SPEDFiscal #ContabilidadeRS #ModoEscritorio",
    "moda": "#GestaoDeModa #LojaDeRoupas #GradeDeCoresETamanhos #ControleDeEstoque #VarejoDeModa",
    "farmacia": "#FarmaciaIndependente #GestaoDeDrogaria #SNGPC #BalcaoDeFarmacia #Medicamentos",
    "servicos": "#OrdemDeServico #OficinaMecanica #PrestadorDeServicos #GestaoDeOS #NFSe"
}

BANCO_GANCHOS_TOP = [
    "Se o seu caixa faz isso na hora do pagamento, você está perdendo clientes todos os dias.",
    "O erro silencioso que acontece na frente de caixa e faz sumir dinheiro no fim do mês.",
    "'Tem no sistema, mas sumiu da arara?' O pesadelo da grade de moda.",
    "Contador: quantas vezes por dia você desloga de um sistema para trocar de cliente?",
    "Quando o sistema da sua loja para, você fala com um robô ou com uma pessoa de verdade?",
    "3 segundos a mais por nota fiscal emitida custam 2 horas de fila na sua loja.",
    "Lote vencido na prateleira de farmácia é prejuízo na certa. Veja como evitar.",
    "O cliente liga perguntando 'meu carro já está pronto?' e ninguém sabe responder.",
    "Reforma Tributária: quem usa sistemas defasados vai sofrer com notas fiscais travadas.",
    "Chega de fechar o navegador para trocar de CNPJ na SEFAZ. Veja como funciona o Modo Escritório."
]

# -------------------------------------------------------------------------
# FUNÇÕES DE HIGIENIZAÇÃO & VALIDAÇÃO
# -------------------------------------------------------------------------

PALAVRAS_SLOP_IA = [
    "no mundo dinâmico de hoje", "revolucione o seu negócio", "mergulhe fundo",
    "uma tapeçaria de", "no cenário em constante evolução", "jogo de xadrez empresarial",
    "revolucionário", "divisor de águas", "inovação sem precedentes"
]

def sanitizar_texto_anti_slop(texto):
    """Remove clichês artificiais de IA e mantém a linguagem natural da TruData."""
    t = texto
    for termo in PALAVRAS_SLOP_IA:
        if termo in t.lower():
            t = re.sub(re.escape(termo), "", t, flags=re.IGNORECASE)
    return t.strip()

def validar_regras_fiscais(texto):
    """Verifica inconsistências fiscais comuns (ex: citar TEF como obrigação universal)."""
    alertas = []
    if "obrigatório para todos" in texto.lower() and "tef" in texto.lower():
        alertas.append("⚠️ Cuidado: O TEF possui regras específicas por segmento no RS. Evite generalizar como regra universal.")
    if "garantia de lucro" in texto.lower():
        alertas.append("⚠️ Evite promessas de resultado financeiro absoluto. Prefira 'organização e controle'.")
    return alertas

def calcular_resumo_legibilidade(texto):
    """Calcula estatísticas do texto para leitura confortável em smartphones."""
    palavras = texto.split()
    chars = len(texto)
    primeira_frase = texto.split('\n')[0] if '\n' in texto else texto
    corte_instagram = len(primeira_frase) <= 125

    return {
        "caracteres": chars,
        "palavras": len(palavras),
        "primeira_linha_chars": len(primeira_frase),
        "corte_ok": corte_instagram,
        "dica_corte": "✅ Gancho visível antes do botão '... mais'" if corte_instagram else "⚠️ Primeira frase longa (pode ser cortada no feed do Instagram)"
    }

# -------------------------------------------------------------------------
# GERADORES DE CONTEÚDO
# -------------------------------------------------------------------------

def gerar_post_framework(segmento_id, framework_tipo="AIDA"):
    """Gera post completo usando um dos frameworks clássicos de copywriting."""
    seg_nome = SEGMENTOS.get(str(segmento_id), "Comércio Geral")
    
    if framework_tipo == "PAS":
        gancho = "O erro que atrasa o fechamento de caixa toda sexta-feira na sua loja 🛑"
        problema = "Quando o sistema trava na emissão da NFC-e ou exige conferência manual de cada comprovante de cartão, a equipe fica presa até tarde e os números não batem."
        agitacao = "Isso gera estresse desnecessário na equipe, divergências de saldo com a contabilidade e insegurança na hora de conferir o faturamento."
        solucao = "Com o Trudata ERP, a frente de caixa é ágil, com TEF integrado e conciliação em tempo real. Fechamento seguro em poucos minutos."
        cta = "Conheça o Trudata ERP para " + seg_nome + ". Toque no link da bio e agende uma conversa rápida com nossos especialistas de Sarandi - RS."
    elif framework_tipo == "BAB":
        gancho = "A diferença entre um estoque desorganizado e um controle que funciona de verdade 📦✨"
        problema = "Antes: Anotações em cadernos ou planilhas soltas. O cliente pergunta pelo produto, você acha que tem, mas não encontra nada na arara."
        agitacao = "Depois: Visão clara em tempo real no Trudata ERP. Cada item identificado com etiqueta de código de barras e saldo auditado."
        solucao = "A ponte para essa transformação é mais simples do que você imagina. Migramos seus dados com suporte humano direto."
        cta = "Comente 'ESTOQUE' para receber um diagnóstico gratuito da sua rotina."
    else: # AIDA
        gancho = "Se o seu sistema trava no horário de pico, você está perdendo vendas silenciosamente."
        problema = "No varejo de " + seg_nome + ", cada segundo na fila conta. Um sistema pesado ou com telas confusas cansa o operador e afasta o cliente."
        agitacao = "O Trudata ERP foi construído com base em mais de 25 anos de experiência e mais de 4 milhões de notas fiscais emitidas com estabilidade máxima."
        solucao = "Aqui você tem suporte de verdade, feito por especialistas que entendem a realidade do comércio gaúcho."
        cta = "Descubra como o Trudata pode simplificar a rotina da sua empresa. Link na bio!"

    legenda_completa = f"{gancho}\n\n{problema}\n\n{agitacao}\n\n{solucao}\n\n👉 {cta}\n\n{HASHTAGS_SEGMENTADAS.get('geral')}"
    legenda_sanitizada = sanitizar_texto_anti_slop(legenda_completa)
    
    return {
        "framework": framework_tipo,
        "segmento": seg_nome,
        "gancho": gancho,
        "legenda": legenda_sanitizada,
        "stats": calcular_resumo_legibilidade(legenda_sanitizada),
        "alertas": validar_regras_fiscais(legenda_sanitizada)
    }

def gerar_prompt_imagem_ia(tema, segmento):
    """Gera prompts fotográficos em inglês e português para Flux, Midjourney e DALL-E no padrão visual TruData."""
    prompt_en = (
        f"A modern, clean, authentic commercial photograph of a business in Brazil ({segmento}), "
        f"focused on '{tema}'. Professional lighting, cinematic depth of field, natural workplace setting. "
        "Subtle modern technological aesthetic with dark navy (#0f172a) and vibrant cyan accents (#009fe3). "
        "No distorted text, realistic human expressions, high-end commercial editorial quality, shot on 35mm lens."
    )
    prompt_pt = (
        f"Fotografia comercial autêntica e profissional de uma empresa ({segmento}) no Brasil, "
        f"com foco em '{tema}'. Iluminação natural, ambiente corporativo acolhedor com toques sutis de azul "
        "ciano e azul escuro profissional. Pessoas reais trabalhando, alta resolução, estilo editorial."
    )
    return {
        "prompt_midjourney_flux": prompt_en,
        "prompt_portugues": prompt_pt,
        "aspect_ratio": "1:1 (Feed) ou 9:16 (Stories/Reels)"
    }

def gerar_sequencia_whatsapp_contador(nome_contador="Colega Contador"):
    """Gera cadência de 3 toques consultivos para prospecção B2B de escritórios de contabilidade."""
    return [
        {
            "toque": "Toque 1 — Convite Consultivo (Dia 1)",
            "canal": "WhatsApp Individual",
            "mensagem": (
                f"Olá, {nome_contador}, tudo bem? Aqui é da equipe TruData (Hansen Software, de Sarandi - RS).\n\n"
                "Desenvolvemos uma funcionalidade pensada especialmente para a rotina contábil chamada **Modo Escritório**: "
                "um painel onde você troca de cliente em apenas 2 cliques, sem precisar deslogar para abrir a próxima empresa na SEFAZ.\n\n"
                "Além disso, o sistema conta com conferência automática de devolução fiscal por XML e cobrança de honorários no Sicredi.\n\n"
                "Criamos uma página com os detalhes práticos:\n"
                "👉 https://trudata.com.br/para-contadores\n\n"
                "Faz sentido conversarmos 5 minutinhos nesta semana para você ver como funciona?"
            )
        },
        {
            "toque": "Toque 2 — Dado de Produtividade (Dia 4)",
            "canal": "WhatsApp Follow-up",
            "mensagem": (
                f"Oi, {nome_contador}, passando apenas para compartilhar um dado rápido da nossa região:\n\n"
                "Em média, os analistas fiscais que atendem empresas clientes da TruData relatam economizar mais de "
                "**3 horas por semana** no fechamento mensal, por não precisarem corrigir rejeições manuais ou cobrar arquivos XML por e-mail.\n\n"
                "Quando tiver 2 minutinhos livres, dê uma olhada no resumo aqui: https://trudata.com.br/para-contadores. Um abraço!"
            )
        },
        {
            "toque": "Toque 3 — Convite Demonstração (Dia 8)",
            "canal": "WhatsApp / Ligação Breve",
            "mensagem": (
                f"Olá, {nome_contador}! Imagino que a rotina esteja corrida com os prazos de obrigações fiscais.\n\n"
                "Se quiser, podemos agendar uma rápida demonstração online de 10 minutos ou até tomar um café para te mostrar "
                "como a integração do Trudata ERP Web com o seu sistema de apuração pode simplificar o seu dia a dia.\n\n"
                "Quinta ou sexta-feira pela manhã fica melhor para você?"
            )
        }
    ]

# -------------------------------------------------------------------------
# EXPORTAÇÃO PARA O PAINEL WEB
# -------------------------------------------------------------------------

def exportar_para_painel_web(titulo, canal, data_prev, pilar, legenda, briefing):
    """Insere o novo post diretamente na fila do painel web (index.html)."""
    index_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "painel_aprovacao", "index.html"))
    if not os.path.exists(index_path):
        return False, "index.html não encontrado"

    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    novo_post = {
        "id": f"post-gen-{int(datetime.now().timestamp())}",
        "titulo": titulo,
        "canal": canal,
        "data": data_prev,
        "isFeriado": False,
        "pilar": pilar,
        "status": "pendente",
        "imagem": "card_tela_real_anonimizada.jpg",
        "comentarios": "Gerado via TruData Marketing CLI V2.0",
        "briefing": briefing,
        "slides": [titulo, briefing, "Conheça o Trudata ERP"],
        "slideAtual": 0,
        "legenda": legenda
    }

    # Match POSTS_INICIAIS
    match = re.search(r"(const POSTS_INICIAIS = \[)([\s\S]*?)(\];\s*let posts = \[\];)", html)
    if match:
        prefix = match.group(1)
        corpo = match.group(2).rstrip()
        suffix = match.group(3)

        novo_json = json.dumps(novo_post, ensure_ascii=False, indent=6)
        corpo_atualizado = corpo + ",\n" + novo_json
        html_novo = html[:match.start()] + prefix + corpo_atualizado + "\n    " + suffix + html[match.end():]

        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html_novo)
        return True, novo_post["id"]

    return False, "Estrutura POSTS_INICIAIS não localizada"

def gerar_campanha_meta_ads_local(cidade="Sarandi", segmento_id="1"):
    """Gera criativo completo de alta conversão para Meta Ads (Instagram/Facebook) segmentado por município."""
    seg_nome = SEGMENTOS.get(segmento_id, "Comércio Varejista")
    
    anuncio = {
        "cidade": cidade,
        "segmento": seg_nome,
        "objetivo": "Leads / Mensagens no WhatsApp",
        "publico_alvo": f"Empresários, Lojistas, Gerentes de {seg_nome} em {cidade} e raio de 25km (25 a 58 anos)",
        "headline": f"Cansado de suporte por robô em {cidade}? Conheça a TruData ERP",
        "texto_primario": f"""Atenção comerciantes e lojistas de {cidade} e região! 📢

Você já passou pelo estresse de ter uma fila de clientes no caixa no sábado de manhã e o sistema travar sem ninguém atender o telefone?

Aqui no Rio Grande do Sul, a Hansen Software desenvolve o TruData ERP há mais de 25 anos com padrão internacional MPS.BR e uma promessa clara:

✅ Frente de caixa (PDV) ultra veloz — emite NFC-e em 3 segundos.
✅ Opera em contingência offline — se a internet de {cidade} oscilar, suas vendas não param.
✅ Suporte 100% humano — você liga ou chama no WhatsApp e fala direto com a gente.
✅ Controle rigoroso de estoque, financeiro e integração contábil automática.

Mais de 300 empresas no Norte Gaúcho já operam com a segurança de quem está perto de você.

👉 Quer ver uma demonstração gratuita de 15 minutos adaptada para o comércio de {cidade}? Toque no botão abaixo e fale direto com nosso consultor no WhatsApp!""",
        "descricao_link": f"Hansen Software · Sarandi/RS · Suporte Local",
        "cta_botao": "Enviar Mensagem no WhatsApp"
    }
    return anuncio

# -------------------------------------------------------------------------
# INTERFACE CLI
# -------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="TruData Marketing Assistant V2.0")
    parser.add_argument("--formato", choices=["feed", "reels", "stories", "whatsapp", "ia-prompt", "meta-ads"], help="Formato do conteúdo")
    parser.add_argument("--segmento", choices=["1", "2", "3", "4", "5", "6"], default="1", help="Segmento de atuação")
    parser.add_argument("--cidade", default="Sarandi", help="Cidade-alvo para campanhas locais de Meta Ads (ex: Sarandi, Passo Fundo, Carazinho, Marau)")
    parser.add_argument("--framework", choices=["AIDA", "PAS", "BAB"], default="AIDA", help="Framework de copywriting")
    parser.add_argument("--exportar", action="store_true", help="Exporta o post diretamente para o painel web")
    parser.add_argument("--ganchos", action="store_true", help="Exibe os top ganchos de alta retenção")

    args = parser.parse_args()

    print("=" * 65)
    print("  TRUDATA ERP — ASSISTENTE DE MARKETING & GERADOR V2.0")
    print("  Hansen Software LTDA · Sarandi - RS · +25 Anos")
    print("=" * 65)

    if args.ganchos:
        print("\n🎯 TOP GANCHOS DE ALTA RETENÇÃO:")
        for idx, g in enumerate(BANCO_GANCHOS_TOP, 1):
            print(f" {idx:02d}. \"{g}\"")
        print("=" * 65)
        return

    if args.formato == "whatsapp":
        print("\n💬 CADÊNCIA DE PROSPECÇÃO B2B (3 TOQUES - CONTABILIDADES):")
        seq = gerar_sequencia_whatsapp_contador()
        for s in seq:
            print(f"\n--- {s['toque']} ({s['canal']}) ---")
            print(s['mensagem'])
        print("=" * 65)
        return

    if args.formato == "meta-ads":
        ad = gerar_campanha_meta_ads_local(cidade=args.cidade, segmento_id=args.segmento)
        print(f"\n📢 CRIATIVO META ADS DE ALTA CONVERSÃO — {ad['cidade'].upper()}:")
        print(f"🎯 Segmento: {ad['segmento']}")
        print(f"📍 Segmentação Sugerida: {ad['publico_alvo']}")
        print(f"📌 Headline (Título): {ad['headline']}")
        print("-" * 65)
        print("📝 Texto Principal (Copy):")
        print(ad['texto_primario'])
        print("-" * 65)
        print(f"🔗 Descrição do Link: {ad['descricao_link']}")
        print(f"🔘 Botão de Ação (CTA): {ad['cta_botao']}")
        print("=" * 65)
        return

    if args.formato == "ia-prompt":
        prompt_info = gerar_prompt_imagem_ia("Operação de Frente de Caixa Ágil", SEGMENTOS.get(args.segmento, "Comércio"))
        print("\n🎨 PROMPT GERADO PARA IMAGENS IA (FLUX / MIDJOURNEY / DALL-E):")
        print(f"Inglês: {prompt_info['prompt_midjourney_flux']}")
        print(f"Português: {prompt_info['prompt_portugues']}")
        print(f"Formato: {prompt_info['aspect_ratio']}")
        print("=" * 65)
        return

    # Default: gerar post com framework
    res = gerar_post_framework(args.segmento, args.framework)
    print(f"\n📌 CONTEÚDO GERADO ({res['framework']} · {res['segmento']}):\n")
    print(res["legenda"])
    print("-" * 65)
    print(f"📊 Legibilidade: {res['stats']['caracteres']} caracteres | {res['stats']['palavras']} palavras")
    print(f"📱 Instagram: {res['stats']['dica_corte']}")
    if res["alertas"]:
        for a in res["alertas"]:
            print(a)

    if args.exportar:
        sucesso, msg = exportar_para_painel_web(
            titulo=f"{args.framework}: Gestão para {res['segmento']}",
            canal="Instagram",
            data_prev="Planejamento Imediato",
            pilar=f"Vendas & {args.framework}",
            legenda=res["legenda"],
            briefing=f"Post gerado no framework {args.framework} com foco em {res['segmento']}."
        )
        if sucesso:
            print(f"\n✅ Post exportado com sucesso para o painel web! ID: {msg}")
        else:
            print(f"\n❌ Falha na exportação: {msg}")

    print("=" * 65)

if __name__ == "__main__":
    main()
