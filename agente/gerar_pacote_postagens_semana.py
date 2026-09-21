import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

POSTS_SEMANA = [
    {
        "id": "post-2026-09-18",
        "data": "18/09/2026 (Sexta-feira)",
        "dia_semana": "Sexta-feira",
        "pilar": "Conexão Regional & Cultura",
        "tema": "Semana Farroupilha — O Comércio que Constrói o Rio Grande do Sul",
        "formato": "Card Fotográfico / Homenagem",
        "imagem": "conteudo_pronto/post_farroupilha_1789496114403.jpg",
        "legenda": """Atrás de cada balcão gaúcho, existe dedicação, coragem e compromisso com a comunidade.

Nesta Semana Farroupilha, a TruData celebra quem abre as portas faça sol, chuva ou minuano: o comerciante, o prestador de serviços e o empresário que fazem a economia do Rio Grande do Sul acontecer.

Temos orgulho de ter nascido em Sarandi/RS e de apoiar milhares de negócios gaúchos há mais de duas décadas com tecnologia confiável e proximidade real.

Qual comércio tradicional da sua cidade merece ser lembrado hoje? Marque nos comentários! 🧉

#SemanaFarroupilha #OrgulhoGaucho #TruDataERP #ComercioGaucho #SarandiRS #VarejoRS #HansenSoftware""",
        "story_do_dia": "Nesta Semana Farroupilha, valorize quem atende, produz e empreende perto de você. Qual comércio da sua cidade merece ser conhecido?",
        "cta": "Comente o nome da loja tradicional da sua cidade!"
    },
    {
        "id": "post-2026-09-19",
        "data": "19/09/2026 (Sábado)",
        "dia_semana": "Sábado",
        "pilar": "Gestão Comercial & Estoque",
        "tema": "Dia do Comprador — Comprar com Base em Dados, Não em Suposições",
        "formato": "Carrossel Educativo (4 Lâminas)",
        "imagem": "conteudo_pronto/post_comprador_1789496114404.jpg",
        "legenda": """Comprar bem é metade do lucro de qualquer comércio varejista.

Muitos lojistas compram pelo 'sentimento' ou pela insistência do representante comercial — e acabam com capital de giro parado na prateleira enquanto os produtos de alto giro faltam no sábado.

Checklist para uma compra inteligente com TruData ERP:
1️⃣ Analise o Relatório de Curva ABC dos últimos 90 dias;
2️⃣ Verifique o ponto de reposição antes de emitir o pedido;
3️⃣ Importe o XML da nota fiscal em 1 clique para confrontar custo e preço de venda;
4️⃣ Calcule a margem real descontando ICMS-ST e taxas de cartão.

Não deixe seu dinheiro empilhado no estoque. Gestão de compras eficiente se faz com dados!

#GestaoDeCompras #EstoqueInteligente #TruDataERP #VarejoLucrativo #ComercioRS #ERPComercial""",
        "story_do_dia": "Você sabe exatamente quais são os 20% de produtos que geram 80% do seu lucro hoje? (Sim / Preciso de relatório)",
        "cta": "Envie uma mensagem e conheça o módulo de Curva ABC da TruData."
    },
    {
        "id": "post-2026-09-20",
        "data": "20/09/2026 (Domingo)",
        "dia_semana": "Domingo",
        "pilar": "Dia do Gaúcho & Identidade",
        "tema": "20 de Setembro: Quem Honra o Trabalho Move Esta Terra",
        "formato": "Card Especial 20 de Setembro",
        "imagem": "conteudo_pronto/post_dia_gaucho_1789496114405.jpg",
        "legenda": """Sirvam nossas façanhas de modelo a toda terra! 🧉🔴🟢🟡

Hoje celebramos a coragem, os ideais e a bravura do povo gaúcho. E no dia a dia, essa bravura se manifesta no trabalho sério, na palavra honrada e no comércio que constrói nossas cidades no interior e na capital.

A TruData (Hansen Software) tem suas raízes fincadas em Sarandi/RS há mais de 25 anos. Nosso compromisso é continuar lado a lado de quem acorda cedo para fazer o Rio Grande crescer.

Um feliz 20 de Setembro a todos os clientes, parceiros, contadores e amigos gaúchos!

#20DeSetembro #DiaDoGaucho #RevolucaoFarroupilha #OrgulhoDeSerGaucho #TruDataERP #SarandiRS""",
        "story_do_dia": "Um chimarrão bem cevado e um feliz 20 de Setembro a todos que honram nossa terra com trabalho e dignidade! 🧉",
        "cta": "Deixe seu abraço gaúcho nos comentários!"
    },
    {
        "id": "post-2026-09-21",
        "data": "21/09/2026 (Segunda-feira)",
        "dia_semana": "Segunda-feira",
        "pilar": "Troca de Estação & Varejo",
        "tema": "Primavera no Varejo — Hora de Organizar a Grade e a Troca de Coleção",
        "formato": "Carrossel de Moda & Grade",
        "imagem": "conteudo_pronto/post_primavera_grade_1789496114406.jpg",
        "legenda": """A Primavera está chegando e com ela a virada de vitrine no comércio de confecções, calçados e bazar! 🌸

Trocar de estação sem dor de cabeça exige controle rigoroso de:
🔹 Grade completa por Cor x Tamanho (P, M, G, GG);
🔹 Liquidação inteligente das peças remanescentes de Inverno;
🔹 Etiquetas com código de barras geradas na entrada da nota;
🔹 Vendas no condicional (leva e traz) sem risco de perder peças.

Com o TruData Moda & Confecções, sua loja atende o cliente no balcão com velocidade e sabe exatamente qual peça está em condicional ou na arara.

Sua loja já está pronta para a nova coleção?

#ModaVarejo #ControleDeGrade #TruDataERP #LojasDeRoupas #GestaoDeModa #SarandiRS""",
        "story_do_dia": "Sua loja já preparou a troca de vitrine para a Primavera? Como você controla o condicional hoje?",
        "cta": "Solicite uma demonstração do módulo de Grade e Condicional."
    },
    {
        "id": "post-2026-09-22",
        "data": "22/09/2026 (Terça-feira)",
        "dia_semana": "Terça-feira",
        "pilar": "Autoridade & Parceria Contábil",
        "tema": "Dia do Contador — A Parceria que Transforma Números em Crescimento Seguro",
        "formato": "Card Homenagem & Reconhecimento",
        "imagem": "conteudo_pronto/post_dia_contador_1789496114407.jpg",
        "legenda": """Por trás de cada empresa próspera e em dia com o fisco, existe o olhar técnico e dedicado de um Contador. 💼📊

Neste 22 de Setembro, a TruData parabeniza todos os profissionais da Contabilidade pelo seu dia!

Sabemos o quanto o fechamento mensal pode ser desgastante quando o software da loja exporta arquivos corrompidos ou cheios de erros. Por isso, desenvolvemos o 'Portal do Contador Gratuito', permitindo que escritórios contábeis baixem SPEDs, Sintegra e XMLs auditados em 1 único clique, sem perder horas cobrando o cliente.

Parabéns pelo trabalho indispensável ao desenvolvimento do nosso país!

#DiaDoContador #ContabilidadeRS #PortalDoContador #TruDataERP #SPEDFiscal #ContabilidadeConsultiva""",
        "story_do_dia": "Hoje é dia de agradecer quem cuida da saúde fiscal da sua empresa. Já deu os parabéns para o seu contador hoje?",
        "cta": "Marque seu contador nos comentários para celebrar o dia dele!"
    },
    {
        "id": "post-2026-09-23",
        "data": "23/09/2026 (Quarta-feira)",
        "dia_semana": "Quarta-feira",
        "pilar": "Inteligência Fiscal & Economia",
        "tema": "Prejuízo Silencioso: Como a Bitributação no Simples Drena o Caixa da Sua Loja",
        "formato": "Carrossel Técnico Explicativo",
        "imagem": "conteudo_pronto/post_bitributacao_1789496114408.jpg",
        "legenda": """Você sabia que muitas lojas do Simples Nacional estão pagando ICMS e PIS/COFINS duas vezes sem saber? 🚨

Produtos como bebidas, medicamentos, cosméticos e autopeças já têm o imposto recolhido na fábrica (Substituição Tributária / Monofásico). Se o seu sistema comercial não segrega essas vendas no cupom fiscal, você paga a alíquota cheia do Simples de novo!

Com o Auditor Fiscal TruData:
🔍 Cada NCM é parametrizado automaticamente;
📉 Segregação correta de ICMS-ST e PIS Monofásico no DAS;
💰 Economia que pode passar de R$ 500 a R$ 2.000 todo mês!

Quer auditar uma nota fiscal da sua loja gratuitamente? Fale com nosso time de Sarandi.

#TributacaoInteligente #ICMSST #SimplesNacional #TruDataERP #AuditoriaFiscal #EconomiaTributaria""",
        "story_do_dia": "Sua loja vende bebidas, remédios ou autopeças? Você pode estar pagando imposto em dobro no Simples. Saiba mais.",
        "cta": "Envie um XML para nossa auditoria fiscal gratuita!"
    },
    {
        "id": "post-2026-09-24",
        "data": "24/09/2026 (Quinta-feira)",
        "dia_semana": "Quinta-feira",
        "pilar": "Segurança de Caixa & Contingência",
        "tema": "Sábado de Movimento: O Que Acontece Quando a Internet Cai no Pico de Vendas?",
        "formato": "Vídeo Reels / Card de Impacto",
        "imagem": "conteudo_pronto/post_contingencia_1789496114409.jpg",
        "legenda": """Sábado, 11h30 da manhã. Loja cheia, carrinhos no caixa e de repente... a internet cai! 😱

Se o seu software for 100% em nuvem daqueles de fora do Estado, sua operação para na hora. Fila no caixa, cliente impaciente indo embora e perda direta de faturamento.

Na TruData ERP isso NUNCA acontece:
⚡ O Frente de Caixa opera com Contingência Offline Nativa;
🧾 Continua emitindo NFC-e e imprimindo cupons em menos de 3 segundos;
🔄 Quando a fibra voltar, todas as notas são sincronizadas sozinhas com a SEFAZ-RS!

Não coloque seu sábado em risco com sistemas frágeis. Tenha a estabilidade que o comércio gaúcho exige.

#FrenteDeCaixa #ContingenciaOffline #TruDataERP #SemTravamentos #VarejoBlindado #SarandiRS""",
        "story_do_dia": "O que acontece na sua loja se a internet cair em pleno sábado com 10 clientes na fila? (O caixa para / Continua vendendo normal)",
        "cta": "Assista à demonstração do PDV offline funcionando!"
    }
]

out_json = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "painel_aprovacao", "planejamento_semana_dados.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(POSTS_SEMANA, f, indent=2, ensure_ascii=False)

print(f"Pacote de postagens da semana gerado com sucesso em: {out_json}")
print(f"Total de publicações estruturadas: {len(POSTS_SEMANA)} dias completos.")
