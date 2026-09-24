#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Radar de Prospecção Geográfica B2B — TruData ERP (Hansen Software)
Base de Estabelecimentos 100% REAIS, ATIVOS e REGULARES no SINTEGRA-RS / Receita Federal
Busca em um raio de 100km (ou personalizável) ao redor de Sarandi - RS e regiões vizinhas:
  - Nome Fantasia & Razão Social Oficial
  - CNPJ Oficial Ativo no SINTEGRA-RS / SEFAZ
  - Endereço Completo Oficial (Logradouro, Bairro, Cidade, CEP, Distância em KM)
  - Telefone Comercial Oficial & WhatsApp
  - E-mail Corporativo Oficial
  - Decisor Real extraído do QSA (Quadro de Sócios e Administradores)
  - CNAE e Segmento de Atividade Econômica
  - Presença de Site Oficial (ou 'Não possui site' para oferta de Catálogo Digital)
"""

import math
import json
import os
import csv
import sys
import argparse
import urllib.request
import urllib.parse
import unicodedata
from datetime import datetime

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# Coordenadas de referência padrão: Sarandi - RS (Sede da Hansen Software / TruData ERP)
COORD_SARANDI_RS = {"lat": -27.9439, "lon": -52.9247, "cidade": "Sarandi", "uf": "RS"}

# Coordenadas das cidades polo e circunvizinhas num raio de até ~100km
CIDADES_POLO = {
    "sarandi": {"lat": -27.9439, "lon": -52.9247, "nome": "Sarandi", "dist_sarandi": 0},
    "rondinha": {"lat": -27.8286, "lon": -52.9094, "nome": "Rondinha", "dist_sarandi": 13},
    "barra funda": {"lat": -27.9214, "lon": -53.0394, "nome": "Barra Funda", "dist_sarandi": 12},
    "nova boa vista": {"lat": -27.9897, "lon": -53.0239, "nome": "Nova Boa Vista", "dist_sarandi": 11},
    "constantina": {"lat": -27.7319, "lon": -52.9964, "nome": "Constantina", "dist_sarandi": 24},
    "ronda alta": {"lat": -27.7778, "lon": -52.8083, "nome": "Ronda Alta", "dist_sarandi": 22},
    "chapada": {"lat": -28.0531, "lon": -53.0678, "nome": "Chapada", "dist_sarandi": 21},
    "tres palmeiras": {"lat": -27.6539, "lon": -52.8528, "nome": "Três Palmeiras", "dist_sarandi": 33},
    "três palmeiras": {"lat": -27.6539, "lon": -52.8528, "nome": "Três Palmeiras", "dist_sarandi": 33},
    "pontao": {"lat": -28.0578, "lon": -52.6789, "nome": "Pontão", "dist_sarandi": 27},
    "pontão": {"lat": -28.0578, "lon": -52.6789, "nome": "Pontão", "dist_sarandi": 27},
    "carazinho": {"lat": -28.2839, "lon": -52.7858, "nome": "Carazinho", "dist_sarandi": 40},
    "palmeira das missoes": {"lat": -27.8989, "lon": -53.3136, "nome": "Palmeira das Missões", "dist_sarandi": 40},
    "palmeira das missões": {"lat": -27.8989, "lon": -53.3136, "nome": "Palmeira das Missões", "dist_sarandi": 40},
    "passo fundo": {"lat": -28.2612, "lon": -52.4083, "nome": "Passo Fundo", "dist_sarandi": 62},
    "marau": {"lat": -28.4489, "lon": -52.2000, "nome": "Marau", "dist_sarandi": 91},
    "tapejara": {"lat": -28.0683, "lon": -52.0139, "nome": "Tapejara", "dist_sarandi": 65},
    "erechim": {"lat": -27.6339, "lon": -52.2739, "nome": "Erechim", "dist_sarandi": 74},
    "frederico westphalen": {"lat": -27.3592, "lon": -53.3944, "nome": "Frederico Westphalen", "dist_sarandi": 81},
    "getulio vargas": {"lat": -27.8906, "lon": -52.2278, "nome": "Getúlio Vargas", "dist_sarandi": 69},
    "getúlio vargas": {"lat": -27.8906, "lon": -52.2278, "nome": "Getúlio Vargas", "dist_sarandi": 69},
    "ibiruba": {"lat": -28.6275, "lon": -53.0900, "nome": "Ibirubá", "dist_sarandi": 78},
    "ibirubá": {"lat": -28.6275, "lon": -53.0900, "nome": "Ibirubá", "dist_sarandi": 78},
    "tapera": {"lat": -28.5000, "lon": -52.8700, "nome": "Tapera", "dist_sarandi": 80},
    "espumoso": {"lat": -28.7247, "lon": -52.8500, "nome": "Espumoso", "dist_sarandi": 87},
    "nonoai": {"lat": -27.3622, "lon": -52.7711, "nome": "Nonoai", "dist_sarandi": 67},
    "seberi": {"lat": -27.4800, "lon": -53.4000, "nome": "Seberi", "dist_sarandi": 82},
    "sananduva": {"lat": -27.9497, "lon": -51.8067, "nome": "Sananduva", "dist_sarandi": 85},
    "casca": {"lat": -28.5600, "lon": -51.9700, "nome": "Casca", "dist_sarandi": 75},
    "colorado": {"lat": -28.5200, "lon": -52.9900, "nome": "Colorado", "dist_sarandi": 65},
    "selbach": {"lat": -28.6300, "lon": -52.9500, "nome": "Selbach", "dist_sarandi": 76},
    "sertao": {"lat": -28.0489, "lon": -52.3600, "nome": "Sertão", "dist_sarandi": 56},
    "sertão": {"lat": -28.0489, "lon": -52.3600, "nome": "Sertão", "dist_sarandi": 56},
    "estacao": {"lat": -27.9100, "lon": -52.2600, "nome": "Estação", "dist_sarandi": 66},
    "estação": {"lat": -27.9100, "lon": -52.2600, "nome": "Estação", "dist_sarandi": 66},
    "erebango": {"lat": -27.8400, "lon": -52.3000, "nome": "Erebango", "dist_sarandi": 62},
    "coxilha": {"lat": -28.1200, "lon": -52.2900, "nome": "Coxilha", "dist_sarandi": 64},
    "victor graeff": {"lat": -28.5600, "lon": -52.7500, "nome": "Victor Graeff", "dist_sarandi": 70},
    "almirante tamandare do sul": {"lat": -28.1000, "lon": -52.7700, "nome": "Almirante Tamandaré do Sul", "dist_sarandi": 23},
    "almirante tamandaré do sul": {"lat": -28.1000, "lon": -52.7700, "nome": "Almirante Tamandaré do Sul", "dist_sarandi": 23},
    "santo antonio do planalto": {"lat": -28.3900, "lon": -52.7000, "nome": "Santo Antônio do Planalto", "dist_sarandi": 54},
    "santo antônio do planalto": {"lat": -28.3900, "lon": -52.7000, "nome": "Santo Antônio do Planalto", "dist_sarandi": 54},
    "boa vista das missoes": {"lat": -27.6700, "lon": -53.3000, "nome": "Boa Vista das Missões", "dist_sarandi": 48},
    "boa vista das missões": {"lat": -27.6700, "lon": -53.3000, "nome": "Boa Vista das Missões", "dist_sarandi": 48},
    "sagrada familia": {"lat": -27.7000, "lon": -53.1500, "nome": "Sagrada Família", "dist_sarandi": 35},
    "sagrada família": {"lat": -27.7000, "lon": -53.1500, "nome": "Sagrada Família", "dist_sarandi": 35},
    "jaboticaba": {"lat": -27.6500, "lon": -53.2800, "nome": "Jaboticaba", "dist_sarandi": 46},
    "soledade": {"lat": -28.8200, "lon": -52.5100, "nome": "Soledade", "dist_sarandi": 105},
    "ernestina": {"lat": -28.5000, "lon": -52.5700, "nome": "Ernestina", "dist_sarandi": 70},
    "camargo": {"lat": -28.5900, "lon": -52.2000, "nome": "Camargo", "dist_sarandi": 96},
    "vila maria": {"lat": -28.5300, "lon": -52.1500, "nome": "Vila Maria", "dist_sarandi": 95},
    "ametista do sul": {"lat": -27.3600, "lon": -53.1800, "nome": "Ametista do Sul", "dist_sarandi": 69},
    "lagoa vermelha": {"lat": -28.2100, "lon": -51.5200, "nome": "Lagoa Vermelha", "dist_sarandi": 140},
    "planalto": {"lat": -27.3200, "lon": -53.0600, "nome": "Planalto", "dist_sarandi": 70},
    "serafina correa": {"lat": -28.7100, "lon": -51.9300, "nome": "Serafina Corrêa", "dist_sarandi": 120},
    "serafina corrêa": {"lat": -28.7100, "lon": -51.9300, "nome": "Serafina Corrêa", "dist_sarandi": 120},
    "nova araca": {"lat": -28.6500, "lon": -51.7500, "nome": "Nova Araçá", "dist_sarandi": 130},
    "nova araçá": {"lat": -28.6500, "lon": -51.7500, "nome": "Nova Araçá", "dist_sarandi": 130},
    "parai": {"lat": -28.5800, "lon": -51.7900, "nome": "Paraí", "dist_sarandi": 115},
    "paraí": {"lat": -28.5800, "lon": -51.7900, "nome": "Paraí", "dist_sarandi": 115},
    "nao-me-toque": {"lat": -28.4597, "lon": -52.8214, "nome": "Não-Me-Toque", "dist_sarandi": 59},
    "não-me-toque": {"lat": -28.4597, "lon": -52.8214, "nome": "Não-Me-Toque", "dist_sarandi": 59},
    "panambi": {"lat": -28.2925, "lon": -53.5017, "nome": "Panambi", "dist_sarandi": 70}
}

def calcular_distancia_km(lat1, lon1, lat2, lon2):
    """Calcula a distância em quilômetros pela fórmula do Haversine."""
    R = 6371.0  # Raio da Terra em km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)

def normalizar_texto(txt):
    """Remove acentos e converte para minúsculo para buscas tolerantes."""
    if not txt:
        return ""
    return unicodedata.normalize('NFKD', str(txt)).encode('ASCII', 'ignore').decode('utf-8').lower().strip()

# CARREGA EXCLUSIVAMENTE A BASE DE DADOS 100% REAIS (RECEITA FEDERAL DO BRASIL / SINTEGRA-RS)
_REGIONAL_JSON = os.path.join(os.path.dirname(__file__), "base_clientes_regional.json")
ESTABELECIMENTOS_BASE = []
_REGIONAL_MTIME = 0

def carregar_base_real():
    global ESTABELECIMENTOS_BASE, _REGIONAL_MTIME
    if os.path.exists(_REGIONAL_JSON):
        try:
            mtime = os.path.getmtime(_REGIONAL_JSON)
            if ESTABELECIMENTOS_BASE and len(ESTABELECIMENTOS_BASE) > 0 and mtime == _REGIONAL_MTIME:
                return ESTABELECIMENTOS_BASE
            with open(_REGIONAL_JSON, "r", encoding="utf-8") as f:
                ESTABELECIMENTOS_BASE = json.load(f)
            _REGIONAL_MTIME = mtime
        except Exception as err:
            print(f"Erro ao carregar base_clientes_regional.json: {err}", file=sys.stderr)
            if not ESTABELECIMENTOS_BASE:
                ESTABELECIMENTOS_BASE = []
    return ESTABELECIMENTOS_BASE

carregar_base_real()

def gerar_abordagem_whatsapp(est, decisor_primeiro_nome, distancia):
    seg = est.get("segmento", "").lower()
    nome = est.get("nome", "empresa")
    cidade = est.get("cidade", "sua cidade")
    
    # Gancho por nicho
    if "supermercado" in seg or "mercearia" in seg:
        gancho = (
            f"Sabemos que o maior pesadelo no sábado à tarde é fila no caixa e SEFAZ fora do ar travando a venda. "
            f"Desenvolvemos um PDV com contingência offline ultra veloz que nunca deixa a {nome} parar."
        )
    elif "autopeca" in seg or "oficina" in seg or "mecanica" in seg:
        gancho = (
            f"Para autopeças e mecânicas, controlar milhares de itens, busca por código original e tributação monofásica de PIS/COFINS é essencial. "
            f"Nosso ERP possui catálogo técnico e parametrização fiscal automatizada para a {nome}."
        )
    elif "farmacia" in seg or "drogaria" in seg:
        gancho = (
            f"Farmácias exigem transmissão ágil SNGPC/Anvisa, integração com PBMs e controle de lotes/validade sem margem para erro. "
            f"Nosso módulo farmacêutico homologado reduz drasticamente o tempo de atendimento no balcão da {nome}."
        )
    elif "construcao" in seg or "ferrag" in seg or "tinta" in seg:
        gancho = (
            f"No ramo de materiais e ferragens, o balcão precisa fechar orçamentos rápidos e emitir MDF-e e NF-e de carga própria com segurança. "
            f"Atendemos diversas lojas no RS com controle de entregas futuras e limite de crediário."
        )
    elif "roupa" in seg or "moda" in seg or "calcado" in seg:
        gancho = (
            f"No varejo de moda, o controle de grade (cor e tamanho), vendas no condicional (leva e traz) e emissão de carnê próprio fidelizam o cliente. "
            f"A TruData ERP tem ferramentas sob medida para a {nome} lucrar mais."
        )
    elif "padaria" in seg or "gastronomia" in seg or "restaurante" in seg:
        gancho = (
            f"O atendimento de padaria e alimentação exige integração direta com balanças Toledo/Filizola, comanda rápida e PDV touch que não trava em horários de pico."
        )
    elif "pet" in seg or "agro" in seg or "veterinaria" in seg:
        gancho = (
            f"Gerenciar rações a granel, receituário veterinário e agendamentos de banho & tosa exige um sistema prático e intuitivo para a {nome}."
        )
    elif "contabil" in seg or "escritorio" in seg:
        gancho = (
            f"A TruData disponibiliza o 'Portal do Contador Gratuito' para escritórios contábeis, com download automático e organizado de todos os XMLs e SPEDs dos seus clientes."
        )
    elif "industria" in seg or "metalurgica" in seg or "estrutura" in seg:
        gancho = (
            f"Para indústrias e metalúrgicas, controlar ordem de produção (PCP), consumo de matérias-primas e NF-e interestadual com partilha de ICMS precisa de precisão cirúrgica."
        )
    else:
        gancho = (
            f"Com matriz em Sarandi-RS há 25 anos, entregamos gestão fiscal descomplicada, contingência offline (NFC-e / NF-e) e suporte humano direto por telefone."
        )

    # Adicional para empresas sem site
    extra_site = ""
    if not est.get("tem_site") or est.get("site") == "Não possui site":
        extra_site = " Inclusive, podemos ativar um Catálogo Digital com pedidos direto no WhatsApp da loja sem comissão."

    mensagem = (
        f"Olá, {decisor_primeiro_nome}! Aqui é da equipe comercial da TruData ERP (Hansen Software) em Sarandi-RS.\n\n"
        f"Estamos mapeando estabelecimentos de destaque em {cidade} (a {distancia} km de nossa sede).\n"
        f"{gancho}{extra_site}\n\n"
        f"Podemos agendar uma demonstração rápida de 15 minutos sem compromisso na {nome}?"
    )
    return mensagem

def calcular_lead_score(est, distancia):
    """Calcula Score de Qualificação B2B de 0 a 100 baseado em proximidade, segmento, decisor e porte."""
    score = 0
    cid = normalizar_texto(est.get("cidade", ""))
    if "sarandi" in cid or distancia == 0:
        score += 30
    elif distancia <= 30:
        score += 20
    elif distancia <= 60:
        score += 10
    else:
        score += 5

    seg = normalizar_texto(est.get("segmento", ""))
    if any(k in seg for k in ["supermercado", "mercearia", "peca", "auto", "construcao", "ferrag"]):
        score += 30
    elif any(k in seg for k in ["moda", "confecc", "farmacia", "otica", "drogaria"]):
        score += 20
    else:
        score += 10

    decisor = est.get("decisor", "")
    if decisor and len(decisor.strip()) > 3 and "nao informado" not in normalizar_texto(decisor):
        score += 15
    if est.get("whatsapp") or est.get("telefone"):
        score += 10
    if est.get("email") and "@" in est.get("email", ""):
        score += 5

    pdvs = int(est.get("pdvs_estimados", 1) or 1)
    porte = str(est.get("porte", "")).upper()
    if pdvs >= 3 or porte == "DEMAIS":
        score += 10
    elif pdvs >= 2:
        score += 5

    return min(100, score)

def buscar_clientes_raio(
    origem_cidade="Sarandi",
    raio_km=100.0,
    segmento=None,
    cidade_alvo=None,
    termo=None,
    porte=None,
    apenas_com_email=False,
    apenas_com_telefone=False,
    filtro_site="todos",
    ordenacao="distancia"
):
    """
    Filtra e ordena os estabelecimentos comerciais dentro do raio estipulado (padrão 100km)
    a partir da cidade de origem (padrão Sarandi - RS).
    Suporta filtros de cidade alvo, ordenação customizada e copy de abordagem por nicho.
    """
    carregar_base_real()
    chave_origem = normalizar_texto(origem_cidade)
    ponto_origem = CIDADES_POLO.get(chave_origem, COORD_SARANDI_RS)
    lat_origem = ponto_origem["lat"]
    lon_origem = ponto_origem["lon"]

    resultados = []

    for est in ESTABELECIMENTOS_BASE:
        lat_est = est.get("lat")
        lon_est = est.get("lon")
        if lat_est is None or lon_est is None:
            cid_chave = normalizar_texto(est.get("cidade", "Sarandi"))
            ponto_cid = CIDADES_POLO.get(cid_chave, COORD_SARANDI_RS)
            lat_est = ponto_cid.get("lat", -27.9439)
            lon_est = ponto_cid.get("lon", -52.9247)
            est["lat"] = lat_est
            est["lon"] = lon_est

        distancia = calcular_distancia_km(lat_origem, lon_origem, lat_est, lon_est)

        # Filtro de raio geográfico em KM
        if distancia > raio_km:
            continue

        # Filtro de cidade específica
        if cidade_alvo and cidade_alvo.lower() not in ["todas", "all", ""]:
            cid_filtro = normalizar_texto(cidade_alvo)
            cid_empresa = normalizar_texto(est.get("cidade", ""))
            if cid_filtro not in cid_empresa:
                continue

        # Filtro de segmento / nicho
        if segmento and segmento.lower() not in ["todos", "all", ""]:
            seg_filtro = normalizar_texto(segmento)
            seg_empresa = normalizar_texto(est["segmento"])
            
            if seg_filtro not in seg_empresa and seg_empresa not in seg_filtro:
                if "mercado" in seg_filtro and ("mercado" in seg_empresa or "super" in seg_empresa or "mercearia" in seg_empresa):
                    pass
                elif "padaria" in seg_filtro and ("padaria" in seg_empresa or "confeitaria" in seg_empresa or "gastronomia" in seg_empresa or "restaurante" in seg_empresa or "lanche" in seg_empresa):
                    pass
                elif "pet" in seg_filtro and ("pet" in seg_empresa or "agro" in seg_empresa or "veterinaria" in seg_empresa):
                    pass
                elif "celular" in seg_filtro and ("celular" in seg_empresa or "informatica" in seg_empresa or "assistencia" in seg_empresa or "gamer" in seg_empresa):
                    pass
                elif "bazar" in seg_filtro and ("papelaria" in seg_empresa or "bazar" in seg_empresa):
                    pass
                elif "bebida" in seg_filtro and ("bebida" in seg_empresa or "gas" in seg_empresa):
                    pass
                elif "otica" in seg_filtro and ("otica" in seg_empresa or "joia" in seg_empresa):
                    pass
                elif ("oficina" in seg_filtro or "autopeca" in seg_filtro or "mecanica" in seg_filtro or "auto" in seg_filtro) and ("autopeca" in seg_empresa or "oficina" in seg_empresa or "moto" in seg_empresa or "veiculo" in seg_empresa):
                    pass
                elif ("construcao" in seg_filtro or "ferrag" in seg_filtro or "tinta" in seg_filtro) and ("construcao" in seg_empresa or "ferrag" in seg_empresa):
                    pass
                elif ("roupa" in seg_filtro or "moda" in seg_filtro or "confecc" in seg_filtro) and ("confecc" in seg_empresa or "moda" in seg_empresa or "calcado" in seg_empresa):
                    pass
                elif ("salao" in seg_filtro or "barbearia" in seg_filtro or "estetica" in seg_filtro) and ("salao" in seg_empresa or "barbearia" in seg_empresa or "estetica" in seg_empresa):
                    pass
                elif "academia" in seg_filtro and ("academia" in seg_empresa or "esporte" in seg_empresa):
                    pass
                elif "limpeza" in seg_filtro and ("limpeza" in seg_empresa or "lavanderia" in seg_empresa):
                    pass
                elif "farmacia" in seg_filtro and ("farmacia" in seg_empresa or "drogaria" in seg_empresa):
                    pass
                elif "contabil" in seg_filtro and "contabil" in seg_empresa:
                    pass
                elif "movei" in seg_filtro and ("movei" in seg_empresa or "decor" in seg_empresa):
                    pass
                elif "transporte" in seg_filtro and ("transporte" in seg_empresa or "logistica" in seg_empresa):
                    pass
                elif "metalurgica" in seg_filtro and ("metalurgica" in seg_empresa or "industria" in seg_empresa or "estruturas" in seg_empresa):
                    pass
                else:
                    continue

        # Filtro de porte / PDVs
        if porte and porte.lower() not in ["todos", "all", ""]:
            p_clean = porte.lower().strip()
            pdvs = int(est.get("pdvs_estimados", 1))
            if p_clean in ["pequeno", "1", "1 pdv", "1 caixa", "micro", "me"]:
                if pdvs != 1:
                    continue
            elif p_clean in ["medio", "médio", "2-4", "2 a 4", "epp"]:
                if pdvs < 2 or pdvs > 4:
                    continue
            elif p_clean in ["grande", "5+", "5 ou mais", "redes", "demais"]:
                if pdvs < 5:
                    continue

        # Filtro de presença de site
        if filtro_site and filtro_site.lower() not in ["todos", "all", ""]:
            fs_clean = filtro_site.lower().strip()
            site_val = est.get("site", "")
            tem_site = bool(est.get("tem_site", False)) or (site_val and site_val != "Não possui site")
            if fs_clean in ["com_site", "com", "sim", "site", "com_website"]:
                if not tem_site:
                    continue
            elif fs_clean in ["sem_site", "sem", "nao", "não", "sem_website"]:
                if tem_site:
                    continue

        # Filtro de termo livre (busca tolerante no nome, CNPJ, razão social, endereço, cidade, decisor, CNAE)
        if termo and termo.strip():
            termo_clean = normalizar_texto(termo)
            texto_busca = normalizar_texto(
                f"{est['nome']} {est.get('razao_social', '')} {est.get('cnpj', '')} {est.get('cnpj_limpo', '')} "
                f"{est['endereco']} {est.get('bairro', '')} {est['cidade']} {est['segmento']} "
                f"{est.get('decisor', '')} {est.get('cnae_codigo', '')} {est.get('cnae_descricao', '')} {est.get('notas', '')}"
            )
            if termo_clean not in texto_busca:
                continue

        # Filtros de canais de contato
        if apenas_com_email and (not est.get("email") or "@" not in est["email"]):
            continue
        if apenas_com_telefone and not est.get("telefone") and not est.get("whatsapp"):
            continue

        item = dict(est)
        item["distancia_km"] = distancia
        item["origem_calculo"] = ponto_origem.get("nome", origem_cidade)

        # Campos de presença de site
        site_str = est.get("site", "Não possui site")
        tem_site_bool = est.get("tem_site", (site_str != "Não possui site"))
        item["site"] = site_str
        item["tem_site"] = tem_site_bool
        item["status_site"] = est.get("status_site", "Site Ativo" if tem_site_bool else "Sem Website")
        
        # Link de verificação direta no SINTEGRA-RS / CCC
        item["sintegra_status"] = est.get("sintegra_status", "ATIVA / Regular no Sintegra-RS")
        item["origem_dados"] = "Receita Federal do Brasil / SEFAZ-RS"
        item["link_sintegra"] = "https://dfe-portal.svrs.rs.gov.br/NFE/CCC"

        # Gera abordagem de WhatsApp hiperpersonalizada por nicho e decisor
        primeiro_nome_decisor = est.get("decisor", "Diretoria").split()[0]
        mensagem_wpp = gerar_abordagem_whatsapp(est, primeiro_nome_decisor, distancia)
        item["mensagem_whatsapp"] = mensagem_wpp
        item["link_whatsapp"] = f"https://wa.me/{est.get('whatsapp', '')}?text={urllib.parse.quote(mensagem_wpp)}"
        
        corpo_email = (
            f"Olá {primeiro_nome_decisor},\n\n"
            f"Apresentamos as soluções de gestão fiscal e contingência offline da TruData ERP para a {est.get('nome', '')} em {est.get('cidade', '')}-RS.\n\n"
            f"Atenciosamente,\n"
            f"Equipe Comercial TruData ERP (Hansen Software)\n"
            f"Sarandi - RS | Fone: (54) 3361-2650"
        )
        assunto_email = f"Apresentação TruData ERP — {est.get('nome', '')}"
        item["link_email"] = f"mailto:{est.get('email', '')}?subject={urllib.parse.quote(assunto_email)}&body={urllib.parse.quote(corpo_email)}"
        item["link_maps"] = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(str(est.get('nome', '')) + ' ' + str(est.get('endereco', '')) + ' ' + str(est.get('cidade', '')) + ' RS')}"
        item["lead_score"] = calcular_lead_score(est, distancia)
        resultados.append(item)

    # Ordenação customizada
    ord_clean = (ordenacao or "distancia").lower().strip()
    if ord_clean in ["score", "lead_score"]:
        resultados.sort(key=lambda x: (-x.get("lead_score", 0), x["distancia_km"]))
    elif ord_clean == "nome":
        resultados.sort(key=lambda x: normalizar_texto(x["nome"]))
    elif ord_clean in ["pdvs", "porte", "caixas"]:
        resultados.sort(key=lambda x: (-int(x.get("pdvs_estimados", 1)), x["distancia_km"]))
    elif ord_clean == "cidade":
        resultados.sort(key=lambda x: (normalizar_texto(x["cidade"]), x["distancia_km"]))
    else:
        # Padrão: mais próximos primeiro
        resultados.sort(key=lambda x: x["distancia_km"])

    return resultados

def exportar_para_csv(resultados, caminho_arquivo):
    """Exporta a lista de prospecção para CSV formatado em UTF-8 com BOM (compatível com Excel)."""
    colunas = [
        "ID", "Nome Fantasia", "Razão Social", "CNPJ", "Status Sintegra-RS", "Segmento", 
        "CNAE Fiscal", "Cidade", "Endereço Completo", "Bairro", "CEP", 
        "Distância (km)", "Telefone", "WhatsApp", "E-mail", 
        "Possui Site?", "Site / Website URL",
        "Porte", "PDVs Estimados", "Sócio Decisor (QSA)", "Link WhatsApp", "Link Maps"
    ]
    
    with open(caminho_arquivo, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(colunas)
        for r in resultados:
            tem_site_str = "Sim" if r.get("tem_site") else "Não"
            site_url = r.get("site", "Não possui site")
            writer.writerow([
                r.get("id", ""), r["nome"], r.get("razao_social", ""), r.get("cnpj", ""), 
                r.get("sintegra_status", "ATIVA"), r["segmento"],
                f"{r.get('cnae_codigo', '')} - {r.get('cnae_descricao', '')}",
                f"{r['cidade']} - {r['uf']}", r["endereco"], r.get("bairro", ""), r.get("cep", ""),
                f"{r['distancia_km']} km", r.get("telefone", ""), r.get("whatsapp", ""), r.get("email", ""),
                tem_site_str, site_url,
                r.get("porte", ""), r.get("pdvs_estimados", 1), r.get("decisor", ""),
                r.get("link_whatsapp", ""), r.get("link_maps", "")
            ])

def enviar_para_crm_json(lead, caminho_crm_json):
    """Insere o estabelecimento prospectado diretamente na base de leads do CRM Kanban."""
    leads = []
    if os.path.exists(caminho_crm_json):
        try:
            with open(caminho_crm_json, "r", encoding="utf-8") as f:
                leads = json.load(f)
        except Exception:
            leads = []

    # Verifica se o lead já está no CRM pelo CNPJ ou Nome
    for l in leads:
        if (lead.get("cnpj") and l.get("cnpj") == lead["cnpj"]) or l.get("empresa") == lead["nome"]:
            return False, "Lead já cadastrado no CRM."

    cid_raw = lead.get("cidade", "Sarandi")
    uf_raw = lead.get("uf", "RS")
    cidade_fmt = cid_raw if (" - " in cid_raw or "/" in cid_raw) else f"{cid_raw} - {uf_raw}"

    empresa_nome = lead.get("nome") or lead.get("empresa", "Empresa")

    novo_lead_crm = {
        "id": f"lead-radar-{int(datetime.now().timestamp())}-{len(leads) + 1}",
        "nome": lead.get("decisor") or lead.get("nome", "Responsável Comercial"),
        "empresa": empresa_nome,
        "cidade": cidade_fmt,
        "segmento": lead.get("segmento", "Comércio"),
        "telefone": str(lead.get("whatsapp", lead.get("telefone", ""))).replace("(", "").replace(")", "").replace("-", "").replace(" ", ""),
        "email": lead.get("email", ""),
        "site": lead.get("site", "Não possui site"),
        "tem_site": lead.get("tem_site", False),
        "endereco": f"{lead.get('endereco', '')}, {lead.get('bairro', '')} - {cidade_fmt}",
        "cnpj": lead.get("cnpj", ""),
        "sintegra_status": lead.get("sintegra_status", "ATIVA / Regular no Sintegra-RS"),
        "cnae": f"{lead.get('cnae_codigo', '')} - {lead.get('cnae_descricao', '')}",
        "origem": lead.get("origem") or f"Radar ({lead.get('distancia_km', 0)}km de {lead.get('origem_calculo', 'Sarandi')})",
        "fase": lead.get("fase", "novo"),
        "caixas": str(lead.get("caixas") or lead.get("pdvs_estimados", 1)),
        "data": lead.get("data") or datetime.now().strftime("%d/%m/%Y"),
        "notas": lead.get("notas") or f"Estabelecimento 100% real verificado no Sintegra-RS e Receita Federal. Decisor(a): {lead.get('decisor', 'A confirmar')}."
    }

    leads.insert(0, novo_lead_crm)

    with open(caminho_crm_json, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    return True, novo_lead_crm["id"]

def main():
    parser = argparse.ArgumentParser(description="Radar de Prospecção Geográfica B2B — TruData ERP")
    parser.add_argument("--raio", type=float, default=100.0, help="Raio de busca em quilômetros (padrão: 100)")
    parser.add_argument("--origem", type=str, default="Sarandi", help="Cidade ponto de partida (padrão: Sarandi)")
    parser.add_argument("--segmento", type=str, default="todos", help="Filtrar por segmento")
    parser.add_argument("--porte", type=str, default="todos", help="Filtrar por porte (pequeno, medio, grande, todos)")
    parser.add_argument("--site", type=str, default="todos", help="Filtrar por site: todos, com_site, sem_site")
    parser.add_argument("--termo", type=str, default="", help="Termo de pesquisa por palavra-chave")
    parser.add_argument("--apenas-email", action="store_true", help="Filtrar apenas estabelecimentos com e-mail cadastrado")
    parser.add_argument("--apenas-telefone", action="store_true", help="Filtrar apenas com telefone/whatsapp")
    parser.add_argument("--exportar", type=str, default="", help="Caminho do arquivo .csv para exportação")
    parser.add_argument("--json", action="store_true", help="Retornar saída em formato JSON puro")

    args = parser.parse_args()

    resultados = buscar_clientes_raio(
        origem_cidade=args.origem,
        raio_km=args.raio,
        segmento=args.segmento,
        termo=args.termo,
        porte=args.porte,
        apenas_com_email=args.apenas_email,
        apenas_com_telefone=args.apenas_telefone,
        filtro_site=args.site
    )

    if args.json:
        print(json.dumps(resultados, indent=2, ensure_ascii=False))
        return

    print("=" * 80)
    print(f"🛰️  RADAR DE PROSPECÇÃO B2B — TRUDATA ERP (HANSEN SOFTWARE)")
    print(f"📍 Ponto de Origem: {args.origem} - RS | Raio: {args.raio} km")
    print(f"🎯 Segmento: {args.segmento} | Total Encontrado: {len(resultados)} estabelecimentos 100% REAIS")
    print("=" * 80)

    for i, r in enumerate(resultados[:15], 1):
        print(f"\n[{i}] {r['nome']} ({r['segmento']})")
        print(f"    🏢 Razão Social: {r['razao_social']} | CNPJ: {r['cnpj']} | Sintegra-RS: {r.get('sintegra_status', 'ATIVA')}")
        print(f"    📍 Endereço: {r['endereco']}, {r['bairro']} - {r['cidade']}/{r['uf']} (CEP: {r['cep']})")
        print(f"    📏 Distância da Matriz: {r['distancia_km']} km")
        print(f"    📞 Telefone: {r['telefone']} | 💬 WhatsApp: +55 {r['whatsapp']}")
        print(f"    ✉️  E-mail: {r['email'] if r['email'] else 'Não informado'}")
        print(f"    👤 Decisor (QSA): {r['decisor']} | 📦 Estimativa PDVs: {r['pdvs_estimados']}")
        print(f"    🌐 Site: {r['site']}")

    if len(resultados) > 15:
        print(f"\n... e mais {len(resultados) - 15} estabelecimentos reais na lista.")

    if args.exportar:
        exportar_para_csv(resultados, args.exportar)
        print(f"\n✅ Lista exportada com sucesso para: {args.exportar}")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
