/* Radar regional: dados existentes, seleção única para lista, mapa e exportação. */
(() => {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const esc = (v) =>
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
  const norm = (v) =>
    String(v ?? "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase();
  const digits = (v) => String(v ?? "").replace(/\D/g, "");
  const icons = {
    download: '<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>',
    briefcase:
      '<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V3h8v4M3 12h18m-9-2v4"/>',
    pin: '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2"/>',
    settings:
      '<path d="M4 6h16M4 12h16M4 18h16"/><circle cx="8" cy="6" r="2"/><circle cx="16" cy="12" r="2"/><circle cx="10" cy="18" r="2"/>',
    mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
    expand: '<path d="M9 3H3v6m12-6h6v6M3 15v6h6m6 0h6v-6"/>',
    search: '<circle cx="10" cy="10" r="7"/><path d="m16 16 5 5"/>',
    list: '<path d="M8 5h13M8 12h13M8 19h13M3 5h1M3 12h1M3 19h1"/>',
    grid: '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>',
    copy: '<rect x="8" y="8" width="12" height="13" rx="2"/><path d="M16 8V3H3v13h5"/>',
    route:
      '<circle cx="5" cy="5" r="2"/><circle cx="19" cy="19" r="2"/><path d="M7 5h9a4 4 0 0 1 0 8H8a3 3 0 0 0 0 6h9"/>',
    plus: '<path d="M12 4v16M4 12h16"/>',
    check: '<path d="m5 12 4 4L19 6"/>',
    close: '<path d="m6 6 12 12M6 18 18 6"/>',
    right: '<path d="m9 5 7 7-7 7"/>',
    external: '<path d="M14 3h7v7m0-7L10 14M10 3H3v18h18v-7"/>',
    chat: '<path d="M21 11a9 9 0 0 1-9 9H4l-3 2 2-7a9 9 0 1 1 18-4Z"/>',
    phone:
      '<path d="m6 3 4 5-3 3a17 17 0 0 0 6 6l3-3 5 4c0 4-5 4-8 2C6 16 2 9 3 5Z"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
  };
  const icon = (n) =>
    `<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">${icons[n] || icons.briefcase}</svg>`;
  document
    .querySelectorAll("[data-icon]")
    .forEach((el) => (el.outerHTML = icon(el.dataset.icon)));
  const phases = {
    novo: ["No CRM · novo", "new", "briefcase"],
    contato: ["Contato iniciado", "progress", "chat"],
    demo: ["Demonstração", "scheduled", "clock"],
    proposta: ["Proposta em negociação", "progress", "briefcase"],
    contatado_whatsapp: ["Contato iniciado", "progress", "chat"],
    email_enviado: ["E-mail enviado", "progress", "mail"],
    demo_agendada: ["Demonstração agendada", "scheduled", "clock"],
    fechado: ["Cliente conquistado", "won", "check"],
    recontato: ["Recontato (6m - 1 ano)", "scheduled", "clock"],
    perdido: ["Sem interesse", "lost", "close"],
  };
  const state = {
    all: [],
    filtered: [],
    selected: new Set(),
    crm: new Map(),
    crmLoaded: false,
    ready: false,
    queue: "all",
    view: "list",
    limit: 30,
    request: 0,
    controller: null,
    company: null,
  };
  let map, markers, radiusCircle, tileLayer, toastTimer, returnFocus;
  let cityPoints = [];
  const dialog = $("radar-detail"),
    toastNode = $("radar-toast");
  function toast(message) {
    toastNode.innerHTML = message;
    toastNode.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => (toastNode.hidden = true), 5500);
  }
  function error(message) {
    if (dialog.open) {
      const el = $("dialog-feedback");
      el.className = "dialog-message error";
      el.textContent = message;
      el.hidden = false;
      dialog.scrollTop = 0;
    } else {
      $("page-error").textContent = message;
      $("page-error").hidden = false;
    }
  }
  async function api(path, body, signal) {
    const response = await fetch(path, {
      signal,
      ...(body !== undefined
        ? {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
          }
        : {}),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    if (data?.offline) throw new Error("Servidor desconectado");
    return data;
  }
  async function copy(value) {
    try {
      await navigator.clipboard.writeText(value);
      toast("Copiado");
    } catch {
      error("Não foi possível copiar. Selecione o texto e use Ctrl+C.");
    }
  }
  function safeUrl(value) {
    try {
      const url = new URL(value);
      return ["https:", "http:"].includes(url.protocol) ? url.href : "";
    } catch {
      return "";
    }
  }
  const external = (url, label, ic = "external") =>
    safeUrl(url)
      ? `<a class="btn" href="${esc(safeUrl(url))}" target="_blank" rel="noopener">${icon(ic)}${esc(label)}</a>`
      : "";
  const nameKey = (p) => norm(p.nome).trim();
  const crmEntry = (p) =>
    state.crm.get(digits(p.cnpj)) || state.crm.get(nameKey(p));
  const inCRM = (p) => Boolean(crmEntry(p));
  const phase = (p) => crmEntry(p)?.fase || "novo";
  function badge(p) {
    if (!state.crmLoaded)
      return '<span class="badge new">CRM indisponível</span>';
    if (!inCRM(p))
      return `<span class="badge new">${icon("plus")}Fora do CRM</span>`;
    const s = phases[phase(p)] || [phase(p), "progress", "briefcase"];
    return `<span class="badge ${s[1]}">${icon(s[2])}${esc(s[0])}</span>`;
  }
  function addLocalCRM(p, fase = "novo") {
    const item = { empresa: p.nome, cnpj: p.cnpj, fase };
    state.crm.set(nameKey(p), item);
    if (digits(p.cnpj)) state.crm.set(digits(p.cnpj), item);
  }
  async function syncCRM() {
    const leads = await api("/api/leads");
    if (!Array.isArray(leads)) throw new Error("Resposta inválida do CRM");
    const fresh = new Map();
    leads.forEach((l) => {
      if (l.empresa) fresh.set(norm(l.empresa).trim(), l);
      if (digits(l.cnpj)) fresh.set(digits(l.cnpj), l);
    });
    state.crm = fresh;
    state.crmLoaded = true;
  }
  function showDialog(title, body, footer = "", meta = "") {
    if (!dialog.open) returnFocus = document.activeElement;
    document.body.append(toastNode);
    dialog.className = "radar-dialog";
    dialog.innerHTML = `<header class="dialog-head"><div><span class="small muted">${esc(meta)}</span><h2 id="dialog-title">${esc(title)}</h2></div><button class="btn icon-only" data-close aria-label="Fechar detalhes">${icon("close")}</button></header><div id="dialog-feedback" class="dialog-message" role="status" hidden></div><div class="dialog-body">${body}</div>${footer ? `<footer class="dialog-foot">${footer}</footer>` : ""}`;
    dialog.append(toastNode);
    if (!dialog.open) dialog.showModal();
    document.body.style.overflow = "hidden";
    dialog.scrollTop = 0;
    dialog.querySelector("[data-close]").focus();
  }
  dialog.addEventListener("close", () => {
    document.body.style.overflow = "";
    document.body.append(toastNode);
    if (returnFocus?.isConnected) returnFocus.focus({ preventScroll: true });
    else $("search").focus({ preventScroll: true });
  });
  dialog.addEventListener("keydown", (e) => {
    if (e.key !== "Tab") return;
    const focusable = [
      ...dialog.querySelectorAll(
        "button:not(:disabled),a[href],input:not(:disabled),select:not(:disabled),textarea:not(:disabled),summary",
      ),
    ].filter((el) => el.getClientRects().length);
    const first = focusable[0],
      last = focusable.at(-1);
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });
  dialog.addEventListener("click", (e) => {
    if (e.target.closest("[data-close]")) dialog.close();
    if (e.target === dialog) {
      const r = dialog.getBoundingClientRect();
      if (
        e.clientX < r.left ||
        e.clientX > r.right ||
        e.clientY < r.top ||
        e.clientY > r.bottom
      )
        dialog.close();
    }
  });
  async function busy(button, fn, label = "Salvando") {
    const original = button.innerHTML;
    button.disabled = true;
    button.setAttribute("aria-busy", "true");
    button.innerHTML = `<span class="spinner"></span>${label}`;
    try {
      await fn();
    } catch (e) {
      error(
        "Não foi possível concluir. Verifique a conexão com o servidor e tente novamente.",
      );
    } finally {
      button.innerHTML = original;
      button.disabled = false;
      button.removeAttribute("aria-busy");
      updateSelection();
    }
  }
  const optionLabels = {
    "sel-origem": "Sarandi · matriz",
    "sel-cidade": "Todas as cidades",
    "sel-segmento": "Todos os segmentos",
    "sel-porte": "Todos os portes",
    "sel-site": "Todos os cadastros",
    "sel-ordenacao": "Mais próximas",
  };
  Object.entries(RADAR_OPTIONS).forEach(([id, options]) => {
    $(id).innerHTML = options
      .map(
        (o, i) =>
          `<option value="${esc(o.value)}">${esc(i === 0 ? optionLabels[id] : o.label.replace(/\([^)]*\)/g, "").trim())}</option>`,
      )
      .join("");
  });
  function requestParams() {
    return new URLSearchParams({
      origem: $("sel-origem").value,
      raio: $("rng-raio").value,
      segmento: $("sel-segmento").value,
      cidade: $("sel-cidade").value,
      porte: $("sel-porte").value,
      site: $("sel-site").value,
      apenas_email: $("chk-email").checked,
      apenas_telefone: $("chk-telefone").checked,
      ordenacao: "distancia",
    });
  }
  async function search() {
    state.controller?.abort();
    state.controller = new AbortController();
    const version = ++state.request;
    state.ready = false;
    state.limit = 30;
    state.selected.clear();
    $("results").setAttribute("aria-busy", "true");
    $("results").innerHTML =
      '<div class="loading"><span class="spinner"></span>Buscando empresas da região</div>';
    updateSelection();
    try {
      const data = await api(
        "/api/prospectar?" + requestParams(),
        undefined,
        state.controller.signal,
      );
      if (version !== state.request) return;
      if (!data.sucesso || !Array.isArray(data.clientes))
        throw new Error("Resposta inválida");
      state.all = data.clientes;
      state.ready = true;
      $("page-error").hidden = true;
      applyFilters();
    } catch (e) {
      if (e.name === "AbortError" || version !== state.request) return;
      state.all = [];
      state.filtered = [];
      renderSummary();
      renderMap();
      $("results").innerHTML =
        '<div class="empty"><h2>A busca não foi carregada.</h2><p>Verifique se o servidor está aberto e tente novamente.</p><button class="btn" data-retry>Buscar novamente</button></div>';
      error(
        "Não foi possível consultar as empresas. Confira a conexão com o servidor local.",
      );
    } finally {
      if (version === state.request) {
        $("results").setAttribute("aria-busy", "false");
        updateSelection();
      }
    }
  }
  function applyFilters() {
    const term = norm($("search").value.trim()),
      numeric = digits(term);
    let list = state.all.filter(
      (p) =>
        !term ||
        norm(
          [
            p.nome,
            p.razao_social,
            p.cidade,
            p.segmento,
            p.decisor,
            p.endereco,
            p.bairro,
            p.email,
            p.telefone,
            p.site,
            p.notas,
            p.cnpj,
          ].join(" "),
        ).includes(term) ||
        (numeric.length >= 3 && digits(p.cnpj).includes(numeric)),
    );
    if (state.queue === "new") list = list.filter((p) => !inCRM(p));
    if (state.queue === "crm") list = list.filter(inCRM);
    const sort = $("sel-ordenacao").value;
    list.sort((a, b) =>
      sort === "score" || state.queue === "top"
        ? (Number(b.lead_score) || 0) - (Number(a.lead_score) || 0)
        : sort === "pdvs"
          ? (Number(b.pdvs_estimados) || 0) - (Number(a.pdvs_estimados) || 0)
          : sort === "nome"
            ? String(a.nome).localeCompare(String(b.nome), "pt-BR")
            : sort === "cidade"
              ? String(a.cidade).localeCompare(String(b.cidade), "pt-BR")
              : (Number(a.distancia_km) || 0) - (Number(b.distancia_km) || 0),
    );
    if (state.queue === "top") list = list.slice(0, 50);
    state.filtered = list;
    const visible = new Set(list.map((p) => p.id));
    state.selected.forEach((id) => {
      if (!visible.has(id)) state.selected.delete(id);
    });
    document.querySelectorAll("[data-queue]").forEach((b) => {
      b.setAttribute("aria-pressed", String(b.dataset.queue === state.queue));
      b.disabled = !state.crmLoaded && ["new", "crm"].includes(b.dataset.queue);
    });
    renderSummary();
    renderResults();
    renderMap();
    updateSelection();
  }
  function renderSummary() {
    const list = state.filtered;
    const stats = [
      [list.length, "Empresas na seleção"],
      [
        state.crmLoaded ? list.filter((p) => !inCRM(p)).length : "—",
        "Fora do CRM",
      ],
      [new Set(list.map((p) => p.cidade)).size, "Cidades"],
      [list.filter((p) => p.whatsapp || p.telefone).length, "Com telefone"],
      [list.filter((p) => p.email).length, "Com e-mail"],
    ];
    $("summary").innerHTML =
      stats
        .map(
          ([count, label]) =>
            `<div class="stat"><strong>${count.toLocaleString("pt-BR")}</strong><span>${label}</span></div>`,
        )
        .join("") +
      '<p class="summary-note">Uma boa conversa começa com o contato certo.</p>';
  }
  function contacts(p) {
    return `<div class="lead-contact">${p.telefone || p.whatsapp ? `<a href="tel:${esc(digits(p.telefone || p.whatsapp))}">${icon("phone")} ${esc(p.telefone || p.whatsapp)}</a>` : '<span class="small muted">Telefone não cadastrado</span>'}${p.email ? `<a href="mailto:${esc(p.email)}">${esc(p.email)}</a>` : '<span class="small muted">E-mail não cadastrado</span>'}</div>`;
  }
  function importButton(p) {
    return `<button class="btn ${inCRM(p) ? "quiet" : ""}" data-import="${esc(p.id)}" ${inCRM(p) ? "disabled" : ""}>${icon(inCRM(p) ? "check" : "plus")}${inCRM(p) ? "No CRM" : "Adicionar ao CRM"}</button>`;
  }
  function score(p) {
    return `<span class="lead-score">Prioridade <strong>${Number.isFinite(Number(p.lead_score)) ? Number(p.lead_score) : "—"}</strong>/100</span>`;
  }
  function renderResults() {
    const list = state.filtered.slice(0, state.limit);
    $("results-count").textContent =
      `${state.filtered.length.toLocaleString("pt-BR")} empresas · ${list.length} exibidas${state.queue === "top" ? " · ordenadas por pontuação" : ""}`;
    $("results").className =
      state.view === "cards" ? "lead-cards" : "lead-list";
    $("results").innerHTML = list.length
      ? list
          .map((p) => {
            const checkbox = `<label class="check-field"><input type="checkbox" data-select="${esc(p.id)}" aria-label="Selecionar ${esc(p.nome)}" ${state.selected.has(p.id) ? "checked" : ""}></label>`;
            const title = `<button class="lead-title" data-company="${esc(p.id)}">${esc(p.nome)}</button><p>${esc(p.segmento)}</p><p>${esc(p.cidade)} · ${Number(p.distancia_km).toLocaleString("pt-BR")} km${located(p) ? " em linha reta" : " estimados · localização pendente"}</p>`;
            return state.view === "list"
              ? `<article class="lead-row ${state.selected.has(p.id) ? "selected" : ""}" data-row="${esc(p.id)}">${checkbox}<div>${title}</div>${contacts(p)}<div class="lead-stage">${badge(p)}${score(p)}</div><button class="btn icon-only open-company" data-company="${esc(p.id)}" aria-label="Ver ${esc(p.nome)}">${icon("right")}</button></article>`
              : `<article class="lead-card ${state.selected.has(p.id) ? "selected" : ""}" data-row="${esc(p.id)}"><header>${checkbox}${badge(p)}</header><div>${title}</div>${score(p)}${contacts(p)}<footer><button class="btn" data-company="${esc(p.id)}">Ver empresa</button>${importButton(p)}</footer></article>`;
          })
          .join("")
      : `<div class="empty"><h2>${state.queue === "new" ? "Nenhuma empresa fora do CRM nesta seleção." : "Nenhuma empresa encontrada."}</h2><p>Amplie o raio ou experimente outro segmento para encontrar novas oportunidades.</p><button class="btn" data-reset>Limpar filtros</button></div>`;
    $("load-more").hidden = list.length >= state.filtered.length;
  }
  function updateSelection() {
    const visible = state.filtered.slice(0, state.limit),
      count = state.selected.size;
    const checked = visible.filter((p) => state.selected.has(p.id)).length;
    $("select-all").checked =
      Boolean(visible.length) && checked === visible.length;
    $("select-all").indeterminate = checked > 0 && checked < visible.length;
    $("select-all").disabled = !state.ready || !visible.length;
    $("selected-count").textContent = count
      ? `${count} selecionada${count === 1 ? "" : "s"}`
      : "Nenhuma selecionada";
    $("clear-selection").disabled = !count;
    $("route").disabled = !state.ready || !count;
    $("bulk-crm").disabled =
      !state.ready ||
      !count ||
      !state.filtered.some((p) => state.selected.has(p.id) && !inCRM(p));
    $("export").disabled = !state.ready || !state.filtered.length;
    $("copy-phones").disabled =
      !state.ready || !state.filtered.some((p) => p.whatsapp || p.telefone);
  }
  function reset() {
    ["sel-cidade", "sel-segmento", "sel-porte", "sel-site"].forEach(
      (id) => ($(id).selectedIndex = 0),
    );
    $("sel-origem").value = "Sarandi";
    $("rng-raio").value = "100";
    $("search").value = "";
    $("sel-ordenacao").value = "distancia";
    $("chk-email").checked = false;
    $("chk-telefone").checked = false;
    state.queue = "all";
    updateRadius();
    search();
  }
  function updateRadius() {
    $("radius-label").textContent = $("rng-raio").value + " km";
    document
      .querySelectorAll("[data-radius]")
      .forEach((b) =>
        b.setAttribute(
          "aria-pressed",
          String(b.dataset.radius === $("rng-raio").value),
        ),
      );
  }
  function cityFilter(city) {
    if (![...$("sel-cidade").options].some((o) => o.value === city))
      $("sel-cidade").add(new Option(city, city));
    $("sel-cidade").value = city;
    search();
  }
  function initMap() {
    if (map) return true;
    if (!window.L) {
      $("map-error").hidden = false;
      return false;
    }
    map = L.map("radar-map", {
      zoomControl: false,
      scrollWheelZoom: false,
    }).setView([-27.9439, -52.9247], 8);
    L.control.zoom({ position: "bottomright" }).addTo(map);
    tileLayer = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors · Powered by <a href="https://www.geoapify.com/">Geoapify</a> · <a href="https://openaddresses.io/">OpenAddresses</a>',
    }).addTo(map);
    tileLayer.on("tileerror", () => {
      $("map-error").hidden = false;
    });
    markers = L.layerGroup().addTo(map);
    map.on("zoomend", renderMarkers);
    return true;
  }
  function groups() {
    const data = new Map();
    state.filtered.forEach((p) => {
      if (!data.has(p.cidade)) data.set(p.cidade, []);
      data.get(p.cidade).push(p);
    });
    return [...data.entries()].sort((a, b) => b[1].length - a[1].length);
  }
  function renderMap() {
    const cities = groups();
    $("cities").innerHTML =
      cities
        .slice(0, 5)
        .map(
          ([city, items]) =>
            `<button class="city-row" data-city="${esc(city)}"><span>${esc(city)}</span><strong>${items.length}</strong></button>`,
        )
        .join("") || '<p class="small muted">Nenhuma cidade nesta seleção.</p>';
    $("territory-label").textContent =
      `${$("sel-origem").value} · raio de ${$("rng-raio").value} km`;
    if (!initMap()) return;
    markers.clearLayers();
    cityPoints = [];
    if (radiusCircle) map.removeLayer(radiusCircle);
    const center =
      COORDENADAS_CIDADES[$("sel-origem").value.toLowerCase()] ||
      COORDENADAS_CIDADES.sarandi;
    const color = getComputedStyle(document.documentElement)
      .getPropertyValue("--color-action")
      .trim();
    radiusCircle = L.circle([center.lat, center.lon], {
      radius: Number($("rng-raio").value) * 1000,
      color,
      weight: 1,
      fillOpacity: 0.03,
      interactive: false,
    }).addTo(map);
    cityPoints = state.filtered.filter(located).map(p => ({...p, lat: Number(p.lat), lon: Number(p.lon)}));
    $("location-count").textContent = `${cityPoints.length} localizadas · ${state.filtered.length - cityPoints.length} pendentes`;
    fitMap();
    renderMarkers();
  }
  function renderMarkers() {
    if (!map || !markers) return;
    markers.clearLayers();
    const clusters = [];
    cityPoints.forEach((point) => {
      const px = map.project([point.lat, point.lon], map.getZoom());
      const cluster = clusters.find(
        (c) => map.getZoom() >= 18 ? c.points[0].lat === point.lat && c.points[0].lon === point.lon : Math.hypot(c.x - px.x, c.y - px.y) < 42,
      );
      if (cluster) cluster.points.push(point);
      else clusters.push({ x: px.x, y: px.y, points: [point] });
    });
    clusters.forEach(({ points }) => {
      const lat = points.reduce((a, p) => a + p.lat, 0) / points.length;
      const lon = points.reduce((a, p) => a + p.lon, 0) / points.length;
      const count = points.length;
      const label = count === 1 ? points[0].nome : `${count} estabelecimentos — amplie para separar`;
      const marker = L.marker([lat, lon], {
        icon: L.divIcon({className: "city-marker", html: count === 1 ? icon("pin") : String(count), iconSize: [34, 34]}),
        title: label, alt: label,
      }).addTo(markers);
      if (count === 1 || map.getZoom() >= 18) marker.bindPopup(
        points.map(p => `<strong>${esc(p.nome)}</strong><p class="small">${esc(locationLabel(p))}</p><p>${esc(p.endereco)} · ${esc(p.cidade)}</p><button class="btn" data-company="${esc(p.id)}">Ver empresa</button>${external(p.geolocalizacao.fonte_url, "Fonte da localização")}`).join("<hr>"), {maxHeight: 230}
      );
      marker.on("popupopen", e => {
        e.popup.getElement().querySelectorAll("[data-company]").forEach(button => {
          button.onclick = event => { event.stopPropagation(); openCompany(button.dataset.company); };
        });
      });
      if (count > 1) marker.on("click", () => {
        if (map.getZoom() < 18) map.fitBounds(L.latLngBounds(points.map(p => [p.lat, p.lon])), {maxZoom: Math.min(18, map.getZoom() + 3), padding: [30,30]});
      });
    });
  }
  function fitMap() {
    if (!map || !radiusCircle) return;
    map.invalidateSize();
    map.fitBounds(cityPoints.length ? L.latLngBounds(cityPoints.map(p => [p.lat, p.lon])) : radiusCircle.getBounds(), {
      maxZoom: 16,
      padding: [18, 18],
      animate: false,
    });
  }
  const located = p => p.geolocalizacao?.status === "localizado" && p.lat != null && p.lon != null && Number.isFinite(Number(p.lat)) && Number.isFinite(Number(p.lon));
  const locationLabel = p => located(p) ? (p.geolocalizacao.precisao === "endereco" ? "Endereço do cadastro localizado" : "Estabelecimento localizado") : "Localização pendente";
  const locationInfo = p => `<p>${locationLabel(p)}</p><p class="prose">${esc(p.geolocalizacao?.observacao || "Confirme o endereço para localizar esta empresa.")}</p>${p.geolocalizacao?.endereco_fonte ? `<p class="prose"><strong>Endereço encontrado:</strong> ${esc(p.geolocalizacao.endereco_fonte)}</p><p class="small">${esc(p.geolocalizacao.fonte?.attribution || "Geoapify")}</p>` : ""}${located(p) ? `<p class="small">Consultado em ${esc(p.geolocalizacao.consultado_em)}. Posição cartográfica; entrada não confirmada.</p><button class="btn" data-locate="${esc(p.id)}">Ver no radar</button>${external(p.geolocalizacao.fonte_url, "Fonte da localização")}` : ""}`;
  const companyById = (id) => state.all.find((p) => p.id === id);
  function toolURL(file, p) {
    return (
      file +
      "?" +
      new URLSearchParams({
        cliente: p.nome || "",
        cidade: p.cidade || "",
        segmento: p.segmento || "",
        cnpj: p.cnpj || "",
        decisor: p.decisor || "",
        telefone: p.whatsapp || p.telefone || "",
        email: p.email || "",
        endereco: p.endereco || "",
        caixas: p.pdvs_estimados || 1,
        distancia: p.distancia_km ?? "",
      })
    );
  }
  function openCompany(id) {
    const p = companyById(id);
    if (!p) return;
    state.company = p;
    const facts = [
      ["CNPJ", p.cnpj],
      ["Razão social", p.razao_social],
      ["Contato no cadastro", p.decisor],
      ["Porte", p.porte],
      [
        "Endereço",
        [p.endereco, p.bairro, p.cidade].filter(Boolean).join(" · "),
      ],
      ["Caixas estimados", p.pdvs_estimados ?? "Não informado"],
    ];
    showDialog(
      p.nome,
      `<div class="company-meta">${badge(p)}${score(p)}</div><div class="dialog-grid"><div><dl class="company-facts">${facts.map(([k, v]) => `<div><dt>${k}</dt><dd>${esc(v || "Não informado")}</dd></div>`).join("")}</dl><div class="company-notes"><h3>Contato</h3>${contacts(p)}${p.site && safeUrl(p.site) ? external(p.site, "Visitar site") : '<p class="small muted">Site não cadastrado.</p>'}</div><div class="company-notes"><h3>Sobre esta oportunidade</h3><p class="prose">${esc(p.notas || "Converse com o responsável para conhecer a operação.")}</p><p class="small muted">Informações do cadastro, sem consulta cadastral em tempo real. A prioridade considera proximidade, segmento, contato e porte; não é uma previsão de venda.</p></div></div><aside class="company-actions"><h3>Próximo passo</h3>${importButton(p)}${p.whatsapp ? external("https://wa.me/" + digits(p.whatsapp) + "?text=" + encodeURIComponent(p.mensagem_whatsapp || ""), "Abrir WhatsApp", "chat") : ""}<button class="btn" data-email="${esc(p.id)}">${icon("mail")}Preparar e-mail</button><a class="btn" href="${esc(toolURL("gerador_proposta.html", p))}" target="_blank" rel="noopener">${icon("briefcase")}Preparar proposta</a><a class="btn" href="${esc(toolURL("copiloto_vendas.html", p))}" target="_blank" rel="noopener">${icon("chat")}Roteiro de conversa</a><label class="field">Etapa no CRM<select id="company-phase">${Object.entries(
        phases,
      )
        .map(
          ([value, [label]]) =>
            `<option value="${value}" ${phase(p) === value ? "selected" : ""}>${label.replace("No CRM · ", "")}</option>`,
        )
        .join(
          "",
        )}</select></label><button class="btn primary" id="save-phase">Salvar etapa</button><p class="small muted">Salvar uma etapa também adiciona a empresa ao CRM.</p></aside></div><div class="company-notes"><h3>Localização e cadastro</h3><div class="actions">${locationInfo(p)}<a class="btn" href="${esc(toolURL(located(p) ? "planejar_visitas.html" : "revisao_enderecos.html", p))}">${located(p) ? "Planejar visita" : "Revisar endereço"}</a>${external(located(p) ? "https://www.google.com/maps/search/?api=1&query=" + p.lat + "," + p.lon : p.link_maps, located(p) ? "Abrir ponto no Google Maps" : "Pesquisar endereço no Google Maps", "pin")}<button class="btn" id="copy-cnpj">${icon("copy")}Copiar CNPJ</button>${external(p.link_sintegra, "Consultar cadastro")}</div></div>`,
      `<a class="btn primary" href="crm_enterprise.html?tab=kanban" target="_blank" style="background:linear-gradient(135deg, #10b981, #059669); border-color:#10b981; font-weight:700; text-decoration:none; display:inline-flex; align-items:center; gap:6px;">🏷️ Abrir no Kanban do CRM</a><button class="btn" data-close>Fechar</button>`,
      `${p.segmento} · ${p.cidade} · ${Number(p.distancia_km).toLocaleString("pt-BR")} km${located(p) ? " em linha reta" : " estimados · localização pendente"}`,
    );
    $("save-phase").addEventListener("click", (e) =>
      busy(e.currentTarget, () => savePhase(p, $("company-phase").value)),
    );
    $("copy-cnpj").addEventListener("click", () => copy(digits(p.cnpj)));
  }
  async function importLeads(list) {
    const candidates = list.filter((p) => !inCRM(p));
    if (!candidates.length) {
      toast("Empresas já estão no CRM");
      return;
    }
    const result = await api(
      "/api/importar_prospect_crm",
      candidates.length === 1 ? candidates[0] : candidates,
    );
    if (!result.sucesso) {
      error(
        result.resultado ||
          "Não foi possível adicionar ao CRM. Tente novamente.",
      );
      return;
    }
    if (candidates.length === 1) addLocalCRM(candidates[0]);
    try {
      await syncCRM();
    } catch {
      if (candidates.length > 1) {
        error(
          "Importação concluída, mas a lista do CRM não foi atualizada. Atualize a página para conferir o resultado.",
        );
      }
    }
    state.selected.clear();
    applyFilters();
    if (dialog.open && state.company) openCompany(state.company.id);
    toast(
      candidates.length === 1
        ? '✓ Adicionado ao CRM! <a href="crm_enterprise.html?tab=kanban" target="_blank" style="color:#38bdf8; font-weight:700; text-decoration:underline; margin-left:6px;">Abrir no Kanban ➔</a>'
        : `✓ ${result.total_adicionados ?? 0} empresas adicionadas! <a href="crm_enterprise.html?tab=kanban" target="_blank" style="color:#38bdf8; font-weight:700; text-decoration:underline; margin-left:6px;">Abrir no Kanban ➔</a>`,
    );
  }
  async function savePhase(p, fase) {
    const result = await api("/api/atualizar_status_lead", {
      cnpj: p.cnpj || "",
      empresa: p.nome,
      fase,
      decisor: p.decisor || "",
      telefone: p.whatsapp || p.telefone || "",
      email: p.email || "",
      cidade: p.cidade,
      segmento: p.segmento,
      caixas: p.pdvs_estimados || 1,
      site: p.site || "",
      tem_site: Boolean(p.tem_site),
      endereco: p.endereco || "",
    });
    if (!result.sucesso) {
      error("Não foi possível salvar a etapa. Tente novamente.");
      return;
    }
    addLocalCRM(p, fase);
    applyFilters();
    openCompany(p.id);
    toast('✓ Etapa salva! <a href="crm_enterprise.html?tab=kanban" target="_blank" style="color:#38bdf8; font-weight:700; text-decoration:underline; margin-left:6px;">Abrir no Kanban ➔</a>');
  }
  function downloadCSV() {
    const selected = state.filtered.filter((p) => state.selected.has(p.id));
    const list = selected.length ? selected : state.filtered;
    const rows = [
      [
        "Empresa",
        "CNPJ",
        "Segmento",
        "Cidade",
        "Distância km",
        "Contato",
        "Telefone",
        "WhatsApp",
        "E-mail",
        "Site",
        "Prioridade",
        "Etapa CRM",
        "Localização",
        "Fonte da localização",
      ],
      ...list.map((p) => [
        p.nome,
        p.cnpj,
        p.segmento,
        p.cidade,
        p.distancia_km,
        p.decisor,
        p.telefone,
        p.whatsapp,
        p.email,
        p.site,
        p.lead_score,
        inCRM(p) ? phase(p) : "Fora do CRM",
        located(p) ? locationLabel(p) : "Pendente; distância estimada",
        p.geolocalizacao?.fonte_url || "",
      ]),
    ];
    const safe = (v) =>
      /^[=+@-]/.test(String(v ?? "")) ? "'" + v : String(v ?? "");
    const data =
      "\uFEFF" +
      rows
        .map((row) =>
          row.map((v) => '"' + safe(v).replaceAll('"', '""') + '"').join(";"),
        )
        .join("\r\n");
    const url = URL.createObjectURL(
      new Blob([data], { type: "text/csv;charset=utf-8" }),
    );
    const a = document.createElement("a");
    a.href = url;
    a.download =
      "trudata-radar-" +
      norm($("sel-origem").value).replaceAll(" ", "-") +
      ".csv";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    toast(`CSV gerado · ${list.length} empresas`);
  }
  async function createRoute() {
    const list = state.filtered.filter((p) => state.selected.has(p.id));
    if (!list.length) return;
    const result = await api("/api/gerar_rota_maps", {
      origem: $("sel-origem").value + ", RS",
      clientes: list,
      retornar_origem: true,
    });
    if (!result.sucesso || !safeUrl(result.rota_url)) throw new Error();
    showDialog(
      "Rota pronta",
      `<p class="form-intro">${list.length} paradas, saindo de ${esc($("sel-origem").value)}. Confira a ordem e os endereços no Google Maps antes de sair.</p><ol>${list.map((p) => `<li>${esc(p.nome)} · ${esc(p.cidade)}</li>`).join("")}</ol>`,
      external(result.rota_url, "Abrir rota no Google Maps", "route"),
    );
    toast("Rota gerada");
  }
  function openEmail(id) {
    const p = companyById(id);
    if (!p) return;
    state.company = p;
    showDialog(
      "Prepare a conversa",
      `<p class="form-intro">Revise o destinatário e a apresentação antes de abrir seu aplicativo de e-mail.</p><form id="email-form"><div class="form-grid"><label class="field">Destinatário<input type="email" id="email-to" required value="${esc(p.email || "")}"></label><label class="field">Nome do contato<input id="email-name" value="${esc(p.decisor || "Responsável Comercial")}"></label><label class="field full">Apresentação<select id="email-template"><option value="contingencia">Gestão e rotina da loja</option><option value="catalogo">Catálogo digital e pequenos negócios</option><option value="migracao">Troca de sistema e suporte</option></select></label><label class="field full">Assunto<input id="email-subject" required></label></div><p class="email-preview prose" id="email-preview"></p></form><details class="company-notes"><summary>Enviar proposta comercial pelo servidor</summary><p class="small muted">Esta opção usa a proposta padrão em HTML, com módulos do segmento da empresa. O modelo de apresentação acima é usado no Gmail e no aplicativo de e-mail.</p><button class="btn" id="server-email">Enviar proposta padrão</button></details>`,
      `<button class="btn" data-company="${esc(id)}">Voltar à empresa</button><div class="actions"><button class="btn" id="mail-app">Abrir aplicativo de e-mail</button><button class="btn primary" id="gmail">Abrir Gmail</button></div>`,
      p.nome,
    );
    const fill = () => {
      const tpl = TEMPLATES_EMAIL[$("email-template").value];
      $("email-subject").value = tpl.assunto(p.nome, p.cidade);
      preview();
    };
    const preview = () => {
      $("email-preview").textContent = TEMPLATES_EMAIL[
        $("email-template").value
      ].corpo($("email-name").value, p.nome, p.cidade, p.site, p.tem_site);
    };
    $("email-template").addEventListener("change", fill);
    $("email-name").addEventListener("input", preview);
    fill();
    const compose = (gmail) => {
      if (!$("email-form").reportValidity()) return;
      const to = $("email-to").value,
        subject = $("email-subject").value,
        body = $("email-preview").textContent;
      const url = gmail
        ? "https://mail.google.com/mail/?" +
          new URLSearchParams({ view: "cm", fs: "1", to, su: subject, body })
        : "mailto:" +
          encodeURIComponent(to) +
          "?" +
          new URLSearchParams({ subject, body });
      const a = document.createElement("a");
      a.href = url;
      a.target = "_blank";
      a.rel = "noopener";
      a.click();
      toast("Rascunho preparado · finalize o envio no seu e-mail");
    };
    $("gmail").addEventListener("click", () => compose(true));
    $("mail-app").addEventListener("click", () => compose(false));
    $("server-email").addEventListener("click", (e) => {
      if (!$("email-form").reportValidity()) return;
      busy(
        e.currentTarget,
        async () => {
          const result = await api("/api/enviar_proposta_email", {
            destinatario: $("email-to").value,
            cliente: p.nome,
            cidade: p.cidade,
            segmento: p.segmento,
            decisor: $("email-name").value,
            caixas: p.pdvs_estimados || 1,
            cnpj: p.cnpj || "",
            telefone: p.whatsapp || p.telefone || "",
            site: p.site || "",
            tem_site: p.tem_site,
            assunto: $("email-subject").value,
          });
          if (!result.sucesso) {
            error(
              result.erro ||
                result.mensagem ||
                "O envio falhou. Confira as configurações de e-mail.",
            );
            return;
          }
          const sent = /entregue via smtp/i.test(result.status || "");
          $("dialog-feedback").className = "dialog-message";
          $("dialog-feedback").hidden = false;
          $("dialog-feedback").innerHTML =
            `<strong>${sent ? "Enviado" : "Proposta preparada"}</strong><p>${sent ? "O servidor confirmou o envio." : "O envio ainda precisa ser concluído no seu aplicativo de e-mail."}</p>${!sent ? external(result.link_gmail, "Continuar no Gmail", "mail") : ""}`;
          if (sent) {
            try {
              await syncCRM();
              applyFilters();
            } catch {
              /* O envio foi confirmado pelo servidor. */
            }
          }
          toast(sent ? "Enviado" : "Proposta preparada");
        },
        "Preparando",
      );
    });
  }
  async function openSettings() {
    showDialog(
      "Configurar e-mail",
      '<div class="loading"><span class="spinner"></span>Carregando configurações</div>',
    );
    try {
      const cfg = await api("/api/config_email");
      showDialog(
        "Configurar e-mail",
        `<form id="settings-form"><div class="form-grid"><label class="field full">Como enviar<select id="cfg-mode"><option value="automatico">Preparar para envio no aplicativo</option><option value="smtp">Enviar pelo servidor SMTP</option></select></label><label class="field">Servidor<input id="cfg-host" value="${esc(cfg.smtp_host || "smtp.gmail.com")}"></label><label class="field">Porta<input id="cfg-port" type="number" min="1" max="65535" required value="${Number(cfg.smtp_port) || 587}"></label><label class="field">Segurança<select id="cfg-tls"><option value="tls">STARTTLS</option><option value="ssl">SSL/TLS</option></select></label><label class="field">Usuário<input id="cfg-user" autocomplete="username" value="${esc(cfg.usuario || "")}"></label><label class="field full">Senha de aplicativo<input id="cfg-password" type="password" autocomplete="new-password" placeholder="${cfg.senha_configurada ? "Deixe vazio para manter a senha atual" : "Informe a senha de aplicativo"}"></label><label class="field">Nome do remetente<input id="cfg-name" required value="${esc(cfg.remetente_nome || "TruData ERP")}"></label><label class="field">E-mail do remetente<input id="cfg-from" type="email" required value="${esc(cfg.remetente_email || "")}"></label></div></form>`,
        `<button class="btn" data-close>Fechar</button><button class="btn primary" id="save-settings">Salvar configurações</button>`,
      );
      $("cfg-mode").value = cfg.modo === "smtp" ? "smtp" : "automatico";
      $("cfg-tls").value = cfg.smtp_port === 465 ? "ssl" : "tls";
      $("save-settings").addEventListener("click", (e) => {
        if (!$("settings-form").reportValidity()) return;
        busy(e.currentTarget, async () => {
          const body = {
            modo: $("cfg-mode").value,
            smtp_host: $("cfg-host").value,
            smtp_port: Number($("cfg-port").value),
            usar_tls: $("cfg-tls").value === "tls",
            usuario: $("cfg-user").value,
            remetente_nome: $("cfg-name").value,
            remetente_email: $("cfg-from").value,
          };
          if ($("cfg-password").value) body.senha = $("cfg-password").value;
          const r = await api("/api/config_email", body);
          if (!r.sucesso) throw new Error();
          $("cfg-password").value = "";
          toast("Configurações salvas");
        });
      });
    } catch {
      error(
        "Não foi possível carregar as configurações. Feche esta janela e tente novamente.",
      );
    }
  }
  async function openHistory() {
    showDialog(
      "Histórico de e-mails",
      '<div class="loading"><span class="spinner"></span>Carregando histórico</div>',
    );
    try {
      const items = await api("/api/historico_emails");
      if (!Array.isArray(items)) throw new Error();
      showDialog(
        "Histórico de e-mails",
        items.length
          ? `<div class="table-scroll"><table class="history-table"><thead><tr><th>Data</th><th>Empresa</th><th>Destinatário</th><th>Resultado</th></tr></thead><tbody>${items
              .slice()
              .reverse()
              .map(
                (i) =>
                  `<tr><td>${esc(i.data)}</td><td>${esc(i.cliente)}</td><td>${esc(i.destinatario)}</td><td>${esc(i.status || "Sem informação")}</td></tr>`,
              )
              .join("")}</tbody></table></div>`
          : '<div class="empty"><h3>Suas próximas conversas começam no radar.</h3><p>Abra uma empresa e prepare o primeiro e-mail de apresentação.</p></div>',
        '<button class="btn" data-close>Voltar ao radar</button>',
      );
    } catch {
      error(
        "Não foi possível carregar o histórico. Feche esta janela e tente novamente.",
      );
    }
  }

  function openManualLeadModal() {
    const segmentosOptions = [
      "Supermercados & Mercearias",
      "Lojas de Confecções & Moda",
      "Farmácias & Drogarias",
      "Autopeças & Oficinas",
      "Padarias & Gastronomia",
      "Materiais de Construção",
      "Pet Shop & Agropecuária",
      "Escritórios de Contabilidade",
      "Postos de Combustíveis & Conveniência",
      "Comércio Geral & Outros"
    ].map(s => `<option value="${esc(s)}">${esc(s)}</option>`).join("");

    const cidadesOptions = [
      "Sarandi - RS",
      "Ronda Alta - RS",
      "Rondinha - RS",
      "Barra Funda - RS",
      "Constantina - RS",
      "Chapada - RS",
      "Nova Boa Vista - RS",
      "Carazinho - RS",
      "Passo Fundo - RS",
      "Marau - RS",
      "Tapejara - RS",
      "Erechim - RS",
      "Palmeira das Missões - RS",
      "Três Palmeiras - RS",
      "Pontão - RS"
    ].map(c => `<option value="${esc(c)}">${esc(c)}</option>`).join("");

    const bodyHtml = `
      <p class="form-intro">Cadastre estabelecimentos ou contatos encontrados fora do mapeamento automático para integrá-los ao Radar e ao Pipeline Comercial.</p>
      <form id="form-manual-lead" onsubmit="return false;">
        <div class="form-grid">
          <label class="field full">Nome Fantasia / Empresa *
            <input type="text" id="ml-nome" required placeholder="Ex: Mercado Bela Vista">
          </label>
          <label class="field">Razão Social (opcional)
            <input type="text" id="ml-razao" placeholder="Ex: Bela Vista Alimentos Ltda">
          </label>
          <label class="field">CNPJ / CPF (opcional)
            <input type="text" id="ml-cnpj" placeholder="00.000.000/0001-00">
          </label>
          <label class="field">Cidade (RS) *
            <select id="ml-cidade">${cidadesOptions}</select>
          </label>
          <label class="field">Segmento *
            <select id="ml-segmento">${segmentosOptions}</select>
          </label>
          <label class="field">PDVs / Caixas
            <input type="number" id="ml-caixas" value="1" min="1" max="50">
          </label>
          <label class="field full">Endereço / Bairro
            <input type="text" id="ml-endereco" placeholder="Ex: Av. Expedicionário, 850 - Centro">
          </label>
          <label class="field">Nome do Decisor / Responsável *
            <input type="text" id="ml-decisor" required placeholder="Ex: Clóvis Silveira" value="Proprietário">
          </label>
          <label class="field">Telefone / WhatsApp *
            <input type="text" id="ml-telefone" required placeholder="Ex: 54999887766">
          </label>
          <label class="field">E-mail (opcional)
            <input type="email" id="ml-email" placeholder="contato@empresa.com.br">
          </label>
          <label class="field">Site / Instagram (opcional)
            <input type="text" id="ml-site" placeholder="https://instagram.com/empresa">
          </label>
          <label class="field full">Observações Comerciais
            <textarea id="ml-notas" rows="2" placeholder="Ex: Visita presencial; cliente demonstrou interesse em trocar o sistema atual..."></textarea>
          </label>
          <label class="check-field full" style="margin-top:0.5rem; color:#10b981; font-weight:600;">
            <input type="checkbox" id="ml-enviar-crm" checked> Inserir automaticamente no Pipeline (Kanban) do CRM Enterprise
          </label>
        </div>
      </form>
    `;

    const footerHtml = `
      <button class="btn" data-close>Cancelar</button>
      <button class="btn primary" id="btn-salvar-manual" style="background:linear-gradient(135deg, #10b981, #059669); border-color:#10b981; font-weight:700;">
        💾 Salvar e Integrar Lead
      </button>
    `;

    showDialog(
      "➕ Adicionar Novo Lead ao Radar",
      bodyHtml,
      footerHtml,
      "Prospecção Ativa B2B Regional"
    );

    const btnSalvar = $("btn-salvar-manual");
    if (btnSalvar) {
      btnSalvar.addEventListener("click", async () => {
        const nome = ($("ml-nome")?.value || "").trim();
        const decisor = ($("ml-decisor")?.value || "").trim();
        const telefone = ($("ml-telefone")?.value || "").trim();

        if (!nome) {
          error("Informe o Nome da Empresa / Fantasia.");
          $("ml-nome")?.focus();
          return;
        }
        if (!decisor) {
          error("Informe o Nome do Decisor / Responsável.");
          $("ml-decisor")?.focus();
          return;
        }
        if (!telefone) {
          error("Informe o Telefone ou WhatsApp de contato.");
          $("ml-telefone")?.focus();
          return;
        }

        const payload = {
          nome,
          razao_social: ($("ml-razao")?.value || "").trim() || nome,
          cnpj: ($("ml-cnpj")?.value || "").trim(),
          cidade: $("ml-cidade")?.value || "Sarandi - RS",
          segmento: $("ml-segmento")?.value || "Comércio Geral",
          caixas: parseInt($("ml-caixas")?.value) || 1,
          endereco: ($("ml-endereco")?.value || "").trim(),
          decisor,
          telefone,
          whatsapp: telefone,
          email: ($("ml-email")?.value || "").trim(),
          site: ($("ml-site")?.value || "").trim(),
          notas: ($("ml-notas")?.value || "").trim(),
          enviar_crm: $("ml-enviar-crm")?.checked ?? true
        };

        busy(btnSalvar, async () => {
          try {
            const res = await api("/api/radar/adicionar_lead_manual", payload);
            if (!res.sucesso) {
              throw new Error(res.erro || "Falha ao adicionar lead.");
            }

            if (res.prospect) {
              state.all.unshift(res.prospect);
              addLocalCRM(res.prospect, "novo");
            }

            dialog.close();
            applyFilters();
            toast(`✓ Lead "${nome}" cadastrado com sucesso no Radar e CRM!`);
            if (res.prospect?.id) {
              openCompany(res.prospect.id);
            }
          } catch (err) {
            error(err.message || "Erro de conexão ao salvar lead manual.");
          }
        }, "Salvando Lead");
      });
    }
  }

  document.addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    if (b.dataset.locate) {
      const p = companyById(b.dataset.locate);
      if (p && located(p) && initMap()) {
        dialog.close();
        map.closePopup();
        map.setView([Number(p.lat), Number(p.lon)], 17, {animate: false});
        $("radar-map").scrollIntoView({block: "center"});
        markers.eachLayer(marker => {if (marker.getLatLng().equals([Number(p.lat), Number(p.lon)])) marker.openPopup();});
      }
    }
    if (b.dataset.company) openCompany(b.dataset.company);
    if (b.dataset.email) openEmail(b.dataset.email);
    if (b.dataset.import) {
      const p = companyById(b.dataset.import);
      if (p) busy(b, () => importLeads([p]));
    }
    if (b.dataset.city) cityFilter(b.dataset.city);
    if (b.dataset.radius) {
      $("rng-raio").value = b.dataset.radius;
      updateRadius();
      search();
    }
    if (b.dataset.queue) {
      state.queue = b.dataset.queue;
      state.limit = 30;
      applyFilters();
    }
    if (b.dataset.view) {
      state.view = b.dataset.view;
      document
        .querySelectorAll("[data-view]")
        .forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      renderResults();
      updateSelection();
    }
    if (b.hasAttribute("data-reset")) reset();
    if (b.hasAttribute("data-retry")) search();
  });
  $("results").addEventListener("change", (e) => {
    const id = e.target.dataset.select;
    if (!id) return;
    e.target.checked ? state.selected.add(id) : state.selected.delete(id);
    e.target
      .closest("[data-row]")
      .classList.toggle("selected", e.target.checked);
    updateSelection();
  });
  $("select-all").addEventListener("change", (e) => {
    state.filtered
      .slice(0, state.limit)
      .forEach((p) =>
        e.target.checked
          ? state.selected.add(p.id)
          : state.selected.delete(p.id),
      );
    renderResults();
    updateSelection();
  });
  $("clear-selection").addEventListener("click", () => {
    state.selected.clear();
    renderResults();
    updateSelection();
  });
  $("bulk-crm").addEventListener("click", (e) =>
    busy(e.currentTarget, () =>
      importLeads(state.filtered.filter((p) => state.selected.has(p.id))),
    ),
  );
  $("route").addEventListener("click", (e) =>
    busy(e.currentTarget, createRoute, "Gerando"),
  );
  $("export").addEventListener("click", downloadCSV);
  $("copy-phones").addEventListener("click", () => {
    const selected = state.filtered.filter((p) => state.selected.has(p.id)),
      list = selected.length ? selected : state.filtered;
    const phones = [
      ...new Set(
        list
          .map((p) => digits(p.whatsapp || p.telefone))
          .filter(Boolean)
          .map((t) => (t.length <= 11 ? "55" + t : t)),
      ),
    ];
    if (!phones.length) {
      toast("Nenhum telefone nesta seleção");
      return;
    }
    copy(phones.join("\n"));
  });
  $("load-more").addEventListener("click", () => {
    state.limit += 30;
    renderResults();
    updateSelection();
  });
  $("reset").addEventListener("click", reset);
  $("fit-map").addEventListener("click", fitMap);
  $("search").addEventListener("input", () => {
    state.limit = 30;
    applyFilters();
  });
  $("sel-ordenacao").addEventListener("change", applyFilters);
  [
    "sel-origem",
    "sel-cidade",
    "sel-segmento",
    "sel-porte",
    "sel-site",
    "chk-email",
    "chk-telefone",
  ].forEach((id) => $(id).addEventListener("change", search));
  $("rng-raio").addEventListener("input", updateRadius);
  $("rng-raio").addEventListener("change", search);
  $("email-settings").addEventListener("click", openSettings);
  $("email-history").addEventListener("click", openHistory);
  const btnLeadManual = $("btn-novo-lead-manual");
  if (btnLeadManual) btnLeadManual.addEventListener("click", openManualLeadModal);
  async function init() {
    try {
      await syncCRM();
    } catch {
      error(
        "O CRM não está disponível. As empresas podem ser consultadas, mas o vínculo com o CRM ainda precisa ser conferido.",
      );
    }
    const mode = new URLSearchParams(location.search).get("modo");
    if (["contadores", "contabilidade"].includes(mode))
      $("sel-segmento").value = "Escritórios de Contabilidade";
    await search();
    if (!state.crmLoaded)
      error(
        "O CRM não está disponível. Os filtros de vínculo ficam desativados até recarregar a página.",
      );
  }
  init();
})();
