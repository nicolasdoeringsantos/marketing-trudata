import urllib.request
import json

cnpjs_teste = [
    ("93801330000167", "Hipermercado Wagner"),
    ("97322853000181", "Salwipa Auto Peças"),
    ("01559964000137", "Finger Móveis"),
    ("04394568000195", "Biomix"),
    ("90511650000194", "Rembecker Estruturas"),
    ("00104314000134", "Giacomini Pneus"),
    ("00109088000184", "Auto Peças A.B.S."),
    ("00112286000105", "Argenta Contabilidade"),
    ("00123352000134", "Dec's Industria Vestuario"),
    ("89336333000108", "Signomar Bebidas")
]

for c, nome_esperado in cnpjs_teste:
    req = urllib.request.Request(f"https://minhareceita.org/{c}", headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode('iso-8859-1'))
    
    # Decisor do QSA
    qsa = data.get('qsa', [])
    decisores = [s.get('nome_socio') for s in qsa if 'administrador' in s.get('qualificacao_socio', '').lower() or 'titular' in s.get('qualificacao_socio', '').lower() or 'socio' in s.get('qualificacao_socio', '').lower()]
    decisor = decisores[0].title() if decisores else "Diretoria"
    
    # Telefone
    tel1 = data.get('ddd_telefone_1', '')
    
    # Email
    email = data.get('email', '')
    
    # Endereço
    end = f"{data.get('descricao_tipo_de_logradouro', '')} {data.get('logradouro', '')}, {data.get('numero', '')} - {data.get('bairro', '')}"
    
    print(f"--- {c} ---")
    print(f"Razão Social : {data.get('razao_social')}")
    print(f"Fantasia     : {data.get('nome_fantasia')}")
    print(f"Município    : {data.get('municipio')} - {data.get('uf')}")
    print(f"Situação     : {data.get('descricao_situacao_cadastral')}")
    print(f"Endereço     : {end}")
    print(f"Telefone RF  : {tel1}")
    print(f"Email RF     : {email}")
    print(f"Decisor QSA  : {decisor}")
    print(f"CNAE         : {data.get('cnae_fiscal')} - {data.get('cnae_fiscal_descricao')}")
