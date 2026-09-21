// Configurações e modelos preservados do Radar original.
const RADAR_OPTIONS = {
  "sel-origem": [
    { value: "Sarandi", label: "Sarandi - RS (Matriz TruData)" },
    { value: "Passo Fundo", label: "Passo Fundo - RS" },
    { value: "Carazinho", label: "Carazinho - RS" },
    { value: "Marau", label: "Marau - RS" },
    { value: "Palmeira das Missões", label: "Palmeira das Missões - RS" },
    { value: "Erechim", label: "Erechim - RS" },
    { value: "Frederico Westphalen", label: "Frederico Westphalen - RS" },
    { value: "Tapejara", label: "Tapejara - RS" },
    { value: "Não-Me-Toque", label: "Não-Me-Toque - RS" },
    { value: "Panambi", label: "Panambi - RS" },
    { value: "Getúlio Vargas", label: "Getúlio Vargas - RS" },
    { value: "Ibirubá", label: "Ibirubá - RS" },
    { value: "Tapera", label: "Tapera - RS" },
    { value: "Espumoso", label: "Espumoso - RS" },
    { value: "Nonoai", label: "Nonoai - RS" },
    { value: "Seberi", label: "Seberi - RS" },
    { value: "Sananduva", label: "Sananduva - RS" },
    { value: "Casca", label: "Casca - RS" },
    { value: "Constantina", label: "Constantina - RS" },
    { value: "Ronda Alta", label: "Ronda Alta - RS" },
    { value: "Rondinha", label: "Rondinha - RS" },
    { value: "Chapada", label: "Chapada - RS" },
    { value: "Barra Funda", label: "Barra Funda - RS" },
    { value: "Nova Boa Vista", label: "Nova Boa Vista - RS" },
    { value: "Três Palmeiras", label: "Três Palmeiras - RS" },
  ],
  "sel-cidade": [
    { value: "todas", label: "Todas as Cidades no Perímetro" },
    { value: "Sarandi", label: "Sarandi - RS" },
    { value: "Passo Fundo", label: "Passo Fundo - RS" },
    { value: "Carazinho", label: "Carazinho - RS" },
    { value: "Marau", label: "Marau - RS" },
    { value: "Palmeira das Missões", label: "Palmeira das Missões - RS" },
    { value: "Erechim", label: "Erechim - RS" },
    { value: "Frederico Westphalen", label: "Frederico Westphalen - RS" },
    { value: "Tapejara", label: "Tapejara - RS" },
    { value: "Não-Me-Toque", label: "Não-Me-Toque - RS" },
    { value: "Panambi", label: "Panambi - RS" },
    { value: "Getúlio Vargas", label: "Getúlio Vargas - RS" },
    { value: "Ibirubá", label: "Ibirubá - RS" },
    { value: "Tapera", label: "Tapera - RS" },
    { value: "Espumoso", label: "Espumoso - RS" },
    { value: "Soledade", label: "Soledade - RS" },
    { value: "Cruz Alta", label: "Cruz Alta - RS" },
    { value: "Ijuí", label: "Ijuí - RS" },
    { value: "Santo Ângelo", label: "Santo Ângelo - RS" },
    { value: "Sananduva", label: "Sananduva - RS" },
    { value: "Nonoai", label: "Nonoai - RS" },
    { value: "Seberi", label: "Seberi - RS" },
    { value: "Casca", label: "Casca - RS" },
    { value: "Constantina", label: "Constantina - RS" },
    { value: "Ronda Alta", label: "Ronda Alta - RS" },
    { value: "Rondinha", label: "Rondinha - RS" },
    { value: "Chapada", label: "Chapada - RS" },
    { value: "Barra Funda", label: "Barra Funda - RS" },
    { value: "Nova Boa Vista", label: "Nova Boa Vista - RS" },
    { value: "Três Palmeiras", label: "Três Palmeiras - RS" },
    { value: "Pontão", label: "Pontão - RS" },
    { value: "Camargo", label: "Camargo - RS" },
  ],
  "sel-segmento": [
    { value: "todos", label: "Todos os Nichos (Pequenos e Médios Negócios)" },
    {
      value: "Supermercados & Mercearias",
      label: "Supermercados, Minimercados & Fruteiras",
    },
    { value: "Autopeças & Oficinas", label: "Autopeças, Oficinas & Mecânicas" },
    {
      value: "Materiais de Construção",
      label: "Materiais de Construção & Ferragens",
    },
    { value: "Farmácias & Drogarias", label: "Farmácias & Drogarias" },
    {
      value: "Lojas de Roupas & Calçados",
      label: "Lojas de Roupas, Calçados & Confecções",
    },
    {
      value: "Padarias & Gastronomia",
      label: "Padarias, Confeitarias & Gastronomia",
    },
    {
      value: "Pet Shops & Agropecuárias",
      label: "Pet Shops, Veterinárias & Agropecuárias",
    },
    { value: "Celulares & Informática", label: "Celulares & Informática" },
    { value: "Papelarias & Bazares", label: "Papelarias & Bazares (1,99)" },
    {
      value: "Distribuidoras de Bebidas & Gás",
      label: "Distribuidoras de Bebidas & Gás",
    },
    { value: "Óticas & Joalherias", label: "Óticas & Joalherias" },
    { value: "Móveis & Decoração", label: "Móveis & Decoração" },
    {
      value: "Escritórios de Contabilidade",
      label: "Escritórios de Contabilidade",
    },
    {
      value: "Construção Civil & Engenharia",
      label: "Construção Civil & Engenharia",
    },
    { value: "Indústrias & Metalúrgicas", label: "Indústrias & Metalúrgicas" },
    { value: "Transporte & Logística", label: "Transporte & Logística" },
    {
      value: "Prestação de Serviços & Varejo",
      label: "Prestação de Serviços & Varejo Regional",
    },
  ],
  "sel-porte": [
    { value: "todos", label: "Todos os Portes (Micro a Redes)" },
    { value: "pequeno", label: "1 Caixa (Micro & Pequeno Negócio / MEI)" },
    { value: "medio", label: "2 a 4 Caixas (Médio Porte)" },
    { value: "grande", label: "5+ Caixas (Grande Porte / Redes)" },
  ],
  "sel-site": [
    { value: "todos", label: "Todos (Com e Sem Site)" },
    { value: "com_site", label: "Possui Site Oficial" },
    {
      value: "sem_site",
      label: "Não Possui Site (Oportunidade Catálogo Digital)",
    },
  ],
  "sel-ordenacao": [
    { value: "distancia", label: "Mais Próximos de Sarandi (km)" },
    { value: "score", label: "Maior Lead Score (0 a 100)" },
    { value: "nome", label: "Nome da Empresa (A - Z)" },
    { value: "pdvs", label: "Maior Quantidade de PDVs (Caixas)" },
    { value: "cidade", label: "Cidade Alfabética (A - Z)" },
  ],
};
const COORDENADAS_CIDADES = {
  sarandi: { lat: -27.9439, lon: -52.9247 },
  rondinha: { lat: -27.8286, lon: -52.9094 },
  "barra funda": { lat: -27.9214, lon: -53.0394 },
  "nova boa vista": { lat: -27.9897, lon: -53.0239 },
  constantina: { lat: -27.7319, lon: -52.9964 },
  "ronda alta": { lat: -27.7778, lon: -52.8083 },
  chapada: { lat: -28.0531, lon: -53.0678 },
  "três palmeiras": { lat: -27.6539, lon: -52.8528 },
  "tres palmeiras": { lat: -27.6539, lon: -52.8528 },
  pontão: { lat: -28.0578, lon: -52.6789 },
  pontao: { lat: -28.0578, lon: -52.6789 },
  carazinho: { lat: -28.2839, lon: -52.7858 },
  "palmeira das missões": { lat: -27.8989, lon: -53.3136 },
  "palmeira das missoes": { lat: -27.8989, lon: -53.3136 },
  "passo fundo": { lat: -28.2612, lon: -52.4083 },
  marau: { lat: -28.4489, lon: -52.2 },
  tapejara: { lat: -28.0683, lon: -52.0139 },
  erechim: { lat: -27.6339, lon: -52.2739 },
  "frederico westphalen": { lat: -27.3592, lon: -53.3944 },
  "getúlio vargas": { lat: -27.8906, lon: -52.2278 },
  "getulio vargas": { lat: -27.8906, lon: -52.2278 },
  ibirubá: { lat: -28.6275, lon: -53.09 },
  ibiruba: { lat: -28.6275, lon: -53.09 },
  tapera: { lat: -28.5, lon: -52.87 },
  espumoso: { lat: -28.7247, lon: -52.85 },
  nonoai: { lat: -27.3622, lon: -52.7711 },
  seberi: { lat: -27.48, lon: -53.4 },
  sananduva: { lat: -27.9497, lon: -51.8067 },
  casca: { lat: -28.56, lon: -51.97 },
  "não-me-toque": { lat: -28.4597, lon: -52.8214 },
  "nao-me-toque": { lat: -28.4597, lon: -52.8214 },
  panambi: { lat: -28.2925, lon: -53.5017 },
};

const TEMPLATES_EMAIL = {
  contingencia: {
    nome: "1. Gestão Fiscal & Contingência Offline no Sábado (Varejo Pesado)",
    assunto: (cli, cid) =>
      `Proposta Comercial TruData ERP — ${cli} (${cid}-RS)`,
    modulos: [
      "⚡ PDV Frente de Caixa Rápido",
      "📑 Contingência Offline NFC-e",
      "💳 TEF Integrado",
      "🤝 Suporte Humano Sarandi-RS",
      "📊 Gestão Fiscal SPED",
    ],
    corpo: (decisor, cli, cid, site, tem_site) => {
      const destaqueWeb =
        tem_site && site && site !== "Não possui site"
          ? `- Integração omnichannel com seu site (${site}) e e-commerce;\n`
          : `- Catálogo digital com pedidos no WhatsApp e Pix para seus clientes;\n`;
      return (
        `Olá ${decisor},\n\n` +
        `Segue a apresentação e proposta da TruData ERP (Hansen Software) para a ${cli} em ${cid}-RS.\n` +
        `Somos especialistas no varejo gaúcho há 25 anos com matriz em Sarandi-RS.\n\n` +
        `Destaques para sua operação:\n` +
        `- Contingência fiscal offline para nunca travar o caixa no sábado;\n` +
        destaqueWeb +
        `- Suporte telefônico 100% humanizado direto de Sarandi;\n` +
        `- Módulos integrados de estoque, balanças, TEF e contabilidade.\n\n` +
        `Podemos agendar uma demonstração de 15 minutos na sua loja?\n\n` +
        `Atenciosamente,\nEquipe Comercial TruData ERP\nSarandi-RS | Fone: (54) 3361-2650`
      );
    },
  },
  catalogo: {
    nome: "2. Especial Pequenos Negócios: Catálogo Digital + PDV Ágil + Pix",
    assunto: (cli, cid) =>
      `Catálogo Digital & Gestão Ágil para ${cli} — TruData ERP`,
    modulos: [
      "🌐 Catálogo Digital no WhatsApp",
      "💳 Pix Dinâmico no Balcão",
      "⚡ PDV Simplificado Rápido",
      "📦 Controle de Estoque Fácil",
      "📱 Suporte WhatsApp Direto",
    ],
    corpo: (decisor, cli, cid, site, tem_site) => {
      return (
        `Olá ${decisor},\n\n` +
        `Preparamos uma solução exclusiva da TruData ERP focada no crescimento da ${cli} em ${cid}-RS.\n\n` +
        `Destaques desta versão:\n` +
        `- Catálogo digital com pedidos automáticos direto no WhatsApp da loja;\n` +
        `- Emissão de cupom fiscal em 3 segundos e recebimento no Pix e Cartão sem complicação;\n` +
        `- Controle de produtos, preços e vendas na palma da mão;\n` +
        `- Investimento acessível e suporte próximo de Sarandi.\n\n` +
        `Gostaria de ver uma prévia do catálogo funcionando para a ${cli}?\n\n` +
        `Atenciosamente,\nEquipe Comercial TruData ERP\nSarandi-RS | Fone: (54) 3361-2650`
      );
    },
  },
  migracao: {
    nome: "3. Migração Sem Trauma: Troca de Sistema Antigo (Suporte Humano de Sarandi)",
    assunto: (cli, cid) =>
      `Migração de Sistema sem Trauma para ${cli} — TruData ERP Sarandi`,
    modulos: [
      "🛡️ Migração Gratuita de Dados e Clientes",
      "📞 Atendimento Telefônico sem Robôs",
      "⚡ PDV Blindado sem Travamentos",
      "📑 SPED Fiscal 100% Homologado",
      "🤝 Treinamento Prático Local",
    ],
    corpo: (decisor, cli, cid, site, tem_site) => {
      return (
        `Olá ${decisor},\n\n` +
        `Sabemos que trocar de sistema de gestão dá receio pelo medo de perder dados ou ficar sem suporte nos momentos de pico.\n` +
        `Na TruData (matriz em Sarandi-RS há 25 anos), nossa equipe técnica realiza a migração completa do seu cadastro de produtos, clientes e saldos sem parar o seu atendimento.\n\n` +
        `Por que lojistas da região migram para a TruData:\n` +
        `- Suporte técnico por telefone atendido em menos de 15 minutos por quem entende o comércio gaúcho;\n` +
        `- Caixa offline que não trava quando a internet oscila;\n` +
        `- Módulos completos sem pegadinhas de cobranças extras.\n\n` +
        `Podemos conversar nesta semana para avaliar a transição segura da ${cli}?\n\n` +
        `Atenciosamente,\nEquipe Comercial TruData ERP\nSarandi-RS | Fone: (54) 3361-2650`
      );
    },
  },
};
