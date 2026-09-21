import urllib.request
import re
import time

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

total_cnpjs = set()
cidades_ok = {}

for cid in cidades:
    url = f"https://empresasriograndedosul.com.br/{cid}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=8).read().decode('utf-8', 'ignore')
        # Procura cnpjs na forma de links com 14 digitos
        cnpjs_slugs = re.findall(r'https://empresasriograndedosul\.com\.br/(\d{14})-[a-z0-9-]+', html)
        # Também procura cnpjs formatados
        cnpjs_fmt = re.findall(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', html)
        
        found = set(cnpjs_slugs)
        for c in cnpjs_fmt:
            clean = re.sub(r'\D', '', c)
            if len(clean) == 14:
                found.add(clean)
                
        cidades_ok[cid] = len(found)
        total_cnpjs.update(found)
        print(f"[{cid}] -> {len(found)} CNPJs encontrados")
    except Exception as e:
        print(f"[{cid}] -> Erro: {e}")
    time.sleep(0.1)

print(f"\nTOTAL CNPJS UNICOS ENCONTRADOS: {len(total_cnpjs)}")
