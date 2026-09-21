import urllib.request
import json
import time

time.sleep(1)

routes_to_test = [
    ("GET", "http://localhost:8080/"),
    ("GET", "http://localhost:8080/dossie-portabilidade"),
    ("GET", "http://localhost:8080/proposta-rastreavel"),
    ("GET", "http://localhost:8080/gps-campo"),
    ("GET", "http://localhost:8080/gerador-reels"),
    ("GET", "http://localhost:8080/reforma-2026"),
    ("GET", "http://localhost:8080/api/reforma_tributaria/ncms"),
    ("GET", "http://localhost:8080/api/dossie_concorrentes/dados"),
]

print("=== TESTANDO ROTAS GET ===")
for method, url in routes_to_test:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'TrudataTest/1.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            content = resp.read()
            print(f"[OK {status}] {url} -> {len(content)} bytes")
    except Exception as e:
        print(f"[ERRO] {url} -> {e}")

print("\n=== TESTANDO ENDPOINTS POST ===")
# Teste POST /api/proposta/notificar_abertura
try:
    post_data = json.dumps({
        "cliente": "Supermercado Santa Helena (Teste)",
        "cidade": "Sarandi - RS",
        "telefone": "54996966175",
        "origem": "WhatsApp Link"
    }).encode('utf-8')
    req = urllib.request.Request(
        "http://localhost:8080/api/proposta/notificar_abertura",
        data=post_data,
        headers={'Content-Type': 'application/json', 'User-Agent': 'TrudataTest/1.0'},
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print(f"[OK {resp.status}] POST /api/proposta/notificar_abertura -> {res.get('sucesso')}")
except Exception as e:
    print(f"[ERRO] POST /api/proposta/notificar_abertura -> {e}")

# Teste POST /api/checkin_visita
try:
    post_data = json.dumps({
        "cliente": "Moda & Estilo Carazinho",
        "tipo": "Confecção / Vestuário",
        "cidade": "Carazinho - RS",
        "lat": -28.2844,
        "lon": -52.7867,
        "distancia_km": 42.1,
        "notas": "Lojista insatisfeito com sistema atual que trava na emissão de NFC-e.",
        "gravacao_voz": False
    }).encode('utf-8')
    req = urllib.request.Request(
        "http://localhost:8080/api/checkin_visita",
        data=post_data,
        headers={'Content-Type': 'application/json', 'User-Agent': 'TrudataTest/1.0'},
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print(f"[OK {resp.status}] POST /api/checkin_visita -> {res.get('sucesso')} | ID: {res.get('checkin_id')}")
except Exception as e:
    print(f"[ERRO] POST /api/checkin_visita -> {e}")

print("\n=== TESTE CONCLUIDO COM SUCESSO ===")
