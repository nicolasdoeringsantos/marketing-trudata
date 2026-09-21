#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Correção e Limpeza Definitiva de Caracteres Corrompidos (Mojibake)
Converte todas as escritas distorcidas (como 'ComÃ©rcio', 'peÃ§as', 'acessÃ³rios', 'veÃ­culos')
para o português brasileiro correto ('Comércio', 'peças', 'acessórios', 'veículos')
em base_clientes_regional.json e clientes_prospeccao_real.csv.
"""

import json
import os
import re
import sys
import csv

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
BASE_JSON = os.path.join(BASE_DIR, "base_clientes_regional.json")
CSV_PATH = os.path.join(PROJECT_ROOT, "painel_aprovacao", "clientes_prospeccao_real.csv")

# Tabela manual de substituição para casos especiais ou fallbacks
SUBSTITUICOES_DIRETAS = {
    "ComÃ©rcio": "Comércio",
    "comÃ©rcio": "comércio",
    "veÃ­culos": "veículos",
    "VeÃ­culos": "Veículos",
    "veÃculos": "veículos",
    "VeÃculos": "Veículos",
    "peÃ§as": "peças",
    "PeÃ§as": "Peças",
    "acessÃ³rios": "acessórios",
    "AcessÃ³rios": "Acessórios",
    "manutenÃ§Ã£o": "manutenção",
    "reparaÃ§Ã£o": "reparação",
    "mecÃ¢nica": "mecânica",
    "edifÃ­cios": "edifícios",
    "edifÃcios": "edifícios",
    "FabricaÃ§Ã£o": "Fabricação",
    "fabricaÃ§Ã£o": "fabricação",
    "ServiÃ§os": "Serviços",
    "serviÃ§os": "serviços",
    "FormaÃ§Ã£o": "Formação",
    "formaÃ§Ã£o": "formação",
    "imÃ³veis": "imóveis",
    "prÃ³prios": "próprios",
    "ConfecÃ§Ã£o": "Confecção",
    "confecÃ§Ã£o": "confecção",
    "vestuÃ¡rio": "vestuário",
    "Ã­ntimas": "íntimas",
    "Ãntimas": "íntimas",
    "instituiÃ§Ãµes": "instituições",
    "nÃ£o-financeiras": "não-financeiras",
    "farmacÃªuticos": "farmacêuticos",
    "manipulaÃ§Ã£o": "manipulação",
    "fÃ³rmulas": "fórmulas",
    "mÃ³veis": "móveis",
    "predominÃ¢ncia": "predominância",
    "automÃ³veis": "automóveis",
    "utilitÃ¡rios": "utilitários",
    "alimentÃ­cios": "alimentícios",
    "alimentÃcios": "alimentícios",
    "mÃ¡quinas": "máquinas",
    "mineraÃ§Ã£o": "mineração",
    "construÃ§Ã£o": "construção",
    "metÃ¡licas": "metálicas",
    "combustÃ­veis": "combustíveis",
    "combustÃveis": "combustíveis",
    "rodoviÃ¡rio": "rodoviário",
    "mudanÃ§as": "mudanças",
    "aÃ§ougues": "açougues",
    "aÃ§Ãºcar": "açúcar",
    "eletrodomÃ©sticos": "eletrodomésticos",
    "Ã¡udio": "áudio",
    "vÃ­deo": "vídeo",
    "vÃdeo": "vídeo",
    "laticÃ­nios": "laticínios",
    "laticÃnios": "laticínios",
    "panificaÃ§Ã£o": "panificação",
    "agrÃ­colas": "agrícolas",
    "agrÃcolas": "agrícolas",
    "liqÃ¼efeito": "liquefeito",
    "petrÃ³leo": "petróleo",
    "Ã³ptica": "óptica",
    "artÃ­stica": "artística",
    "audiovisuais": "audiovisuais",
    "promoÃ§Ã£o": "promoção",
    "instalaÃ§Ã£o": "instalação",
    "clÃ­nicas": "clínicas",
    "mÃ©dicas": "médicas",
    "odontolÃ³gicas": "odontológicas",
    "veterinÃ¡rias": "veterinárias",
    "distribuiÃ§Ã£o": "distribuição",
    "refrigeraÃ§Ã£o": "refrigeração",
    "comunicaÃ§Ã£o": "comunicação",
    "seguranÃ§a": "segurança",
    "limpeza": "limpeza",
    "educaÃ§Ã£o": "educação",
    "ensino": "ensino",
    "publicaÃ§Ã£o": "publicação",
    "ediÃ§Ã£o": "edição",
    "impressÃ£o": "impressão",
    "gravaÃ§Ã£o": "gravação",
    "locaÃ§Ã£o": "locação",
    "reparaÃ§Ã£o": "reparação",
    "manutenÃ§Ã£o": "manutenção",
    "PrestaÃ§Ã£o": "Prestação",
    "prestaÃ§Ã£o": "prestação"
}

def corrigir_texto(texto):
    if not isinstance(texto, str):
        return texto
    
    # Verifica se há indícios de mojibake UTF-8 decodificado como latin1
    padroes_mojibake = ['Ã©', 'Ã§', 'Ã£', 'Ã³', 'Ã¡', 'Ã\xad', 'Ãª', 'Ã¢', 'Ãµ', 'Ãº', 'Ã‰', 'Ã‡', 'Ãƒ', 'Ã“', 'Ã\xa0', 'Âº', 'Âª', 'Ã', 'Â']
    if not any(p in texto for p in padroes_mojibake):
        return texto

    # Tentativa 1: Inversão matemática padrão latin1 -> utf-8
    try:
        corrigido = texto.encode('latin1').decode('utf-8')
        return corrigido
    except Exception:
        pass

    # Tentativa 2: Dicionário de termos frequentes
    res = texto
    for k, v in SUBSTITUICOES_DIRETAS.items():
        res = res.replace(k, v)
    
    # Tentativa 3: Substituição de sequências residuais
    res = res.replace('Ã©', 'é').replace('Ã§', 'ç').replace('Ã£', 'ã').replace('Ã³', 'ó')
    res = res.replace('Ã¡', 'á').replace('Ã­', 'í').replace('Ãª', 'ê').replace('Ã¢', 'â')
    res = res.replace('Ãµ', 'õ').replace('Ãº', 'ú').replace('Ã‰', 'É').replace('Ã‡', 'Ç')
    res = res.replace('Ãƒ', 'Ã').replace('Ã“', 'Ó').replace('Ã\xa0', 'à').replace('Âº', 'º')
    res = res.replace('Âª', 'ª').replace('Â°', '°')
    
    return res

def processar_base():
    print(f"Lendo base em: {BASE_JSON}")
    with open(BASE_JSON, "r", encoding="utf-8") as f:
        leads = json.load(f)

    total_alterados = 0
    total_campos_alterados = 0

    for l in leads:
        lead_alterado = False
        for k, v in list(l.items()):
            if isinstance(v, str):
                novo_v = corrigir_texto(v)
                if novo_v != v:
                    l[k] = novo_v
                    total_campos_alterados += 1
                    lead_alterado = True
        if lead_alterado:
            total_alterados += 1

    with open(BASE_JSON, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2, ensure_ascii=False)

    print(f"Sucesso em base_clientes_regional.json:")
    print(f"  • Leads corrigidos: {total_alterados}")
    print(f"  • Total de campos de texto corrigidos: {total_campos_alterados}")

    # Regenera o CSV com os textos 100% corretos
    colunas = [
        "ID", "Nome Fantasia", "Razão Social", "CNPJ", "Status Sintegra-RS", "Segmento", 
        "CNAE Fiscal", "Cidade", "Endereço Completo", "Bairro", "CEP", 
        "Distância (km)", "Telefone", "WhatsApp", "E-mail", 
        "Possui Site?", "Site / Website URL",
        "Porte", "PDVs Estimados", "Sócio Decisor (QSA)", "Link WhatsApp", "Link Maps"
    ]

    with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(colunas)
        for r in leads:
            tem_site_str = "Sim" if r.get("tem_site") else "Não"
            site_url = r.get("site", "Não possui site")
            writer.writerow([
                r.get("id", ""), r.get("nome", ""), r.get("razao_social", ""), r.get("cnpj", ""), 
                r.get("sintegra_status", "ATIVA / Regular no Sintegra-RS"), r.get("segmento", ""),
                f"{r.get('cnae_codigo', '')} - {r.get('cnae_descricao', '')}",
                f"{r.get('cidade', '')} - {r.get('uf', 'RS')}", r.get("endereco", ""), r.get("bairro", ""), r.get("cep", ""),
                f"{r.get('distancia_km', 0.0)} km", r.get("telefone", ""), r.get("whatsapp", ""), r.get("email", ""),
                tem_site_str, site_url,
                r.get("porte", ""), r.get("pdvs_estimados", 1), r.get("decisor", ""),
                r.get("link_whatsapp", ""), r.get("link_maps", "")
            ])

    print(f"Sucesso em clientes_prospeccao_real.csv: planilha regenerada em UTF-8-sig.")

    # Também checa leads_crm.json se houver algum campo afetado
    crm_json = os.path.join(PROJECT_ROOT, "painel_aprovacao", "leads_crm.json")
    if os.path.exists(crm_json):
        with open(crm_json, "r", encoding="utf-8") as f:
            crm_leads = json.load(f)
        crm_alterados = 0
        for item in crm_leads:
            for k, v in list(item.items()):
                if isinstance(v, str):
                    novo = corrigir_texto(v)
                    if novo != v:
                        item[k] = novo
                        crm_alterados += 1
        with open(crm_json, "w", encoding="utf-8") as f:
            json.dump(crm_leads, f, indent=2, ensure_ascii=False)
        print(f"Sucesso em leads_crm.json: {crm_alterados} campos corrigidos.")

if __name__ == "__main__":
    processar_base()
