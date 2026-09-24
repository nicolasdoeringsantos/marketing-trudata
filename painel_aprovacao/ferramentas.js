(() => {
  "use strict";
  const tools = [
    ["crm_enterprise.html?tab=atividades", "Ações e agendamentos", "Comercial", "Agenda visual com calendário mensal, semanal, diário e agendamento de ações comerciais.", "CRM Enterprise"],
    ["revisao_enderecos.html", "Revisão de endereços", "Comercial", "Corrija endereços pendentes, consulte a API e confira os pontos antes de atualizar o radar.", "Integrado ao radar"],
    ["planejar_visitas.html", "Planejamento de visitas", "Comercial", "Monte a agenda, abra o trajeto e registre as visitas realizadas.", "Agenda compartilhada"],
    ["proximos_contatos.html", "Próximos contatos", "Comercial", "Veja retornos do CRM, registre conversas e combine a próxima ação.", "Acompanhamento diário"],
    ["resultado_prospeccao.html", "Resultado da prospecção", "Comercial", "Acompanhe contatos, visitas, propostas apresentadas e aceites registrados.", "Dados da operação"],
    [
      "radar_clientes.html",
      "Radar de clientes",
      "Comercial",
      "Encontre empresas da região, filtre oportunidades e adicione ao CRM.",
      "Base regional",
    ],
    [
      "crm.html",
      "CRM de acompanhamento",
      "Comercial",
      "Organize contatos, notas e etapas das oportunidades comerciais.",
      "Integrado ao servidor",
    ],
    [
      "radar_clientes.html?modo=contadores",
      "Contadores e parcerias",
      "Comercial",
      "Consulte os escritórios da região no radar e prepare a abordagem.",
      "Filtro do radar",
    ],
    [
      "cadencia_sdr.html",
      "Preparar uma conversa",
      "Comercial",
      "Escreva uma apresentação, um retorno ou um convite para demonstração.",
      "Mensagem editável",
    ],
    [
      "gerador_proposta.html",
      "Preparar proposta",
      "Comercial",
      "Escolha o cliente do radar, monte serviços e valores e acompanhe a negociação.",
      "Propostas compartilhadas",
    ],
    [
      "checkup_loja.html",
      "Diagnóstico da loja",
      "Planejamento",
      "Registre necessidades e defina o próximo passo com o responsável.",
      "Roteiro de levantamento",
    ],
    [
      "tco_roi.html",
      "Comparar custos",
      "Planejamento",
      "Compare dois cenários usando os custos e o período que você informar.",
      "Premissas abertas",
    ],
    [
      "checklist_implantacao.html",
      "Planejar implantação",
      "Planejamento",
      "Acompanhe preparação, conferências e treinamento da equipe.",
      "Rascunho neste navegador",
    ],
    [
      "auditor_xml.html",
      "Ler arquivo XML",
      "Planejamento",
      "Confira emitente, destinatário, itens e total de uma NF-e ou NFC-e.",
      "Leitura local do arquivo",
    ],
    [
      "demo_pdv.html",
      "Demonstração de caixa",
      "Comercial",
      "Experimente um carrinho de exemplo e a conclusão de uma venda simulada.",
      "Demonstração didática",
    ],
    [
      "calendario.html",
      "Calendário editorial",
      "Conteúdo",
      "Consulte os dias planejados, roteiros e materiais de publicação.",
      "Planejamento de conteúdo",
    ],
    [
      "index.html",
      "Aprovação de conteúdo",
      "Conteúdo",
      "Revise as peças e acompanhe o que está aprovado ou publicado.",
      "Galeria de peças",
    ],
    [
      "teleprompter.html",
      "Teleprompter",
      "Conteúdo",
      "Cole seu roteiro e controle a leitura durante a gravação.",
      "Texto, velocidade e tamanho",
    ],
    [
      "biblioteca.html",
      "Biblioteca de referência",
      "Conteúdo",
      "Encontre roteiros e ideias das coleções anteriores para revisar e adaptar.",
      "13 coleções preservadas",
    ],
  ];
  const norm = (s) =>
    s
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase();
  let group = "Todas";
  function render() {
    const term = norm(document.getElementById("tool-search").value.trim());
    const list = tools.filter(
      (t) =>
        (group === "Todas" || t[2] === group) &&
        norm(t.join(" ")).includes(term),
    );
    document.getElementById("catalogue-title").textContent =
      group === "Todas" ? "Todas as ferramentas" : group;
    document.getElementById("tool-count").textContent =
      `${list.length} ${list.length === 1 ? "ferramenta" : "ferramentas"}`;
    document.getElementById("tool-list").innerHTML = list.length
      ? list
          .map(
            (t) =>
              `<article class="tool-entry"><div><h3><a href="${t[0]}">${t[1]}</a></h3><small>${t[4]}</small></div><p>${t[3]}</p><a class="btn" href="${t[0]}" aria-label="Abrir ${t[1]}">Abrir</a></article>`,
          )
          .join("")
      : '<div class="empty"><h3>Qual tarefa você precisa resolver?</h3><p>Tente buscar por cliente, proposta, custos ou conteúdo.</p><button class="btn" id="clear-search">Limpar busca e filtros</button></div>';
    document.getElementById("clear-search")?.addEventListener("click", () => {
      document.getElementById("tool-search").value = "";
      group = "Todas";
      setGroup();
      render();
      document.getElementById("tool-search").focus();
    });
  }
  function setGroup() {
    document
      .querySelectorAll("[data-group]")
      .forEach((b) =>
        b.setAttribute("aria-pressed", String(b.dataset.group === group)),
      );
  }
  document.querySelectorAll("[data-group]").forEach((b) =>
    b.addEventListener("click", () => {
      group = b.dataset.group;
      setGroup();
      render();
    }),
  );
  document.getElementById("tool-search").addEventListener("input", render);
  render();
})();
