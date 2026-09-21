#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador da Base Regional Massiva de Estabelecimentos Comerciais (100km Sarandi-RS)
Cobre 44 municípios polo e satélites e 16 nichos de micro, pequenos e médios negócios:
1. Padarias, Confeitarias & Gastronomia (Padarias, Lanchonetes, Pizzarias, Restaurantes, Sorveterias)
2. Pet Shops, Veterinárias & Agropecuárias (Banho & Tosa, Rações, Clínicas, Agropecuárias)
3. Celulares, Informática & Assistência (Conserto de Telas, Acessórios, Games, Redes)
4. Papelarias, Bazares & Variedades (Material Escolar, Bazares de 1,99, Brinquedos, Aviamentos)
5. Distribuidoras de Bebidas, Gás & Conveniências (Tele-Gás, Água, Cervejas, Conveniência 24h)
6. Óticas, Relojoarias & Joalherias (Armações, Óculos de Grau, Relógios, Joias e Semijoias)
7. Móveis, Colchões & Decoração (Móveis Modulados, Colchões, Cortinas, Marcenarias)
8. Autopeças, Oficinas & Motos (Mecânica Leve, Moto Peças, Autoelétricas, Borracharias)
9. Materiais de Construção, Tintas & Ferragens (Tintas, Ferragens, Elétrica, Hidráulica, Vidros)
10. Lojas de Roupas, Calçados & Confecções (Boutiques, Moda Jovem, Moda Íntima, Calçados)
11. Farmácias, Drogarias & Cosméticos (Drogarias, Manipulação, Cosméticos, Suplementos)
12. Supermercados, Minimercados & Fruteiras (Mercadinhos de Bairro, Açougues, Fruteiras)
13. Salões de Beleza, Barbearias & Estética (Cortes Masculinos, Salões, Esmalterias, Estética)
14. Escritórios de Contabilidade & Serviços (Assessoria Fiscal, Auditoria, Perícias, Seguros)
15. Academias, Esportes & Fitness (Musculação, CT Funcional, Suplementos, Artigos Esportivos)
16. Produtos de Limpeza, Lavanderias & Embalagens (Químicos, Lavanderias, Descartáveis)
"""

import json
import os
import math
try:
    from enriquecer_websites import determinar_site_estabelecimento
    from revisar_emails import revisar_email_estabelecimento
except ImportError:
    from agente.enriquecer_websites import determinar_site_estabelecimento
    from agente.revisar_emails import revisar_email_estabelecimento

# Coordenadas reais dos 44 municípios no raio de ~100km ao redor de Sarandi-RS
CIDADES = [
    # Cidades Polo / Centros Maiores (raio 0 a 100km)
    {"nome": "Sarandi", "lat": -27.9439, "lon": -52.9247, "cep": "99560-000", "ddd": "54", "peso": 3},
    {"nome": "Passo Fundo", "lat": -28.2612, "lon": -52.4083, "cep": "99010-000", "ddd": "54", "peso": 4},
    {"nome": "Carazinho", "lat": -28.2839, "lon": -52.7864, "cep": "99500-000", "ddd": "54", "peso": 3},
    {"nome": "Palmeira das Missões", "lat": -27.8986, "lon": -53.3136, "cep": "98300-000", "ddd": "55", "peso": 3},
    {"nome": "Marau", "lat": -28.4489, "lon": -52.2003, "cep": "99150-000", "ddd": "54", "peso": 3},
    {"nome": "Erechim", "lat": -27.6339, "lon": -52.2689, "cep": "99700-000", "ddd": "54", "peso": 3},
    {"nome": "Frederico Westphalen", "lat": -27.3592, "lon": -53.3944, "cep": "98400-000", "ddd": "55", "peso": 3},
    {"nome": "Não-Me-Toque", "lat": -28.4597, "lon": -52.8214, "cep": "99470-000", "ddd": "54", "peso": 2},
    {"nome": "Panambi", "lat": -28.2925, "lon": -53.5017, "cep": "98280-000", "ddd": "55", "peso": 2},
    {"nome": "Tapejara", "lat": -28.0683, "lon": -52.0139, "cep": "99950-000", "ddd": "54", "peso": 2},
    {"nome": "Getúlio Vargas", "lat": -27.8906, "lon": -52.2281, "cep": "99900-000", "ddd": "54", "peso": 2},
    {"nome": "Ibirubá", "lat": -28.6275, "lon": -53.0897, "cep": "98200-000", "ddd": "54", "peso": 2},
    {"nome": "Tapera", "lat": -28.6617, "lon": -52.8683, "cep": "99490-000", "ddd": "54", "peso": 2},
    {"nome": "Espumoso", "lat": -28.7247, "lon": -52.8500, "cep": "99400-000", "ddd": "54", "peso": 2},
    {"nome": "Nonoai", "lat": -27.3581, "lon": -52.7725, "cep": "99600-000", "ddd": "54", "peso": 2},
    {"nome": "Seberi", "lat": -27.4789, "lon": -53.4022, "cep": "98380-000", "ddd": "55", "peso": 2},
    {"nome": "Sananduva", "lat": -27.9497, "lon": -51.8067, "cep": "99840-000", "ddd": "54", "peso": 2},
    {"nome": "Casca", "lat": -28.5622, "lon": -51.9753, "cep": "99260-000", "ddd": "54", "peso": 2},

    # Cidades Satélites & Vizinhas Diretas (raio 10 a 45km)
    {"nome": "Rondinha", "lat": -27.8286, "lon": -52.9097, "cep": "99590-000", "ddd": "54", "peso": 2},
    {"nome": "Barra Funda", "lat": -27.9208, "lon": -53.0397, "cep": "99585-000", "ddd": "54", "peso": 1},
    {"nome": "Nova Boa Vista", "lat": -27.9861, "lon": -53.0181, "cep": "99580-000", "ddd": "54", "peso": 1},
    {"nome": "Constantina", "lat": -27.7347, "lon": -52.9961, "cep": "99680-000", "ddd": "54", "peso": 2},
    {"nome": "Ronda Alta", "lat": -27.7733, "lon": -52.8086, "cep": "99670-000", "ddd": "54", "peso": 2},
    {"nome": "Chapada", "lat": -28.0558, "lon": -53.0694, "cep": "99530-000", "ddd": "54", "peso": 2},
    {"nome": "Pontão", "lat": -28.0583, "lon": -52.6806, "cep": "99190-000", "ddd": "54", "peso": 1},
    {"nome": "Três Palmeiras", "lat": -27.6408, "lon": -52.8553, "cep": "99660-000", "ddd": "54", "peso": 1},
    {"nome": "Engenho Velho", "lat": -27.7039, "lon": -52.8986, "cep": "99690-000", "ddd": "54", "peso": 1},
    {"nome": "Novo Xingu", "lat": -27.6756, "lon": -53.0347, "cep": "99685-000", "ddd": "54", "peso": 1},
    {"nome": "Liberato Salzano", "lat": -27.5956, "lon": -53.0664, "cep": "99695-000", "ddd": "54", "peso": 1},
    {"nome": "Gramado dos Loureiros", "lat": -27.4608, "lon": -52.8028, "cep": "99615-000", "ddd": "54", "peso": 1},
    {"nome": "Sagrada Família", "lat": -27.7028, "lon": -53.1556, "cep": "98340-000", "ddd": "55", "peso": 1},
    {"nome": "São José das Missões", "lat": -27.7850, "lon": -53.1972, "cep": "98325-000", "ddd": "55", "peso": 1},
    {"nome": "Boa Vista das Missões", "lat": -27.6744, "lon": -53.3106, "cep": "98335-000", "ddd": "55", "peso": 1},
    {"nome": "Jaboticaba", "lat": -27.6408, "lon": -53.2844, "cep": "98350-000", "ddd": "55", "peso": 1},
    {"nome": "Almirante Tamandaré do Sul", "lat": -28.1067, "lon": -52.7667, "cep": "99523-000", "ddd": "54", "peso": 1},
    {"nome": "Coqueiros do Sul", "lat": -28.1189, "lon": -52.7844, "cep": "99528-000", "ddd": "54", "peso": 1},
    {"nome": "Santo Antônio do Planalto", "lat": -28.4042, "lon": -52.7306, "cep": "99525-000", "ddd": "54", "peso": 1},
    {"nome": "Victor Graeff", "lat": -28.5606, "lon": -52.7533, "cep": "99390-000", "ddd": "54", "peso": 1},
    {"nome": "Colorado", "lat": -28.5256, "lon": -52.9933, "cep": "99460-000", "ddd": "54", "peso": 1},
    {"nome": "Selbach", "lat": -28.6300, "lon": -52.9533, "cep": "99450-000", "ddd": "54", "peso": 1},
    {"nome": "Coxilha", "lat": -28.1250, "lon": -52.2967, "cep": "99145-000", "ddd": "54", "peso": 1},
    {"nome": "Sertão", "lat": -28.0483, "lon": -52.2611, "cep": "99170-000", "ddd": "54", "peso": 1},
    {"nome": "Ernestina", "lat": -28.4986, "lon": -52.5714, "cep": "99180-000", "ddd": "54", "peso": 1},
    {"nome": "Tio Hugo", "lat": -28.5833, "lon": -52.6000, "cep": "99380-000", "ddd": "54", "peso": 1}
]

# 16 Modelos de Negócios detalhados com foco primário em pequenos negócios (1 PDV / MEI / ME)
MODELOS_NEGOCIOS = [
    # 1. Padarias & Gastronomia
    {
        "segmento": "Padarias & Gastronomia",
        "templates": [
            ("Padaria & Confeitaria Pão Quente", "Panificadora Pão Quente LTDA", "Av. Principal", 1, "Padaria artesanal, pães, cucas e salgados"),
            ("Cafeteria & Bistrô Grão Nobre", "Grão Nobre Cafés EIRELI", "Rua do Comércio", 1, "Cafés especiais, lanches rápidos e doces finos"),
            ("Pizzaria & Lancheria Forno a Lenha", "Forno a Lenha Alimentos LTDA", "Rua Sete de Setembro", 2, "Pizzas artesanais, calzones e tele-entrega"),
            ("Pastelaria & Lanches Ponto Certo", "Ponto Certo Pasteis e Sucos ME", "Av. Brasil", 1, "Pastéis fritos na hora, lanches e sucos naturais"),
            ("Hamburgueria Artesanal Burger House", "Burger House Gastronomia EIRELI", "Rua Independência", 1, "Hambúrgueres artesanais, batatas rústicas e chopp"),
            ("Confeitaria & Doceria Doce Encanto", "Doce Encanto Bolos e Doces LTDA", "Rua Flores da Cunha", 1, "Bolos de aniversário, tortas e docinhos para festas"),
            ("Sorveteria & Açaiteria Tropical", "Tropical Gelatos e Açaí EIRELI", "Praça Central", 1, "Sorvetes artesanais, açaí no copo e picolés"),
            ("Restaurante & Buffet Sabor Gaúcho", "Restaurante Sabor Gaúcho LTDA", "Rua Marechal Deodoro", 2, "Almoço caseiro por quilo e marmitex diário")
        ],
        "decisores": ["Cláudia Bertoncello", "Fábio Mantovani", "Nelci Dal Bosco", "Tiago Pavan", "Luciana Tonial", "Everaldo Silveira"]
    },

    # 2. Pet Shops, Veterinárias & Agropecuárias
    {
        "segmento": "Pet Shops & Agropecuárias",
        "templates": [
            ("Pet Shop & Estética Animal Bichos e Mimos", "Bichos e Mimos Estética Animal ME", "Rua Flores da Cunha", 1, "Banho e tosa, corte de unhas e cosméticos pet"),
            ("Agropecuária & Pet Rações Campeiro", "Agro Campeiro Insumos e Rações LTDA", "Av. Expedicionário", 2, "Rações a granel, botinas, chapéus e sementes"),
            ("Clínica Veterinária & Pet Shop Vida Animal", "Vida Animal Serviços Veterinários LTDA", "Rua Presidente Vargas", 2, "Consultas veterinárias, vacinas, cirurgias e rações premium"),
            ("Casa das Rações & Artigos de Pesca", "Casa das Rações do Sul ME", "Rua 15 de Novembro", 1, "Venda a granel de rações, arreios, anzóis e iscas"),
            ("Hotel & Banho e Tosa Patinhas Felizes", "Patinhas Felizes Cuidados Animais ME", "Rua Morom", 1, "Creche canina, banho e tosa e hotelzinho")
        ],
        "decisores": ["Dr. Rodrigo Zanella (Vet)", "Jéssica Cordeiro", "Mateus Siqueira", "Gilmar Pegoraro", "Dra. Camila Duarte"]
    },

    # 3. Lojas de Celulares, Informática & Assistência
    {
        "segmento": "Celulares, Informática & Assistência",
        "templates": [
            ("SmartCell Conserto de Celulares & Películas", "SmartCell Reparos Rápidos ME", "Rua Júlio de Castilhos", 1, "Troca de telas na hora, baterias, capas e películas 3D"),
            ("Mundo dos Celulares & Eletrônicos", "Mundo Cell Comércio de Acessórios LTDA", "Av. Brasil", 2, "Smartphones novos e seminovos, fones bluetooth e caixas de som"),
            ("Tech Solutions Informática & Gamer", "Tech Solutions Computadores EIRELI", "Rua General Osório", 2, "Montagem de PCs gamers, upgrades de SSD, formatação e redes"),
            ("Hospital do Celular & Tablets", "Hospital do Celular Assistência ME", "Rua Sete de Setembro", 1, "Reparo em placas, conectores de carga e desoxidação"),
            ("Ponto Digital Eletrônicos & Acessórios", "Ponto Digital Comércio Eletrônico LTDA", "Av. Flores da Cunha", 1, "Cabos, carregadores por indução e periféricos para PC")
        ],
        "decisores": ["Felipe Basso", "Lucas Morais", "Vinícius Meneguzzi", "Camila Zanchet", "Diego Trentin"]
    },

    # 4. Papelarias, Bazares & Variedades
    {
        "segmento": "Papelarias, Bazares & Variedades",
        "templates": [
            ("Papelaria & Livraria Estudantil", "Comercial Estudantil de Papéis LTDA", "Rua Morom", 2, "Material escolar, cadernos, mochilas, impressões e xerox"),
            ("Bazar & Utilidades Tem Tudo (R$ 1,99)", "Tem Tudo Comércio de Variedades LTDA", "Av. Flores da Cunha", 2, "Utilidades plásticas, brinquedos, ferramentas manuais e decoração"),
            ("Criativo Bazar Presentes & Brinquedos", "Criativo Bazar EIRELI", "Rua Independência", 1, "Artigos para presentes, embalagens decorativas e lembranças"),
            ("Loja Mega Variedades Popular", "Mega Variedades do Sul LTDA", "Av. Presidente Vargas", 2, "Itens para casa, cozinha, copos, organizadores e bazar"),
            ("Armarinho & Loja de Aviamentos Ponto a Ponto", "Ponto a Ponto Armarinhos ME", "Rua do Comércio", 1, "Linhas, lãs, botões, zíperes, tecidos para artesanato e fitas")
        ],
        "decisores": ["Marilce Scortegagna", "Dionei Fontana", "Renata Bortolini", "Cleusa Albuquerque", "Neusa Zandoná"]
    },

    # 5. Distribuidoras de Bebidas, Gás & Conveniências
    {
        "segmento": "Distribuidoras de Bebidas & Gás",
        "templates": [
            ("Disk Gás & Água Mineral Central", "Central Gás e Distribuição EIRELI", "Rua Coronel Chicuta", 1, "Tele-entrega rápida de botijões P13 e galões de água 20L"),
            ("Distribuidora de Bebidas Geladão", "Geladão Comércio de Bebidas LTDA", "Av. Maurício Cardoso", 2, "Cervejas em fardo e caixa, refrigerantes, gelo e carvão"),
            ("Depósito de Bebidas & Disk Chopp Ponto Certo", "Ponto Certo Bebidas LTDA", "Rua Santo Antônio", 1, "Barril de chopp para eventos, aluguel de chopeira e destilados"),
            ("Adega & Conveniência Noturna 24h", "Adega e Conveniência Noturna LTDA", "Av. Sete de Setembro", 1, "Vinhos, destilados importados, tabacaria, gelo e petiscos"),
            ("Pit Dog & Conveniência de Bebidas", "Pit Dog Distribuidora ME", "Av. Brasil Oeste", 1, "Bebidas trincando de geladas, salgadinhos e carvão para churrasco")
        ],
        "decisores": ["Valdir Romani", "Alexandre Pozzer", "Émerson Dall Agnol", "Leandro Carra", "Cristiano Fontana"]
    },

    # 6. Óticas, Relojoarias & Joalherias
    {
        "segmento": "Óticas & Joalherias",
        "templates": [
            ("Ótica Visão Cristalina", "Ótica Cristalina Comércio Óptico LTDA", "Rua Capitão Eleutério", 2, "Exame computadorizado, lentes multifocais e armações de grau"),
            ("Relojoaria & Ótica Suíça", "Relojoaria Suíça de Precisão EIRELI", "Av. Brasil Oeste", 1, "Conserto de relógios de pulso, troca de baterias e alianças de ouro"),
            ("Ótica & Joias do Vale", "Joalheria e Ótica do Vale LTDA", "Rua Marechal Floriano", 2, "Óculos solares esportivos, semijoias com garantia e relógios"),
            ("Espaço Óptico & Relógios Elegance", "Elegance Óptica e Acessórios ME", "Rua Morom", 1, "Lentes fotossensíveis, armações leves em titânio e acetato")
        ],
        "decisores": ["Geraldo Tonetto", "Viviane Miorando", "Celson Chagas", "Fabiane Bortoluzzi"]
    },

    # 7. Móveis, Colchões & Decoração
    {
        "segmento": "Móveis & Decoração",
        "templates": [
            ("Móveis & Estofados Conforto", "Conforto Comércio de Móveis LTDA", "Av. Presidente Vargas", 2, "Sofás retráteis, mesas de jantar, quartos e salas completas"),
            ("Espaço dos Colchões Sono Bom", "Sono Bom Comércio de Colchões EIRELI", "Rua Fagundes dos Reis", 1, "Colchões ortopédicos de molas ensacadas, camas box e travesseiros"),
            ("Decorações Bella Casa, Cortinas & Tapetes", "Bella Casa Artigos Têxteis LTDA", "Rua Morom", 1, "Cortinas sob medida, persianas, papéis de parede e almofadas"),
            ("Marcenaria & Móveis Planejados Sob Medida", "Planejados Arte em Madeira ME", "Distrito Industrial", 1, "Cozinhas planejadas, closets e painéis de TV sob encomenda")
        ],
        "decisores": ["Paulo Sérgio Gheller", "Marta Vanzin", "Clóvis Somavilla", "Gilmar Censi"]
    },

    # 8. Autopeças, Oficinas & Mecânicas de Motos
    {
        "segmento": "Autopeças & Oficinas",
        "templates": [
            ("Moto Peças & Oficina Duas Rodas", "Duas Rodas Serviços e Peças EIRELI", "Rua Bento Gonçalves", 2, "Revisão geral de motos, troca de óleo, pneus e capacetes"),
            ("Bicicletaria & Bike Shop Sul", "Bike Shop Sul Comércio e Reparos LTDA", "Rua Tiradentes", 1, "Bicicletas MTB, marchas Shimano, regulagem e acessórios"),
            ("Autoelétrica & Baterias São Jorge", "Autoelétrica São Jorge de Serviços LTDA", "Rua XV de Novembro", 2, "Troca de baterias Heliar/Moura, alternadores e motores de arranque"),
            ("Centro Automotivo & Troca de Óleo Rápida", "Centro Automotivo Lubri Express ME", "Av. Brasil", 1, "Filtros de óleo e ar, pastilhas de freio e alinhamento a laser"),
            ("Borracharia & Geometria 24 Horas", "Borracharia Pneu Forte ME", "RS-324, Trevo", 1, "Vulcanização de pneus, balanceamento, conserto de furos e rodas"),
            ("Oficina Mecânica & Injeção Eletrônica Gaúcha", "Mecânica Gaúcha de Motores LTDA", "Rua dos Imigrantes", 2, "Scanner de injeção, cabeçotes, suspensão e freios ABS")
        ],
        "decisores": ["Marciano Perin", "Danilo Grotto", "Sandro Fachinetto", "Dirceu Tedesco", "Adilson Marcon", "César Dal Moro"]
    },

    # 9. Materiais de Construção, Tintas & Ferragens
    {
        "segmento": "Materiais de Construção",
        "templates": [
            ("Mundo das Tintas & Texturas", "Mundo das Tintas Comércio Varejista LTDA", "Av. Brasil", 2, "Tintas imobiliárias Coral/Suvinil, resinas, trinchas e rolos"),
            ("Casa Elétrica & Iluminação LED", "Casa Elétrica Materiais e Serviços LTDA", "Rua Uruguai", 2, "Fios antichama, disjuntores, painéis LED, lustres e tomadas"),
            ("Ferragens & Ferramentas São Pedro", "Comercial São Pedro de Ferragens LTDA", "Rua Paissandu", 2, "Furadeiras, parafusos, fechaduras, dobradiças e discos de corte"),
            ("Hidráulica & Acabamentos D'Água", "D'Água Materiais Hidráulicos ME", "Rua 20 de Setembro", 1, "Tubos e conexões Tigre, torneiras metálicas, caixas d'água e registros"),
            ("Vidraçaria & Box de Vidro Temperado", "Cristal Vidros e Molduras ME", "Av. Presidente Vargas", 1, "Box Blindex para banheiro, espelhos lapidados e sacadas de vidro")
        ],
        "decisores": ["Everton Battisti", "Valmor Dalla Rosa", "Milton Sebben", "Clécio Zardo", "Evandro Pegoraro"]
    },

    # 10. Lojas de Roupas, Calçados & Confecções
    {
        "segmento": "Lojas de Confecções & Moda",
        "templates": [
            ("Boutique Charme & Moda Feminina", "Charme Boutique e Moda Íntima LTDA", "Rua do Comércio", 1, "Moda feminina casual, calças jeans, blusas e vestidos de festa"),
            ("Sapataria & Calçados Passos Firmes", "Passos Firmes Comércio Calçadista LTDA", "Av. Central", 2, "Tênis esportivos Olympikus/Nike, sapatos sociais e botas"),
            ("Moda Jovem & Streetwear Skate Shop", "Urban Streetwear Comércio de Roupas EIRELI", "Rua Sete de Setembro", 1, "Camisetas over, bonés, bermudas jeans e moletons com capuz"),
            ("Loja Infantil Bebê Sonho Colorido", "Sonho Colorido Artigos Infantis LTDA", "Rua 20 de Setembro", 1, "Moda infantil do RN ao 16, bodies de algodão e brinquedos"),
            ("Loja de Moda Íntima, Lingerie & Pijamas", "Segredo Íntimo Lingerie ME", "Rua Bento Gonçalves", 1, "Sutiãs reforçados, calcinhas de renda, pijamas e moda praia"),
            ("Confecções & Moda Masculina Estilo", "Estilo Moda Homem Comércio LTDA", "Av. Flores da Cunha", 2, "Camisas polo, camisas sociais sob medida, ternos e cintos de couro")
        ],
        "decisores": ["Carla Meneghetti", "Aline Trentin", "Gabriel De Bastiani", "Silvana Cadorin", "Rafael Rigo", "Vanessa Peruzzo"]
    },

    # 11. Farmácias, Drogarias & Cosméticos
    {
        "segmento": "Farmácias & Drogarias",
        "templates": [
            ("Farmácia Bem Estar & Saúde Popular", "Drogaria Bem Estar do Rio Grande LTDA", "Av. Brasil", 2, "Medicamentos genéricos com desconto, fraldas e primeiros socorros"),
            ("Farmácia de Manipulação Fórmula Natural", "Fórmula Natural Manipulações LTDA", "Rua Morom", 2, "Fórmulas médicas dermatológicas, fitoterápicos e florais"),
            ("Drogaria Nova Esperança", "Nova Esperança Medicamentos EIRELI", "Rua Independência", 1, "Medicamentos de uso contínuo, aferição de pressão e perfumaria"),
            ("Perfumaria, Cosméticos & Maquiagens Glamour", "Glamour Casa de Cosméticos LTDA", "Av. Central", 1, "Linhas profissionais para cabelo, secadores, maquiagens e esmaltes"),
            ("Empório Natural & Suplementos Vida Leve", "Vida Leve Produtos Naturais ME", "Rua Sete de Setembro", 1, "Chás a granel, farinhas integrais, whey protein e creatina")
        ],
        "decisores": ["Dra. Patrícia Dalla Lana", "Dr. Fabiano Rossetto", "Elizete Marcon", "Cíntia Pires", "Rodrigo Bresolin"]
    },

    # 12. Supermercados, Minimercados, Açougues & Fruteiras
    {
        "segmento": "Supermercados & Mercearias",
        "templates": [
            ("Minimercado da Família & Padaria de Bairro", "Minimercado da Família LTDA", "Rua dos Imigrantes", 2, "Alimentos de cesta básica, fatiamento de queijos e pão francês"),
            ("Açougue & Casa de Carnes Boi Gordo", "Boi Gordo Carnes Nobres EIRELI", "Av. Sete de Setembro", 2, "Cortes especiais para churrasco, linguiça campeira e costela"),
            ("Fruteira & Hortifrúti Da Horta Fresquinho", "Da Horta Comércio de Frutas LTDA", "Rua Marechal Floriano", 1, "Frutas da estação, verduras colhidas no dia e legumes lavados"),
            ("Mercado & Armazém Colonial do Sul", "Armazém Colonial de Alimentos LTDA", "Rua São Pedro", 2, "Queijo colonial, salames, chimarrão, erva-mate e compotas doces"),
            ("Mercearia & Varejão Bom Preço", "Bom Preço Mercearia de Alimentos ME", "Rua XV de Novembro", 1, "Gêneros alimentícios, produtos de higiene pessoal e limpeza")
        ],
        "decisores": ["Gilmar Spagnol", "Darci Zanrosso", "Vanderlei Moretto", "Leonir Dalberto", "Altair Scariot"]
    },

    # 13. Salões de Beleza, Barbearias & Estética
    {
        "segmento": "Salões, Barbearias & Estética",
        "templates": [
            ("Barbearia Tradicional & Clube da Navalha", "Clube da Navalha Barbearia EIRELI", "Rua Central", 1, "Cortes masculinos na tesoura, degradê, barba toalha quente e pomadas"),
            ("Espaço Beleza & Salão Bella Mulher", "Bella Mulher Salão e Cosméticos LTDA", "Rua Bento Gonçalves", 1, "Escova progressiva, mechas loiras, manicure/pedicure e penteados"),
            ("Esmalteria & Spa dos Pés Unhas de Luxo", "Unhas de Luxo Esmalteria ME", "Rua Flores da Cunha", 1, "Alongamento em fibra de vidro, gel e cutilagem russa"),
            ("Clínica de Estética & Sobrancelhas Harmonia", "Harmonia Estética Facial ME", "Av. Brasil", 1, "Design de sobrancelhas, limpeza de pele profunda e depilação a laser")
        ],
        "decisores": ["Matheus Silveira", "Giseli Bressan", "Tatiana Fornari", "Priscila Zanchett"]
    },

    # 14. Escritórios Contábeis & Serviços B2B
    {
        "segmento": "Escritórios de Contabilidade",
        "templates": [
            ("Assessoria Contábil Integrada", "Integrada Serviços Contábeis e Fiscais SS", "Rua Capitão Eleutério", 1, "Escrituração contábil, folha de pagamento, cálculo de ICMS e SPED"),
            ("Escritório Contábil Progresso Rural & Urbano", "Progresso Contabilidade e Gestão SS", "Av. Flores da Cunha", 1, "Abertura de empresas, assessoria fiscal para produtores e MEIs"),
            ("Exata Contabilidade & Consultoria Tributária", "Exata Assessoria Empresarial LTDA", "Rua General Netto", 1, "Planejamento tributário, recuperação de tributos e BPO financeiro"),
            ("Corretora de Seguros Pampa Forte", "Pampa Forte Corretora de Seguros EIRELI", "Rua Morom", 1, "Seguro empresarial para comércio, seguro de frota de veículos e vida")
        ],
        "decisores": ["Gilberto Zanin (Contador)", "Dra. Sandra Pegoraro", "Maurício Tomasi", "Renan Cenci"]
    },

    # 15. Academias, Esportes & Fitness
    {
        "segmento": "Academias & Artigos Esportivos",
        "templates": [
            ("Academia Iron Fitness & Musculação", "Iron Fitness Centro de Treinamento LTDA", "Av. Brasil", 2, "Aparelhos de musculação modernos, esteiras, spinning e personal trainer"),
            ("Centro de Treinamento Funcional & CrossBox", "CrossBox Treinamento Funcional ME", "Rua Independência", 1, "Aulas de condicionamento físico em grupo, mobilidade e levantamento de peso"),
            ("Loja de Artigos Esportivos & Suplementos Campeão", "Campeão Artigos Esportivos LTDA", "Rua Morom", 1, "Tênis esportivos, kimonos, bolas de futebol, luvas e creatina pura")
        ],
        "decisores": ["Prof. Eduardo Fachin", "Marcelo Rossi", "Diego Casagrande"]
    },

    # 16. Produtos de Limpeza, Lavanderias & Embalagens
    {
        "segmento": "Limpeza, Lavanderias & Embalagens",
        "templates": [
            ("Casa da Limpeza & Produtos Químicos", "Casa da Limpeza Distribuidora LTDA", "Av. Expedicionário", 1, "Desinfetantes em galão, sabão líquido para roupas, ceras e rodos"),
            ("Lavanderia Express & Lavagem a Seco", "Lavanderia Express do Sul ME", "Rua Sete de Setembro", 1, "Lavagem de edredons, ternos, vestidos de festa e tapetes"),
            ("Distribuidora de Embalagens & Descartáveis Práticos", "Práticos Embalagens Comerciais LTDA", "Av. Flores da Cunha", 2, "Sacolas plásticas, marmitex de isopor, copos descartáveis e bobinas térmicas")
        ],
        "decisores": ["Vilmar Biazus", "Sirlei Zanella", "Marcos Antônio Dall Agnol"]
    }
]

def gerar_cnpj_ficticio(idx):
    base1 = 10 + (idx % 80)
    base2 = 100 + (idx * 3 % 899)
    base3 = 100 + (idx * 7 % 899)
    filial = "0001"
    dv = 10 + (idx % 89)
    return f"{base1:02d}.{base2:03d}.{base3:03d}/{filial}-{dv:02d}"

def gerar_telefone(ddd, idx):
    num = 3300 + (idx * 17 % 6500)
    return f"({ddd}) {num // 100:02d}{num % 100:02d}-{1000 + (idx * 31 % 8999)}"

def gerar_whatsapp(ddd, idx):
    num = 99000000 + (idx * 7919 % 999999)
    return f"{ddd}{num}"

def gerar_email(nome_fantasia, cidade):
    clean_nome = "".join(c for c in nome_fantasia.lower().replace(" ", "").replace("&", "") if c.isalnum())[:13]
    clean_cid = "".join(c for c in cidade.lower().replace(" ", "").replace("-", "") if c.isalnum())[:8]
    dominios = ["com.br", "gmail.com", "contato.com.br", "far.br"]
    dom = dominios[len(clean_nome) % len(dominios)]
    if "gmail" in dom:
        return f"{clean_nome}.{clean_cid}@gmail.com"
    return f"contato@{clean_nome}.{dom}"

def main():
    print("Iniciando geração massiva da base regional de clientes B2B (100km ao redor de Sarandi-RS)...")

    todos_estabelecimentos = []
    global_id = 1

    # Percorre cada município do raio de 100km
    for cid in CIDADES:
        cidade_nome = cid["nome"]
        lat_base = cid["lat"]
        lon_base = cid["lon"]
        cep = cid["cep"]
        ddd = cid["ddd"]
        peso = cid.get("peso", 1)

        # Para cada grupo/nicho de negócios
        for grupo in MODELOS_NEGOCIOS:
            segmento = grupo["segmento"]
            templates = grupo["templates"]
            decisores = grupo["decisores"]

            # Define quantos estabelecimentos desse nicho colocar nesta cidade
            # Cidades de peso 3 ou 4 terão múltiplos (2 a 3) estabelecimentos por nicho
            # Cidades menores terão 1 estabelecimento por nicho
            qtd_a_gerar = min(peso, len(templates))
            if peso == 1 and (global_id % 3 == 0):
                # Para cidades muito pequenas, nem todo nicho tem filial, mas a maioria sim
                qtd_a_gerar = 1

            for i in range(qtd_a_gerar):
                tpl = templates[i % len(templates)]
                nome_base, razao_base, rua_base, pdvs, resumo = tpl
                decisor = decisores[(i + global_id) % len(decisores)]

                num_predio = 20 + (global_id * 37 % 1900)
                endereco_completo = f"{rua_base}, {num_predio}"
                bairros_opcoes = ["Centro", "Bairro São Cristóvão", "Bairro Industrial", "Vila Nova", "Bairro Santa Gema", "Bairro Operário"]
                bairro = bairros_opcoes[global_id % len(bairros_opcoes)]

                # Variação sutil de coordenadas geográficas dentro do município
                delta_lat = ((global_id * 13 % 100) - 50) * 0.00035
                delta_lon = ((global_id * 17 % 100) - 50) * 0.00035

                cnpj = gerar_cnpj_ficticio(global_id)
                telefone = gerar_telefone(ddd, global_id)
                whatsapp = gerar_whatsapp(ddd, global_id)
                email = gerar_email(nome_base, cidade_nome)

                item = {
                    "id": f"lead-reg-{global_id:04d}",
                    "nome": f"{nome_base} - {cidade_nome}",
                    "razao_social": f"{razao_base}",
                    "cnpj": cnpj,
                    "endereco": endereco_completo,
                    "bairro": bairro,
                    "cidade": cidade_nome,
                    "uf": "RS",
                    "cep": cep,
                    "telefone": telefone,
                    "whatsapp": whatsapp,
                    "email": email,
                    "segmento": segmento,
                    "pdvs_estimados": pdvs,
                    "decisor": decisor,
                    "notas": resumo,
                    "lat": round(lat_base + delta_lat, 5),
                    "lon": round(lon_base + delta_lon, 5)
                }

                url_site, tem_site, status_site = determinar_site_estabelecimento(item, seed_id=global_id)
                item["site"] = url_site
                item["tem_site"] = tem_site
                item["status_site"] = status_site

                rev_email = revisar_email_estabelecimento(item, global_id)
                item["email"] = rev_email["email"]
                item["email_secundario"] = rev_email["email_secundario"]
                item["tipo_email"] = rev_email["tipo_email"]

                todos_estabelecimentos.append(item)
                global_id += 1

    print(f"Total de estabelecimentos comerciais criados na base regional: {len(todos_estabelecimentos)}")
    cidades_unicas = set(e["cidade"] for e in todos_estabelecimentos)
    segmentos_unicos = set(e["segmento"] for e in todos_estabelecimentos)
    print(f"Cidades cobertas: {len(cidades_unicas)}")
    print(f"Segmentos/Nichos cobertos: {len(segmentos_unicos)}")

    # Salva em JSON
    output_path = os.path.join(os.path.dirname(__file__), "base_clientes_regional.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(todos_estabelecimentos, f, indent=2, ensure_ascii=False)

    print(f"Arquivo gerado com sucesso em: {output_path}")

if __name__ == "__main__":
    main()
