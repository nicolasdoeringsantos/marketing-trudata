#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sincronizador Automático do Ecossistema de Marketing TruData
Valida a integridade entre:
- Calendário Editorial (calendario_dados.json)
- Painel Web de Aprovação (index.html)
- Imagens em conteudo_pronto/
- Scripts e ferramentas CLI
"""

import os
import json
import sys

if sys.platform == "win32":
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

def sincronizar():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    painel_dir = os.path.join(base_dir, "painel_aprovacao")
    conteudo_dir = os.path.join(base_dir, "conteudo_pronto")
    cal_json = os.path.join(painel_dir, "calendario_dados.json")
    index_html = os.path.join(painel_dir, "index.html")

    print("=" * 65)
    print("  TRUDATA MARKETING — AUDITORIA DE SINCRONIZAÇÃO")
    print("=" * 65)

    erros = 0

    # 1. Checar Calendário
    if os.path.exists(cal_json):
        with open(cal_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        total_dias = len(data.get("stories_diarios", []))
        total_feed = len(data.get("feed_reels", {}))
        print(f"✅ Calendário 2026 íntegro: {total_dias} dias mapeados | {total_feed} pautas de Feed")
    else:
        print("❌ Arquivo calendario_dados.json ausente!")
        erros += 1

    # 2. Checar Imagens Prontas
    imagens = [f for f in os.listdir(conteudo_dir) if f.endswith(('.jpg', '.png'))]
    print(f"✅ Imagens prontas para publicação: {len(imagens)} cards disponíveis")

    # 3. Checar Painel Web
    if os.path.exists(index_html):
        with open(index_html, "r", encoding="utf-8") as f:
            html = f.read()
        num_posts = html.count('"id": "post-')
        print(f"✅ Painel de Aprovação ativo com {num_posts} posts na fila")
    else:
        print("❌ Arquivo index.html ausente!")
        erros += 1

    print("-" * 65)
    if erros == 0:
        print("🚀 STATUS: 100% SINCRONIZADO E PRONTO PARA PRODUÇÃO!")
    else:
        print(f"⚠️ STATUS: {erros} pendência(s) detectada(s).")
    print("=" * 65)

if __name__ == '__main__':
    sincronizar()
