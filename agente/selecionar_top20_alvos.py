import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

BASE_JSON = os.path.join(os.path.dirname(__file__), "base_clientes_regional.json")
with open(BASE_JSON, 'r', encoding='utf-8') as f:
    leads = json.load(f)

segmentos_chave = [
    'Supermercados & Mercearias',
    'Farmácias & Drogarias',
    'Autopeças & Oficinas',
    'Materiais de Construção'
]

alvos = [l for l in leads if l.get('segmento') in segmentos_chave and float(l.get('distancia_km', 999)) <= 30.0]
# Ordena por maior número de PDVs e menor distância da matriz Sarandi
alvos.sort(key=lambda x: (-int(x.get('pdvs_estimados', 1)), float(x.get('distancia_km', 999))))

top20 = alvos[:20]

# Salva arquivo específico de alvos prioritários
output_alvos = os.path.join(os.path.dirname(os.path.dirname(__file__)), "painel_aprovacao", "alvos_prioritarios_piloto.json")
with open(output_alvos, 'w', encoding='utf-8') as f:
    json.dump(top20, f, indent=2, ensure_ascii=False)

print(f"Top 20 alvos selecionados e salvos em: {output_alvos}")
for i, a in enumerate(top20, 1):
    print(f"{i:02d}. {a['nome']} | {a['cidade']} ({a['distancia_km']}km) | {a['segmento']} | {a['pdvs_estimados']} PDVs | {a['decisor']} | Fone: {a['telefone']}")
