"""Servidor de QA isolado: nenhuma requisição é encaminhada ao CRM real.
Execute python painel_aprovacao/qa/radar_fixture_server.py e acesse :8877.
Estado e registros de teste existem apenas na memória deste processo.
"""
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parents[2]
LEADS = [{"empresa": "Mercado Exemplo 1", "cnpj": "00000000000001", "fase": "proposta"}]
CALLS = []
MODE = {"fail": False, "smtp": False}
CLIENTS = [dict(id=str(i), nome=f"Mercado Exemplo {i}", cnpj=f"{i:014}",
    cidade="Sarandi" if i % 2 else "Passo Fundo", segmento="Supermercados & Mercearias",
    distancia_km=i, lead_score=100-i, telefone="(54) 99999-0000", whatsapp="5554999990000",
    email="contato@example.test", decisor="Equipe de compras", porte="ME", pdvs_estimados=2,
    lat=-27.9443 if i % 2 else -28.2628, lon=-52.9231 if i % 2 else -52.4067,
    endereco="Rua de exemplo", tem_site=False, notas="Cadastro de teste.") for i in range(1,61)]

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)
    def log_message(self, *args):
        pass
    def respond(self, obj, status=200):
        body=json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        url=urlparse(self.path); q=parse_qs(url.query)
        if url.path == "/qa/state": return self.respond({"calls":CALLS,"leads":LEADS})
        if url.path == "/qa/mode":
            MODE.update({k:v[0]=="true" for k,v in q.items()}); return self.respond(MODE)
        if url.path == "/api/leads": return self.respond(LEADS)
        if url.path == "/api/prospectar":
            if MODE["fail"]: return self.respond({"sucesso":False},503)
            city=q.get("cidade",[""])[0]
            data=[p for p in CLIENTS if city in ("", "todas") or p["cidade"]==city]
            return self.respond({"sucesso":True,"clientes":data})
        if url.path == "/api/config_email": return self.respond({"modo":"automatico","senha_configurada":True,"remetente_email":"teste@example.test"})
        if url.path == "/api/historico_emails": return self.respond([])
        if url.path.startswith("/api/"): return self.respond({"erro":"Endpoint não simulado"},404)
        if url.path == "/radar_clientes.html": self.path="/painel_aprovacao/radar_clientes.html"
        return super().do_GET()
    def do_POST(self):
        data=json.loads(self.rfile.read(int(self.headers.get("Content-Length",0))))
        CALLS.append({"path":self.path,"body":data})
        if self.path == "/api/importar_prospect_crm":
            items=data if isinstance(data,list) else [data]
            for p in items: LEADS.append({"empresa":p["nome"],"cnpj":p["cnpj"],"fase":"novo"})
            return self.respond({"sucesso":True,"total_adicionados":len(items)})
        if self.path == "/api/atualizar_status_lead":
            LEADS[:]=[p for p in LEADS if p["cnpj"]!=data["cnpj"]]; LEADS.append(data)
            return self.respond({"sucesso":True})
        if self.path == "/api/gerar_rota_maps": return self.respond({"sucesso":True,"rota_url":"https://www.google.com/maps/dir/?api=1&destination=Sarandi"})
        if self.path == "/api/config_email": return self.respond({"sucesso":True})
        if self.path == "/api/enviar_proposta_email": return self.respond({"sucesso":True,"status":"Entregue via SMTP" if MODE["smtp"] else "Registrado & Pronto para Envio","link_gmail":"https://mail.google.com/mail/"})
        return self.respond({"erro":"Nenhuma escrita real permitida"},404)

if __name__ == "__main__":
    print("QA isolado em http://127.0.0.1:8877/radar_clientes.html",flush=True)
    ThreadingHTTPServer(("127.0.0.1",8877),Handler).serve_forever()
