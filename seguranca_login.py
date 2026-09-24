#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proxy Reverso de Segurança com Tela de Login Visual — TruData Hub
Não altera nenhuma linha do projeto original.
Escuta na porta 8081 e redireciona os acessos autorizados para a porta 8080.
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
import urllib.error
import http.cookies
import json
import os
import sys
import secrets
import hashlib
import time
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "usuarios.json")
SESSOES_FILE = os.path.join(BASE_DIR, ".sessoes_ativas.json")
LOGO_FILE = os.path.join(BASE_DIR, "brand", "logo_direta_b64.txt")

def obter_logo_base64():
    if os.path.exists(LOGO_FILE):
        try:
            with open(LOGO_FILE, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception:
            pass
    return ""

# Carrega configurações
def carregar_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "usuarios": {
            "admin": {
                "senha_hash": hashlib.sha256("admin123".encode("utf-8")).hexdigest(),
                "nome": "Administrador"
            }
        },
        "configuracoes": {
            "duracao_sessao_dias": 7,
            "porta_proxy": 8081,
            "porta_servidor_original": 8080
        }
    }

config = carregar_config()
PORTA_PROXY = int(os.environ.get("PORT", config.get("configuracoes", {}).get("porta_proxy", 8081)))
PORTA_ORIGINAL = int(os.environ.get("INTERNAL_PORT", config.get("configuracoes", {}).get("porta_servidor_original", 8080)))
URL_DESTINO = f"http://127.0.0.1:{PORTA_ORIGINAL}"

# Gerenciamento de Sessões
sessoes = {}

def carregar_sessoes():
    global sessoes
    if os.path.exists(SESSOES_FILE):
        try:
            with open(SESSOES_FILE, "r", encoding="utf-8") as f:
                dados = json.load(f)
                agora = time.time()
                sessoes = {k: v for k, v in dados.items() if v.get("expira", 0) > agora}
        except Exception:
            sessoes = {}

def salvar_sessoes():
    try:
        with open(SESSOES_FILE, "w", encoding="utf-8") as f:
            json.dump(sessoes, f, indent=2)
    except Exception:
        pass

carregar_sessoes()

def validar_credenciais(usuario, senha):
    cfg = carregar_config()
    usuarios = cfg.get("usuarios", {})
    usuario = (usuario or "").strip()
    if usuario in usuarios:
        dados_user = usuarios[usuario]
        senha_hash_esperada = dados_user.get("senha_hash")
        senha_texto = dados_user.get("senha")  # suporte a senha direta em texto se usuário preferir
        
        senha_hash_input = hashlib.sha256(senha.encode("utf-8")).hexdigest()
        if senha_hash_esperada and senha_hash_input.lower() == senha_hash_esperada.lower():
            return True, dados_user.get("nome", usuario)
        if senha_texto and senha == senha_texto:
            return True, dados_user.get("nome", usuario)
    return False, None

def criar_sessao(usuario, nome):
    token = secrets.token_hex(32)
    dias = carregar_config().get("configuracoes", {}).get("duracao_sessao_dias", 7)
    expira = time.time() + (dias * 86400)
    sessoes[token] = {
        "usuario": usuario,
        "nome": nome,
        "criado_em": time.time(),
        "expira": expira
    }
    salvar_sessoes()
    return token

def verificar_sessao(token):
    if not token or token not in sessoes:
        return None
    sessao = sessoes[token]
    if time.time() > sessao.get("expira", 0):
        del sessoes[token]
        salvar_sessoes()
        return None
    return sessao

def revogar_sessao(token):
    if token in sessoes:
        del sessoes[token]
        salvar_sessoes()

HTML_LOGIN_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Acesso Seguro — TruData Marketing</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    }
    body {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #090D16;
      background-image: 
        radial-gradient(at 15% 15%, rgba(37, 99, 235, 0.18) 0px, transparent 50%),
        radial-gradient(at 85% 85%, rgba(6, 182, 212, 0.15) 0px, transparent 50%),
        radial-gradient(at 50% 50%, rgba(30, 41, 59, 0.3) 0px, transparent 70%);
      color: #F1F5F9;
      padding: 20px;
    }
    .login-container {
      width: 100%;
      max-width: 420px;
      background: rgba(17, 24, 39, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.65), 0 0 30px -5px rgba(59, 130, 246, 0.2);
      border-radius: 20px;
      padding: 36px 32px;
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      position: relative;
      overflow: hidden;
    }
    .login-container::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, #2563EB, #06B6D4, #3B82F6);
    }
    .trudata-brand-header {
      display: flex;
      justify-content: center;
      align-items: center;
      margin-bottom: 24px;
    }
    .trudata-logo-wrapper {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 14px 28px 12px 28px;
      background: rgba(15, 23, 42, 0.45);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      box-shadow: 0 10px 30px -8px rgba(0, 0, 0, 0.5), 0 0 25px rgba(6, 182, 212, 0.12);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }
    .trudata-main-logo {
      height: 46px;
      width: auto;
      max-width: 250px;
      object-fit: contain;
      filter: drop-shadow(0 2px 14px rgba(6, 182, 212, 0.4));
      display: block;
    }
    .trudata-subtag {
      font-size: 0.78rem;
      font-weight: 600;
      color: #38BDF8;
      margin-top: 8px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }
    .header-sub {
      margin-bottom: 24px;
    }
    .header-sub h2 {
      font-size: 1.1rem;
      font-weight: 700;
      color: #F8FAFC;
      margin-bottom: 4px;
    }
    .header-sub p {
      font-size: 0.85rem;
      color: #94A3B8;
    }
    .alert-error {
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.35);
      color: #FCA5A5;
      padding: 12px 14px;
      border-radius: 10px;
      font-size: 0.85rem;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 10px;
      animation: shake 0.35s ease-in-out;
    }
    @keyframes shake {
      0%, 100% { transform: translateX(0); }
      20%, 60% { transform: translateX(-6px); }
      40%, 80% { transform: translateX(6px); }
    }
    .form-group {
      margin-bottom: 18px;
    }
    label {
      display: block;
      font-size: 0.82rem;
      font-weight: 600;
      color: #CBD5E1;
      margin-bottom: 8px;
    }
    .input-wrapper {
      position: relative;
    }
    .input-wrapper svg.field-icon {
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      width: 18px;
      height: 18px;
      fill: #64748B;
      pointer-events: none;
      transition: fill 0.2s;
    }
    input[type="text"],
    input[type="password"] {
      width: 100%;
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 12px;
      padding: 12px 14px 12px 42px;
      font-size: 0.92rem;
      color: #F8FAFC;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    input:focus {
      border-color: #3B82F6;
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
    }
    input:focus + svg.field-icon {
      fill: #3B82F6;
    }
    .btn-toggle-pass {
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      cursor: pointer;
      color: #64748B;
      display: flex;
      align-items: center;
      padding: 4px;
    }
    .btn-toggle-pass:hover {
      color: #94A3B8;
    }
    .btn-submit {
      width: 100%;
      background: linear-gradient(135deg, #2563EB, #1D4ED8);
      color: #FFFFFF;
      border: none;
      border-radius: 12px;
      padding: 13px;
      font-size: 0.95rem;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
      transition: transform 0.15s, box-shadow 0.15s, filter 0.15s;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      margin-top: 8px;
    }
    .btn-submit:hover {
      filter: brightness(1.1);
      box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45);
    }
    .btn-submit:active {
      transform: scale(0.98);
    }
    .footer-note {
      text-align: center;
      margin-top: 24px;
      font-size: 0.75rem;
      color: #64748B;
    }
    .footer-note span {
      color: #06B6D4;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div class="login-container">
    <div class="trudata-brand-header">
      <div class="trudata-logo-wrapper">
        <img src="data:image/png;base64,{{LOGO_BASE64}}" alt="TruData" class="trudata-main-logo">
        <div class="trudata-subtag">Estúdio de conteúdo</div>
      </div>
    </div>

    <div class="header-sub">
      <h2>Painel Corporativo</h2>
      <p>Informe suas credenciais para liberar o cockpit.</p>
    </div>

    {{ALERT_ERROR}}

    <form method="POST" action="/login" autocomplete="on">
      <input type="hidden" name="redirect" value="{{REDIRECT_URL}}">
      
      <div class="form-group">
        <label for="usuario">Usuário</label>
        <div class="input-wrapper">
          <input type="text" id="usuario" name="usuario" placeholder="Seu usuário" required autofocus autocomplete="username" value="{{VAL_USUARIO}}">
          <svg class="field-icon" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
        </div>
      </div>

      <div class="form-group">
        <label for="senha">Senha de Acesso</label>
        <div class="input-wrapper">
          <input type="password" id="senha" name="senha" placeholder="••••••••••••" required autocomplete="current-password">
          <svg class="field-icon" viewBox="0 0 24 24"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>
          <button type="button" class="btn-toggle-pass" onclick="toggleSenha()" title="Mostrar/Ocultar Senha">
            <svg id="eye-icon" style="width:20px;height:20px;fill:currentColor" viewBox="0 0 24 24"><path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
          </button>
        </div>
      </div>

      <button type="submit" class="btn-submit">
        <span>Acessar Painel</span>
        <svg style="width:18px;height:18px;fill:currentColor" viewBox="0 0 24 24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
      </button>
    </form>

    <div class="footer-note">
      Conexão segura • <span>Criptografia Ativa</span>
    </div>
  </div>

  <script>
    function toggleSenha() {
      const input = document.getElementById('senha');
      if (input.type === 'password') {
        input.type = 'text';
      } else {
        input.type = 'password';
      }
    }
  </script>
</body>
</html>
"""

class AuthProxyHandler(http.server.BaseHTTPRequestHandler):
    def get_token_cookie(self):
        cookie_header = self.headers.get("Cookie")
        if not cookie_header:
            return None
        cookies = http.cookies.SimpleCookie()
        try:
            cookies.load(cookie_header)
            if "trudata_auth" in cookies:
                return cookies["trudata_auth"].value
        except Exception:
            pass
        return None

    def redirecionar_para_login(self, mensagem_erro=None):
        redirect_url = self.path
        if redirect_url in ["/login", "/logout"]:
            redirect_url = "/"
        
        self.send_response(302)
        params = urllib.parse.urlencode({"redirect": redirect_url})
        self.send_header("Location", f"/login?{params}")
        self.end_headers()

    def exibir_login_page(self, erro=None, usuario_previo="", redirect_target="/"):
        html = HTML_LOGIN_TEMPLATE
        if erro:
            alert = f"""<div class="alert-error">
                <svg style="width:20px;height:20px;fill:currentColor;flex-shrink:0" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
                <span>{erro}</span>
            </div>"""
        else:
            alert = ""

        html = html.replace("{{ALERT_ERROR}}", alert)
        html = html.replace("{{VAL_USUARIO}}", usuario_previo or "")
        html = html.replace("{{REDIRECT_URL}}", urllib.parse.quote(redirect_target or "/"))
        html = html.replace("{{LOGO_BASE64}}", obter_logo_base64())

        conteudo = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(conteudo)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(conteudo)

    def do_GET(self):
        clean_path = self.path.split("?")[0].split("#")[0]

        # Rota de Logout
        if clean_path == "/logout":
            token = self.get_token_cookie()
            if token:
                revogar_sessao(token)
            self.send_response(302)
            self.send_header("Set-Cookie", "trudata_auth=; Path=/; Max-Age=0; HttpOnly")
            self.send_header("Location", "/login")
            self.end_headers()
            return

        # Rota de Login (GET)
        if clean_path == "/login":
            token = self.get_token_cookie()
            if verificar_sessao(token):
                self.send_response(302)
                self.send_header("Location", "/")
                self.end_headers()
                return

            qs = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(qs)
            redirect_target = params.get("redirect", ["/"])[0]
            self.exibir_login_page(redirect_target=redirect_target)
            return

        # Para qualquer outra rota: Verificar autenticação
        token = self.get_token_cookie()
        sessao = verificar_sessao(token)
        if not sessao:
            # Se for requisição de API interna, responde com 401
            if clean_path.startswith("/api/"):
                resp = json.dumps({"erro": "Acesso nao autorizado. Faca login.", "auth_necessaria": True}).encode("utf-8")
                self.send_response(401)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(resp)))
                self.end_headers()
                self.wfile.write(resp)
                return

            self.redirecionar_para_login()
            return

        # Usuário autenticado: Repassa para o servidor original
        self.repassar_requisicao("GET")

    def do_POST(self):
        clean_path = self.path.split("?")[0].split("#")[0]

        # Processar formulário de login
        if clean_path == "/login":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            dados = urllib.parse.parse_qs(body)

            usuario = dados.get("usuario", [""])[0]
            senha = dados.get("senha", [""])[0]
            redirect_target = urllib.parse.unquote(dados.get("redirect", ["/"])[0] or "/")
            if not redirect_target.startswith("/"):
                redirect_target = "/"

            valido, nome = validar_credenciais(usuario, senha)
            if valido:
                token = criar_sessao(usuario, nome)
                dias = carregar_config().get("configuracoes", {}).get("duracao_sessao_dias", 7)
                max_age = dias * 86400

                self.send_response(302)
                # Cookie HttpOnly e seguro
                self.send_header("Set-Cookie", f"trudata_auth={token}; Path=/; Max-Age={max_age}; SameSite=Lax; HttpOnly")
                self.send_header("Location", redirect_target)
                self.end_headers()
            else:
                self.exibir_login_page(
                    erro="Usuário ou senha incorretos. Tente novamente.",
                    usuario_previo=usuario,
                    redirect_target=redirect_target
                )
            return

        # Para outros POSTs: verificar autenticação
        token = self.get_token_cookie()
        if not verificar_sessao(token):
            resp = json.dumps({"erro": "Nao autorizado"}).encode("utf-8")
            self.send_response(401)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp)))
            self.end_headers()
            self.wfile.write(resp)
            return

        self.repassar_requisicao("POST")

    def do_OPTIONS(self):
        self.repassar_requisicao("OPTIONS")

    def do_HEAD(self):
        token = self.get_token_cookie()
        if not verificar_sessao(token):
            self.send_response(401)
            self.end_headers()
            return
        self.repassar_requisicao("HEAD")

    def repassar_requisicao(self, metodo):
        """Repassa a requisição HTTP transparentemente para o servidor original (porta 8080)"""
        url_alvo = f"{URL_DESTINO}{self.path}"
        
        # Lê corpo da requisição se houver
        length = int(self.headers.get("Content-Length", 0))
        corpo = self.rfile.read(length) if length > 0 else None

        # Monta headers para encaminhar
        headers_forward = {}
        for k, v in self.headers.items():
            if k.lower() not in ["host", "connection"]:
                headers_forward[k] = v
        headers_forward["Host"] = f"127.0.0.1:{PORTA_ORIGINAL}"
        headers_forward["X-Forwarded-For"] = self.client_address[0]
        headers_forward["X-Forwarded-Proto"] = "http"

        req = urllib.request.Request(url_alvo, data=corpo, headers=headers_forward, method=metodo)

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                self.send_response(response.status)
                for header, valor in response.getheaders():
                    # Não duplica chunked transfer se enviar direto
                    if header.lower() not in ["transfer-encoding", "connection"]:
                        self.send_header(header, valor)
                self.end_headers()
                
                # Streaming de dados do servidor original para o cliente
                while True:
                    pedaco = response.read(65536)
                    if not pedaco:
                        break
                    self.wfile.write(pedaco)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            for header, valor in e.headers.items():
                if header.lower() not in ["transfer-encoding", "connection"]:
                    self.send_header(header, valor)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            # Se o servidor original não estiver ligado
            msg_erro = f"""<!DOCTYPE html>
            <html lang="pt-BR">
            <head><meta charset="utf-8"><title>Aguardando Servidor</title>
            <style>
              body {{ font-family: sans-serif; background: #0B0F19; color: #fff; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
              .box {{ background: #1E293B; padding: 30px; border-radius: 12px; max-width: 500px; text-align: center; border: 1px solid #334155; }}
              h2 {{ color: #38BDF8; margin-top: 0; }}
              p {{ color: #94A3B8; font-size: 14px; line-height: 1.6; }}
            </style>
            </head>
            <body>
              <div class="box">
                <h2>Servidor TruData Inicializando</h2>
                <p>O servidor original na porta {PORTA_ORIGINAL} ainda não respondeu.</p>
                <p>Certifique-se de executar o <b>servidor_painel.py</b> ou use o inicializador automático.</p>
              </div>
            </body></html>""".encode("utf-8")
            self.send_response(503)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(msg_erro)))
            self.end_headers()
            self.wfile.write(msg_erro)

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

def run():
    print("=" * 60)
    print("   TruData ERP — Proxy de Segurança com Tela de Login")
    print("=" * 60)
    print(f"[*] Porta Protegida (com Login)  : http://localhost:{PORTA_PROXY}/")
    print(f"[*] Repasse Interno (sem mexer) : {URL_DESTINO}")
    print(f"[*] Configurações de Usuários   : {CONFIG_FILE}")
    print("=" * 60)
    print("[+] Servidor de segurança ativo e pronto. Pressione Ctrl+C para encerrar.\n")
    
    server = ThreadedHTTPServer(("0.0.0.0", PORTA_PROXY), AuthProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Encerrando proxy de segurança...")
        server.server_close()

if __name__ == "__main__":
    run()
