(() => {
  "use strict";
  const $ = (id) => document.getElementById(id),
    esc = (v) =>
      String(v ?? "").replace(
        /[&<>"']/g,
        (c) =>
          ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;",
          })[c],
      );
  const money = (v) =>
    Number(v).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
  const kind = document.body.dataset.tool;
  const checks = [
    "Responsável e escopo definidos",
    "Backup realizado e restauração conferida",
    "Cadastros de produtos e clientes revisados",
    "Parâmetros fiscais conferidos com o contador",
    "Equipamentos e integrações testados",
    "Venda e cancelamento testados no ambiente adequado",
    "Conferência de estoque e saldos concluída",
    "Equipe treinada para a rotina e contingências",
    "Responsáveis pelo suporte e próximos passos definidos",
  ];
  const field = (
    id,
    label,
    type = "text",
    value = "",
    wide = false,
    extra = "",
  ) =>
    `<label class="field ${wide ? "wide" : ""}">${label}<input id="${id}" name="${id}" type="${type}" value="${esc(value)}" ${extra}></label>`;
  const area = (id, label, value = "", extra = "") =>
    `<label class="field wide">${label}<textarea id="${id}" name="${id}" ${extra}>${esc(value)}</textarea></label>`;
  const num = (id, label, value = "") =>
    field(
      id,
      label,
      "number",
      value,
      false,
      'min="0" max="1000000000" step="0.01" required',
    );
  const common = () =>
    field("cliente", "Empresa", "text", "", false, 'required maxlength="160"') +
    field("responsavel", "Responsável", "text", "", false, 'maxlength="160"');
  const definitions = {
    diagnostico: {
      title: "Diagnóstico da loja",
      desc: "Uma boa proposta começa por entender a operação.",
      note: "Registre o que foi observado e o que o cliente relatou. Este roteiro não atribui perdas financeiras nem emite laudo fiscal.",
      fields: () =>
        common() +
        area(
          "rotina",
          "Como funciona a operação?",
          "",
          'required maxlength="6000"',
        ) +
        area(
          "necessidades",
          "O que precisa melhorar?",
          "",
          'required maxlength="6000"',
        ) +
        area("integracoes", "Equipamentos e integrações a conferir") +
        area(
          "proximo",
          "Próximo passo combinado",
          "",
          'required maxlength="3000"',
        ),
      build: (v) =>
        `DIAGNÓSTICO DA LOJA\n${v.cliente}\nResponsável: ${v.responsavel || "A definir"}\n\nOperação\n${v.rotina}\n\nNecessidades relatadas\n${v.necessidades}\n\nEquipamentos e integrações\n${v.integracoes || "A conferir"}\n\nPróximo passo\n${v.proximo}\n\nLevantamento comercial; informações fornecidas durante a conversa.`,
    },
    custos: {
      title: "Comparar custos",
      desc: "Dois cenários. As mesmas premissas. Uma comparação clara.",
      note: "Use valores de contratos ou cotações. O resultado compara apenas os custos informados, sem presumir ganho de vendas ou eliminação de perdas.",
      fields: () =>
        field("cliente", "Empresa") +
        field(
          "meses",
          "Período em meses",
          "number",
          "12",
          false,
          'min="1" max="120" step="1" required',
        ) +
        num("atual", "Cenário atual · custo mensal (R$)") +
        num("novo", "Novo cenário · custo mensal (R$)") +
        num("extraAtual", "Cenário atual · outros custos mensais (R$)", "0") +
        num("extraNovo", "Novo cenário · outros custos mensais (R$)", "0") +
        num(
          "inicialAtual",
          "Cenário atual · custos únicos no período (R$)",
          "0",
        ) +
        num(
          "inicialNovo",
          "Novo cenário · custos únicos no período (R$)",
          "0",
        ) +
        area("premissas", "Fontes e premissas da comparação"),
      build: (v) => {
        const cents = (n) => Math.round(Number(n) * 100);
        const months = +v.meses,
          ac =
            (cents(v.atual) + cents(v.extraAtual)) * months +
            cents(v.inicialAtual),
          bc =
            (cents(v.novo) + cents(v.extraNovo)) * months +
            cents(v.inicialNovo),
          a = ac / 100,
          b = bc / 100,
          d = (ac - bc) / 100;
        return `COMPARAÇÃO DE CUSTOS\n${v.cliente || "Empresa não informada"} · ${months} meses\n\nCenário atual\nMensalidade: ${money(v.atual)}\nOutros custos mensais: ${money(v.extraAtual)}\nCustos únicos: ${money(v.inicialAtual)}\nTotal do período: ${money(a)}\n\nNovo cenário\nMensalidade: ${money(v.novo)}\nOutros custos mensais: ${money(v.extraNovo)}\nCustos únicos: ${money(v.inicialNovo)}\nTotal do período: ${money(b)}\n\n${d > 0 ? "Redução de custo no novo cenário" : d < 0 ? "Aumento de custo no novo cenário" : "Custos equivalentes"}: ${money(Math.abs(d))}\n\nFórmula: (mensalidade + outros custos mensais) × meses + custos únicos.\n\nPremissas\n${v.premissas || "Não informadas."}\n\nEstimativa baseada nos valores preenchidos. Não inclui custos não informados.`;
      },
    },
    proposta: {
      title: "Preparar proposta",
      desc: "Deixe o escopo e os valores claros antes de apresentar.",
      note: "Preencha os valores negociados. Este documento é uma proposta comercial; não registra aceite, assinatura ou pagamento.",
      fields: () =>
        common() +
        field("cidade", "Cidade") +
        field("validade", "Válida até", "date", "", false, "required") +
        num("mensal", "Mensalidade total (R$)") +
        num("implantacao", "Implantação (R$)") +
        num("equipamentos", "Equipamentos e outros itens (R$)", "0") +
        area("escopo", "Escopo incluído", "", 'required maxlength="6000"') +
        area(
          "condicoes",
          "Prazos, pagamento e condições",
          "",
          'required maxlength="6000"',
        ),
      build: (v) =>
        `PROPOSTA COMERCIAL · TRUDATA\nCliente: ${v.cliente}\nResponsável: ${v.responsavel || "A definir"}\nCidade: ${v.cidade || "Não informada"}\nVálida até: ${v.validade.split("-").reverse().join("/")}\n\nEscopo\n${v.escopo}\n\nInvestimento\nMensalidade: ${money(v.mensal)}\nImplantação: ${money(v.implantacao)}\nEquipamentos e outros itens: ${money(v.equipamentos)}\nValores únicos: ${money(+v.implantacao + +v.equipamentos)}\nPrimeiro mês + valores únicos: ${money(+v.mensal + +v.implantacao + +v.equipamentos)}\n\nCondições\n${v.condicoes}\n\nDocumento para negociação. Aceite e formalização devem ser combinados com o responsável comercial.`,
    },
    conversa: {
      title: "Preparar uma conversa",
      desc: "Contexto, uma pergunta útil e um próximo passo.",
      note: "O texto é um ponto de partida editável. Copiar ou baixar não envia mensagem e não altera a etapa do CRM.",
      fields: () =>
        common() +
        field(
          "consultor",
          "Seu nome",
          "text",
          "",
          false,
          'required maxlength="160"',
        ) +
        `<label class="field">Momento da conversa<select id="momento" name="momento"><option value="primeiro">Primeiro contato</option><option value="retorno">Retomar conversa</option><option value="demo">Convidar para demonstração</option></select></label>` +
        area(
          "contexto",
          "Contexto ou necessidade do cliente",
          "",
          'required maxlength="3000"',
        ) +
        area(
          "mensagem",
          "Mensagem para revisar antes de usar",
          "",
          'required maxlength="10000"',
        ) +
        '<button class="btn" type="button" id="suggest-message">Montar texto com estes dados</button>',
      build: (v) =>
        v.mensagem.trim() ||
        "Preencha a mensagem ou use “Montar texto com estes dados”.",
    },
    implantacao: {
      title: "Planejar implantação",
      desc: "Combine responsáveis e confira cada etapa da preparação.",
      note: "Este checklist registra a conferência da equipe. O rascunho fica neste navegador; não assina termos nem altera registros do servidor.",
      fields: () =>
        common() +
        field("data", "Data prevista", "date") +
        `<div class="wide checklist-items">${checks.map((s, i) => `<label><input name="check${i}" type="checkbox">${s}</label>`).join("")}</div>` +
        area("pendencias", "Pendências, responsáveis e próximos passos"),
      build: (v) =>
        `PLANO DE IMPLANTAÇÃO\nEmpresa: ${v.cliente}\nResponsável: ${v.responsavel || "A definir"}\nData prevista: ${v.data ? v.data.split("-").reverse().join("/") : "A definir"}\n\n${checks.filter((_, i) => v["check" + i]).length} de ${checks.length} conferências concluídas\n\n${checks.map((s, i) => `${v["check" + i] ? "[x]" : "[ ]"} ${s}`).join("\n")}\n\nPendências\n${v.pendencias || "Nenhuma registrada."}`,
    },
    xml: {
      title: "Ler arquivo XML",
      desc: "Confira o conteúdo do documento sem enviar o arquivo.",
      note: "Leitura local de NF-e/NFC-e. Não verifica autorização, assinatura, alíquotas ou conformidade tributária.",
      fields: () =>
        '<label class="field wide">Arquivo XML (até 2 MB)<input id="xml-file" type="file" accept=".xml,text/xml,application/xml"></label>' +
        area("xml", "Ou cole o conteúdo do XML", "", "required"),
      build: (v) => {
        if (v.xml.length > 2097152)
          throw Error("O XML excede 2 MB. Selecione um arquivo menor.");
        if (/<!DOCTYPE|<!ENTITY/i.test(v.xml))
          throw Error(
            "O arquivo contém declarações externas. Use o XML original da nota, sem entidades externas.",
          );
        const doc = new DOMParser().parseFromString(v.xml, "application/xml");
        if (doc.querySelector("parsererror"))
          throw Error(
            "Não foi possível ler este XML. Confira se o arquivo está completo.",
          );
        const all = (root, tag) => [...root.getElementsByTagNameNS("*", tag)],
          text = (root, tag) =>
            all(root, tag)[0]?.textContent || "Não informado",
          inf = all(doc, "infNFe")[0];
        if (!inf)
          throw Error(
            "Não foi encontrada uma NF-e ou NFC-e neste arquivo. Selecione o XML da nota.",
          );
        const emit = all(inf, "emit")[0],
          dest = all(inf, "dest")[0],
          items = all(inf, "det"),
          total = all(inf, "ICMSTot")[0];
        return `LEITURA DO XML\nDocumento: ${inf.getAttribute("Id") || "Sem identificador"}\nEmitente: ${emit ? text(emit, "xNome") : "Não informado"}\nCNPJ emitente: ${emit ? text(emit, "CNPJ") : "Não informado"}\nDestinatário: ${dest ? text(dest, "xNome") : "Não informado"}\nTotal declarado: ${total ? text(total, "vNF") : "Não informado"}\n\n${items.length} itens\n${items.map((i) => `${text(i, "xProd")} · Quantidade: ${text(i, "qCom")} · Valor: ${text(i, "vProd")}`).join("\n")}\n\nValores transcritos do arquivo, sem auditoria fiscal ou consulta à SEFAZ.`;
      },
    },
    prompter: {
      title: "Teleprompter",
      desc: "Seu roteiro, no ritmo da sua leitura.",
      note: "Cole o texto que deseja gravar. A ferramenta apenas exibe e rola o roteiro; não grava câmera nem microfone.",
      fields: () =>
        area("roteiro", "Roteiro", "", 'required maxlength="30000"') +
        field(
          "velocidade",
          "Velocidade (pixels por segundo)",
          "range",
          "25",
          false,
          'min="5" max="100"',
        ) +
        field(
          "tamanho",
          "Tamanho do texto",
          "range",
          "30",
          false,
          'min="20" max="60"',
        ),
      build: (v) => v.roteiro,
    },
    demo: {
      title: "Demonstração de caixa",
      desc: "Um exemplo simples para explicar o fluxo de uma venda.",
      note: "Ambiente didático com produtos fictícios. Não emite documento fiscal, processa pagamento ou testa equipamentos.",
      fields: () =>
        '<div class="wide demo-products"><button class="btn" type="button" data-product="0">Café · R$ 18,00</button><button class="btn" type="button" data-product="1">Arroz · R$ 24,00</button><button class="btn" type="button" data-product="2">Leite · R$ 6,00</button></div><ul id="cart" class="wide cart-list"></ul>',
      build: () => {
        if (!cart.some(Boolean))
          throw Error("Adicione um produto para experimentar a venda.");
        return `VENDA SIMULADA\nSem valor fiscal\n\n${products
          .map((p, i) =>
            cart[i] ? `${cart[i]} × ${p[0]} · ${money(cart[i] * p[1])}` : "",
          )
          .filter(Boolean)
          .join(
            "\n",
          )}\n\nTotal: ${money(products.reduce((s, p, i) => s + p[1] * cart[i], 0))}\n\nDemonstração concluída. Nenhum pagamento foi processado.`;
      },
    },
  };
  const def = definitions[kind];
  if (!def) return;
  const products = [
      ["Café", 18],
      ["Arroz", 24],
      ["Leite", 6],
    ],
    cart = [0, 0, 0];
  $("work-title").textContent = def.title;
  $("work-desc").textContent = def.desc;
  $("work-notice").textContent = def.note;
  $("fields").innerHTML = def.fields();
  document.title = def.title + " · TruData";
  const form = $("work-form");
  let output = "",
    timer,
    frame = 0,
    last = 0,
    running = false;
  const values = () => Object.fromEntries(new FormData(form));
  const toast = (s) => {
    $("work-toast").textContent = s;
    $("work-toast").hidden = false;
    clearTimeout(timer);
    timer = setTimeout(() => ($("work-toast").hidden = true), 4000);
  };
  function clearError() {
    $("work-error").hidden = true;
  }
  function fail(s) {
    $("work-error").textContent = s;
    $("work-error").hidden = false;
  }
  function stale() {
    output = "";
    $("result").hidden = true;
    $("result-empty").hidden = false;
    if ($("prompter")) $("prompter").hidden = true;
    document
      .querySelectorAll("[data-output]")
      .forEach((b) => (b.disabled = true));
    stop();
  }
  function generate() {
    clearError();
    if (!form.reportValidity()) return false;
    try {
      output = def.build(values());
      $("result").textContent = output;
      $("result").hidden = false;
      $("result-empty").hidden = true;
      document
        .querySelectorAll("[data-output]")
        .forEach((b) => (b.disabled = false));
      if (kind === "prompter") {
        $("result").hidden = true;
        $("prompter").textContent = output;
        $("prompter").hidden = false;
        $("prompter").scrollTop = 0;
      }
      return true;
    } catch (e) {
      stale();
      fail(e.message);
      return false;
    }
  }
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (generate()) toast("Resumo atualizado");
  });
  form.addEventListener("input", (e) => {
    if (["velocidade", "tamanho"].includes(e.target.id)) {
      if ($("prompter"))
        $("prompter").style.fontSize = $("tamanho").value + "px";
      return;
    }
    stale();
    clearError();
  });
  $("copy-result").addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(output);
      toast("Copiado");
    } catch {
      fail("Não foi possível copiar. Selecione o resumo e use Ctrl+C.");
    }
  });
  $("download-result").addEventListener("click", () => {
    const url = URL.createObjectURL(
        new Blob([output], { type: "text/plain;charset=utf-8" }),
      ),
      a = document.createElement("a");
    a.href = url;
    a.download = "trudata-" + kind + ".txt";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    toast("Arquivo gerado");
  });
  $("print-result").addEventListener("click", () => window.print());
  const key = "trudata-oficina-v1-" + kind;
  $("save-draft").addEventListener("click", () => {
    try {
      localStorage.setItem(key, JSON.stringify(values()));
      toast("Rascunho salvo neste navegador");
    } catch {
      fail(
        "Não foi possível salvar neste navegador. Baixe o resumo para guardar o conteúdo.",
      );
    }
  });
  $("load-draft").addEventListener("click", () => {
    try {
      const data = JSON.parse(localStorage.getItem(key) || "null");
      if (!data) {
        toast("Nenhum rascunho salvo");
        return;
      }
      for (const el of form.elements) {
        if (!el.name) continue;
        if (el.type === "checkbox") el.checked = Boolean(data[el.name]);
        else el.value = data[el.name] ?? "";
      }
      stale();
      toast("Rascunho recuperado");
    } catch {
      fail("O rascunho não pôde ser lido. Preencha os dados novamente.");
    }
  });
  const params = new URLSearchParams(location.search);
  for (const id of ["cliente", "cidade", "responsavel"]) {
    const value = params.get(id === "responsavel" ? "decisor" : id);
    if (value && $(id)) $(id).value = value;
  }
  $("suggest-message")?.addEventListener("click", () => {
    const v = values();
    if (!v.cliente?.trim() || !v.consultor?.trim() || !v.contexto?.trim()) {
      fail("Informe empresa, seu nome e o contexto para montar a mensagem.");
      return;
    }
    const hello = `Olá${v.responsavel ? ", " + v.responsavel : ""}! Sou ${v.consultor}, da TruData.`;
    const templates = {
      primeiro: `${hello} Gostaria de entender como vocês cuidam de ${v.contexto} na ${v.cliente}. Faz sentido conversarmos sobre isso?`,
      retorno: `${hello} Retomando nossa conversa sobre ${v.contexto} na ${v.cliente}: ficou alguma dúvida que eu possa ajudar a esclarecer?`,
      demo: `${hello} Podemos preparar uma demonstração focada em ${v.contexto} para a equipe da ${v.cliente}. Qual horário seria bom para vocês?`,
    };
    $("mensagem").value = templates[v.momento];
    stale();
    clearError();
    generate();
  });
  $("xml-file")?.addEventListener("change", async (e) => {
    const f = e.target.files[0];
    if (!f) return;
    stale();
    if (f.size > 2097152) {
      fail("O arquivo excede 2 MB. Selecione um XML menor.");
      return;
    }
    try {
      $("xml").value = await f.text();
      generate();
    } catch {
      fail("O arquivo não pôde ser lido. Selecione-o novamente.");
    }
  });
  if (kind === "xml") {
    $("save-draft").hidden = true;
    $("load-draft").hidden = true;
    form.querySelector(".work-help").hidden = true;
  }
  function stop() {
    running = false;
    cancelAnimationFrame(frame);
    if ($("play")) $("play").textContent = "Iniciar leitura";
  }
  if (kind === "prompter") {
    let scrollPosition = 0;
    $("output-special").innerHTML =
      '<div class="prompter" id="prompter" tabindex="0" aria-label="Área de leitura" hidden></div><div class="actions"><button class="btn" id="play" data-output disabled>Iniciar leitura</button><button class="btn" id="rewind" data-output disabled>Voltar ao início</button></div>';
    const tick = (t) => {
      if (!running) return;
      if (last) {
        scrollPosition += ((t - last) / 1000) * Number($("velocidade").value);
        $("prompter").scrollTop = scrollPosition;
      }
      last = t;
      if (
        $("prompter").scrollTop + $("prompter").clientHeight >=
        $("prompter").scrollHeight - 1
      ) {
        stop();
        toast("Leitura concluída");
        return;
      }
      frame = requestAnimationFrame(tick);
    };
    $("play").addEventListener("click", () => {
      if (running) {
        stop();
        return;
      }
      running = true;
      last = 0;
      scrollPosition = $("prompter").scrollTop;
      $("play").textContent = "Pausar leitura";
      frame = requestAnimationFrame(tick);
    });
    $("rewind").addEventListener("click", () => {
      stop();
      $("prompter").scrollTop = 0;
    });
  }
  if (kind === "demo") {
    $("save-draft").hidden = true;
    $("load-draft").hidden = true;
    form.querySelector(".work-help").hidden = true;
    const draw = () => {
      $("cart").innerHTML =
        products
          .map((p, i) =>
            cart[i]
              ? `<li><span>${p[0]} · ${cart[i]} un. · ${money(p[1] * cart[i])}</span><button class="btn" type="button" data-remove="${i}" aria-label="Remover uma unidade de ${p[0]}">Remover</button></li>`
              : "",
          )
          .join("") || "<li>Adicione um produto para começar.</li>";
      stale();
    };
    form.addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b) return;
      if (b.dataset.product !== undefined) {
        cart[+b.dataset.product]++;
        draw();
      }
      if (b.dataset.remove !== undefined) {
        cart[+b.dataset.remove] = Math.max(0, cart[+b.dataset.remove] - 1);
        draw();
      }
    });
    draw();
    $("generate").textContent = "Concluir venda simulada";
  }
})();
