// Conteúdo original preservado do painel de aprovação.
const LEGENDAS_CARDS = {
  1: `Chega de abrir 20 abas na SEFAZ: veja como funciona a troca de clientes no Trudata ERP Web na prática! 💻⚡

1️⃣ Seletor no topo da tela: você troca de empresa pelo menu em 2 cliques ou visualiza a carteira em modo consolidado;
2️⃣ Certificados A1 e Séries Fiscais 100% Isolados: emita NF-e, NFC-e, NFS-e e MDF-e de cada cliente sem precisar deslogar;
3️⃣ Faturamento e NFS-e em Lote: configure os honorários e emita as notas do mês de uma só vez;
4️⃣ Painel Executivo com KPIs em Tempo Real: acompanhe faturamento, compras e contas a pagar/receber de cada empresa.

O emissor gratuito parece de graça por nota, mas custa muito caro por carteira de clientes.

Preparamos uma página demonstrativa para os escritórios da nossa região:
👉 https://trudata.com.br/para-contadores

Podemos agendar uma demonstração rápida de 10 minutos pelo computador? ☕🤝`,

  2: `Chegou um arquivo XML para devolver mercadoria? Pare de recalcular impostos e conferir itens manualmente! 📑✅

No Trudata ERP Web, a devolução fiscal virou um processo de poucos segundos:
1️⃣ Você só faz o upload do arquivo XML original;
2️⃣ O sistema valida na SEFAZ e reconhece sozinho se é devolução ao cliente ou ao fornecedor;
3️⃣ Monta a devolução com os impostos espelhados e trava devoluções em duplicidade;
4️⃣ E o principal: é fiscal e só fiscal — não altera o estoque nem o financeiro do seu cliente!

Veja como funciona no link:
👉 https://trudata.com.br/para-contadores`,

  3: `Como o seu escritório faz a emissão e cobrança dos próprios honorários contábeis todo mês? 💼✨

O Trudata ERP Web possui um módulo completo de cobrança para o seu escritório:
✔️ Contrato cadastrado uma única vez por cliente;
✔️ Emissão em lote de todas as NFS-e da competência com um clique;
✔️ Ordem travada: a nota é autorizada antes do boleto/PIX sair;
✔️ Régua de cobrança automática por WhatsApp e e-mail;
✔️ Baixa automática via API do Sicredi e PIX QR Code.

Acesse:
👉 https://trudata.com.br/para-contadores`,

  4: `Cansado de indicar sistemas onde você e seus clientes ficam presos em filas infinitas de robôs no suporte? 🤖❌

A equipe da Hansen Software desenvolve o Trudata ERP em Sarandi - RS há mais de 25 anos:
✅ Suporte 100% humano via WhatsApp e telefone direto com quem entende de balcão;
✅ 98% de índice de satisfação entre mais de 300 clientes atendidos;
✅ Domínio completo de NFC-e, TEF, NF-e, NFS-e e MDF-e.

Conheça nossa área de parcerias com contabilidades:
👉 https://trudata.com.br/para-contadores`,

  5: `A transição da Reforma Tributária vai separar os escritórios que operam com tranquilidade daqueles que vão enfrentar notas rejeitadas na SEFAZ. 📑⚖️

O Trudata ERP Web já está preparado:
▪️ Motor fiscal que já monta os grupos de IBS e CBS na emissão e na devolução;
▪️ Exportação de dados limpos para a apuração mensal do seu escritório;
▪️ Painel multiempresa para acompanhar a situação fiscal de cada cliente em tempo real.

Proteja a sua carteira de clientes antes da virada fiscal:
👉 https://trudata.com.br/para-contadores`,
};

const POSTS_INICIAIS = [
  {
    id: "post-contadores-real",
    titulo: "Modo Escritório: Troca de Cliente em 2 Cliques (Tela Real)",
    canal: "WhatsApp",
    data: "Prospecção Contadores Locais",
    isFeriado: true,
    pilar: "Parceria Contábil",
    status: "pendente",
    imagem: "card_tela_real_anonimizada.jpg",
    comentarios:
      "Arte oficial com a tela escura real e nomes anonimizados. Pronta para envio.",
    briefing:
      "Card baseado na interface real do Trudata ERP Web. Mostra o seletor com 2 cliques e os nomes padronizados protegidos.",
    slides: [
      "Troca de cliente em 2 cliques. Sem deslogar e sem risco na SEFAZ!",
      "Certificados A1 e dados fiscais 100% isolados.",
      "Faturamento recorrente e devolução fiscal por XML.",
      "Conheça em: trudata.com.br/para-contadores",
    ],
    slideAtual: 0,
    legenda: LEGENDAS_CARDS[1],
  },
  {
    id: "post-devolucao",
    titulo: "Devolução Fiscal por XML: Subiu, Validou na SEFAZ",
    canal: "WhatsApp",
    data: "Prospecção Setor Fiscal",
    isFeriado: false,
    pilar: "Autoridade Fiscal",
    status: "pendente",
    imagem: "card_devolucao_xml.jpg",
    comentarios: "Focado no analista fiscal do escritório de contabilidade.",
    briefing: "Upload de XML com validação verde da SEFAZ.",
    slides: [
      "Chegou um XML para devolver? O Trudata valida na SEFAZ e monta a devolução sozinho.",
      "Identifica compra ou venda automaticamente.",
      "Não altera estoque ou financeiro do cliente.",
    ],
    slideAtual: 0,
    legenda: LEGENDAS_CARDS[2],
  },
  {
    id: "post-honorarios",
    titulo: "Honorários no Automático: NFS-e em Lote e Sicredi",
    canal: "WhatsApp",
    data: "Prospecção Sócios Contábeis",
    isFeriado: false,
    pilar: "Gestão Contábil",
    status: "pendente",
    imagem: "card_honorarios.jpg",
    comentarios: "Focado em reduzir inadimplência do escritório.",
    briefing:
      "Emissão de NFS-e em lote com régua no WhatsApp e boleto Sicredi/PIX.",
    slides: [
      "Cobre seus honorários no automático: NFS-e em lote e régua no WhatsApp.",
      "Ordem travada: nota antes do boleto.",
      "Baixa automática diária.",
    ],
    slideAtual: 0,
    legenda: LEGENDAS_CARDS[3],
  },
  {
    id: "post-suporte-real",
    titulo: "Aqui Seu Escritório Fala com Pessoas de Verdade",
    canal: "Instagram",
    data: "Institucional Hansen",
    isFeriado: false,
    pilar: "Suporte Humano",
    status: "pendente",
    imagem: "trudata_suporte_sarandi_1789497393778.jpg",
    comentarios:
      "Destaca os 25 anos da Hansen Software e 98% de satisfação direto de Sarandi/RS.",
    briefing:
      "Foto real da equipe de Sarandi com chimarrão e crachá contrapondo robôs frios.",
    slides: [
      "Aqui seu comércio fala com pessoas de verdade.",
      "Suporte direto por WhatsApp e telefone em Sarandi - RS.",
      "+25 anos de tradição e selo MPS.BR.",
    ],
    slideAtual: 0,
    legenda: LEGENDAS_CARDS[4],
  },
  {
    id: "post-reforma-trib",
    titulo: "Reforma Tributária: Seu Escritório e Clientes Seguros",
    canal: "LinkedIn",
    data: "Compliance Fiscal",
    isFeriado: false,
    pilar: "Autoridade Fiscal",
    status: "pendente",
    imagem: "card_reforma_tributaria.jpg",
    comentarios: "Direcionado a contadores e diretores financeiros.",
    briefing: "Simulador de IBS e CBS no painel do Trudata ERP.",
    slides: [
      "A Reforma Tributária vai mudar as regras do jogo fiscal.",
      "O Trudata ERP já está preparado para a transição do IBS e CBS.",
      "Conheça em: trudata.com.br/reforma-tributaria",
    ],
    slideAtual: 0,
    legenda: LEGENDAS_CARDS[5],
  },
  {
    id: "post-cal-15-09",
    titulo: "REELS: Obrigado por compartilhar sua rotina com a Trudata (15/09)",
    canal: "Instagram",
    data: "15/09/2026 às 08:00 (terça-feira)",
    isFeriado: false,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "card_suporte_humano.jpg",
    comentarios:
      "Roteiro de Produção: Reel de 25 a 35 segundos · 0–4s: equipe agradece. 4–20s: três colaboradores contam o tipo de necessidade que escutam, sem citar clientes. 20–30s: convite para o público compartilhar uma dificuldade.",
    briefing:
      "Formato: Reel de 25 a 35 segundos · 0–4s: equipe agradece. 4–20s: três colaboradores contam o tipo de necessidade que escutam, sem citar clientes. 20–30s: convite para o público compartilhar uma dificuldade.\nMaterial: Vídeos da equipe; legendas; nenhum depoimento ou resultado inventado.\nChamada: Responder nos comentários.",
    slides: [
      "08:00 AM · 15/09/2026",
      "Obrigado por compartilhar sua rotina com a Trudata",
      "Responder nos comentários.",
    ],
    slideAtual: 0,
    legenda:
      "Hoje nosso agradecimento vai para quem confia na Trudata e divide com a gente os desafios da sua empresa. Qual rotina você gostaria de simplificar?\n\n👉 Responder nos comentários.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
  {
    id: "post-cal-20-09",
    titulo: "REELS: De Sarandi para as histórias do comércio gaúcho (20/09)",
    canal: "Instagram",
    data: "20/09/2026 às 08:00 (domingo)",
    isFeriado: false,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "trudata_dia_gaucho_sarandi_1789497459083.jpg",
    comentarios:
      "Roteiro de Produção: Reel de 20 a 30 segundos · Abrir com referência a Sarandi; mostrar equipe e registros locais autorizados; terminar com mensagem de valorização da cultura e das pessoas do RS.",
    briefing:
      "Formato: Reel de 20 a 30 segundos · Abrir com referência a Sarandi; mostrar equipe e registros locais autorizados; terminar com mensagem de valorização da cultura e das pessoas do RS.\nMaterial: Imagens próprias; referências regionais sem caricatura; evitar sugerir parceria com eventos.\nChamada: Comentar a cidade de onde acompanha a empresa.",
    slides: [
      "08:00 AM · 20/09/2026",
      "De Sarandi para as histórias do comércio gaúcho",
      "Comentar a cidade de onde acompanha a empresa.",
    ],
    slideAtual: 0,
    legenda:
      "Neste 20 de setembro, celebramos nossas raízes e as pessoas que fazem o Rio Grande do Sul acontecer. Um abraço da equipe Trudata a todas as cidades que caminham conosco.\n\n👉 Comentar a cidade de onde acompanha a empresa.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
  {
    id: "post-cal-22-09",
    titulo:
      "CARROSSEL: Uma boa parceria com a contabilidade começa na rotina (22/09)",
    canal: "Instagram",
    data: "22/09/2026 às 08:00 (terça-feira)",
    isFeriado: false,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "trudata_contador_sarandi_1789497638360.jpg",
    comentarios:
      "Roteiro de Produção: Carrossel de 5 telas · 1: homenagem. 2: organizar documentos. 3: combinar periodicidade de envio. 4: conferir pendências com o contador. 5: agradecimento e convite para compartilhar.",
    briefing:
      "Formato: Carrossel de 5 telas · 1: homenagem. 2: organizar documentos. 3: combinar periodicidade de envio. 4: conferir pendências com o contador. 5: agradecimento e convite para compartilhar.\nMaterial: Arte simples; não ensinar regra fiscal nem anunciar prazo de obrigação.\nChamada: Compartilhar com o contador.",
    slides: [
      "08:00 AM · 22/09/2026",
      "Uma boa parceria com a contabilidade começa na rotina",
      "Compartilhar com o contador.",
    ],
    slideAtual: 0,
    legenda:
      "No Dia do Contador, reconhecemos quem acompanha decisões importantes das empresas. Organização e comunicação ajudam essa parceria a funcionar melhor todos os dias.\n\n👉 Compartilhar com o contador.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
  {
    id: "post-cal-25-09",
    titulo:
      "REELS: Nosso reconhecimento a quem cuida com responsabilidade (25/09)",
    canal: "Instagram",
    data: "25/09/2026 às 08:00 (sexta-feira)",
    isFeriado: false,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "post_farmaceutico_1789496201382.jpg",
    comentarios:
      "Roteiro de Produção: Reel de 20 a 30 segundos · Abrir com homenagem; mostrar profissional autorizado ou equipe fazendo o agradecimento; concluir sem demonstração de medicamento ou promessa clínica.",
    briefing:
      "Formato: Reel de 20 a 30 segundos · Abrir com homenagem; mostrar profissional autorizado ou equipe fazendo o agradecimento; concluir sem demonstração de medicamento ou promessa clínica.\nMaterial: Autorização do participante; arte própria; não utilizar a identidade oficial da campanha como anúncio comercial.\nChamada: Deixar uma mensagem de reconhecimento.",
    slides: [
      "08:00 AM · 25/09/2026",
      "Nosso reconhecimento a quem cuida com responsabilidade",
      "Deixar uma mensagem de reconhecimento.",
    ],
    slideAtual: 0,
    legenda:
      "No Dia Mundial do Farmacêutico, promovido pela FIP, nosso reconhecimento a quem dedica conhecimento e responsabilidade ao cuidado com as pessoas.\n\n👉 Deixar uma mensagem de reconhecimento.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
  {
    id: "post-cal-05-10",
    titulo:
      "REELS: Qual rotina do seu pequeno negócio precisa se organizar primeiro (05/10)",
    canal: "Instagram",
    data: "05/10/2026 às 08:00 (segunda-feira)",
    isFeriado: false,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "card_reforma_tributaria.jpg",
    comentarios:
      "Roteiro de Produção: Reel de 30 segundos · Mostrar três situações encenadas: documentos espalhados, busca de informação e dúvida sobre emissão. Apresentar o Easy como solução web divulgada pela Trudata; convidar para avaliar aderência.",
    briefing:
      "Formato: Reel de 30 segundos · Mostrar três situações encenadas: documentos espalhados, busca de informação e dúvida sobre emissão. Apresentar o Easy como solução web divulgada pela Trudata; convidar para avaliar aderência.\nMaterial: Captura de demonstração validada do Easy; confirmar condições de contratação antes de incluí-las.\nChamada: Solicitar uma demonstração pelo link da bio.",
    slides: [
      "08:00 AM · 05/10/2026",
      "Qual rotina do seu pequeno negócio precisa se organizar primeiro",
      "Solicitar uma demonstração pelo link da bio.",
    ],
    slideAtual: 0,
    legenda:
      "No Dia da Micro e Pequena Empresa, valorizamos quem empreende todos os dias. Se organizar a emissão fiscal é uma prioridade, conheça a proposta do Trudata Easy e converse com nossa equipe.\n\n👉 Solicitar uma demonstração pelo link da bio.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
  {
    id: "post-cal-12-10",
    titulo: "POST ESTÁTICO: Um dia para valorizar a infância (12/10)",
    canal: "Instagram",
    data: "12/10/2026 às 08:00 (segunda-feira)",
    isFeriado: false,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "card_devolucao_xml.jpg",
    comentarios:
      "Roteiro de Produção: Post estático · Ilustração original de brincadeiras; frase principal curta; legenda acolhedora. Evitar usar criança como porta-voz comercial.",
    briefing:
      "Formato: Post estático · Ilustração original de brincadeiras; frase principal curta; legenda acolhedora. Evitar usar criança como porta-voz comercial.\nMaterial: Preferir ilustração; se houver fotos de menores, obter autorização dos responsáveis.\nChamada: Compartilhar uma lembrança de infância, se desejar.",
    slides: [
      "08:00 AM · 12/10/2026",
      "Um dia para valorizar a infância",
      "Compartilhar uma lembrança de infância, se desejar.",
    ],
    slideAtual: 0,
    legenda:
      "Que toda criança tenha espaço para brincar, aprender e imaginar. A equipe Trudata deseja um Dia das Crianças com cuidado e bons momentos.\n\n👉 Compartilhar uma lembrança de infância, se desejar.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
  {
    id: "post-cal-19-10",
    titulo: "REELS: Toda melhoria começa com uma pergunta (19/10)",
    canal: "Instagram",
    data: "19/10/2026 às 08:00 (segunda-feira)",
    isFeriado: false,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "card_devolucao_xml.jpg",
    comentarios:
      "Roteiro de Produção: Reel de 30 a 40 segundos · 0–5s: qual tarefa dá trabalho. 5–15s: equipe entende a necessidade. 15–30s: bastidor de teste de rotina já existente. Final: valorização dos profissionais de tecnologia.",
    briefing:
      "Formato: Reel de 30 a 40 segundos · 0–5s: qual tarefa dá trabalho. 5–15s: equipe entende a necessidade. 15–30s: bastidor de teste de rotina já existente. Final: valorização dos profissionais de tecnologia.\nMaterial: Bastidores reais; não apresentar rotina existente como lançamento nem prometer recurso futuro.\nChamada: Comentar uma tarefa que gostaria de simplificar.",
    slides: [
      "08:00 AM · 19/10/2026",
      "Toda melhoria começa com uma pergunta",
      "Comentar uma tarefa que gostaria de simplificar.",
    ],
    slideAtual: 0,
    legenda:
      "No Dia Nacional da Inovação, mostramos o valor de entender a rotina antes de propor uma solução. Nosso reconhecimento aos profissionais de TI que participam desse trabalho.\n\n👉 Comentar uma tarefa que gostaria de simplificar.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
  {
    id: "post-cal-30-10",
    titulo: "REELS: Quem faz o comércio acontecer (30/10)",
    canal: "Instagram",
    data: "30/10/2026 às 08:00 (sexta-feira)",
    isFeriado: false,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "card_devolucao_xml.jpg",
    comentarios:
      "Roteiro de Produção: Reel de 20 a 30 segundos · Sequência de funções: atendimento, organização, reposição e caixa. Cada pessoa aparece por alguns segundos; finalizar com agradecimento coletivo.",
    briefing:
      "Formato: Reel de 20 a 30 segundos · Sequência de funções: atendimento, organização, reposição e caixa. Cada pessoa aparece por alguns segundos; finalizar com agradecimento coletivo.\nMaterial: Equipe ou clientes com autorização; não prometer alteração do funcionamento na data.\nChamada: Marcar um colega, se desejar.",
    slides: [
      "08:00 AM · 30/10/2026",
      "Quem faz o comércio acontecer",
      "Marcar um colega, se desejar.",
    ],
    slideAtual: 0,
    legenda:
      "Hoje nosso reconhecimento vai a quem trabalha no comércio e cuida de tantos detalhes para atender bem. Feliz Dia do Comerciário.\n\n👉 Marcar um colega, se desejar.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
  {
    id: "post-cal-12-11",
    titulo:
      "REELS: Antes de o produto chegar à cesta existe uma operação inteira (12/11)",
    canal: "Instagram",
    data: "12/11/2026 às 08:00 (quinta-feira)",
    isFeriado: false,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "card_devolucao_xml.jpg",
    comentarios:
      "Roteiro de Produção: Reel de 30 segundos · Mostrar uma sequência ilustrativa de compra, recebimento, estoque e atendimento. Concluir com homenagem e convite para conversar sobre gestão.",
    briefing:
      "Formato: Reel de 30 segundos · Mostrar uma sequência ilustrativa de compra, recebimento, estoque e atendimento. Concluir com homenagem e convite para conversar sobre gestão.\nMaterial: Imagens autorizadas de mercado; só demonstrar módulos já confirmados pela equipe de produto.\nChamada: Conversar sobre a operação pelo link da bio.",
    slides: [
      "08:00 AM · 12/11/2026",
      "Antes de o produto chegar à cesta existe uma operação inteira",
      "Conversar sobre a operação pelo link da bio.",
    ],
    slideAtual: 0,
    legenda:
      "No Dia Nacional do Supermercado, valorizamos as equipes que abastecem a rotina das famílias. Organização acompanha cada etapa desse trabalho.\n\n👉 Conversar sobre a operação pelo link da bio.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
  {
    id: "post-cal-19-11",
    titulo:
      "REELS: Uma decisão que ajudou minha empresa a se organizar (19/11)",
    canal: "Instagram",
    data: "19/11/2026 às 08:00 (quinta-feira)",
    isFeriado: false,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "card_devolucao_xml.jpg",
    comentarios:
      "Roteiro de Produção: Reel de entrevista de 30 a 45 segundos · Perguntar a uma empreendedora: qual era a dificuldade, o que mudou no processo e o que aprendeu. Usar sua resposta real, sem atribuir resultado à Trudata sem evidência.",
    briefing:
      "Formato: Reel de entrevista de 30 a 45 segundos · Perguntar a uma empreendedora: qual era a dificuldade, o que mudou no processo e o que aprendeu. Usar sua resposta real, sem atribuir resultado à Trudata sem evidência.\nMaterial: Convidada e fala aprovadas. Se não houver entrevista, usar mensagem da equipe sem inventar personagem.\nChamada: Compartilhar um aprendizado.",
    slides: [
      "08:00 AM · 19/11/2026",
      "Uma decisão que ajudou minha empresa a se organizar",
      "Compartilhar um aprendizado.",
    ],
    slideAtual: 0,
    legenda:
      "No Dia do Empreendedorismo Feminino, abrimos espaço para uma experiência real de quem empreende. Hoje, nosso reconhecimento às mulheres que constroem seus negócios.\n\n👉 Compartilhar um aprendizado.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
  {
    id: "post-cal-20-11",
    titulo:
      "POST ESTÁTICO: Respeito precisa fazer parte de todos os dias (20/11)",
    canal: "Instagram",
    data: "20/11/2026 às 08:00 (sexta-feira)",
    isFeriado: false,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "card_devolucao_xml.jpg",
    comentarios:
      "Roteiro de Produção: Post institucional · Arte com texto curto e legível; legenda sobre enfrentamento ao racismo nas relações. Publicar sem oferta, promoção ou chamada para demonstração.",
    briefing:
      "Formato: Post institucional · Arte com texto curto e legível; legenda sobre enfrentamento ao racismo nas relações. Publicar sem oferta, promoção ou chamada para demonstração.\nMaterial: Revisão de linguagem; não atribuir programas de diversidade inexistentes à Trudata.\nChamada: Leitura e reflexão, sem chamada comercial.",
    slides: [
      "08:00 AM · 20/11/2026",
      "Respeito precisa fazer parte de todos os dias",
      "Leitura e reflexão, sem chamada comercial.",
    ],
    slideAtual: 0,
    legenda:
      "O Dia Nacional de Zumbi e da Consciência Negra convida à memória e ao compromisso com relações mais justas. Respeito e enfrentamento ao racismo fazem parte dessa construção diária.\n\n👉 Leitura e reflexão, sem chamada comercial.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
  {
    id: "post-cal-27-11",
    titulo: "REELS: Três conferências antes do movimento aumentar (27/11)",
    canal: "Instagram",
    data: "27/11/2026 às 08:00 (sexta-feira)",
    isFeriado: false,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "card_devolucao_xml.jpg",
    comentarios:
      "Roteiro de Produção: Reel de 20 a 30 segundos · Abrir com a Black Friday; mostrar conferência de produtos anunciados, condições de venda e orientações da equipe; terminar desejando bom trabalho.",
    briefing:
      "Formato: Reel de 20 a 30 segundos · Abrir com a Black Friday; mostrar conferência de produtos anunciados, condições de venda e orientações da equipe; terminar desejando bom trabalho.\nMaterial: Conteúdo educativo. Não anunciar suporte especial, desconto ou capacidade técnica sem confirmação.\nChamada: Salvar o checklist.",
    slides: [
      "08:00 AM · 27/11/2026",
      "Três conferências antes do movimento aumentar",
      "Salvar o checklist.",
    ],
    slideAtual: 0,
    legenda:
      "A Black Friday chegou. Confira o que foi anunciado, alinhe a equipe e acompanhe a operação ao longo do dia. Bom trabalho a quem está no atendimento, no caixa e no estoque.\n\n👉 Salvar o checklist.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
  {
    id: "post-cal-30-11",
    titulo: "CARROSSEL: Cyber Monday com informação organizada (30/11)",
    canal: "Instagram",
    data: "30/11/2026 às 08:00 (segunda-feira)",
    isFeriado: false,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "card_devolucao_xml.jpg",
    comentarios:
      "Roteiro de Produção: Carrossel de 5 telas · 1: chamada. 2: conferir pedidos. 3: acompanhar saldos nos canais. 4: organizar retornos ao cliente. 5: avaliar a integração disponível para a operação.",
    briefing:
      "Formato: Carrossel de 5 telas · 1: chamada. 2: conferir pedidos. 3: acompanhar saldos nos canais. 4: organizar retornos ao cliente. 5: avaliar a integração disponível para a operação.\nMaterial: Usar esquema ilustrativo; não afirmar que toda loja virtual é compatível com o ERP.\nChamada: Pedir uma conversa sobre integração.",
    slides: [
      "08:00 AM · 30/11/2026",
      "Cyber Monday com informação organizada",
      "Pedir uma conversa sobre integração.",
    ],
    slideAtual: 0,
    legenda:
      "Na Cyber Monday, a experiência do cliente também depende da informação que circula entre os canais. Revise pedidos, disponibilidade e atendimento com sua equipe.\n\n👉 Pedir uma conversa sobre integração.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
  {
    id: "post-cal-03-12",
    titulo: "CARROSSEL: Seu atendimento é fácil de entender (03/12)",
    canal: "Instagram",
    data: "03/12/2026 às 08:00 (quinta-feira)",
    isFeriado: false,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "card_devolucao_xml.jpg",
    comentarios:
      "Roteiro de Produção: Carrossel de 5 telas · 1: pergunta. 2: letras legíveis. 3: vídeos legendados. 4: instruções claras e escuta. 5: escolher uma melhoria prática.",
    briefing:
      "Formato: Carrossel de 5 telas · 1: pergunta. 2: letras legíveis. 3: vídeos legendados. 4: instruções claras e escuta. 5: escolher uma melhoria prática.\nMaterial: Bom contraste e linguagem respeitosa; não anunciar certificação de acessibilidade.\nChamada: Compartilhar com quem cuida do atendimento.",
    slides: [
      "08:00 AM · 03/12/2026",
      "Seu atendimento é fácil de entender",
      "Compartilhar com quem cuida do atendimento.",
    ],
    slideAtual: 0,
    legenda:
      "No Dia Internacional das Pessoas com Deficiência, propomos uma revisão concreta: o que pode ficar mais acessível na comunicação da sua empresa?\n\n👉 Compartilhar com quem cuida do atendimento.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
  {
    id: "post-cal-20-12",
    titulo:
      "REELS: Cada serviço tem uma história que precisa ser registrada (20/12)",
    canal: "Instagram",
    data: "20/12/2026 às 08:00 (domingo)",
    isFeriado: false,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "card_devolucao_xml.jpg",
    comentarios:
      "Roteiro de Produção: Reel de 30 segundos · Usar solicitação fictícia de oficina; mostrar identificação, descrição do pedido e acompanhamento da ordem de serviço. Encerrar agradecendo aos mecânicos.",
    briefing:
      "Formato: Reel de 30 segundos · Usar solicitação fictícia de oficina; mostrar identificação, descrição do pedido e acompanhamento da ordem de serviço. Encerrar agradecendo aos mecânicos.\nMaterial: Ambiente de teste; confirmar telas e caminhos atuais do módulo antes de gravar.\nChamada: Solicitar demonstração para prestação de serviços.",
    slides: [
      "08:00 AM · 20/12/2026",
      "Cada serviço tem uma história que precisa ser registrada",
      "Solicitar demonstração para prestação de serviços.",
    ],
    slideAtual: 0,
    legenda:
      "No Dia do Mecânico, nosso reconhecimento a quem cuida de cada detalhe do serviço. Uma rotina registrada ajuda a equipe a acompanhar o trabalho e orientar o cliente.\n\n👉 Solicitar demonstração para prestação de serviços.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
  {
    id: "post-cal-25-12",
    titulo: "POST ESTÁTICO: Feliz Natal da equipe Trudata (25/12)",
    canal: "Instagram",
    data: "25/12/2026 às 08:00 (sexta-feira)",
    isFeriado: true,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "card_suporte_humano.jpg",
    comentarios:
      "Roteiro de Produção: Post estático · Arte com mensagem central e identidade da empresa; foto da equipe é alternativa se autorizada. Manter leitura simples e sem oferta comercial.",
    briefing:
      "Formato: Post estático · Arte com mensagem central e identidade da empresa; foto da equipe é alternativa se autorizada. Manter leitura simples e sem oferta comercial.\nMaterial: Arte própria; assinatura Trudata; publicação às 8h.\nChamada: Sem chamada comercial.",
    slides: [
      "08:00 AM · 25/12/2026",
      "Feliz Natal da equipe Trudata",
      "Sem chamada comercial.",
    ],
    slideAtual: 0,
    legenda:
      "Desejamos um Natal de paz, acolhimento e bons momentos. Obrigado a clientes, parceiros e colaboradores por fazerem parte da nossa história.\n\n👉 Sem chamada comercial.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
  {
    id: "post-cal-31-12",
    titulo: "REELS: Obrigado por fazer parte de 2026 (31/12)",
    canal: "Instagram",
    data: "31/12/2026 às 08:00 (quinta-feira)",
    isFeriado: false,
    pilar: "Calendário 2026",
    status: "pendente",
    imagem: "card_devolucao_xml.jpg",
    comentarios:
      "Roteiro de Produção: Reel de 30 a 40 segundos · Organizar registros reais de equipe, trabalho e encontros. Cada trecho recebe uma frase curta. Finalizar com votos para 2027.",
    briefing:
      "Formato: Reel de 30 a 40 segundos · Organizar registros reais de equipe, trabalho e encontros. Cada trecho recebe uma frase curta. Finalizar com votos para 2027.\nMaterial: Usar apenas acontecimentos reais; métricas e resultados só entram com fonte e aprovação.\nChamada: Contar qual conteúdo deseja acompanhar no próximo ano.",
    slides: [
      "08:00 AM · 31/12/2026",
      "Obrigado por fazer parte de 2026",
      "Contar qual conteúdo deseja acompanhar no próximo ano.",
    ],
    slideAtual: 0,
    legenda:
      "Encerramos 2026 com gratidão pelas relações construídas e pelas conversas que tivemos ao longo do ano. Desejamos saúde e bons caminhos para 2027.\n\n👉 Contar qual conteúdo deseja acompanhar no próximo ano.\n\n#TrudataERP #GestaoEmpresarial #SarandiRS #ComercioGaucho",
  },
];
