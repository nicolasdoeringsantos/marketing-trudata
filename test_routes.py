import urllib.request
import json
import sys

routes = [
    '/',
    '/tco-roi',
    '/checklist-implantacao',
    '/regua-cobranca',
    '/health-score',
    '/estudio-brolls',
    '/campanhas-trafego',
    '/analytics',
    '/base-conhecimento',
    '/proposta-online',
    '/migracao-concorrentes',
    '/cadencia-sdr',
    '/simulador-contingencia',
    '/mercados',
    '/reforma-tributaria',
    '/hardware',
    '/radar',
    '/emails'
]

results = []
all_ok = True

for r in routes:
    url = f'http://127.0.0.1:8080{r}'
    try:
        req = urllib.request.urlopen(url, timeout=5)
        status = req.getcode()
        results.append((r, status, 'OK'))
    except Exception as e:
        all_ok = False
        results.append((r, getattr(e, 'code', 'ERR'), str(e)))

for r, st, msg in results:
    print(f"[{st}] -> {r}")

# Teste POST /api/salvar_implantacao
try:
    data_imp = json.dumps({'razao_social': 'Teste Sarandi LTDA', 'progresso': 100, 'tecnico': 'Hansen'}).encode('utf-8')
    req_imp = urllib.request.Request('http://127.0.0.1:8080/api/salvar_implantacao', data=data_imp, headers={'Content-Type': 'application/json'})
    res_imp = urllib.request.urlopen(req_imp, timeout=5)
    print(f"[{res_imp.getcode()}] -> POST /api/salvar_implantacao")
except Exception as e:
    all_ok = False
    print(f"[ERR] -> POST /api/salvar_implantacao: {e}")

# Teste POST /api/disparar_cobranca
try:
    data_cob = json.dumps({'cliente': 'Supermercado Teste', 'fase': 'D-3', 'valor': '499.00'}).encode('utf-8')
    req_cob = urllib.request.Request('http://127.0.0.1:8080/api/disparar_cobranca', data=data_cob, headers={'Content-Type': 'application/json'})
    res_cob = urllib.request.urlopen(req_cob, timeout=5)
    print(f"[{res_cob.getcode()}] -> POST /api/disparar_cobranca")
except Exception as e:
    all_ok = False
    print(f"[ERR] -> POST /api/disparar_cobranca: {e}")

if all_ok:
    print("ALL ROUTES & APIS PASSED 200 OK")
else:
    sys.exit(1)
