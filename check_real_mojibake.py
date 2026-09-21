import re

files_to_check = [
    "painel_aprovacao/dossie_portabilidade.html",
    "painel_aprovacao/proposta_rastreavel.html",
    "painel_aprovacao/gps_campo.html",
    "painel_aprovacao/gerador_reels.html",
    "painel_aprovacao/simulador_tributario_2026.html"
]

# Procurando padrões reais de dupla codificação UTF-8 (mojibake)
# onde caracteres como á, é, í, ó, ú, ç, ã foram decodificados como latin1
mojibake_real = [
    'Ã¡', 'Ã©', 'Ã­', 'Ã³', 'Ãº', 'Ã£', 'Ãµ', 'Ã§', 'Ãª', 'Â§', 'â€“', 'â€”', 'â€œ', 'â€\x9d', 'ï»¿'
]

for fpath in files_to_check:
    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    problemas = []
    for num, line in enumerate(lines, 1):
        for moj in mojibake_real:
            if moj in line:
                problemas.append((num, moj, line.strip()[:80]))
    
    if problemas:
        print(f"Problemas em {fpath}:")
        for num, moj, trecho in problemas:
            print(f"  L{num} [{moj}]: {trecho}")
    else:
        print(f"{fpath}: ZERO MOJIBAKE (100% LIMPO)")
