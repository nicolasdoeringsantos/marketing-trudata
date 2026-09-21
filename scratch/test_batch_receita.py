import urllib.request
import json
import time

with open('scratch/cnpjs_brutos.txt', 'r', encoding='utf-8') as f:
    cnpjs = [line.strip() for line in f if line.strip()][:10]

print(f"Testando 10 CNPJs:")
for c in cnpjs:
    t0 = time.time()
    try:
        req = urllib.request.Request(f"https://minhareceita.org/{c}", headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=5)
        raw = res.read()
        data = json.loads(raw.decode('iso-8859-1'))
        dt = time.time() - t0
        print(f"[{dt:.2f}s] {c} -> {data.get('razao_social')} | {data.get('municipio')} | {data.get('descricao_situacao_cadastral')} | CNAE: {data.get('cnae_fiscal')}")
    except Exception as e:
        print(f"ERRO {c}: {e}")
