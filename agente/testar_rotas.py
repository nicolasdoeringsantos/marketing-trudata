import urllib.request
import json

urls = [
    'http://localhost:8080/index.html',
    'http://localhost:8080/calendario.html',
    'http://localhost:8080/mercados',
    'http://localhost:8080/moda',
    'http://localhost:8080/farmacias',
    'http://localhost:8080/reforma-tributaria',
    'http://localhost:8080/carrosseis',
    'http://localhost:8080/teleprompter',
    'http://localhost:8080/proposta',
    'http://localhost:8080/crm',
    'http://localhost:8080/estudio',
    'http://localhost:8080/tutoriais',
    'http://localhost:8080/analytics',
    'http://localhost:8080/emails',
    'http://localhost:8080/modulos',
    'http://localhost:8080/tco',
    'http://localhost:8080/parceiros',
    'http://localhost:8080/objecoes',
    'http://localhost:8080/contratos',
    'http://localhost:8080/hardware',
    'http://localhost:8080/matriz-fiscal',
    'http://localhost:8080/stories',
    'http://localhost:8080/stories.html',
    'http://localhost:8080/stories_dados.json',
    'http://localhost:8080/proposta-online',
    'http://localhost:8080/calculadora-tef',
    'http://localhost:8080/versus',
    'http://localhost:8080/carne-crediario',
    'http://localhost:8080/auditor-xml',
    'http://localhost:8080/status-sefaz',
    'http://localhost:8080/simulador-simples',
    'http://localhost:8080/regua-cobranca',
    'http://localhost:8080/roteiros-reels',
    'http://localhost:8080/figurinhas',
    'http://localhost:8080/link-bio',
    'http://localhost:8080/catalogo-digital',
    'http://localhost:8080/treinamento-caixa',
    'http://localhost:8080/dimensionador-ti',
    'http://localhost:8080/portal-cliente',
    'http://localhost:8080/perdas-caixa',
    'http://localhost:8080/copiloto-vendas',
    'http://localhost:8080/fidelidade',
    'http://localhost:8080/simulador-mdfe',
    'http://localhost:8080/cases',
    'http://localhost:8080/campanhas-ads',
    'http://localhost:8080/trafego-pago',
    'http://localhost:8080/migracao',
    'http://localhost:8080/pitch',
    'http://localhost:8080/respostas-whatsapp',
    'http://localhost:8080/carrosseis-feed',
    'http://localhost:8080/api/relatorio_semanal',
    'http://localhost:8080/api/leads',
    'http://localhost:8080/api/webhook_config'
]

print("--- TESTE DE ENDPOINTS GET ---")
for u in urls:
    try:
        r = urllib.request.urlopen(u)
        print(f"{u} -> {r.status} OK")
    except Exception as e:
        print(f"{u} -> ERRO: {e}")

print("\n--- TESTE DE DISPARO DE WEBHOOK (POST) ---")
try:
    payload = json.dumps({
        "id": "post_teste_auditoria",
        "titulo": "Sábado de Loja Cheia e PDV Rápido",
        "legenda": "Teste de automação via webhook para n8n.",
        "imagem": "trudata_pdv_caixa_sarandi_1789497541970.jpg"
    }).encode('utf-8')
    req = urllib.request.Request("http://localhost:8080/api/disparar_publicacao", data=payload, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        print(f"POST /api/disparar_publicacao -> {resp.status} OK: {resp.read().decode('utf-8')}")
except Exception as e:
    print(f"ERRO POST: {e}")
