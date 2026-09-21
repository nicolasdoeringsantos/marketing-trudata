import json
import socket
import urllib.request
import urllib.error
import ssl
import sys
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

DOMINIOS_INVALIDOS = {
    'gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com', 'yahoo.com.br',
    'annex.com.br', 'bol.com.br', 'uol.com.br', 'terra.com.br',
    'sarandi.com.br', 'nonoai.com.br', 'panambi.com.br', 'rondaalta.com.br', 'erechim.com.br'
}

def verificar_url(url):
    if not url or url in ['Não possui site', 'null', None, '-', '']:
        return False, "Vazio / Sem site"
    
    parsed = urlparse(url if '://' in url else 'http://' + url)
    host = parsed.netloc.lower().split(':')[0]
    host_sem_www = host[4:] if host.startswith('www.') else host
    
    if host in DOMINIOS_INVALIDOS or host_sem_www in DOMINIOS_INVALIDOS:
        return False, f"Provedor ou portal genérico ({host})"
    
    try:
        socket.setdefaulttimeout(3)
        socket.gethostbyname(host)
    except Exception as e:
        return False, f"Falha DNS: {host}"
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req_url = url if '://' in url else f"http://{url}"
    req = urllib.request.Request(
        req_url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )

    try:
        with urllib.request.urlopen(req, timeout=3, context=ctx) as resp:
            code = resp.getcode()
            if 200 <= code < 400:
                return True, f"OK ({code})"
            return False, f"Status HTTP {code}"
    except urllib.error.HTTPError as e:
        if e.code in [401, 403]:
            return True, f"Host Ativo ({e.code})"
        return False, f"HTTP Error {e.code}"
    except Exception:
        alt_url = req_url.replace("http://", "https://") if req_url.startswith("http://") else req_url.replace("https://", "http://")
        try:
            req2 = urllib.request.Request(
                alt_url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
            )
            with urllib.request.urlopen(req2, timeout=3, context=ctx) as resp2:
                return True, f"OK Alt ({resp2.getcode()})"
        except Exception as e2:
            return False, f"Conexão Recusada / Timeout"

def processar_lead(lead):
    site_atual = lead.get('site')
    ok, motivo = verificar_url(site_atual)
    return lead, ok, motivo, site_atual

def main():
    print("Iniciando auditoria paralela de websites dos contadores com 20 threads...", flush=True)
    with open('agente/base_clientes_regional.json', 'r', encoding='utf-8') as f:
        leads = json.load(f)

    contab_leads = []
    for l in leads:
        seg = l.get('segmento', '').lower()
        nome = l.get('nome', '').lower()
        if 'contab' in seg or 'contábil' in nome or 'contabilidade' in nome:
            contab_leads.append(l)

    print(f"Total de contabilidades a auditar: {len(contab_leads)}", flush=True)

    with ThreadPoolExecutor(max_workers=20) as executor:
        resultados = list(executor.map(processar_lead, contab_leads))

    validos = 0
    removidos = 0

    for lead, ok, motivo, site_atual in resultados:
        if ok:
            validos += 1
            lead['tem_site'] = True
            lead['status_site'] = 'Site Ativo Verificado'
            print(f"[VALIDO] {lead.get('nome')} ({lead.get('cidade')}) -> {site_atual} ({motivo})", flush=True)
        else:
            if site_atual and site_atual not in ['Não possui site', 'null', None, '-', '']:
                removidos += 1
                print(f"[REMOVIDO] {lead.get('nome')} ({lead.get('cidade')}) -> '{site_atual}' ({motivo})", flush=True)
            lead['tem_site'] = False
            lead['site'] = "Não possui site"
            lead['status_site'] = "Não possui site"

    print("\n" + "="*60, flush=True)
    print(f"Total auditadas: {len(contab_leads)}", flush=True)
    print(f"Sites REAIS comprovados e no ar: {validos}", flush=True)
    print(f"Sites FICTÍCIOS / INVÁLIDOS removidos: {removidos}", flush=True)
    print(f"Contabilidades sem site oficial: {len(contab_leads) - validos}", flush=True)
    print("="*60, flush=True)

    with open('agente/base_clientes_regional.json', 'w', encoding='utf-8') as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)
    print("Salvo com sucesso em 'agente/base_clientes_regional.json'!", flush=True)

if __name__ == '__main__':
    main()
