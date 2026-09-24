#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inicializador Unificado para Nuvem (Render, Railway, Fly.io, VPS, Docker)
Inicia o Servidor Backend (APIs + Estáticos) e o Proxy de Autenticação Segura
em um único comando pronto para produção 24/7.
"""

import os
import sys
import time
import threading

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "painel_aprovacao"))

# Configuração de Portas para Nuvem
# PORT: Porta pública atribuída pelo provedor de nuvem (Render, Railway, etc.)
PORTA_PUBLICA = os.environ.get("PORT", "8080")
PORTA_INTERNA = os.environ.get("INTERNAL_PORT", "8089")

os.environ["PORT"] = str(PORTA_PUBLICA)
os.environ["INTERNAL_PORT"] = str(PORTA_INTERNA)

def iniciar_servidor_backend():
    print(f"[*] Iniciando Servidor Backend Interno na porta {PORTA_INTERNA}...")
    try:
        import painel_aprovacao.servidor_painel as servidor_backend
        servidor_backend.PORT = int(PORTA_INTERNA)
        servidor_backend.run()
    except Exception as e:
        print(f"[!] Erro no Servidor Backend: {e}")

def iniciar_proxy_seguranca():
    print(f"[*] Iniciando Proxy de Segurança e Login na porta pública {PORTA_PUBLICA}...")
    try:
        import seguranca_login
        seguranca_login.PORTA_PROXY = int(PORTA_PUBLICA)
        seguranca_login.PORTA_ORIGINAL = int(PORTA_INTERNA)
        seguranca_login.URL_DESTINO = f"http://127.0.0.1:{PORTA_INTERNA}"
        seguranca_login.run()
    except Exception as e:
        print(f"[!] Erro no Proxy de Segurança: {e}")

if __name__ == "__main__":
    print("=" * 65)
    print("   TruData Marketing & CRM Enterprise — Inicializador Cloud 24/7")
    print("=" * 65)
    print(f"[*] Porta Pública (Acesso Seguro) : {PORTA_PUBLICA}")
    print(f"[*] Porta Interna (Backend)       : {PORTA_INTERNA}")
    print("=" * 65)

    # Inicia Backend em Thread de Fundo
    t_backend = threading.Thread(target=iniciar_servidor_backend, daemon=True)
    t_backend.start()

    time.sleep(1.2)

    # Inicia Proxy de Segurança no Processo Principal
    iniciar_proxy_seguranca()
