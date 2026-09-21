/* Interface compartilhada. Conteúdo e IDs originais permanecem nos arquivos de dados. */
(() => {
  "use strict";
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker
      .getRegistration()
      .then((registration) => registration?.update())
      .catch(() => {});
  }
  const $ = (id) => document.getElementById(id);
  const esc = (value) =>
    String(value ?? "").replace(
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
  const normalize = (value) =>
    String(value ?? "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase();
  const paths = {
    check: '<path d="m5 12 4 4L19 6"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    calendar:
      '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 3v4m10-4v4M3 10h18"/>',
    grid: '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    download: '<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>',
    copy: '<rect x="8" y="8" width="12" height="13" rx="2"/><path d="M16 8V3H3v13h5"/>',
    close: '<path d="m6 6 12 12M6 18 18 6"/>',
    left: '<path d="m14 5-7 7 7 7"/>',
    right: '<path d="m10 5 7 7-7 7"/>',
    publish: '<path d="M12 16V3m-5 5 5-5 5 5M4 15v6h16v-6"/>',
    chat: '<path d="M21 11a9 9 0 0 1-9 9H4l-3 2 2-7a9 9 0 1 1 18-4Z"/>',
    image:
      '<rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8" cy="8" r="1"/><path d="m3 17 6-6 5 5 3-3 4 4"/>',
    edit: '<path d="m14 4 6 6M3 21l6-2L21 7l-4-4L5 15z"/>',
    external: '<path d="M14 3h7v7m0-7L10 14M10 3H3v18h18v-7"/>',
  };
  const icon = (name) =>
    `<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">${paths[name] || paths.image}</svg>`;
  document
    .querySelectorAll("[data-icon]")
    .forEach((el) => (el.outerHTML = icon(el.dataset.icon)));
  const statuses = {
    pendente: ["Pendente", "clock"],
    aprovado: ["Aprovado", "check"],
    publicado: ["Publicado", "publish"],
    ajuste: ["Em ajuste", "edit"],
    planejado: ["Planejado", "clock"],
    gravado: ["Gravado", "image"],
    edicao: ["Em edição", "edit"],
    agendado: ["Agendado", "calendar"],
  };
  const badge = (status) =>
    `<span class="badge ${esc(status)}">${icon(statuses[status]?.[1] || "clock")}${esc(statuses[status]?.[0] || "Pendente")}</span>`;
  const img = (post) => "/conteudo_pronto/" + encodeURIComponent(post.imagem);
  const toastElement = $("toast");
  let toastTimer;
  function toast(message) {
    $("toast").textContent = message;
    $("toast").hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      $("toast").hidden = true;
    }, 4500);
  }
  function error(message) {
    $("error").textContent = message;
    $("error").hidden = false;
    if (dialog.open) {
      let banner = dialog.querySelector(".dialog-error");
      if (!banner) {
        banner = document.createElement("div");
        banner.className = "error-banner dialog-error";
        banner.setAttribute("role", "alert");
        dialog.querySelector(".dialog-head").after(banner);
      }
      banner.textContent = message;
      dialog.scrollTop = 0;
    }
  }
  function read(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch {
      error(
        "Não foi possível ler as alterações salvas. Os conteúdos originais estão disponíveis; confira o armazenamento do navegador antes de continuar.",
      );
      return fallback;
    }
  }
  function save(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch {
      error(
        "O navegador não conseguiu salvar a alteração. Libere espaço ou permita o armazenamento e tente novamente.",
      );
      return false;
    }
  }
  async function copy(text) {
    try {
      await navigator.clipboard.writeText(text);
      toast("Copiado");
    } catch {
      error(
        "Não foi possível copiar. Selecione o texto da pauta e use Ctrl+C.",
      );
    }
  }
  function download(name, content, type = "text/plain;charset=utf-8") {
    const url = URL.createObjectURL(new Blob([content], { type }));
    const a = document.createElement("a");
    a.href = url;
    a.download = name;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  let opener;
  const dialog = $("detail");
  dialog.addEventListener("keydown", (e) => {
    if (e.key !== "Tab") return;
    const focusable = [
      ...dialog.querySelectorAll(
        'button:not(:disabled),a[href],input:not(:disabled),select:not(:disabled),textarea:not(:disabled),[tabindex="0"]',
      ),
    ].filter((el) => el.getClientRects().length);
    const first = focusable[0],
      last = focusable.at(-1);
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last?.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first?.focus();
    }
  });
  function showDialog(html) {
    if (!dialog.open) opener = document.activeElement;
    document.body.append(toastElement);
    dialog.innerHTML = html;
    dialog.append(toastElement);
    if (!dialog.open) dialog.showModal();
    document.body.style.overflow = "hidden";
    dialog.scrollTop = 0;
    dialog.querySelector("[data-close]")?.focus();
  }
  function closeDialog() {
    dialog.close();
  }
  dialog.addEventListener("close", () => {
    document.body.append(toastElement);
    document.body.style.overflow = "";
    if (opener?.isConnected) opener.focus();
    else
      document.querySelector(".tabs button[aria-pressed=true],#month")?.focus();
  });
  dialog.addEventListener("click", (e) => {
    if (e.target.closest("[data-close]")) closeDialog();
    if (e.target === dialog) {
      const r = dialog.getBoundingClientRect();
      if (
        e.clientX < r.left ||
        e.clientX > r.right ||
        e.clientY < r.top ||
        e.clientY > r.bottom
      )
        closeDialog();
    }
  });
  const dialogHead = (title, meta = "") =>
    `<header class="dialog-head"><div>${meta}<h2 id="dialog-title">${esc(title)}</h2></div><button class="btn icon-only" data-close aria-label="Fechar detalhes">${icon("close")}</button></header>`;
  const savedPosts = read("trudata_posts_marketing", []);
  const posts = POSTS_INICIAIS.map((p) => ({
    ...p,
    status:
      (Array.isArray(savedPosts) &&
        savedPosts.find((s) => s.id === p.id && statuses[s.status])?.status) ||
      p.status,
  }));
  let serverReady = false;
  let revision = 0;
  async function loadSharedStatus() {
    try {
      const res = await fetch("/api/status");
      if (!res.ok) return;
      const data = await res.json();
      if (
        !data ||
        typeof data !== "object" ||
        data.offline ||
        data.sucesso === false
      )
        return;
      serverReady = true;
      if (revision) return;
      posts.forEach((p) => {
        if (statuses[data[p.id]]) p.status = data[p.id];
      });
      if (document.body.dataset.page === "index") renderPosts();
      $("storage-note").textContent =
        "Status compartilhados na rede · cópia neste navegador";
    } catch {
      /* A versão estática usa armazenamento local. */
    }
  }
  async function setPostStatus(id, status) {
    const post = posts.find((p) => p.id === id);
    if (!post) return;
    const updated = posts.map((p) => (p.id === id ? { ...p, status } : p));
    if (!save("trudata_posts_marketing", updated)) return;
    post.status = status;
    revision++;
    renderPosts();
    if (!dialog.open) {
      (
        document.querySelector(`[data-detail="${CSS.escape(id)}"]`) ||
        document.querySelector('.tabs button[aria-pressed="true"]')
      )?.focus({ preventScroll: true });
    }
    toast(
      status === "ajuste"
        ? "Reprovado · enviado para ajuste"
        : statuses[status][0],
    );
    if (dialog.open) openPost(id);
    if (serverReady) {
      try {
        const r = await fetch("/api/status", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ id, status }),
        });
        if (!r.ok) throw new Error();
        const result = await r.json();
        if (result.offline || result.sucesso === false) throw new Error();
      } catch {
        error(
          "Alteração salva neste navegador, mas não sincronizada na rede. Verifique o servidor e repita a ação para sincronizar.",
        );
      }
    }
  }
  function postActions(p) {
    return `<div class="post-actions">${p.status !== "aprovado" && p.status !== "publicado" ? `<button class="btn primary" data-status="aprovado" data-id="${esc(p.id)}">${icon("check")}Aprovar</button>` : ""}${p.status !== "publicado" ? `<button class="btn ${p.status === "aprovado" ? "primary" : ""}" data-status="publicado" data-id="${esc(p.id)}">${icon("publish")}Marcar publicado</button>` : ""}${p.status !== "ajuste" ? `<button class="btn danger" data-status="ajuste" data-id="${esc(p.id)}">${icon("close")}Reprovar</button>` : `<button class="btn" data-status="pendente" data-id="${esc(p.id)}">Reabrir revisão</button>`}</div>`;
  }
  let activeStatus = "";
  function renderPosts() {
    const counts = Object.fromEntries(
      ["pendente", "aprovado", "publicado", "ajuste"].map((s) => [
        s,
        posts.filter((p) => p.status === s).length,
      ]),
    );
    $("stats").innerHTML = ["pendente", "aprovado", "publicado"]
      .map(
        (s) =>
          `<div class="stat"><strong>${counts[s]}</strong><span>${icon(statuses[s][1])}${{ pendente: "Pendentes", aprovado: "Aprovados", publicado: "Publicados" }[s]}</span></div>`,
      )
      .join("");
    $("status-tabs").innerHTML = [
      ["", "Todos"],
      ["pendente", "Pendentes"],
      ["aprovado", "Aprovados"],
      ["publicado", "Publicados"],
      ["ajuste", "Em ajuste"],
    ]
      .map(
        ([s, label]) =>
          `<button data-filter="${s}" aria-pressed="${activeStatus === s}">${label} <span class="small">${s ? counts[s] : posts.length}</span></button>`,
      )
      .join("");
    const search = normalize($("search").value);
    const channel = $("channel").value;
    const filtered = posts.filter(
      (p) =>
        (!activeStatus || p.status === activeStatus) &&
        (!channel || p.canal === channel) &&
        normalize(p.titulo + " " + p.legenda + " " + p.pilar).includes(search),
    );
    $("result-count").textContent =
      `${filtered.length} de ${posts.length} publicações`;
    $("posts").innerHTML = filtered.length
      ? filtered
          .map(
            (p) =>
              `<article class="post"><button class="image-button" data-detail="${esc(p.id)}" aria-label="Ver detalhes: ${esc(p.titulo)}"><img src="${img(p)}" alt="Arte de referência: ${esc(p.titulo)}" loading="lazy" width="1024" height="1024"><span class="image-label">${icon("image")} Ver detalhes</span></button><div class="post-content"><div class="post-meta"><span>${esc(p.canal)}</span>${badge(p.status)}</div><h3>${esc(p.titulo)}</h3><p class="excerpt">${esc(p.legenda)}</p><span class="small muted">${esc(p.pilar)}</span>${postActions(p)}</div></article>`,
          )
          .join("")
      : `<div class="empty"><h2>${activeStatus === "pendente" && !search && !channel ? "Tudo revisado por aqui." : "Nenhuma publicação nesta seleção."}</h2><p>${activeStatus === "pendente" ? "Veja os aprovados ou prepare as próximas publicações." : "Experimente outro canal ou limpe os filtros para ver a fila completa."}</p><button class="btn" data-reset>Ver todas as publicações</button></div>`;
    $("diagnostic").innerHTML =
      `<header><h2>Seus canais</h2><p class="small muted">Um retrato da fila de conteúdo.</p></header>` +
      ["Instagram", "Facebook"]
        .map((c) => {
          const items = posts.filter((p) => p.canal === c),
            published = items.filter((p) => p.status === "publicado").length;
          return `<section class="channel"><h3>${c}<a href="${c === "Instagram" ? "https://www.instagram.com/trudata_/" : "https://www.facebook.com/trudata.BR/"}" target="_blank" rel="noopener" aria-label="Abrir ${c}">${icon("external")}</a></h3><p>${c === "Instagram" ? "@trudata_" : "trudata.BR"}</p><strong class="number">${published}<span class="small muted"> / ${items.length}</span></strong><p>publicações marcadas como publicadas</p><progress max="${Math.max(1, items.length)}" value="${published}" aria-label="${published} de ${items.length} publicações no ${c}"></progress><p>${items.length ? "Prioridade: revisar as pautas e manter a frequência." : "Ainda sem pautas neste canal. Planeje o próximo conteúdo."}</p></section>`;
        })
        .join("") +
      `<section class="rail-note"><h3>Proximidade é a nossa marca.</h3><p>Mostre quem atende, compartilhe a rotina do comércio e dê espaço às histórias de Sarandi.</p><a href="calendario.html">Consultar o calendário</a></section><p class="small muted">Alcance e seguidores: sem medição registrada. Os números acima são da fila, não das redes sociais.</p>`;
  }
  function openPost(id) {
    const p = posts.find((p) => p.id === id);
    if (!p) return;
    showDialog(
      dialogHead(
        p.titulo,
        `${badge(p.status)} <span class="small muted">${esc(p.canal)} · ${esc(p.data)}</span>`,
      ) +
        `<div class="dialog-body detail-grid"><div><img class="detail-image" src="${img(p)}" alt="Arte de referência: ${esc(p.titulo)}"><p class="small muted">Arte de referência do acervo. Confira sua relação com a pauta antes de publicar.</p></div><div class="detail-copy"><h3>Legenda pronta</h3><p class="prose">${esc(p.legenda)}</p><button class="btn" data-copy-post="${esc(p.id)}">${icon("copy")}Copiar legenda</button><h3>Orientação de produção</h3><p class="prose">${esc(p.briefing)}</p>${p.slides?.length ? `<h3>Sequência sugerida</h3><ol>${p.slides.map((s) => `<li>${esc(s)}</li>`).join("")}</ol>` : ""}<h3>Observações</h3><p class="prose">${esc(p.comentarios || "Revise a arte e a legenda antes de aprovar.")}</p></div></div><footer class="dialog-foot">${postActions(p)}<a class="btn" href="${img(p)}" download>${icon("download")}Baixar arte</a></footer>`,
    );
  }
  if (document.body.dataset.page === "index") {
    $("search").addEventListener("input", renderPosts);
    $("channel").addEventListener("change", renderPosts);
    document.addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b) return;
      if (b.hasAttribute("data-filter")) {
        activeStatus = b.dataset.filter;
        renderPosts();
        document.querySelector(`[data-filter="${activeStatus}"]`).focus();
      }
      if (b.hasAttribute("data-reset")) {
        activeStatus = "";
        $("search").value = "";
        $("channel").value = "";
        renderPosts();
        $("search").focus();
      }
      if (b.dataset.detail) openPost(b.dataset.detail);
      if (b.dataset.status) setPostStatus(b.dataset.id, b.dataset.status);
      if (b.dataset.copyPost)
        copy(posts.find((p) => p.id === b.dataset.copyPost).legenda);
    });
    renderPosts();
    loadSharedStatus();
    window.addEventListener("storage", (e) => {
      if (e.key === "trudata_posts_marketing") {
        const latest = read(e.key, []);
        if (Array.isArray(latest))
          posts.forEach((p) => {
            const s = latest.find((x) => x.id === p.id);
            if (s && statuses[s.status]) p.status = s.status;
          });
        renderPosts();
      }
    });
    return;
  }
  // Calendário: todos os filtros se aplicam à grade, exportações e prévia.
  const stories = DADOS_CALENDARIO.stories_diarios;
  const feeds = DADOS_CALENDARIO.feed_reels;
  let dayStatuses = read("trudata_status_dias", {});
  if (
    !dayStatuses ||
    typeof dayStatuses !== "object" ||
    Array.isArray(dayStatuses)
  )
    dayStatuses = {};
  const storyText = (s) =>
    normalize(
      [
        s.tema,
        s.tela1,
        s.tela2,
        s.tela3,
        feeds[s.data]?.ideia,
        feeds[s.data]?.legenda,
      ].join(" "),
    );
  function pillars(s) {
    const t = storyText(s),
      r = [];
    if (/estoque|caixa|venda|compra|financeir|produto|gestao/.test(t))
      r.push("Gestão e estoque");
    if (/fiscal|nota|contador|contabil|tribut|imposto/.test(t))
      r.push("Fiscal e contabilidade");
    if (/suporte|equipe|atendimento|trudata|hansen/.test(t))
      r.push("Suporte e marca");
    if (s.ocasiao || /comunidade|cidade|gaucho|sarandi/.test(t))
      r.push("Datas e comunidade");
    return r;
  }
  function segments(s) {
    const t = storyText(s),
      r = [];
    if (/loja|comercio|varejo|caixa|estoque|produto|venda/.test(t))
      r.push("Varejo");
    if (/moda|roupa|calcado|confecc|grade/.test(t)) r.push("Moda");
    if (/farmac|medicamento|sngpc/.test(t)) r.push("Farmácia");
    if (/servico|oficina|manutenc|mecanico/.test(t)) r.push("Serviços");
    if (/contador|contabil|fiscal/.test(t)) r.push("Contabilidade");
    return r;
  }
  function matches(s) {
    return (
      (!$("pillar").value || pillars(s).includes($("pillar").value)) &&
      (!$("segment").value || segments(s).includes($("segment").value)) &&
      storyText(s).includes(normalize($("search").value))
    );
  }
  const selected = () =>
    stories.filter(
      (s) => s.data.endsWith("/" + $("month").value) && matches(s),
    );
  let currentDay = 0;
  function renderCalendar() {
    const month = Number($("month").value),
      first = new Date(2026, month - 1, 1).getDay(),
      days = new Date(2026, month, 0).getDate(),
      visible = selected();
    const complete = stories.filter((s) =>
      ["aprovado", "agendado", "publicado"].includes(dayStatuses[s.data]),
    ).length;
    $("total-days").textContent = stories.length;
    $("total-stories").textContent = stories.length * 3;
    $("total-feed").textContent = Object.keys(feeds).length;
    $("progress-label").textContent =
      `${complete} de ${stories.length} dias aprovados ou agendados`;
    $("plan-progress").max = stories.length;
    $("plan-progress").value = complete;
    $("calendar-count").textContent =
      `${visible.length} pautas nesta seleção · ${stories.length} dias planejados no total`;
    $("export-scope").textContent = `${visible.length} dias selecionados`;
    $("previous-month").disabled = month === 9;
    $("next-month").disabled = month === 12;
    let html = Array.from(
      { length: first },
      () => '<div class="day off" aria-hidden="true"></div>',
    ).join("");
    const now = new Date();
    for (let d = 1; d <= days; d++) {
      const date =
        String(d).padStart(2, "0") + "/" + String(month).padStart(2, "0");
      const index = stories.findIndex((s) => s.data === date),
        s = stories[index],
        feed = feeds[date];
      if (!s) {
        html += `<div class="day off"><span class="day-number">${d}</span><span class="small">Fora do plano</span></div>`;
        continue;
      }
      if (!matches(s)) {
        html += `<div class="day filtered"><span class="day-number">${d}</span><span class="small muted">Fora do filtro</span></div>`;
        continue;
      }
      const today =
        now.getFullYear() === 2026 &&
        now.getMonth() === month - 1 &&
        now.getDate() === d;
      html += `<button class="day${today ? " today" : ""}" data-day="${index}" aria-label="${esc(date + " de 2026, " + s.tema + ", " + (statuses[dayStatuses[date] || "planejado"]?.[0] || "Planejado"))}"><span class="day-head"><span class="day-number">${d}</span>${dayStatuses[date] && dayStatuses[date] !== "planejado" ? badge(dayStatuses[date]) : ""}</span><span class="day-title">${esc(s.tema || s.tela1)}</span>${feed ? `<span class="feed-tag">${esc(feed.tipo)}</span>` : ""}<span class="day-time">08:00 · 3 Stories</span></button>`;
    }
    const padding = (7 - ((first + days) % 7)) % 7;
    html += Array.from(
      { length: padding },
      () => '<div class="day off" aria-hidden="true"></div>',
    ).join("");
    $("calendar-grid").innerHTML = html;
    $("calendar-empty").hidden = visible.length > 0;
    $("calendar-empty").innerHTML =
      '<div class="empty"><h2>Nenhuma pauta nesta seleção.</h2><p>Escolha outro mês ou limpe os filtros para encontrar seu conteúdo.</p><button class="btn" data-clear-calendar>Limpar filtros</button></div>';
    document
      .querySelectorAll("[data-export]")
      .forEach((b) => (b.disabled = !visible.length));
  }
  function dayText(s) {
    const f = feeds[s.data];
    return `${s.data}/2026 · ${s.tema}\n\nStories · 08:00\nVisual: ${s.visual}\n\nTela 1\n${s.tela1}\n\nTela 2\n${s.tela2}\n\nTela 3\n${s.tela3}\n${s.opcoes_enquete?.length ? "\nEnquete: " + s.opcoes_enquete.join(" / ") : ""}${f ? "\n\n" + f.tipo + " · " + f.ideia + "\n\nRoteiro\n" + f.producao + "\n\nMaterial\n" + f.material + "\n\nLegenda\n" + f.legenda + "\n\nChamada\n" + f.chamada : ""}`;
  }
  function openDay(index) {
    if (index < 0 || index >= stories.length) return;
    currentDay = index;
    const s = stories[index],
      f = feeds[s.data];
    showDialog(
      dialogHead(
        s.tema || s.tela1,
        `<span class="small muted">${esc(s.data)}/2026 · ${esc(s.dia_semana)}</span>`,
      ) +
        `<div class="dialog-body"><div class="section-line"><div><h3>Stories · 08:00</h3><p class="small muted">Visual: ${esc(s.visual)}</p></div><label class="field">Etapa da produção<select id="day-status">${["planejado", "gravado", "edicao", "aprovado", "agendado", "publicado"].map((v) => `<option value="${v}"${(dayStatuses[s.data] || "planejado") === v ? " selected" : ""}>${statuses[v][0]}</option>`).join("")}</select></label></div><div class="stories">${[1, 2, 3].map((n) => `<section class="story"><div class="story-steps" aria-hidden="true">${[1, 2, 3].map((i) => `<span class="${i === n ? "current" : ""}"></span>`).join("")}</div><small>TruData · ${n === 1 ? "Abertura" : n === 2 ? "Conteúdo" : "Interação"}</small><p>${esc(s["tela" + n])}</p>${n === 3 && s.opcoes_enquete?.length ? `<div class="poll"><strong class="small">Enquete</strong>${s.opcoes_enquete.map((o) => `<button data-poll aria-pressed="false">${esc(o)}</button>`).join("")}<small>Prévia interativa</small></div>` : ""}<button class="btn" data-copy-story="${n}">${icon("copy")}Copiar tela ${n}</button></section>`).join("")}</div>${f ? `<section class="feed-details"><h3>${esc(f.tipo)} · ${esc(f.ideia)}</h3><div class="detail-grid"><div><h3>Roteiro de produção</h3><p class="prose">${esc(f.producao)}</p><h3>Material</h3><p class="prose">${esc(f.material)}</p><h3>Chamada</h3><p class="prose">${esc(f.chamada)}</p></div><div><h3>Legenda pronta</h3><p class="prose">${esc(f.legenda)}</p><button class="btn" data-copy-feed>${icon("copy")}Copiar legenda</button></div></div></section>` : '<p class="muted">Neste dia, a pauta é dedicada aos Stories.</p>'}</div><footer class="dialog-foot"><div class="actions"><button class="btn icon-only" data-day="${index - 1}" ${index === 0 ? "disabled" : ""} aria-label="Dia anterior">${icon("left")}</button><span class="small muted">Dia ${index + 1} de ${stories.length}</span><button class="btn icon-only" data-day="${index + 1}" ${index === stories.length - 1 ? "disabled" : ""} aria-label="Próximo dia">${icon("right")}</button></div><div class="actions"><button class="btn" data-whatsapp>${icon("chat")}Abrir no WhatsApp</button><button class="btn primary" data-package>${icon("download")}Baixar pacote .txt</button></div></footer>`,
    );
    $("day-status").addEventListener("change", (e) => {
      const next = { ...dayStatuses, [s.data]: e.target.value };
      if (save("trudata_status_dias", next)) {
        dayStatuses = next;
        renderCalendar();
        toast(statuses[e.target.value][0]);
      } else e.target.value = dayStatuses[s.data] || "planejado";
    });
  }
  function openFeed() {
    const feedDays = selected()
      .filter((s) => feeds[s.data])
      .slice(0, 9);
    showDialog(
      dialogHead(
        "Prévia do Instagram",
        '<span class="small muted">Composição 3 × 3 · mês e filtros selecionados</span>',
      ) +
        `<div class="dialog-body feed-preview"><div class="feed-profile"><span class="brand-mark">T</span><div><h3>@trudata_</h3><p class="small muted">TruData ERP · Hansen Software</p></div></div><div class="feed-mosaic">${Array.from(
          { length: 9 },
          (_, i) => {
            const s = feedDays[i];
            if (!s)
              return '<div class="feed-tile" aria-label="Espaço sem pauta de feed"></div>';
            const post = posts.find(
              (p) => p.id === "post-cal-" + s.data.replace("/", "-"),
            );
            return `<button class="feed-tile" data-day="${stories.indexOf(s)}" aria-label="Abrir pauta: ${esc(feeds[s.data].ideia)}">${post ? `<img src="${img(post)}" alt="Arte de referência para ${esc(s.tema)}">` : icon("image")}<span>${esc(s.data)} · ${esc(feeds[s.data].tipo)}</span></button>`;
          },
        ).join(
          "",
        )}</div><p class="small muted" style="margin-top:var(--space-4)">${feedDays.length} pautas na prévia. As artes são referências do acervo, ainda sujeitas à revisão. Passe o mouse, use Tab ou selecione uma peça para abrir a pauta.</p>${!feedDays.length ? "<p>Nenhuma pauta de feed neste filtro. Escolha outro mês ou limpe os filtros.</p>" : ""}</div>`,
    );
  }
  function exportRows() {
    return [
      [
        "Data",
        "Tema",
        "Status",
        "Visual",
        "Story 1",
        "Story 2",
        "Story 3",
        "Enquete",
        "Formato",
        "Roteiro",
        "Material",
        "Legenda",
        "Chamada",
      ],
      ...selected().map((s) => {
        const f = feeds[s.data] || {};
        return [
          s.data + "/2026",
          s.tema,
          statuses[dayStatuses[s.data] || "planejado"]?.[0] || "Planejado",
          s.visual,
          s.tela1,
          s.tela2,
          s.tela3,
          (s.opcoes_enquete || []).join(" / "),
          f.tipo || "",
          f.producao || "",
          f.material || "",
          f.legenda || "",
          f.chamada || "",
        ];
      }),
    ];
  }
  async function exportFile(type, button) {
    const old = button.innerHTML;
    button.disabled = true;
    button.setAttribute("aria-busy", "true");
    button.innerHTML = '<span class="spinner"></span>Gerando';
    try {
      await new Promise((r) => setTimeout(r, 180));
      const name = "trudata-2026-" + $("month").value;
      if (type === "md")
        download(
          name + ".md",
          selected()
            .map((s) => "# " + dayText(s))
            .join("\n\n---\n\n"),
          "text/markdown;charset=utf-8",
        );
      else if (type === "xlsx")
        download(
          name + ".xlsx",
          makeXlsx(exportRows()),
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        );
      else {
        const safe = (v) => (/^[=+@-]/.test(String(v)) ? "'" + v : v);
        const csv = exportRows()
          .map((row) =>
            row
              .map((v) => '"' + String(safe(v)).replaceAll('"', '""') + '"')
              .join(","),
          )
          .join("\r\n");
        download(
          name + (type === "notion" ? "-notion" : "") + ".csv",
          "\uFEFF" + csv,
          "text/csv;charset=utf-8",
        );
      }
      toast(
        type === "notion"
          ? "CSV gerado · importe o arquivo no Notion"
          : "Arquivo gerado",
      );
    } catch {
      error(
        "Não foi possível gerar o arquivo. Tente novamente ou escolha o formato CSV.",
      );
    } finally {
      button.innerHTML = old;
      button.disabled = false;
      button.removeAttribute("aria-busy");
    }
  }
  ["month", "pillar", "segment"].forEach((id) =>
    $(id).addEventListener("change", renderCalendar),
  );
  $("search").addEventListener("input", renderCalendar);
  function clearFilters() {
    ["pillar", "segment", "search"].forEach((id) => ($(id).value = ""));
    renderCalendar();
  }
  $("clear-filters").addEventListener("click", clearFilters);
  $("previous-month").addEventListener("click", () => {
    $("month").value = String(Number($("month").value) - 1).padStart(2, "0");
    renderCalendar();
  });
  $("next-month").addEventListener("click", () => {
    $("month").value = String(Number($("month").value) + 1).padStart(2, "0");
    renderCalendar();
  });
  $("preview-feed").addEventListener("click", openFeed);
  document.addEventListener("click", async (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    if (b.hasAttribute("data-day")) openDay(Number(b.dataset.day));
    if (b.hasAttribute("data-clear-calendar")) clearFilters();
    if (b.hasAttribute("data-copy-story"))
      copy(stories[currentDay]["tela" + b.dataset.copyStory]);
    if (b.hasAttribute("data-copy-feed"))
      copy(feeds[stories[currentDay].data].legenda);
    if (b.hasAttribute("data-poll")) {
      b.parentElement
        .querySelectorAll("button")
        .forEach((el) => el.setAttribute("aria-pressed", String(el === b)));
      toast("Opção selecionada na prévia");
    }
    if (b.hasAttribute("data-package")) {
      const s = stories[currentDay],
        label = b.innerHTML;
      b.disabled = true;
      b.setAttribute("aria-busy", "true");
      b.innerHTML = '<span class="spinner"></span>Gerando pacote';
      try {
        await new Promise((r) => setTimeout(r, 180));
        download(
          "trudata-" + s.data.replace("/", "-") + "-2026.txt",
          dayText(s),
        );
        toast("Pacote gerado");
      } catch {
        error(
          "Não foi possível gerar o pacote. Tente novamente ou copie as telas individualmente.",
        );
      } finally {
        b.innerHTML = label;
        b.disabled = false;
        b.removeAttribute("aria-busy");
      }
    }
    if (b.hasAttribute("data-whatsapp")) {
      const link = document.createElement("a");
      link.href =
        "https://wa.me/?text=" +
        encodeURIComponent(dayText(stories[currentDay]));
      link.target = "_blank";
      link.rel = "noopener";
      link.click();
      toast("Continue no WhatsApp: escolha o contato e envie a pauta.");
    }
    if (b.dataset.export) exportFile(b.dataset.export, b);
  });
  window.addEventListener("storage", (e) => {
    if (e.key === "trudata_status_dias") {
      const data = read(e.key, {});
      if (data && typeof data === "object" && !Array.isArray(data)) {
        dayStatuses = data;
        renderCalendar();
      }
    }
  });
  renderCalendar();

  // XLSX nativo: planilha OOXML com strings explícitas, empacotada em ZIP sem compressão.
  // Não depende de CDN e não interpreta o conteúdo editorial como fórmulas.
  function makeXlsx(rows) {
    const xml = (s) =>
      String(s)
        .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, "")
        .replace(
          /[<>&"]/g,
          (c) => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;" })[c],
        );
    const sheet =
      '<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews><sheetData>' +
      rows
        .map(
          (row, i) =>
            `<row r="${i + 1}">` +
            row
              .map(
                (v, j) =>
                  `<c r="${String.fromCharCode(65 + j)}${i + 1}" t="inlineStr"><is><t xml:space="preserve">${xml(v)}</t></is></c>`,
              )
              .join("") +
            "</row>",
        )
        .join("") +
      `</sheetData><autoFilter ref="A1:M${rows.length}"/></worksheet>`;
    const files = {
      "[Content_Types].xml":
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>',
      "_rels/.rels":
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>',
      "xl/workbook.xml":
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Calendário 2026" sheetId="1" r:id="rId1"/></sheets></workbook>',
      "xl/_rels/workbook.xml.rels":
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>',
      "xl/worksheets/sheet1.xml": sheet,
    };
    const encoder = new TextEncoder(),
      parts = [],
      central = [];
    let offset = 0,
      centralSize = 0;
    const crc32 = (bytes) => {
      let crc = -1;
      for (const b of bytes) {
        crc ^= b;
        for (let i = 0; i < 8; i++)
          crc = (crc >>> 1) ^ (crc & 1 ? 0xedb88320 : 0);
      }
      return (crc ^ -1) >>> 0;
    };
    for (const [name, content] of Object.entries(files)) {
      const n = encoder.encode(name),
        d = encoder.encode(content),
        crc = crc32(d),
        h = new Uint8Array(30),
        v = new DataView(h.buffer);
      v.setUint32(0, 0x04034b50, true);
      v.setUint16(4, 20, true);
      v.setUint32(14, crc, true);
      v.setUint32(18, d.length, true);
      v.setUint32(22, d.length, true);
      v.setUint16(26, n.length, true);
      parts.push(h, n, d);
      const c = new Uint8Array(46),
        cv = new DataView(c.buffer);
      cv.setUint32(0, 0x02014b50, true);
      cv.setUint16(4, 20, true);
      cv.setUint16(6, 20, true);
      cv.setUint32(16, crc, true);
      cv.setUint32(20, d.length, true);
      cv.setUint32(24, d.length, true);
      cv.setUint16(28, n.length, true);
      cv.setUint32(42, offset, true);
      central.push(c, n);
      centralSize += 46 + n.length;
      offset += 30 + n.length + d.length;
    }
    const end = new Uint8Array(22),
      ev = new DataView(end.buffer);
    ev.setUint32(0, 0x06054b50, true);
    ev.setUint16(8, 5, true);
    ev.setUint16(10, 5, true);
    ev.setUint32(12, centralSize, true);
    ev.setUint32(16, offset, true);
    return new Blob([...parts, ...central, end]);
  }
})();
