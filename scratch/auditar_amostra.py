# -*- coding: utf-8 -*-
import json
import random

data = json.load(open('agente/base_clientes_regional.json', encoding='utf-8'))
random.seed(42)  # Amostra reprodutível
amostra = random.sample(data, 10)

print("=== AMOSTRA DE AUDITORIA (10 ESTABELECIMENTOS 100% REAIS) ===")
for i, item in enumerate(amostra, 1):
    print(f"\n[{i}] {item['nome']} ({item['segmento']})")
    print(f"    Razao Social : {item['razao_social']}")
    print(f"    CNPJ Oficial : {item['cnpj']} (Sintegra: {item['sintegra_status']})")
    print(f"    Municipio    : {item['cidade']} - RS ({item['distancia_km']} km de Sarandi)")
    print(f"    Endereco     : {item['endereco']}, {item['bairro']} (CEP: {item['cep']})")
    print(f"    Socio QSA    : {item['decisor']}")
    print(f"    Telefone     : {item['telefone']}")
    print(f"    CNAE         : {item['cnae_codigo']} - {item['cnae_descricao']}")
    print(f"    Site         : {item['site']}")
