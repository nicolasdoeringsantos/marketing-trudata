import urllib.request
import re
import concurrent.futures

cidades = [
    'sarandi', 'passo-fundo', 'carazinho', 'marau', 'tapejara', 
    'erechim', 'frederico-westphalen', 'palmeira-das-missoes', 
    'getulio-vargas', 'ibiruba', 'tapera', 'espumoso', 'nonoai', 
    'seberi', 'sananduva', 'casca', 'constantina', 'ronda-alta', 
    'rondinha', 'chapada', 'barra-funda', 'nova-boa-vista', 
    'tres-palmeiras', 'colorado', 'selbach', 'pontao', 'sertao',
    'estacao', 'erebango', 'coxilha', 'victor-graeff',
    'almirante-tamandare-do-sul', 'santo-antonio-do-planalto',
    'boa-vista-das-missoes', 'sagrada-familia', 'jaboticaba',
    'soledade', 'ernestina', 'camargo', 'vila-maria', 'serafina-correa',
    'nova-araca', 'parai', 'lagoa-vermelha', 'ametista-do-sul', 'planalto'
]

def fetch_cidade(cid):
    url = f"https://empresasriograndedosul.com.br/{cid}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8', 'ignore')
        cnpjs_slugs = re.findall(r'https://empresasriograndedosul\.com\.br/(\d{14})-[a-z0-9-]+', html)
        cnpjs_fmt = re.findall(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', html)
        found = set(cnpjs_slugs)
        for c in cnpjs_fmt:
            clean = re.sub(r'\D', '', c)
            if len(clean) == 14:
                found.add(clean)
        print(f"OK: {cid} -> {len(found)} CNPJs", flush=True)
        return found
    except Exception as e:
        print(f"ERRO: {cid} -> {e}", flush=True)
        return set()

todos = set()
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(fetch_cidade, cidades)
    for res in results:
        todos.update(res)

print(f"\nTOTAL GERAL DE CNPJS COLETADOS: {len(todos)}", flush=True)

with open('scratch/cnpjs_brutos.txt', 'w', encoding='utf-8') as f:
    for c in sorted(todos):
        f.write(c + '\n')
print("Salvo em scratch/cnpjs_brutos.txt", flush=True)
