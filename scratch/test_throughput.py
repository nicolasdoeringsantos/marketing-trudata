import urllib.request
import json
import time
import concurrent.futures

with open('scratch/cnpjs_brutos.txt', 'r', encoding='utf-8') as f:
    cnpjs = [line.strip() for line in f if line.strip()][:50]

def test_fetch(c):
    url = f"https://minhareceita.org/{c}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        t0 = time.time()
        res = urllib.request.urlopen(req, timeout=5)
        raw = res.read()
        data = json.loads(raw.decode('iso-8859-1'))
        dt = time.time() - t0
        return (True, c, dt, data.get('razao_social'), data.get('municipio'), data.get('descricao_situacao_cadastral'))
    except Exception as e:
        return (False, c, 0, str(e), None, None)

t_start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(test_fetch, cnpjs))
total_time = time.time() - t_start

success = [r for r in results if r[0]]
print(f"50 requisições feitas em {total_time:.2f} segundos!")
print(f"Sucesso: {len(success)}/50 ({len(success)/50*100:.1f}%)")
for r in success[:8]:
    print(f"  {r[1]} -> {r[3]} ({r[4]}) - Status: {r[5]} em {r[2]:.2f}s")
