import os
import re

files_to_check = [
    "painel_aprovacao/dossie_portabilidade.html",
    "painel_aprovacao/proposta_rastreavel.html",
    "painel_aprovacao/gps_campo.html",
    "painel_aprovacao/gerador_reels.html",
    "painel_aprovacao/simulador_tributario_2026.html",
    "painel_aprovacao/index.html",
    "painel_aprovacao/servidor_painel.py"
]

mojibake_patterns = [
    r'Ã¡', r'Ã©', r'Ã­', r'Ã³', r'Ãº', r'Ã£', r'Ãµ', r'Ã§', r'Ãª', r'Ã', r'Â§', r'â€“', r'â€”', r'â€œ', r'â€\x9d', r'ï»¿'
]

print("=== AUDITORIA UTF-8 & MOJIBAKE ===")
erros = 0
for filepath in files_to_check:
    if not os.path.exists(filepath):
        print(f"[ERRO - NÃO ENCONTRADO] {filepath}")
        erros += 1
        continue
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        found = []
        for pat in mojibake_patterns:
            matches = re.findall(pat, content)
            if matches:
                found.append(f"{pat}: {len(matches)}")
        
        if found:
            print(f"[ALERTA MOJIBAKE] {filepath}: {', '.join(found)}")
            erros += 1
        else:
            print(f"[LIMPO UTF-8 100%] {filepath} ({len(content)} caracteres)")
    except Exception as e:
        print(f"[ERRO DE LEITURA] {filepath}: {e}")
        erros += 1

if erros == 0:
    print("\nTODOS OS ARQUIVOS APROVADOS COM UTF-8 PERFEITO!")
else:
    print(f"\nENCONTRADOS {erros} PROBLEMAS.")
