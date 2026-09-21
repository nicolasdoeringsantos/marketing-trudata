#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Avaliador Automático de Qualidade de Conteúdo Editorial — TruData Marketing
Calcula uma nota de 0 a 100 baseada em:
- Força do Gancho (primeiros 125 caracteres)
- Clareza da Proposta de Valor
- Eficácia do CTA
- Ausência de clichês / AI-slop
- Conformidade e segurança fiscal
"""

import sys
import re

if sys.platform == "win32":
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

TERMOS_SLOP = [
    "no mundo dinâmico de hoje", "revolucione o seu negócio", "mergulhe fundo",
    "uma tapeçaria de", "no cenário em constante evolução", "jogo de xadrez empresarial",
    "revolucionário", "divisor de águas", "inovação sem precedentes", "sinergia perfeita",
    "potencialize seu negócio", "transforme seu negócio", "solução inovadora",
    "no atual ecossistema", "rumo ao sucesso", "desbloqueie o poder"
]

TERMOS_AUTORIDADE_REGIONAL = [
    "sarandi", "hansen software", "mps.br", "rio grande do sul", "sefaz/rs",
    "+25 anos", "25 anos", "humano", "suporte de verdade"
]

TERMOS_FISCAIS_RISCO = [
    ("tef obrigatório para todos", "TEF possui regras por segmento no RS; evitar generalizar como obrigação universal."),
    ("garantia de aumento de 50% de lucro", "Promessa financeira não mensurada; evitar promessas absolutas.")
]

def avaliar_texto(texto):
    pontuacao = 100
    feedbacks = []
    
    # 1. Tamanho do Gancho (máximo 125 chars antes do corte do Instagram)
    primeira_linha = texto.strip().split('\n')[0]
    if len(primeira_linha) > 125:
        pontuacao -= 15
        feedbacks.append(f"⚠️ Gancho longo ({len(primeira_linha)} caracteres). O Instagram cortará no feed antes do botão '... mais'.")
    else:
        feedbacks.append(f"✅ Gancho objetivo ({len(primeira_linha)} caracteres). Não será cortado precocemente.")

    # 2. Presença de CTA claro
    tem_cta = any(k in texto.lower() for k in ["link na bio", "comente", "responda", "compartilhe", "salve", "chame no direct", "whatsapp", "toque no botão"])
    if not tem_cta:
        pontuacao -= 20
        feedbacks.append("❌ Nenhuma Chamada para Ação (CTA) clara detectada no texto.")
    else:
        feedbacks.append("✅ CTA claro e direcionado identificado.")

    # 3. Clichês de IA (AI Slop)
    slop_encontrados = [t for t in TERMOS_SLOP if t in texto.lower()]
    if slop_encontrados:
        pontuacao -= (len(slop_encontrados) * 20)
        feedbacks.append(f"❌ Termos artificiais de IA detectados: {', '.join(slop_encontrados)}")
    else:
        feedbacks.append("✅ Linguagem humana, sem clichês genéricos de IA.")

    # 4. Autoridade e Regionalismo (Bônus de proximidade)
    autoridade_encontrada = [t for t in TERMOS_AUTORIDADE_REGIONAL if t in texto.lower()]
    if autoridade_encontrada:
        pontuacao += min(15, len(autoridade_encontrada) * 5)
        feedbacks.append(f"⭐ Elementos de autoridade e proximidade regional ({', '.join(autoridade_encontrada)}).")

    # 5. Checagem Fiscal
    for termo, aviso in TERMOS_FISCAIS_RISCO:
        if termo in texto.lower():
            pontuacao -= 25
            feedbacks.append(f"⚠️ Alerta Fiscal: {aviso}")

    # 6. Hashtags
    hashtags = re.findall(r'#\w+', texto)
    if len(hashtags) == 0:
        pontuacao -= 10
        feedbacks.append("⚠️ Nenhuma hashtag identificada para alcance orgânico.")
    elif len(hashtags) > 10:
        pontuacao -= 5
        feedbacks.append(f"⚠️ Excesso de hashtags ({len(hashtags)}). Recomendado: entre 3 e 7.")
    else:
        feedbacks.append(f"✅ Bloco de hashtags equilibrado ({len(hashtags)} tags).")

    pontuacao = max(0, min(100, pontuacao))
    return pontuacao, feedbacks

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Auditor de Qualidade Editorial TruData")
    parser.add_argument("texto", nargs="?", default="", help="Texto a ser avaliado")
    parser.add_argument("--trava-minima", type=int, default=85, help="Nota mínima de corte para aprovação (default: 85)")
    args = parser.parse_args()

    print("=" * 65)
    print("  TRUDATA ERP — AUDITOR DE QUALIDADE EDITORIAL (0-100)")
    print(f"  Nota de Corte para Publicação: {args.trava_minima}/100")
    print("=" * 65)
    
    if args.texto:
        texto = args.texto
    else:
        texto = """O erro que atrasa o fechamento de caixa toda sexta-feira na sua loja 🛑\n\nQuando o sistema trava na emissão da NFC-e ou exige conferência manual de cada comprovante de cartão, a equipe fica presa até tarde e os números não batem.\n\nCom o Trudata ERP da Hansen Software, a frente de caixa é ágil, com TEF integrado e conciliação em tempo real.\n\n👉 Toque no link da bio e agende uma conversa com nossos especialistas de Sarandi - RS.\n\n#TrudataERP #VarejoGaucho #GestaoDeCaixa"""

    nota, feedbacks = avaliar_texto(texto)
    
    print(f"\n🎯 NOTA DE QUALIDADE: {nota}/100")
    print("-" * 65)
    for fb in feedbacks:
        print(f" • {fb}")
    print("=" * 65)

    if nota < args.trava_minima:
        print(f"\n🚫 REPROVADO NA TRAVA DE QUALIDADE ({nota} < {args.trava_minima})")
        print("Ajuste o texto removendo termos genéricos ou fortalecendo o gancho/CTA antes de publicar.")
        sys.exit(1)
    else:
        print(f"\n🎉 APROVADO PARA PUBLICAÇÃO! ({nota} >= {args.trava_minima})")
        sys.exit(0)

if __name__ == '__main__':
    main()
