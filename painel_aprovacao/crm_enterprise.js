/**
 * TruData CRM Enterprise - Controlador de Interface & Lógica Comercial 360°
 * Múltiplos Funis, Kanban Drag-and-Drop, Gestão PF/PJ, Atividades, Automações,
 * Deduplicação, Métricas, Conformidade LGPD e Swagger/ER Interativo.
 */

function obterConfiguracoesPadraoKanban() {
  return {
    wipLimites: {
      'etapa-lead': 60,
      'etapa-contato': 15,
      'etapa-demo': 10,
      'etapa-proposta': 15,
      'etapa-fechado': 100,
      'etapa-recontato': 50,
      'etapa-perdido': 200
    },
    tempoParado: {
      verdeMaxDias: 3,
      amareloMaxDias: 10
    },
    temperatura: {
      quenteMaxDias: 3,
      mornoMaxDias: 10
    }
  };
}

function carregarConfiguracoesKanban() {
  try {
    const raw = localStorage.getItem('trudata_crm_kanban_config');
    if (raw) {
      const parsed = JSON.parse(raw);
      const def = obterConfiguracoesPadraoKanban();
      return {
        wipLimites: { ...def.wipLimites, ...(parsed.wipLimites || {}) },
        tempoParado: { ...def.tempoParado, ...(parsed.tempoParado || {}) },
        temperatura: { ...def.temperatura, ...(parsed.temperatura || {}) }
      };
    }
  } catch (e) {
    console.error('Erro ao ler config do kanban:', e);
  }
  return obterConfiguracoesPadraoKanban();
}

const CRM_STATE = {
  dados: null,
  funilAtivoId: 'funil-vendas-novas',
  subAbaAtiva: 'dashboard',
  usuarioAtivo: { id: 'usr-admin', perfil: 'admin', nome: 'Administrador TruData' },
  filtroBusca: '',
  filtroFase: 'todas',
  filtroSegmento: 'todos',
  agendaModo: 'calendario',
  agendaVisao: 'mes',
  agendaDataRef: new Date(),
  agendaFiltroTipo: 'todos',
  agendaFiltroResponsavel: 'todos',
  agendaFiltroStatus: 'todos',
  agendaFiltroBusca: '',
  kanban: {
    modoExibicaoGlobal: 'expandido',
    colModos: {},
    colBusca: {},
    colOrdenacao: {},
    colLimitesExibicao: {},
    funilResumoAberto: true,
    filtrosGlobais: {
      busca: '',
      responsavel: 'todos',
      mrr: 'todos',
      cidade: 'todas',
      segmento: 'todos',
      origem: 'todas'
    },
    config: carregarConfiguracoesKanban()
  }
};

document.addEventListener('DOMContentLoaded', () => {
  inicializarCRM();
});

async function inicializarCRM() {
  const urlParams = new URLSearchParams(window.location.search);
  let requestedTab = urlParams.get('tab') || urlParams.get('aba');
  const path = (window.location.pathname || '').toLowerCase();
  if (!requestedTab) {
    if (path.includes('agenda') || path.includes('agendamento') || path.includes('acoes') || path.includes('acao')) {
      requestedTab = 'atividades';
    }
  }
  const tabAliases = {
    'agenda': 'atividades',
    'agendamento': 'atividades',
    'agendamentos': 'atividades',
    'acoes': 'atividades',
    'acao': 'atividades',
    'atividades': 'atividades',
    'empresas': 'contatos_empresas',
    'contatos': 'contatos_empresas'
  };
  if (requestedTab && tabAliases[requestedTab.toLowerCase()]) {
    requestedTab = tabAliases[requestedTab.toLowerCase()];
  }
  if (requestedTab && ['kanban', 'dashboard', 'contatos_empresas', 'negociacoes', 'onboarding', 'metas', 'atividades', 'automacoes', 'usuarios', 'integracoes_api'].includes(requestedTab)) {
    CRM_STATE.subAbaAtiva = requestedTab;
  }
  const requestedFunil = urlParams.get('funil');
  if (requestedFunil) {
    CRM_STATE.funilAtivoId = requestedFunil;
  }
  await carregarEstadoCRM();
  configurarEventosGerais();
}

async function carregarEstadoCRM() {
  try {
    const res = await fetch('/api/crm/v2/estado', {
      headers: {
        'X-Usuario-Id': CRM_STATE.usuarioAtivo.id,
        'X-Usuario-Perfil': CRM_STATE.usuarioAtivo.perfil
      }
    });
    const json = await res.json();
    if (json.sucesso) {
      CRM_STATE.dados = json.dados;
      renderizarTudo();
    } else {
      console.error('Erro ao carregar CRM:', json.erro);
    }
  } catch (e) {
    console.error('Falha na requisição do CRM:', e);
  }
}

function configurarEventosGerais() {
  // Navegação por sub-abas
  document.querySelectorAll('.crm-tab-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const tab = btn.dataset.tab;
      trocarSubAba(tab);
    });
  });

  // Seletor de usuário para simulação de permissões
  const selUser = document.getElementById('crm-user-sim');
  if (selUser) {
    selUser.addEventListener('change', async (e) => {
      const val = e.target.value;
      const usr = (CRM_STATE.dados?.usuarios || []).find(u => u.id === val);
      if (usr) {
        CRM_STATE.usuarioAtivo = { id: usr.id, perfil: usr.perfil, nome: usr.nome };
      } else {
        CRM_STATE.usuarioAtivo = { id: 'usr-admin', perfil: 'admin', nome: 'Administrador TruData' };
      }
      await carregarEstadoCRM();
    });
  }
}

function atualizarSelectUsuarios() {
  const selUser = document.getElementById('crm-user-sim');
  if (!selUser || !CRM_STATE.dados?.usuarios) return;
  const currentVal = CRM_STATE.usuarioAtivo?.id || 'usr-admin';
  selUser.innerHTML = CRM_STATE.dados.usuarios.map(u => 
    `<option value="${u.id}" ${u.id === currentVal ? 'selected' : ''}>${u.nome} (${u.perfil.toUpperCase()})</option>`
  ).join('');
}

function trocarSubAba(tabId) {
  const tabAliases = {
    'agenda': 'atividades',
    'agendamento': 'atividades',
    'agendamentos': 'atividades',
    'acoes': 'atividades',
    'acao': 'atividades',
    'empresas': 'contatos_empresas',
    'contatos': 'contatos_empresas'
  };
  if (tabAliases[tabId]) tabId = tabAliases[tabId];
  CRM_STATE.subAbaAtiva = tabId;
  document.querySelectorAll('.crm-tab-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.tab === tabId);
  });
  document.querySelectorAll('.crm-view-pane').forEach(p => {
    p.classList.toggle('active', p.id === `view-${tabId}`);
  });
  renderizarSubAba(tabId);
}

function renderizarTudo() {
  if (!CRM_STATE.dados) return;
  atualizarSelectUsuarios();
  atualizarSelectFunis();
  document.querySelectorAll('.crm-tab-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.tab === CRM_STATE.subAbaAtiva);
  });
  document.querySelectorAll('.crm-view-pane').forEach(p => {
    p.classList.toggle('active', p.id === `view-${CRM_STATE.subAbaAtiva}`);
  });
  renderizarSubAba(CRM_STATE.subAbaAtiva);
}

function renderizarSubAba(tabId) {
  switch (tabId) {
    case 'dashboard':
      renderizarDashboard();
      break;
    case 'kanban':
      renderizarKanban();
      break;
    case 'contatos_empresas':
      renderizarContatosEmpresas();
      break;
    case 'negociacoes':
      renderizarNegociacoes();
      break;
    case 'onboarding':
      renderizarOnboarding();
      break;
    case 'metas':
      renderizarMetas();
      break;
    case 'atividades':
      renderizarAtividades();
      break;
    case 'automacoes':
      renderizarAutomacoes();
      break;
    case 'usuarios':
      renderizarUsuarios();
      break;
    case 'integracoes_api':
      renderizarIntegracoes();
      break;
  }
}

// ==================== 1. DASHBOARD & MÉTRICAS-CHAVE ====================
function renderizarDashboard() {
  const m = CRM_STATE.dados.metricas;
  if (!m) return;

  const container = document.getElementById('view-dashboard');
  if (!container) return;

  const metas = m.metas_painel || {};
  const ranking = metas.ranking_vendedores || [];

  container.innerHTML = `
    <!-- ITEM 3: TERMÔMETRO DE METAS & RUN-RATE COMERCIAL -->
    <div class="metas-thermometer-box">
      <div class="thermo-header">
        <h3>🎯 Metas Comerciais · ${metas.mes_referencia || 'Mês Atual'}</h3>
        <button onclick="abrirModalConfigMetas()" class="btn-crm" style="font-size:0.75rem; padding:0.35rem 0.75rem;">⚙️ Configurar Metas</button>
      </div>
      <div class="thermo-stats-grid">
        <div class="thermo-stat-card">
          <div class="thermo-stat-label">Meta MRR Empresa</div>
          <div class="thermo-stat-val" style="color:#38bdf8;">R$ ${(metas.mrr_atingido || 0).toLocaleString('pt-BR', {minimumFractionDigits: 2})} <span style="font-size:0.8rem; color:#94a3b8;">/ R$ ${(metas.meta_mrr_empresa || 15000).toLocaleString('pt-BR', {minimumFractionDigits: 2})}</span></div>
          <div style="font-size:0.75rem; color:#cbd5e1;">Atingido: <strong style="color:#38bdf8;">${metas.pct_meta_mrr || 0}%</strong> da meta</div>
        </div>
        <div class="thermo-stat-card">
          <div class="thermo-stat-label">Meta PDVs Homologados</div>
          <div class="thermo-stat-val" style="color:#34d399;">${metas.pdvs_atingidos || 0} <span style="font-size:0.8rem; color:#94a3b8;">/ ${metas.meta_pdvs_empresa || 50} PDVs</span></div>
          <div style="font-size:0.75rem; color:#cbd5e1;">Atingido: <strong style="color:#34d399;">${metas.pct_meta_pdvs || 0}%</strong> da meta</div>
        </div>
        <div class="thermo-stat-card">
          <div class="thermo-stat-label">Projeção Run-Rate</div>
          <div class="thermo-stat-val" style="color:#facc15;">R$ ${(metas.projecao_run_rate_mrr || 0).toLocaleString('pt-BR', {minimumFractionDigits: 2})}</div>
          <div style="font-size:0.75rem; color:#cbd5e1;">Estimativa de fechamento no ritmo atual</div>
        </div>
        <div class="thermo-stat-card">
          <div class="thermo-stat-label">Comissão Total Equipe</div>
          <div class="thermo-stat-val" style="color:#a855f7;">R$ ${(metas.total_comissao_equipe || 0).toLocaleString('pt-BR', {minimumFractionDigits: 2})}</div>
          <div style="font-size:0.75rem; color:#cbd5e1;">Remuneração variável apurada em tempo real</div>
        </div>
      </div>
      <div>
        <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:0.4rem;">
          <span style="font-weight:700; color:#cbd5e1;">Termômetro de Realização da Meta:</span>
          <span style="font-weight:800; color:#38bdf8;">${metas.pct_meta_mrr || 0}% Conquistado</span>
        </div>
        <div class="thermo-progress-container">
          <div class="thermo-progress-fill" style="width:${Math.min(100, Math.max(8, metas.pct_meta_mrr || 0))}%;">
            ${metas.pct_meta_mrr || 0}%
          </div>
        </div>
      </div>
    </div>

    <!-- KPIs TRADICIONAIS -->
    <div class="kpi-grid">
      <div class="kpi-card-ent">
        <div class="kpi-header-line"><span>Pipeline Total</span><span>🏢</span></div>
        <div class="kpi-number">${m.total_deals}</div>
        <div class="kpi-foot"><span>${m.total_abertos} abertos · ${m.total_ganhos} ganhos</span></div>
      </div>
      <div class="kpi-card-ent">
        <div class="kpi-header-line"><span>MRR em Negociação</span><span>💰</span></div>
        <div class="kpi-number" style="color:#34d399;">R$ ${m.total_mrr_aberto.toLocaleString('pt-BR', {minimumFractionDigits: 2})}</div>
        <div class="kpi-foot"><span>Mensalidades recorrentes potenciais</span></div>
      </div>
      <div class="kpi-card-ent">
        <div class="kpi-header-line"><span>Forecast Ponderado</span><span>🎯</span></div>
        <div class="kpi-number" style="color:#38bdf8;">R$ ${m.forecast_mrr_ponderado.toLocaleString('pt-BR', {minimumFractionDigits: 2})}</div>
        <div class="kpi-foot"><span>Ajustado pela probabilidade real</span></div>
      </div>
      <div class="kpi-card-ent">
        <div class="kpi-header-line"><span>Taxa de Conversão</span><span>📈</span></div>
        <div class="kpi-number" style="color:#facc15;">${m.taxa_conversao}%</div>
        <div class="kpi-foot"><span>Ticket médio: R$ ${m.ticket_medio.toFixed(2)}/mês</span></div>
      </div>
    </div>

    <!-- PÓDIO DE GAMIFICAÇÃO COMERCIAL -->
    ${ranking.length > 0 ? `
      <div class="dash-box" style="margin-bottom:1.5rem;">
        <div class="dash-box-title">
          <span>🏆 Pódio da Equipe Comercial & Gamificação</span>
          <span style="font-size:0.75rem; color:#94a3b8;">Classificação mensal por MRR fechado</span>
        </div>
        <div class="podium-container">
          ${ranking.slice(0, 3).map((v, i) => `
            <div class="podium-card ${i === 0 ? 'first' : ''}">
              <div class="podium-medal">${i === 0 ? '🥇' : (i === 1 ? '🥈' : '🥉')}</div>
              <div class="podium-seller-name">${v.nome}</div>
              <div style="font-size:0.75rem; color:#94a3b8;">${v.equipe} · ${v.ganhos} fechamentos</div>
              <div class="podium-seller-mrr">R$ ${v.mrr_ganho.toFixed(2)}/mês</div>
              <div class="podium-comissao">💰 Comissão Estimada: R$ ${v.comissao_estimada.toFixed(2)}</div>
              <div style="margin-top:0.5rem; font-size:0.75rem; color:#cbd5e1;">
                Meta Atingida: <strong style="color:${v.pct_meta >= 100 ? '#10b981' : '#38bdf8'};">${v.pct_meta}%</strong> (Alvo: R$ ${v.meta_mrr.toFixed(0)})
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    ` : ''}

    <div class="dash-columns-2">
      <!-- Funil de Vendas com Taxa por Etapa -->
      <div class="dash-box">
        <div class="dash-box-title">
          <span>Funil de Conversão Comercial</span>
          <button onclick="exportarRelatorioPDF()" class="btn-crm" style="font-size:0.75rem; padding:0.3rem 0.6rem;">📄 Exportar Relatório</button>
        </div>
        <div>
          ${m.etapas_funil_padrao.map(et => {
            const pct = m.total_deals > 0 ? (et.total_deals / m.total_deals * 100) : 0;
            return `
              <div class="funnel-stage-bar">
                <div class="funnel-stage-meta">
                  <span style="font-weight:700; color:${et.cor};">${et.nome}</span>
                  <span style="color:#94a3b8;">${et.total_deals} deals · R$ ${et.valor_mrr.toLocaleString('pt-BR', {minimumFractionDigits: 2})}/mês (${pct.toFixed(0)}%)</span>
                </div>
                <div class="funnel-progress-bg">
                  <div class="funnel-progress-fill" style="width: ${Math.max(pct, 5)}%; background: ${et.cor};">
                    ${pct.toFixed(0)}%
                  </div>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>

      <!-- Desempenho por Vendedor / Equipe -->
      <div class="dash-box">
        <div class="dash-box-title">
          <span>Produtividade da Equipe Comercial</span>
          <span style="font-size:0.75rem; color:#94a3b8;">Ciclo Médio: ${m.ciclo_medio_dias} dias</span>
        </div>
        <table class="crm-table">
          <thead>
            <tr>
              <th>Consultor</th>
              <th>Time</th>
              <th>Deals</th>
              <th>Ganhos</th>
              <th>MRR Ganho</th>
              <th>Conversão</th>
            </tr>
          </thead>
          <tbody>
            ${Object.values(m.vendedores_stats).map(v => `
              <tr>
                <td><strong>${v.nome}</strong></td>
                <td><span class="badge-ent badge-pj">${v.equipe}</span></td>
                <td>${v.total_deals}</td>
                <td><span style="color:#34d399; font-weight:700;">${v.ganhos}</span></td>
                <td style="color:#34d399; font-family:'JetBrains Mono'; font-weight:700;">R$ ${v.mrr_ganho.toFixed(2)}</td>
                <td><strong>${v.taxa_conversao}%</strong></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function exportarRelatorioPDF() {
  window.print();
}

// ==================== 2. PIPELINE KANBAN COM DRAG-AND-DROP REDESENHADO ====================

function atualizarSelectFunis() {
  const sel = document.getElementById('kanban-select-funil');
  if (!sel || !CRM_STATE.dados?.funis) return;
  sel.innerHTML = CRM_STATE.dados.funis.map(f => `
    <option value="${f.id}" ${f.id === CRM_STATE.funilAtivoId ? 'selected' : ''}>${f.nome}</option>
  `).join('');
  sel.onchange = (e) => {
    CRM_STATE.funilAtivoId = e.target.value;
    renderizarKanban();
  };
}

// P1: Popular selects dos Filtros Globais do Board
function atualizarSelectsFiltrosGlobaisKanban() {
  if (!CRM_STATE.dados) return;

  // 1. Responsáveis
  const selResp = document.getElementById('kanban-filtro-responsavel');
  if (selResp && CRM_STATE.dados.usuarios) {
    const curResp = CRM_STATE.kanban.filtrosGlobais.responsavel;
    selResp.innerHTML = '<option value="todos">Todos os Responsáveis</option>' +
      CRM_STATE.dados.usuarios.map(u => `
        <option value="${u.id}" ${u.id === curResp ? 'selected' : ''}>👤 ${escapeHtml(u.nome)}</option>
      `).join('');
  }

  // 2. Cidades (únicas e ordenadas)
  const selCidade = document.getElementById('kanban-filtro-cidade');
  if (selCidade && CRM_STATE.dados.empresas) {
    const cidadesSet = new Set();
    CRM_STATE.dados.empresas.forEach(e => {
      if (e.cidade && e.cidade.trim()) cidadesSet.add(e.cidade.trim());
    });
    const cidades = Array.from(cidadesSet).sort((a, b) => a.localeCompare(b));
    const curCid = CRM_STATE.kanban.filtrosGlobais.cidade;
    selCidade.innerHTML = '<option value="todas">Todas as Cidades</option>' +
      cidades.map(c => `
        <option value="${escapeHtml(c)}" ${c === curCid ? 'selected' : ''}>📍 ${escapeHtml(c)}</option>
      `).join('');
  }

  // 3. Segmentos (únicos e ordenados)
  const selSeg = document.getElementById('kanban-filtro-segmento');
  if (selSeg && CRM_STATE.dados.empresas) {
    const segSet = new Set();
    CRM_STATE.dados.empresas.forEach(e => {
      if (e.segmento && e.segmento.trim()) segSet.add(e.segmento.trim());
    });
    const segmentos = Array.from(segSet).sort((a, b) => a.localeCompare(b));
    const curSeg = CRM_STATE.kanban.filtrosGlobais.segmento;
    selSeg.innerHTML = '<option value="todos">Todos os Segmentos</option>' +
      segmentos.map(s => `
        <option value="${escapeHtml(s)}" ${s === curSeg ? 'selected' : ''}>🏢 ${escapeHtml(s)}</option>
      `).join('');
  }
}

// P1: Controle de Filtros Globais do Board
function aoMudarFiltroGlobal(campo, valor) {
  CRM_STATE.kanban.filtrosGlobais[campo] = valor;
  const btnLimpar = document.getElementById('btn-limpar-busca-global');
  if (btnLimpar) {
    btnLimpar.classList.toggle('hidden', !CRM_STATE.kanban.filtrosGlobais.busca);
  }
  atualizarChipsFiltrosAtivos();
  renderizarKanban();
}

function limparBuscaGlobalKanban() {
  const inp = document.getElementById('kanban-filtro-global-busca');
  if (inp) inp.value = '';
  aoMudarFiltroGlobal('busca', '');
}

function limparTodosFiltrosKanban() {
  CRM_STATE.kanban.filtrosGlobais = {
    busca: '',
    responsavel: 'todos',
    mrr: 'todos',
    cidade: 'todas',
    segmento: 'todos',
    origem: 'todas'
  };

  const inpBusca = document.getElementById('kanban-filtro-global-busca');
  if (inpBusca) inpBusca.value = '';

  const selResp = document.getElementById('kanban-filtro-responsavel');
  if (selResp) selResp.value = 'todos';

  const selMrr = document.getElementById('kanban-filtro-mrr');
  if (selMrr) selMrr.value = 'todos';

  const selCid = document.getElementById('kanban-filtro-cidade');
  if (selCid) selCid.value = 'todas';

  const selSeg = document.getElementById('kanban-filtro-segmento');
  if (selSeg) selSeg.value = 'todos';

  const selOri = document.getElementById('kanban-filtro-origem');
  if (selOri) selOri.value = 'todas';

  const btnLimparBusca = document.getElementById('btn-limpar-busca-global');
  if (btnLimparBusca) btnLimparBusca.classList.add('hidden');

  atualizarChipsFiltrosAtivos();
  renderizarKanban();
}

function atualizarChipsFiltrosAtivos() {
  const infoWrap = document.getElementById('kanban-active-filters-info');
  if (!infoWrap) return;

  const f = CRM_STATE.kanban.filtrosGlobais;
  const chips = [];

  if (f.busca) chips.push(`Texto: "<strong>${escapeHtml(f.busca)}</strong>"`);
  if (f.responsavel !== 'todos') {
    const usr = (CRM_STATE.dados?.usuarios || []).find(u => u.id === f.responsavel);
    chips.push(`Responsável: <strong>${escapeHtml(usr ? usr.nome : f.responsavel)}</strong>`);
  }
  if (f.mrr !== 'todos') {
    const labelMrr = f.mrr === 'ate-200' ? 'Até R$ 200' : (f.mrr === '200-500' ? 'R$ 200 a R$ 500' : 'Acima de R$ 500');
    chips.push(`MRR: <strong>${labelMrr}</strong>`);
  }
  if (f.cidade !== 'todas') chips.push(`Cidade: <strong>${escapeHtml(f.cidade)}</strong>`);
  if (f.segmento !== 'todos') chips.push(`Segmento: <strong>${escapeHtml(f.segmento)}</strong>`);
  if (f.origem !== 'todas') chips.push(`Canal: <strong>${escapeHtml(f.origem)}</strong>`);

  if (chips.length > 0) {
    infoWrap.classList.remove('hidden');
    infoWrap.innerHTML = `
      <span style="font-weight:700; color:#94a3b8;">Filtros Ativos:</span>
      ${chips.map(c => `<span class="kanban-filter-chip-active">${c}</span>`).join('')}
      <button type="button" onclick="limparTodosFiltrosKanban()" style="background:none; border:none; color:#f87171; font-size:0.72rem; cursor:pointer; text-decoration:underline; margin-left:6px;">Limpar todos</button>
    `;
  } else {
    infoWrap.classList.add('hidden');
    infoWrap.innerHTML = '';
  }
}

// P2: Barra de Funil Resumida (Colapsável)
function alternarVisibilidadeFunilResumo() {
  const body = document.getElementById('kanban-funnel-body');
  const icon = document.getElementById('funnel-toggle-icon');
  const btn = document.getElementById('btn-toggle-funil');
  if (!body) return;

  CRM_STATE.kanban.funilResumoAberto = !CRM_STATE.kanban.funilResumoAberto;
  if (CRM_STATE.kanban.funilResumoAberto) {
    body.classList.remove('collapsed');
    if (icon) icon.textContent = '▲';
    if (btn) btn.innerHTML = '<span id="funnel-toggle-icon">▲</span> Recolher';
  } else {
    body.classList.add('collapsed');
    if (icon) icon.textContent = '▼';
    if (btn) btn.innerHTML = '<span id="funnel-toggle-icon">▼</span> Ver Métricas';
  }
}

function renderizarBarraFunilResumo() {
  const body = document.getElementById('kanban-funnel-body');
  const badgeSum = document.getElementById('kanban-funnel-badge-summary');
  if (!body || !CRM_STATE.dados) return;

  const m = CRM_STATE.dados.metricas || {};
  const fRes = m.funil_resumo || {};
  const passos = fRes.conversao_passos || [
    { de: 'Lead', para: 'Contato', taxa: 15.0, de_count: 54, para_count: 1 },
    { de: 'Contato', para: 'Demonstração', taxa: 66.7, de_count: 1, para_count: 2 },
    { de: 'Demonstração', para: 'Proposta', taxa: 60.0, de_count: 2, para_count: 3 },
    { de: 'Proposta', para: 'Contrato Ganho', taxa: 50.0, de_count: 3, para_count: 3 }
  ];
  const tempos = fRes.tempo_medio_dias_etapas || {};
  const ganhos = m.total_ganhos || 0;
  const perdidos = m.total_perdidos || 0;
  const mrrGanho = m.total_ganho_mrr || 0;
  const princPerda = fRes.principal_motivo_perda || { motivo: 'Preço / Condição Comercial', quantidade: 2, percentual: 40.0 };

  if (badgeSum) {
    badgeSum.innerHTML = `🏆 ${ganhos} Ganhos (R$ ${mrrGanho.toLocaleString('pt-BR', {minimumFractionDigits: 0})}/mês) · ❌ ${perdidos} Perdidos`;
  }

  body.innerHTML = `
    <div class="funnel-analytics-grid">
      ${passos.map((p, idx) => {
        let corTaxa = '#38bdf8';
        if (p.taxa >= 50) corTaxa = '#34d399';
        else if (p.taxa < 20) corTaxa = '#fbbf24';

        return `
          <div class="funnel-step-card">
            <div class="funnel-step-top">
              <span>Passo ${idx + 1}: ${escapeHtml(p.de)} ➔ ${escapeHtml(p.para)}</span>
              <span style="font-size:0.8rem;">📈</span>
            </div>
            <div class="funnel-step-conversion" style="color:${corTaxa};">
              ${p.taxa}% <span style="font-size:0.75rem; color:#94a3b8; font-weight:500;">conversão</span>
            </div>
            <div class="funnel-step-sub">
              <span>Base: <strong>${p.de_count}</strong> ➔ Avançaram: <strong>${p.para_count}</strong></span>
            </div>
          </div>
        `;
      }).join('')}

      <!-- Card Balanço Ganhos vs Perdidos & Motivo de Perda -->
      <div class="funnel-summary-badge-card">
        <div class="funnel-step-top" style="color:#e2e8f0;">
          <span>Desfechos Comerciais</span>
          <span>⚖️</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin:0.3rem 0;">
          <div>
            <div style="font-size:1.1rem; font-weight:800; color:#34d399;">✓ ${ganhos} Ganhos</div>
            <div style="font-size:0.72rem; color:#94a3b8;">MRR: R$ ${mrrGanho.toLocaleString('pt-BR', {minimumFractionDigits: 2})}</div>
          </div>
          <div style="text-align:right;">
            <div style="font-size:1.1rem; font-weight:800; color:#f87171;">✕ ${perdidos} Perdidos</div>
            <div style="font-size:0.72rem; color:#94a3b8;">Taxa Geral: ${m.taxa_conversao || 0}%</div>
          </div>
        </div>
        <div style="background:rgba(0,0,0,0.3); border-radius:5px; padding:0.35rem 0.5rem; font-size:0.7rem; color:#cbd5e1; display:flex; align-items:center; justify-content:space-between;">
          <span>🚨 Principal Perda:</span>
          <strong style="color:#f87171;">${escapeHtml(princPerda.motivo || 'N/A')} (${princPerda.percentual || 0}%)</strong>
        </div>
      </div>
    </div>
  `;
}

// P1: Modo de Exibição dos Cards (Global e por Coluna)
function definirModoExibicaoCardsGlobal(modo) {
  CRM_STATE.kanban.modoExibicaoGlobal = modo;
  // Reseta modos individuais de coluna para acompanhar o modo global
  CRM_STATE.kanban.colModos = {};

  const btnExp = document.getElementById('btn-mode-expanded');
  const btnCmp = document.getElementById('btn-mode-compact');
  if (btnExp && btnCmp) {
    btnExp.classList.toggle('active', modo === 'expandido');
    btnCmp.classList.toggle('active', modo === 'compacto');
  }

  renderizarKanban();
}

function alternarModoExibicaoColuna(etapaId) {
  const atual = CRM_STATE.kanban.colModos[etapaId] || CRM_STATE.kanban.modoExibicaoGlobal;
  CRM_STATE.kanban.colModos[etapaId] = (atual === 'compacto') ? 'expandido' : 'compacto';
  renderizarKanban();
}

// P0: Busca e Ordenação por Coluna
function filtrarColunaKanban(etapaId, termo) {
  CRM_STATE.kanban.colBusca[etapaId] = termo;
  renderizarKanban();
}

function ordenarColunaKanban(etapaId, criterio) {
  CRM_STATE.kanban.colOrdenacao[etapaId] = criterio;
  renderizarKanban();
}

// P0: Paginação / Lazy Load por Coluna
function carregarMaisCardsColuna(etapaId, todos = false) {
  const limiteAtual = CRM_STATE.kanban.colLimitesExibicao[etapaId] || 25;
  CRM_STATE.kanban.colLimitesExibicao[etapaId] = todos ? 9999 : (limiteAtual + 25);
  renderizarKanban();
}

// P0: Cálculo de Tempo Parado no Estágio
function calcularDiasSemMover(deal) {
  const dataRefStr = deal.etapa_atualizada_em || deal.criado_em;
  if (!dataRefStr) return 0;
  try {
    const dataRef = new Date(dataRefStr);
    if (isNaN(dataRef.getTime())) return 0;
    const diffMs = new Date() - dataRef;
    return Math.max(0, Math.floor(diffMs / (1000 * 60 * 60 * 24)));
  } catch (e) {
    return 0;
  }
}

function obterEstiloTempoParado(dias, etapaId) {
  const cfg = CRM_STATE.kanban.config.tempoParado || { verdeMaxDias: 3, amareloMaxDias: 10 };
  const verde = cfg.verdeMaxDias || 3;
  const amarelo = cfg.amareloMaxDias || 10;

  if (dias <= verde) {
    return { classe: 'tempo-verde', label: `🕐 ${dias}d no estágio` };
  } else if (dias <= amarelo) {
    return { classe: 'tempo-amarelo', label: `🕐 ${dias}d no estágio` };
  } else {
    return { classe: 'tempo-vermelho', label: `🕐 ${dias}d sem mover` };
  }
}

// P0: Indicador de Temperatura do Lead (Quente/Morno/Frio)
function calcularTemperaturaLead(deal, emp, ativPendente) {
  const cfg = CRM_STATE.kanban.config.temperatura || { quenteMaxDias: 3, mornoMaxDias: 10 };
  const quenteDias = cfg.quenteMaxDias || 3;
  const mornoDias = cfg.mornoMaxDias || 10;

  // Busca última atividade ou histórico
  let ultimaInteracaoDate = null;
  if (ativPendente && ativPendente.data_hora) {
    ultimaInteracaoDate = new Date(ativPendente.data_hora);
  }

  if (!ultimaInteracaoDate && CRM_STATE.dados?.historico_interacoes) {
    const hist = CRM_STATE.dados.historico_interacoes.find(h => h.deal_id === deal.id || h.empresa_id === deal.empresa_id);
    if (hist && hist.data_hora) {
      ultimaInteracaoDate = new Date(hist.data_hora);
    }
  }

  if (!ultimaInteracaoDate && deal.etapa_atualizada_em) {
    ultimaInteracaoDate = new Date(deal.etapa_atualizada_em);
  }

  if (!ultimaInteracaoDate && deal.criado_em) {
    ultimaInteracaoDate = new Date(deal.criado_em);
  }

  let dias = 15;
  if (ultimaInteracaoDate && !isNaN(ultimaInteracaoDate.getTime())) {
    dias = Math.max(0, Math.floor((new Date() - ultimaInteracaoDate) / (1000 * 60 * 60 * 24)));
  }

  if (dias <= quenteDias) {
    return { nivel: 'quente', label: '🔥 Quente', dias, desc: `Atividade recente (${dias}d atrás)` };
  } else if (dias <= mornoDias) {
    return { nivel: 'morno', label: '☀️ Morno', dias, desc: `Interação moderada (${dias}d atrás)` };
  } else {
    return { nivel: 'frio', label: '❄️ Frio', dias, desc: `Sem interação há ${dias}d` };
  }
}

// P0: Verificação de Atividade Atrasada (Prioridade Visual Máxima)
function verificarAtividadeAtrasada(ativPendente) {
  if (!ativPendente || ativPendente.status !== 'pendente' || !ativPendente.data_hora) {
    return { atrasada: false, diasAtraso: 0 };
  }
  try {
    const dt = new Date(ativPendente.data_hora);
    const agora = new Date();
    if (dt < agora) {
      const diasAtraso = Math.max(1, Math.floor((agora - dt) / (1000 * 60 * 60 * 24)));
      return { atrasada: true, diasAtraso, dataHora: ativPendente.data_hora, titulo: ativPendente.titulo };
    }
  } catch (e) {
    // ignore
  }
  return { atrasada: false, diasAtraso: 0 };
}

// P1: Ícone padronizado de canal com tooltip
function obterIconeCanalPadronizado(tipo, tituloAtiv, dataHora) {
  const t = (tipo || 'whatsapp').toLowerCase();
  let icone = '💬';
  let classe = 'wpp';
  let canalNome = 'WhatsApp';

  if (t.includes('ligacao') || t.includes('tel')) {
    icone = '📞'; classe = 'tel'; canalNome = 'Ligação Telefônica';
  } else if (t.includes('reuniao') || t.includes('demo')) {
    icone = '🤝'; classe = 'reuniao'; canalNome = 'Reunião / Demonstração';
  } else if (t.includes('visita') || t.includes('presencial')) {
    icone = '🚗'; classe = 'visita'; canalNome = 'Visita Presencial';
  } else if (t.includes('email')) {
    icone = '✉️'; classe = 'email'; canalNome = 'E-mail Comercial';
  } else if (t.includes('recontato')) {
    icone = '⏰'; classe = 'recontato'; canalNome = 'Recontato Programado';
  }

  const tooltip = `${canalNome}: ${tituloAtiv || 'Ação'} (${formatarDataHoraCurta(dataHora)})`;
  return `
    <span class="channel-icon-tag ${classe}" title="${escapeHtml(tooltip)}">
      ${icone}
    </span>
  `;
}

// Renderização Completa do Card
function renderCardDeal(deal, modoColuna) {
  const emp = (CRM_STATE.dados.empresas || []).find(e => e.id === deal.empresa_id) || {};
  const ctt = (CRM_STATE.dados.contatos || []).find(c => c.id === deal.contato_id) || {};
  const usr = (CRM_STATE.dados.usuarios || []).find(u => u.id === deal.responsavel_id) || {};

  const modo = modoColuna || CRM_STATE.kanban.modoExibicaoGlobal || 'expandido';
  const isCompacto = modo === 'compacto';

  const temProposta = deal.tem_proposta_rastreada || deal.proposta_hash;
  const isGanho = deal.status === 'ganho' || deal.etapa_id === 'etapa-fechado';
  const isAberta = Boolean(deal.ultima_visualizacao_proposta);
  const isRecontato = deal.etapa_id === 'etapa-recontato' || deal.status === 'recontato';

  const ativPendente = (CRM_STATE.dados.atividades || []).find(a => 
    a.status === 'pendente' && (a.deal_id === deal.id || a.empresa_id === deal.empresa_id)
  );

  // Cálculos visuais
  const atraso = verificarAtividadeAtrasada(ativPendente);
  const temp = calcularTemperaturaLead(deal, emp, ativPendente);
  const diasParado = calcularDiasSemMover(deal);
  const estiloParado = obterEstiloTempoParado(diasParado, deal.etapa_id);

  // Iniciais do responsável
  const nomeResp = usr.nome || 'Vendedor TruData';
  const iniciaisResp = nomeResp.split(' ').filter(Boolean).map(n => n[0]).slice(0, 2).join('').toUpperCase() || 'VD';

  // Informações de Recontato
  let badgeRecontatoHtml = '';
  if (isRecontato && deal.data_prevista) {
    try {
      const dtRec = new Date(deal.data_prevista + 'T09:00:00');
      const diasRestantes = Math.ceil((dtRec - new Date()) / (1000 * 60 * 60 * 24));
      let classeRec = '';
      let labelRec = `📅 Recontato: ${formatarDataCurta(deal.data_prevista)} (em ${diasRestantes}d)`;
      if (diasRestantes < 0) {
        classeRec = 'alerta-vencido';
        labelRec = `🚨 Recontato Vencido (${Math.abs(diasRestantes)}d atrás)`;
      } else if (diasRestantes <= 7) {
        classeRec = 'alerta-proximo';
        labelRec = `⚠️ Recontato Próximo (${diasRestantes}d)`;
      }
      badgeRecontatoHtml = `
        <span class="badge-recontato-futuro ${classeRec}" title="Data programada para reengajar esta oportunidade">
          ${labelRec}
        </span>
      `;
    } catch (e) {
      badgeRecontatoHtml = `<span class="badge-recontato-futuro">⏰ Recontato: ${escapeHtml(deal.data_prevista)}</span>`;
    }
  }

  return `
    <div class="deal-card temp-${temp.nivel} ${atraso.atrasada ? 'card-urgente-atrasado' : ''} ${isCompacto ? 'deal-card-compact' : 'deal-card-expanded'}" 
         id="card-${deal.id}" 
         draggable="true" 
         data-deal-id="${deal.id}"
         data-etapa-id="${deal.etapa_id}">
      
      <!-- P0: PRIORIDADE VISUAL MÁXIMA - ATIVIDADE ATRASADA -->
      ${atraso.atrasada ? `
        <div class="badge-urgencia-atrasada" title="Atividade pendente expirada há ${atraso.diasAtraso} dia(s). Requer atenção prioritária!">
          <span>🚨</span> <strong>Ação Atrasada há ${atraso.diasAtraso}d:</strong> ${escapeHtml(atraso.titulo || 'Atividade')}
        </div>
      ` : ''}

      <!-- CABEÇALHO DO CARD -->
      <div class="deal-card-header">
        <div class="deal-title" title="${escapeHtml(deal.titulo)}">${escapeHtml(deal.titulo)}</div>
        <div style="display:flex; align-items:center; gap:4px; flex-shrink:0;">
          <div class="resp-avatar-circle" title="Responsável: ${escapeHtml(nomeResp)}">
            ${iniciaisResp}
          </div>
          <button type="button" onclick="confirmarRemoverDeal('${deal.id}', event)" class="btn-crm" style="padding:0.15rem 0.35rem; font-size:0.7rem; color:#f87171; border-color:rgba(239,68,68,0.25); background:rgba(239,68,68,0.08); border-radius:4px; line-height:1;" title="Remover oportunidade do Kanban">🗑️</button>
        </div>
      </div>

      <!-- EMPRESA & CONTATO -->
      <div class="deal-company">
        🏢 <strong>${escapeHtml(emp.nome_fantasia || emp.razao_social || 'Empresa')}</strong>
        <span style="font-size:0.7rem; color:#94a3b8; font-weight:400;">(📍 ${escapeHtml(emp.cidade || 'RS')})</span>
      </div>

      <div class="deal-contact-line">
        <span>👤 ${escapeHtml(ctt.nome || 'Decisor')}</span>
        ${!isCompacto && emp.telefone ? `<span style="color:#64748b;">·</span> <span>📞 ${escapeHtml(emp.telefone)}</span>` : ''}
      </div>

      <!-- P0: BADGES DE TEMPERATURA & TEMPO PARADO NO ESTÁGIO -->
      <div class="deal-badges-row">
        <span class="badge-tempo-parado ${estiloParado.classe}" title="Tempo sem movimentação de estágio">
          ${estiloParado.label}
        </span>
        <span class="badge-temp-pill temp-${temp.nivel}" title="${escapeHtml(temp.desc)}">
          ${temp.label}
        </span>
        ${badgeRecontatoHtml}
      </div>

      <!-- FINANCEIRO: MRR & SETUP -->
      <div class="deal-financials">
        <span>MRR: <strong class="deal-mrr">R$ ${parseFloat(deal.valor_mrr || 0).toFixed(2)}/mês</strong></span>
        <span class="deal-setup-wrap" style="color:#94a3b8;">Setup: <strong style="color:#38bdf8;">R$ ${parseFloat(deal.valor_setup_produtos || 0).toFixed(2)}</strong></span>
      </div>

      <!-- P1: PRÓXIMA ATIVIDADE AGENDADA COM ÍCONES PADRONIZADOS -->
      ${ativPendente ? `
        <div class="activity-banner-card ${atraso.atrasada ? 'atrasada' : ''}">
          <div style="display:flex; align-items:center; gap:6px; overflow:hidden;">
            ${obterIconeCanalPadronizado(ativPendente.tipo, ativPendente.titulo, ativPendente.data_hora)}
            <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-weight:600;" title="${escapeHtml(ativPendente.titulo)}">
              ${escapeHtml(ativPendente.titulo)}
            </span>
          </div>
          <span style="font-family:'JetBrains Mono'; font-size:0.7rem; color:${atraso.atrasada ? '#f87171' : '#facc15'}; flex-shrink:0; font-weight:700;">
            ${formatarDataHoraCurta(ativPendente.data_hora)}
          </span>
        </div>
      ` : ''}

      <!-- AÇÕES RÁPIDAS (EXPANDIDO) -->
      <div class="deal-actions-expand-only" style="display:flex; justify-content:space-between; align-items:center; margin-top:0.15rem; padding-top:0.3rem; border-top:1px solid rgba(255,255,255,0.06);">
        <div style="display:flex; gap:0.25rem; align-items:center; flex-wrap:wrap;">
          ${temProposta ? `
            <span class="badge-proposal ${isGanho ? 'signed' : (isAberta ? 'opened' : '')}">
              ${isGanho ? '✓ Assinada' : (isAberta ? '👁️ Aberta' : '📄 Proposta')}
            </span>
          ` : ''}
          ${isGanho ? `
            <button type="button" onclick="irParaOnboardingDeal('${deal.id}')" class="btn-proposal-action" style="color:#10b981; border-color:rgba(16,185,129,0.4);" title="Ver Checklist de Implantação">
              🚀 Onboarding
            </button>
          ` : ''}
          <button type="button" onclick="abrirModalNovaAtividade('${deal.id}')" class="btn-proposal-action" style="color:#38bdf8; border-color:rgba(56,189,248,0.4);" title="Agendar ação (ligação, reunião, visita) para este lead">
            📅 Agendar
          </button>
        </div>
        <div>
          ${temProposta ? `
            <button type="button" onclick="abrirLinkProposta('${deal.proposta_hash}')" class="btn-proposal-action" title="Abrir link rastreável">🔗 Proposta</button>
          ` : `
            <button type="button" onclick="gerarProposta1Click('${deal.id}')" class="btn-proposal-action" title="Gerar Proposta Comercial 1-Click">📄 Proposta</button>
          `}
        </div>
      </div>

      <!-- RODAPÉ DO CARD: RESPONSÁVEL & EDIÇÃO -->
      <div class="deal-footer">
        <div class="resp-badge-wrapper" title="Vendedor responsável">
          <span style="font-weight:600; color:#e2e8f0;">👤 ${escapeHtml(nomeResp.split(' ')[0])}</span>
        </div>
        <div style="display:flex; gap:0.3rem; align-items:center;">
          <button type="button" onclick="abrirModalDetalhesDeal('${deal.id}')" class="btn-crm" style="padding:0.18rem 0.45rem; font-size:0.68rem;">Editar</button>
        </div>
      </div>
    </div>
  `;
}

// Renderização Geral do Kanban Board
function renderizarKanban() {
  const container = document.getElementById('kanban-board-container');
  if (!container || !CRM_STATE.dados) return;

  atualizarSelectsFiltrosGlobaisKanban();
  renderizarBarraFunilResumo();

  const funil = CRM_STATE.dados.funis.find(f => f.id === CRM_STATE.funilAtivoId) || CRM_STATE.dados.funis[0];
  if (!funil) return;

  // Filtragem Global Multidimensional (sem quebrar estrutura de colunas)
  const fg = CRM_STATE.kanban.filtrosGlobais;
  const termoGlobal = (fg.busca || '').toLowerCase().trim();

  const dealsFiltrados = CRM_STATE.dados.negociacoes.filter(deal => {
    if (deal.funil_id !== funil.id) return false;

    // Filtro por Responsável
    if (fg.responsavel !== 'todos' && deal.responsavel_id !== fg.responsavel) {
      return false;
    }

    // Filtro por MRR
    const mrr = parseFloat(deal.valor_mrr || 0);
    if (fg.mrr === 'ate-200' && mrr > 200) return false;
    if (fg.mrr === '200-500' && (mrr <= 200 || mrr > 500)) return false;
    if (fg.mrr === 'acima-500' && mrr <= 500) return false;

    // Dados da Empresa e Contato
    const emp = (CRM_STATE.dados.empresas || []).find(e => e.id === deal.empresa_id) || {};
    const ctt = (CRM_STATE.dados.contatos || []).find(c => c.id === deal.contato_id) || {};

    // Filtro por Cidade
    if (fg.cidade !== 'todas' && (emp.cidade || '').trim().toLowerCase() !== fg.cidade.toLowerCase()) {
      return false;
    }

    // Filtro por Segmento / Tag
    if (fg.segmento !== 'todos') {
      const matchEmpSeg = (emp.segmento || '').trim().toLowerCase() === fg.segmento.toLowerCase();
      const matchTags = (deal.tags || []).some(t => t.toLowerCase() === fg.segmento.toLowerCase());
      if (!matchEmpSeg && !matchTags) return false;
    }

    // Filtro por Origem
    if (fg.origem !== 'todas') {
      const matchOrig = (emp.origem || '').toLowerCase().includes(fg.origem.toLowerCase()) ||
                        (deal.tags || []).some(t => t.toLowerCase().includes(fg.origem.toLowerCase()));
      if (!matchOrig) return false;
    }

    // Busca textual global
    if (termoGlobal) {
      const textoCompleto = `${deal.titulo} ${emp.nome_fantasia || ''} ${emp.razao_social || ''} ${emp.cidade || ''} ${emp.telefone || ''} ${ctt.nome || ''}`.toLowerCase();
      if (!textoCompleto.includes(termoGlobal)) return false;
    }

    return true;
  });

  const cfgKanban = CRM_STATE.kanban.config;
  const wipMap = cfgKanban.wipLimites || {};

  container.innerHTML = funil.etapas.map(etapa => {
    // Negócios desta etapa após filtros globais
    let dealsEtapa = dealsFiltrados.filter(d => d.etapa_id === etapa.id);

    // Totais da etapa (calculados sobre o universo total filtrado da coluna)
    const totalCardsEtapa = dealsEtapa.length;
    const mrrEtapa = dealsEtapa.reduce((acc, d) => acc + (parseFloat(d.valor_mrr) || 0), 0);
    const setupEtapa = dealsEtapa.reduce((acc, d) => acc + (parseFloat(d.valor_setup_produtos) || 0), 0);

    // P0: Limites de WIP e Alertas no cabeçalho
    const wipLimite = wipMap[etapa.id] || 50;
    const isWipExceeded = totalCardsEtapa > wipLimite;
    const isWipNear = !isWipExceeded && totalCardsEtapa >= Math.floor(wipLimite * 0.85);

    let wipBadgeClass = 'wip-ok';
    let colWipClass = '';
    if (isWipExceeded) {
      wipBadgeClass = 'wip-exceeded';
      colWipClass = 'wip-exceeded';
    } else if (isWipNear) {
      wipBadgeClass = 'wip-warning';
      colWipClass = 'wip-warning';
    }

    // P0: Busca interna dentro da coluna
    const termoColuna = (CRM_STATE.kanban.colBusca[etapa.id] || '').toLowerCase().trim();
    if (termoColuna) {
      dealsEtapa = dealsEtapa.filter(d => {
        const emp = (CRM_STATE.dados.empresas || []).find(e => e.id === d.empresa_id) || {};
        const ctt = (CRM_STATE.dados.contatos || []).find(c => c.id === d.contato_id) || {};
        const usr = (CRM_STATE.dados.usuarios || []).find(u => u.id === d.responsavel_id) || {};
        const txt = `${d.titulo} ${emp.nome_fantasia || ''} ${emp.razao_social || ''} ${emp.cidade || ''} ${ctt.nome || ''} ${usr.nome || ''}`.toLowerCase();
        return txt.includes(termoColuna);
      });
    }

    // P0: Ordenação por coluna
    const ordenacao = CRM_STATE.kanban.colOrdenacao[etapa.id] || 'recente';
    dealsEtapa.sort((a, b) => {
      if (ordenacao === 'mrr_desc') {
        return (parseFloat(b.valor_mrr) || 0) - (parseFloat(a.valor_mrr) || 0);
      } else if (ordenacao === 'prob_desc') {
        return (parseFloat(b.probabilidade) || 0) - (parseFloat(a.probabilidade) || 0);
      } else if (ordenacao === 'tempo_parado') {
        return calcularDiasSemMover(b) - calcularDiasSemMover(a);
      } else if (ordenacao === 'ativ_prox') {
        const ativA = (CRM_STATE.dados.atividades || []).find(x => x.status === 'pendente' && x.deal_id === a.id);
        const ativB = (CRM_STATE.dados.atividades || []).find(x => x.status === 'pendente' && x.deal_id === b.id);
        const dataA = ativA?.data_hora || '9999';
        const dataB = ativB?.data_hora || '9999';
        return dataA.localeCompare(dataB);
      } else {
        // 'recente' padrão
        const dataA = a.etapa_atualizada_em || a.criado_em || '';
        const dataB = b.etapa_atualizada_em || b.criado_em || '';
        return dataB.localeCompare(dataA);
      }
    });

    // P0: Paginação / Lazy-load na coluna
    const limiteCards = CRM_STATE.kanban.colLimitesExibicao[etapa.id] || 25;
    const cardsParaExibir = dealsEtapa.slice(0, limiteCards);
    const temMaisCards = dealsEtapa.length > limiteCards;

    // Modo da coluna (compacto ou expandido)
    const modoColuna = CRM_STATE.kanban.colModos[etapa.id] || CRM_STATE.kanban.modoExibicaoGlobal;
    const isColCompacta = modoColuna === 'compacto';

    return `
      <div class="kanban-col-ent ${colWipClass}" 
           data-etapa-id="${etapa.id}" 
           ondragover="permitirSoltarKanban(event)" 
           ondragleave="sairSoltarKanban(event)" 
           ondrop="soltarNoKanban(event, '${etapa.id}')">
        
        <!-- CABEÇALHO DA COLUNA -->
        <div class="col-header-ent">
          <div class="col-header-top-row">
            <span class="col-title-ent" style="color: ${etapa.cor};" title="${escapeHtml(etapa.nome)}">
              <span>●</span> ${escapeHtml(etapa.nome)}
            </span>
            <div class="col-header-badges">
              <span class="badge-wip ${wipBadgeClass}" title="Capacidade da etapa: ${totalCardsEtapa} cards de limite ${wipLimite}">
                WIP: ${totalCardsEtapa}/${wipLimite} ${isWipExceeded ? '⚠️' : ''}
              </span>
              <span class="badge-ent" style="background:rgba(255,255,255,0.08); font-size:0.75rem;">
                ${totalCardsEtapa}
              </span>
            </div>
          </div>

          <!-- TOTAIS DA ETAPA -->
          <div class="col-totals-ent">
            <span>MRR: <strong style="color:#34d399;">R$ ${mrrEtapa.toFixed(0)}</strong></span>
            <span>Setup: <strong style="color:#38bdf8;">R$ ${setupEtapa.toFixed(0)}</strong></span>
            <span>Prob: <strong>${etapa.probabilidade}%</strong></span>
          </div>

          <!-- P0: CONTROLES INTERNOS DA COLUNA (BUSCA, ORDENAÇÃO E TOGGLE DE MODO) -->
          <div class="col-controls-ent">
            <input type="text" 
                   class="col-search-input" 
                   placeholder="🔍 Buscar na coluna..." 
                   value="${escapeHtml(termoColuna)}" 
                   oninput="filtrarColunaKanban('${etapa.id}', this.value)">
            
            <select class="col-sort-select" onchange="ordenarColunaKanban('${etapa.id}', this.value)" title="Ordenar cards desta coluna">
              <option value="recente" ${ordenacao === 'recente' ? 'selected' : ''}>Mais recente</option>
              <option value="mrr_desc" ${ordenacao === 'mrr_desc' ? 'selected' : ''}>Maior MRR</option>
              <option value="prob_desc" ${ordenacao === 'prob_desc' ? 'selected' : ''}>Maior Prob.</option>
              <option value="tempo_parado" ${ordenacao === 'tempo_parado' ? 'selected' : ''}>Tempo parado</option>
              <option value="ativ_prox" ${ordenacao === 'ativ_prox' ? 'selected' : ''}>Próx. ação</option>
            </select>

            <button type="button" 
                    class="btn-col-toggle-mode" 
                    onclick="alternarModoExibicaoColuna('${etapa.id}')" 
                    title="Alternar entre modo compacto e expandido para esta coluna">
              ${isColCompacta ? '⊟' : '⊞'}
            </button>
          </div>
        </div>

        <!-- LISTA DE CARDS (COM DRAG-AND-DROP E LAZY LOADING) -->
        <div class="col-cards-list" id="cards-list-${etapa.id}" data-etapa-id="${etapa.id}">
          ${cardsParaExibir.length === 0 ? `
            <div style="text-align:center; padding:1.5rem 0.5rem; color:#64748b; font-size:0.75rem;">
              ${termoColuna ? 'Nenhum lead encontrado com esta busca.' : 'Nenhum negócio nesta etapa.'}
            </div>
          ` : cardsParaExibir.map(d => renderCardDeal(d, modoColuna)).join('')}
        </div>

        <!-- P0: FOOTER DE LAZY LOADING -->
        ${temMaisCards ? `
          <div class="col-lazy-footer">
            <div>Exibindo <strong>${cardsParaExibir.length}</strong> de <strong>${dealsEtapa.length}</strong> negócios</div>
            <div style="display:flex; justify-content:center; gap:0.4rem; margin-top:0.25rem;">
              <button type="button" class="btn-lazy-load" onclick="carregarMaisCardsColuna('${etapa.id}', false)">
                + Carregar mais 25
              </button>
              <button type="button" class="btn-lazy-load" style="background:rgba(255,255,255,0.06); color:#cbd5e1; border-color:rgba(255,255,255,0.15);" onclick="carregarMaisCardsColuna('${etapa.id}', true)">
                Ver todos (${dealsEtapa.length})
              </button>
            </div>
          </div>
        ` : (dealsEtapa.length > 25 ? `
          <div class="col-lazy-footer" style="color:#64748b;">
            Todos os ${dealsEtapa.length} negócios carregados.
          </div>
        ` : '')}
      </div>
    `;
  }).join('');

  // Ativar eventos de Drag and Drop
  document.querySelectorAll('.deal-card').forEach(card => {
    card.addEventListener('dragstart', iniciarArrastoDeal);
    card.addEventListener('dragend', finalizarArrastoDeal);
  });

  // Ativar detecção automática de rolagem para Lazy Loading infinito
  document.querySelectorAll('.col-cards-list').forEach(list => {
    list.addEventListener('scroll', function() {
      const etapaId = this.dataset.etapaId;
      if (!etapaId) return;
      if (this.scrollHeight - this.scrollTop - this.clientHeight < 120) {
        const limiteAtual = CRM_STATE.kanban.colLimitesExibicao[etapaId] || 25;
        const total = dealsFiltrados.filter(d => d.etapa_id === etapaId).length;
        if (limiteAtual < total) {
          carregarMaisCardsColuna(etapaId, false);
        }
      }
    });
  });
}

// Drag and Drop Nativo HTML5
let DEAL_ARRASTADO_ID = null;

function iniciarArrastoDeal(e) {
  DEAL_ARRASTADO_ID = e.target.dataset.dealId;
  e.target.classList.add('dragging');
  e.dataTransfer.setData('text/plain', DEAL_ARRASTADO_ID);
}

function finalizarArrastoDeal(e) {
  e.target.classList.remove('dragging');
}

function permitirSoltarKanban(e) {
  e.preventDefault();
  e.currentTarget.classList.add('drag-over');
}

function sairSoltarKanban(e) {
  e.currentTarget.classList.remove('drag-over');
}

async function soltarNoKanban(e, novaEtapaId) {
  e.preventDefault();
  e.currentTarget.classList.remove('drag-over');
  const dealId = e.dataTransfer.getData('text/plain') || DEAL_ARRASTADO_ID;
  if (!dealId) return;

  // P1: Ao mover para Negócio Perdido, abrir modal obrigatório em vez de prompt simples
  if (novaEtapaId.includes('perdido') || novaEtapaId.includes('descarte') || novaEtapaId.includes('recusa')) {
    abrirModalMotivoPerda(dealId, novaEtapaId);
    return;
  }

  // Estágio Recontato: solicitar prazo
  if (novaEtapaId === 'etapa-recontato' || novaEtapaId.includes('recontato')) {
    solicitarPrazoRecontatoDeal(dealId, novaEtapaId);
    return;
  }

  await enviarMudancaEtapa(dealId, novaEtapaId, '', '');
}

async function enviarMudancaEtapa(dealId, novaEtapaId, motivoPerda = '', observacaoPerda = '') {
  try {
    const res = await fetch('/api/crm/v2/mover_etapa', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Usuario-Id': CRM_STATE.usuarioAtivo.id
      },
      body: JSON.stringify({
        deal_id: dealId,
        nova_etapa_id: novaEtapaId,
        motivo_perda: motivoPerda,
        observacao_perda: observacaoPerda
      })
    });
    const json = await res.json();
    if (json.sucesso) {
      await carregarEstadoCRM();
    } else {
      alert('Erro ao mover etapa: ' + (json.erro || 'Falha desconhecida'));
    }
  } catch (e) {
    console.error('Falha ao mover etapa:', e);
  }
}

// P1: Fluxo do Modal Obrigatório de Negócio Perdido
function abrirModalMotivoPerda(dealId, novaEtapaId) {
  const modal = document.getElementById('modal-motivo-perda');
  const inpDealId = document.getElementById('perda-deal-id');
  const inpNovaEtapa = document.getElementById('perda-nova-etapa-id');
  const selMotivo = document.getElementById('perda-motivo-select');
  const wrapOutro = document.getElementById('perda-campo-outro-wrap');
  const inpOutro = document.getElementById('perda-motivo-outro-input');
  const inpObs = document.getElementById('perda-observacoes-input');
  const txtTitulo = document.getElementById('perda-deal-titulo');
  const txtEmpresa = document.getElementById('perda-deal-empresa');

  if (!modal) return;

  const deal = (CRM_STATE.dados?.negociacoes || []).find(d => d.id === dealId);
  const emp = deal ? (CRM_STATE.dados?.empresas || []).find(e => e.id === deal.empresa_id) : null;

  if (inpDealId) inpDealId.value = dealId;
  if (inpNovaEtapa) inpNovaEtapa.value = novaEtapaId;
  if (selMotivo) selMotivo.value = '';
  if (wrapOutro) wrapOutro.classList.add('hidden');
  if (inpOutro) inpOutro.value = '';
  if (inpObs) inpObs.value = '';

  if (txtTitulo) txtTitulo.textContent = deal ? deal.titulo : 'Negociação';
  if (txtEmpresa) txtEmpresa.textContent = emp ? `🏢 ${emp.nome_fantasia || emp.razao_social} (${emp.cidade || 'RS'})` : '';

  modal.classList.remove('hidden');
}

function aoMudarMotivoPerdaSelect(val) {
  const wrapOutro = document.getElementById('perda-campo-outro-wrap');
  if (wrapOutro) {
    wrapOutro.classList.toggle('hidden', val !== 'Outro');
  }
}

function cancelarModalMotivoPerda() {
  const modal = document.getElementById('modal-motivo-perda');
  if (modal) modal.classList.add('hidden');
  renderizarKanban(); // Restaura posição original sem alterar
}

async function confirmarSalvarPerdaDeal() {
  const dealId = document.getElementById('perda-deal-id')?.value;
  const novaEtapaId = document.getElementById('perda-nova-etapa-id')?.value || 'etapa-perdido';
  const selMotivo = document.getElementById('perda-motivo-select')?.value;
  const inpOutro = document.getElementById('perda-motivo-outro-input')?.value.trim();
  const obs = document.getElementById('perda-observacoes-input')?.value.trim();

  if (!selMotivo) {
    alert('Por favor, selecione o motivo da perda do negócio.');
    return;
  }

  let motivoFinal = selMotivo;
  if (selMotivo === 'Outro') {
    if (!inpOutro) {
      alert('Por favor, descreva o motivo específico da perda no campo indicado.');
      return;
    }
    motivoFinal = `Outro: ${inpOutro}`;
  }

  const modal = document.getElementById('modal-motivo-perda');
  if (modal) modal.classList.add('hidden');

  await enviarMudancaEtapa(dealId, novaEtapaId, motivoFinal, obs);
}

function solicitarPrazoRecontatoDeal(dealId, novaEtapaId) {
  const prazo = prompt('⏰ Recontato Comercial (Nutrição):\nQual o prazo previsto para recontatar este cliente?\n\n• Digite "6 meses" (Padrão: 180 dias)\n• Digite "1 ano" (365 dias)\n• Ou digite uma data / motivo personalizado:', '6 meses');
  if (prazo !== null) {
    enviarMudancaEtapa(dealId, novaEtapaId, prazo.trim(), '');
  } else {
    renderizarKanban(); // Cancela arrasto
  }
}

// P0/P2: Modal de Configuração de Regras do Kanban
function abrirModalConfigKanban() {
  const modal = document.getElementById('modal-config-kanban');
  if (!modal) return;

  const cfg = CRM_STATE.kanban.config;
  const w = cfg.wipLimites || {};
  const tp = cfg.tempoParado || {};
  const temp = cfg.temperatura || {};

  const elWLead = document.getElementById('cfg-wip-lead');
  if (elWLead) elWLead.value = w['etapa-lead'] || 60;

  const elWContato = document.getElementById('cfg-wip-contato');
  if (elWContato) elWContato.value = w['etapa-contato'] || 15;

  const elWDemo = document.getElementById('cfg-wip-demo');
  if (elWDemo) elWDemo.value = w['etapa-demo'] || 10;

  const elWProp = document.getElementById('cfg-wip-proposta');
  if (elWProp) elWProp.value = w['etapa-proposta'] || 15;

  const elWFechado = document.getElementById('cfg-wip-fechado');
  if (elWFechado) elWFechado.value = w['etapa-fechado'] || 100;

  const elWRecontato = document.getElementById('cfg-wip-recontato');
  if (elWRecontato) elWRecontato.value = w['etapa-recontato'] || 50;

  const elTV = document.getElementById('cfg-tempo-verde');
  if (elTV) elTV.value = tp.verdeMaxDias || 3;

  const elTA = document.getElementById('cfg-tempo-amarelo');
  if (elTA) elTA.value = tp.amareloMaxDias || 10;

  const elTQ = document.getElementById('cfg-temp-quente');
  if (elTQ) elTQ.value = temp.quenteMaxDias || 3;

  const elTM = document.getElementById('cfg-temp-morno');
  if (elTM) elTM.value = temp.mornoMaxDias || 10;

  modal.classList.remove('hidden');
}

function fecharModalConfigKanban() {
  const modal = document.getElementById('modal-config-kanban');
  if (modal) modal.classList.add('hidden');
}

function salvarConfiguracoesKanbanForm() {
  const novaConfig = {
    wipLimites: {
      'etapa-lead': parseInt(document.getElementById('cfg-wip-lead')?.value || 60, 10),
      'etapa-contato': parseInt(document.getElementById('cfg-wip-contato')?.value || 15, 10),
      'etapa-demo': parseInt(document.getElementById('cfg-wip-demo')?.value || 10, 10),
      'etapa-proposta': parseInt(document.getElementById('cfg-wip-proposta')?.value || 15, 10),
      'etapa-fechado': parseInt(document.getElementById('cfg-wip-fechado')?.value || 100, 10),
      'etapa-recontato': parseInt(document.getElementById('cfg-wip-recontato')?.value || 50, 10),
      'etapa-perdido': 200
    },
    tempoParado: {
      verdeMaxDias: parseInt(document.getElementById('cfg-tempo-verde')?.value || 3, 10),
      amareloMaxDias: parseInt(document.getElementById('cfg-tempo-amarelo')?.value || 10, 10)
    },
    temperatura: {
      quenteMaxDias: parseInt(document.getElementById('cfg-temp-quente')?.value || 3, 10),
      mornoMaxDias: parseInt(document.getElementById('cfg-temp-morno')?.value || 10, 10)
    }
  };

  CRM_STATE.kanban.config = novaConfig;
  try {
    localStorage.setItem('trudata_crm_kanban_config', JSON.stringify(novaConfig));
  } catch (e) {
    console.error('Falha ao salvar config do kanban:', e);
  }

  fecharModalConfigKanban();
  renderizarKanban();
  if (typeof mostrarToastCRM === 'function') {
    mostrarToastCRM('Regras do Kanban atualizadas com sucesso!', 'sucesso');
  }
}

function restaurarConfiguracoesPadraoKanban() {
  const def = obterConfiguracoesPadraoKanban();
  CRM_STATE.kanban.config = def;
  try {
    localStorage.removeItem('trudata_crm_kanban_config');
  } catch (e) {
    // ignore
  }
  abrirModalConfigKanban(); // Atualiza campos com padrão
  renderizarKanban();
  if (typeof mostrarToastCRM === 'function') {
    mostrarToastCRM('Padrões recomendados restaurados!', 'info');
  }
}

// ==================== 3. GESTÃO DE CONTATOS & EMPRESAS ====================
function renderizarContatosEmpresas() {
  const container = document.getElementById('view-contatos_empresas');
  if (!container) return;

  const termo = CRM_STATE.filtroBusca.toLowerCase().trim();
  const empresas = CRM_STATE.dados.empresas.filter(e => {
    if (termo) {
      const txt = `${e.nome_fantasia} ${e.razao_social} ${e.documento} ${e.cidade} ${e.telefone} ${e.email}`.toLowerCase();
      if (!txt.includes(termo)) return false;
    }
    return true;
  });

  container.innerHTML = `
    <div class="kanban-toolbar">
      <div style="display:flex; gap:0.5rem; align-items:center; flex-wrap:wrap;">
        <input type="text" id="busca-contatos" class="crm-form-input" style="min-width:260px;" placeholder="🔍 Buscar empresa, CNPJ/CPF, cidade..." value="${CRM_STATE.filtroBusca}" oninput="filtrarContatos(event)">
        <button onclick="abrirModalNovaEmpresa()" class="btn-crm btn-crm-primary">+ Nova Empresa (PF/PJ)</button>
        <button onclick="verificarDuplicidades()" class="btn-crm" style="background:#d97706; color:#fff;">⚡ Deduplicação Automática</button>
      </div>
      <div style="display:flex; gap:0.5rem; align-items:center;">
        <button onclick="document.getElementById('input-import-csv').click()" class="btn-crm">📥 Importar CSV</button>
        <input type="file" id="input-import-csv" style="display:none;" accept=".csv,.txt" onchange="importarPlanilhaCSV(event)">
        <a href="/api/crm/v2/exportar_csv?tipo=empresas" download class="btn-crm btn-crm-success">📤 Exportar Planilha</a>
      </div>
    </div>

    <div id="painel-deduplicacao" style="display:none;"></div>

    <div class="crm-table-container">
      <table class="crm-table crm-table-empresas">
        <thead>
          <tr>
            <th style="width:75px; text-align:center;">Tipo</th>
            <th>Empresa / Razão Social</th>
            <th>Documento (CNPJ/CPF)</th>
            <th>Cidade / UF</th>
            <th>Segmento & PDVs</th>
            <th>Telefone / WhatsApp</th>
            <th style="width:110px; text-align:center;">LGPD</th>
            <th style="width:160px; text-align:center;">Ações</th>
          </tr>
        </thead>
        <tbody>
          ${empresas.map(emp => {
            const contatos = CRM_STATE.dados.contatos.filter(c => c.empresa_id === emp.id);
            const nomeExibicao = emp.nome_fantasia || emp.razao_social || 'Empresa sem nome';
            const inicial = (nomeExibicao.trim().charAt(0) || 'E').toUpperCase();
            
            const tipoUpper = (emp.tipo || 'PJ').toUpperCase();
            let badgeClass = 'badge-pj';
            if (tipoUpper === 'PF') badgeClass = 'badge-pf';
            else if (tipoUpper === 'MEI') badgeClass = 'badge-mei';
            else if (tipoUpper.includes('RURAL')) badgeClass = 'badge-rural';
            else if (tipoUpper !== 'PJ') badgeClass = 'badge-outro';

            return `
              <tr>
                <td style="text-align:center; white-space:nowrap;"><span class="badge-ent ${badgeClass}">${tipoUpper}</span></td>
                <td>
                  <div class="crm-empresa-cell">
                    <div class="crm-avatar-empresa" aria-hidden="true">${inicial}</div>
                    <div class="crm-empresa-meta">
                      <span class="crm-empresa-name">${escapeHtml(nomeExibicao)}</span>
                      <span class="crm-empresa-sub">${contatos.length} contato(s) vinculado(s)</span>
                    </div>
                  </div>
                </td>
                <td style="font-family:'JetBrains Mono'; font-size:0.78rem; color:#cbd5e1; white-space:nowrap;">${emp.documento || 'Não informado'}</td>
                <td style="white-space:nowrap;">
                  <span class="crm-chip-cidade">
                    <svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                    ${escapeHtml(emp.cidade || 'Não informada')} - ${escapeHtml(emp.uf || 'RS')}
                  </span>
                </td>
                <td>
                  <div style="font-size:0.82rem; color:#f8fafc;">${escapeHtml(emp.segmento || 'Geral')}</div>
                  <div style="font-size:0.73rem; color:#94a3b8;">${emp.pdvs_estimados || 1} PDV(s)</div>
                </td>
                <td style="font-size:0.82rem; color:#cbd5e1; white-space:nowrap;">${escapeHtml(emp.telefone || emp.whatsapp || '-')}</td>
                <td style="text-align:center; white-space:nowrap;">
                  <span class="badge-ent ${emp.consentimento_lgpd?.autorizado ? 'badge-ganho' : 'badge-perdido'}" style="white-space:nowrap; display:inline-flex; align-items:center; justify-content:center; gap:0.35rem;">
                    ${emp.consentimento_lgpd?.autorizado ? '<span>✓</span><span>Ativo</span>' : '<span>Revogado</span>'}
                  </span>
                </td>
                <td>
                  <div class="crm-actions-group" style="justify-content:center;">
                    <button onclick="abrirModalDetalhesEmpresa('${emp.id}')" class="btn-crm-icon btn-action-view" data-tooltip="Visualizar Detalhes" title="Visualizar Detalhes" aria-label="Visualizar">
                      <svg viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                    </button>
                    <button onclick="abrirModalEditarEmpresa('${emp.id}')" class="btn-crm-icon btn-action-edit" data-tooltip="Editar Empresa" title="Editar Empresa" aria-label="Editar">
                      <svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                    </button>
                    <button onclick="exportarDossieLGPD('${emp.documento || emp.email || emp.id}')" class="btn-crm-icon btn-action-lgpd" data-tooltip="Dossiê LGPD" title="Dossiê LGPD" aria-label="LGPD">
                      <svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                    </button>
                    <button onclick="confirmarExcluirEmpresa('${emp.id}')" class="btn-crm-icon btn-action-delete" data-tooltip="Excluir Empresa" title="Excluir Empresa" aria-label="Excluir">
                      <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                    </button>
                  </div>
                </td>
              </tr>
            `;
          }).join('')}
        </tbody>
      </table>
    </div>
  `;
}

function filtrarContatos(e) {
  CRM_STATE.filtroBusca = e.target.value;
  renderizarContatosEmpresas();
}

async function verificarDuplicidades() {
  const painel = document.getElementById('painel-deduplicacao');
  if (!painel) return;

  try {
    const res = await fetch('/api/crm/v2/deduplicar');
    const json = await res.json();
    if (json.total_grupos === 0) {
      painel.style.display = 'block';
      painel.innerHTML = `
        <div class="dedup-card" style="border-color:#10b981; background:rgba(16,185,129,0.1);">
          <div style="color:#34d399; font-weight:700;">✅ Nenhuma duplicidade detectada! Base 100% íntegra.</div>
        </div>
      `;
      return;
    }

    painel.style.display = 'block';
    painel.innerHTML = `
      <div class="dedup-card">
        <h4 style="color:#fbbf24; margin-bottom:0.5rem;">⚠️ ${json.total_grupos} grupo(s) de registros duplicados encontrados:</h4>
        ${json.grupos.map(g => `
          <div style="background:#090e18; padding:0.75rem; border-radius:8px; margin-bottom:0.5rem; display:flex; justify-content:space-between; align-items:center;">
            <div>
              <strong>Conflito por ${g.criterio}:</strong> <code>${g.chave_conflito}</code> (${g.quantidade} registros)
              <div style="font-size:0.75rem; color:#94a3b8;">${g.empresas.map(e => e.nome_fantasia).join(' | ')}</div>
            </div>
            <button onclick="mesclarGrupoDuplicados('${g.empresas[0].id}', ${JSON.stringify(g.empresas.slice(1).map(e => e.id))})" class="btn-crm btn-crm-primary" style="font-size:0.75rem;">
              ⚡ Mesclar em 1 Registro
            </button>
          </div>
        `).join('')}
      </div>
    `;
  } catch (e) {
    console.error('Erro na deduplicação:', e);
  }
}

async function mesclarGrupoDuplicados(idPrimario, idsSecundarios) {
  if (!confirm('Confirma mesclar esses registros duplicados mantendo o primeiro como principal?')) return;
  try {
    const res = await fetch('/api/crm/v2/mesclar_empresas', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Usuario-Id': CRM_STATE.usuarioAtivo.id },
      body: JSON.stringify({ id_primario: idPrimario, ids_secundarios: idsSecundarios })
    });
    const json = await res.json();
    if (json.sucesso) {
      alert('Registros mesclados com sucesso!');
      await carregarEstadoCRM();
    }
  } catch (e) {
    console.error('Erro ao mesclar:', e);
  }
}

// ==================== 4. NEGOCIAÇÕES & DEALS ====================
function renderizarNegociacoes() {
  const container = document.getElementById('view-negociacoes');
  if (!container) return;

  const deals = CRM_STATE.dados.negociacoes;

  container.innerHTML = `
    <div class="kanban-toolbar">
      <div style="display:flex; gap:0.5rem; align-items:center;">
        <button onclick="abrirModalNovoDeal()" class="btn-crm btn-crm-primary">+ Nova Negociação (Deal)</button>
      </div>
      <div>
        <a href="/api/crm/v2/exportar_csv?tipo=negociacoes" download class="btn-crm btn-crm-success">📤 Exportar Negociações (.CSV)</a>
      </div>
    </div>

    <div class="crm-table-container">
      <table class="crm-table">
        <thead>
          <tr>
            <th>Título da Oportunidade</th>
            <th>Empresa</th>
            <th>Funil & Etapa</th>
            <th>MRR</th>
            <th>Setup</th>
            <th>Probabilidade</th>
            <th>Previsão</th>
            <th>Status</th>
            <th>Responsável</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          ${deals.map(d => {
            const emp = CRM_STATE.dados.empresas.find(e => e.id === d.empresa_id) || {};
            const usr = CRM_STATE.dados.usuarios.find(u => u.id === d.responsavel_id) || {};
            return `
              <tr>
                <td><strong>${d.titulo}</strong></td>
                <td>${emp.nome_fantasia || 'Empresa'}</td>
                <td><span class="badge-ent" style="background:#1e293b;">${d.etapa_id}</span></td>
                <td style="color:#34d399; font-family:'JetBrains Mono'; font-weight:700;">R$ ${parseFloat(d.valor_mrr || 0).toFixed(2)}</td>
                <td style="color:#38bdf8; font-family:'JetBrains Mono';">R$ ${parseFloat(d.valor_setup_produtos || 0).toFixed(2)}</td>
                <td><strong>${d.probabilidade}%</strong></td>
                <td>${d.data_prevista || '-'}</td>
                <td>
                  <span class="badge-ent ${d.status === 'ganho' ? 'badge-ganho' : d.status === 'perdido' ? 'badge-perdido' : 'badge-aberto'}">
                    ${d.status.toUpperCase()}
                  </span>
                </td>
                <td>👤 ${usr.nome ? usr.nome.split(' ')[0] : '-'}</td>
                <td>
                  <div style="display:flex; gap:0.3rem;">
                    <button onclick="abrirModalDetalhesDeal('${d.id}')" class="btn-crm" style="padding:0.2rem 0.5rem; font-size:0.7rem;">Editar</button>
                    <button onclick="confirmarRemoverDeal('${d.id}', event)" class="btn-crm" style="padding:0.2rem 0.5rem; font-size:0.7rem; color:#ef4444; border-color:rgba(239,68,68,0.3); background:rgba(239,68,68,0.08);" title="Remover do Kanban">🗑️</button>
                  </div>
                </td>
              </tr>
            `;
          }).join('')}
        </tbody>
      </table>
    </div>
  `;
}

// ==================== 5. ATIVIDADES, TAREFAS & CALENDÁRIO VISUAL ====================

const DIAS_SEMANA_NOMES = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'];
const DIAS_SEMANA_CURTO = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'];
const MESES_NOMES = [
  'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
  'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
];

function iconeTipoAtividade(t) {
  switch ((t || '').toLowerCase()) {
    case 'ligacao': return '📞';
    case 'reuniao': return '🤝';
    case 'visita': return '🚗';
    case 'whatsapp': return '💬';
    case 'email': return '✉️';
    case 'recontato': return '⏰';
    default: return '📋';
  }
}

function corTipoAtividade(t) {
  switch ((t || '').toLowerCase()) {
    case 'whatsapp':
      return { border: '#10b981', bg: 'rgba(16, 185, 129, 0.16)', text: '#34d399', badgeBg: 'rgba(16, 185, 129, 0.25)' };
    case 'ligacao':
      return { border: '#0284c7', bg: 'rgba(2, 132, 199, 0.16)', text: '#38bdf8', badgeBg: 'rgba(2, 132, 199, 0.25)' };
    case 'reuniao':
      return { border: '#a855f7', bg: 'rgba(168, 85, 247, 0.16)', text: '#c084fc', badgeBg: 'rgba(168, 85, 247, 0.25)' };
    case 'visita':
      return { border: '#f59e0b', bg: 'rgba(245, 158, 11, 0.16)', text: '#fbbf24', badgeBg: 'rgba(245, 158, 11, 0.25)' };
    case 'email':
      return { border: '#06b6d4', bg: 'rgba(6, 182, 212, 0.16)', text: '#22d3ee', badgeBg: 'rgba(6, 182, 212, 0.25)' };
    case 'recontato':
      return { border: '#ec4899', bg: 'rgba(236, 72, 153, 0.16)', text: '#f472b6', badgeBg: 'rgba(236, 72, 153, 0.25)' };
    default:
      return { border: '#94a3b8', bg: 'rgba(148, 163, 184, 0.16)', text: '#cbd5e1', badgeBg: 'rgba(148, 163, 184, 0.25)' };
  }
}

function formatarDataHora(dh) {
  if (!dh) return '-';
  try {
    const d = new Date(dh);
    if (isNaN(d.getTime())) return dh;
    return d.toLocaleString('pt-BR');
  } catch (e) {
    return dh;
  }
}

function formatarIsoDate(d) {
  const pad = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

function formatarHoraCurta(dh) {
  if (!dh) return '--:--';
  try {
    const d = new Date(dh);
    if (isNaN(d.getTime())) return '--:--';
    const pad = n => String(n).padStart(2, '0');
    return `${pad(d.getHours())}:${pad(d.getMinutes())}`;
  } catch (e) {
    return '--:--';
  }
}

function obterNomeEmpresa(empId) {
  const emp = (CRM_STATE.dados?.empresas || []).find(e => e.id === empId);
  return emp ? (emp.nome_fantasia || emp.razao_social || 'Empresa') : 'Empresa não vinculada';
}

function obterTituloPeriodoAgenda() {
  const ref = CRM_STATE.agendaDataRef || new Date();
  if (CRM_STATE.agendaVisao === 'mes') {
    return `${MESES_NOMES[ref.getMonth()]} de ${ref.getFullYear()}`;
  } else if (CRM_STATE.agendaVisao === 'semana') {
    const currentDay = ref.getDay();
    const diffToMonday = (currentDay + 6) % 7;
    const mon = new Date(ref);
    mon.setDate(mon.getDate() - diffToMonday);
    const sun = new Date(mon);
    sun.setDate(sun.getDate() + 6);
    return `${mon.getDate()} a ${sun.getDate()} de ${MESES_NOMES[sun.getMonth()]} de ${sun.getFullYear()}`;
  } else {
    const diaSemana = DIAS_SEMANA_NOMES[(ref.getDay() + 6) % 7];
    return `${diaSemana}, ${ref.getDate()} de ${MESES_NOMES[ref.getMonth()]} de ${ref.getFullYear()}`;
  }
}

function renderizarAtividades() {
  const container = document.getElementById('view-atividades');
  if (!container) return;

  const todasAtivs = CRM_STATE.dados?.atividades || [];
  
  // Filtros aplicados
  const ativsFiltradas = todasAtivs.filter(a => {
    if (CRM_STATE.agendaFiltroTipo !== 'todos' && (a.tipo || '').toLowerCase() !== CRM_STATE.agendaFiltroTipo.toLowerCase()) {
      return false;
    }
    if (CRM_STATE.agendaFiltroResponsavel !== 'todos' && a.responsavel_id !== CRM_STATE.agendaFiltroResponsavel) {
      return false;
    }
    if (CRM_STATE.agendaFiltroStatus === 'pendente' && a.status === 'concluida') {
      return false;
    }
    if (CRM_STATE.agendaFiltroStatus === 'concluida' && a.status !== 'concluida') {
      return false;
    }
    if (CRM_STATE.agendaFiltroBusca) {
      const q = CRM_STATE.agendaFiltroBusca.toLowerCase();
      const empNome = obterNomeEmpresa(a.empresa_id).toLowerCase();
      const tit = (a.titulo || '').toLowerCase();
      const notas = (a.notas || '').toLowerCase();
      if (!empNome.includes(q) && !tit.includes(q) && !notas.includes(q)) return false;
    }
    return true;
  });

  const total = ativsFiltradas.length;
  const pendentes = ativsFiltradas.filter(a => a.status !== 'concluida').length;
  const concluidas = ativsFiltradas.filter(a => a.status === 'concluida').length;
  const usuarios = CRM_STATE.dados?.usuarios || [];

  const ref = CRM_STATE.agendaDataRef || new Date();
  const mesAtual = ref.getMonth();
  const anoAtual = ref.getFullYear();

  const anoBase = new Date().getFullYear();
  const anoMin = Math.min(anoAtual, anoBase) - 5;
  const anoMax = Math.max(anoAtual, anoBase) + 6;
  const anosLista = [];
  for (let y = anoMin; y <= anoMax; y++) anosLista.push(y);

  let subTituloPeriodo = '';
  if (CRM_STATE.agendaVisao === 'semana') {
    const currentDay = ref.getDay();
    const diffToMonday = (currentDay + 6) % 7;
    const mon = new Date(ref);
    mon.setDate(mon.getDate() - diffToMonday);
    const sun = new Date(mon);
    sun.setDate(sun.getDate() + 6);
    subTituloPeriodo = `Semana: ${mon.getDate()} a ${sun.getDate()}`;
  } else if (CRM_STATE.agendaVisao === 'dia') {
    const diaSemana = DIAS_SEMANA_NOMES[(ref.getDay() + 6) % 7];
    subTituloPeriodo = `${diaSemana}, dia ${ref.getDate()}`;
  }

  container.innerHTML = `
    <div class="crm-agenda-header">
      <div class="crm-agenda-toolbar">
        <!-- Esquerda: Nova Atividade + Toggle de Modo -->
        <div style="display:flex; gap:0.6rem; align-items:center;">
          <button onclick="abrirModalNovaAtividade()" class="btn-crm btn-crm-primary" style="font-weight:700; background:linear-gradient(135deg, #0284c7, #0369a1); border:none; box-shadow:0 2px 8px rgba(2,132,199,0.3);">➕ Agendar Ação</button>
          <button onclick="limparTodasAtividades()" class="btn-crm" style="font-weight:600; background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.4); color:#f87171;" title="Remover todas as ações e agendamentos">🗑️ Limpar Todas</button>
          
          <div class="crm-segmented-group" title="Alternar formato de visualização">
            <button onclick="trocarModoAgenda('calendario')" class="crm-segmented-btn ${CRM_STATE.agendaModo === 'calendario' ? 'active' : ''}">
              📅 Calendário Visual
            </button>
            <button onclick="trocarModoAgenda('lista')" class="crm-segmented-btn ${CRM_STATE.agendaModo === 'lista' ? 'active' : ''}">
              📋 Lista de Ações
            </button>
          </div>
        </div>

        <!-- Centro: Navegação de Datas e Visão (apenas se Calendário) -->
        ${CRM_STATE.agendaModo === 'calendario' ? `
          <div class="crm-agenda-nav">
            <button onclick="navegarAgenda('ant')" class="btn-crm" style="padding:0.35rem 0.65rem;" title="Período anterior">◀</button>
            <button onclick="navegarAgenda('hoje')" class="btn-crm" style="padding:0.35rem 0.75rem; font-weight:700;" title="Ir para a data atual">Hoje</button>
            <button onclick="navegarAgenda('prox')" class="btn-crm" style="padding:0.35rem 0.65rem;" title="Próximo período">▶</button>
            
            <div class="crm-agenda-picker-group">
              <select class="crm-select-mes" onchange="alterarMesAgenda(this.value)" title="Alterar Mês">
                ${MESES_NOMES.map((m, idx) => `
                  <option value="${idx}" ${idx === mesAtual ? 'selected' : ''}>${m}</option>
                `).join('')}
              </select>
              <select class="crm-select-ano" onchange="alterarAnoAgenda(this.value)" title="Alterar Ano">
                ${anosLista.map(y => `
                  <option value="${y}" ${y === anoAtual ? 'selected' : ''}>${y}</option>
                `).join('')}
              </select>
              <input type="date" 
                     class="crm-date-jump-input" 
                     value="${formatarIsoDate(ref)}" 
                     title="Ir diretamente para uma data específica"
                     onchange="irParaDataAgenda(this.value)">
            </div>

            ${subTituloPeriodo ? `<span class="crm-agenda-subinfo">${subTituloPeriodo}</span>` : ''}
          </div>

          <div class="crm-segmented-group">
            <button onclick="trocarVisaoAgenda('mes')" class="crm-segmented-btn ${CRM_STATE.agendaVisao === 'mes' ? 'active' : ''}">Mês</button>
            <button onclick="trocarVisaoAgenda('semana')" class="crm-segmented-btn ${CRM_STATE.agendaVisao === 'semana' ? 'active' : ''}">Semana</button>
            <button onclick="trocarVisaoAgenda('dia')" class="crm-segmented-btn ${CRM_STATE.agendaVisao === 'dia' ? 'active' : ''}">Dia</button>
          </div>
        ` : `
          <div class="crm-agenda-title" style="min-width:auto;">📋 Lista de Ações & Agendamentos</div>
        `}

        <!-- Direita: Exportar .ICS -->
        <div>
          <button onclick="exportarCalendarioICS()" class="btn-crm" style="background:#4338ca; color:#fff; border-color:#6366f1;" title="Exportar calendário .ICS para Google Calendar, Apple e Outlook">
            📅 Exportar .ICS (Google/Outlook)
          </button>
        </div>
      </div>

      <!-- Barra de Filtros Integrados -->
      <div class="crm-agenda-filters">
        <div class="crm-agenda-filter-inputs">
          <input type="text" class="crm-form-input" style="min-width:200px; padding:0.35rem 0.65rem; font-size:0.78rem;" placeholder="🔍 Buscar tarefa, empresa..." value="${escapeHtml(CRM_STATE.agendaFiltroBusca || '')}" oninput="filtrarAgendaBusca(event)">

          <select class="crm-form-select" style="min-width:140px; padding:0.35rem 0.65rem; font-size:0.78rem;" onchange="filtrarAgendaTipo(this.value)">
            <option value="todos" ${CRM_STATE.agendaFiltroTipo === 'todos' ? 'selected' : ''}>Todos os Tipos</option>
            <option value="whatsapp" ${CRM_STATE.agendaFiltroTipo === 'whatsapp' ? 'selected' : ''}>💬 WhatsApp</option>
            <option value="ligacao" ${CRM_STATE.agendaFiltroTipo === 'ligacao' ? 'selected' : ''}>📞 Ligação</option>
            <option value="reuniao" ${CRM_STATE.agendaFiltroTipo === 'reuniao' ? 'selected' : ''}>🤝 Reunião</option>
            <option value="visita" ${CRM_STATE.agendaFiltroTipo === 'visita' ? 'selected' : ''}>🚗 Visita</option>
            <option value="email" ${CRM_STATE.agendaFiltroTipo === 'email' ? 'selected' : ''}>✉️ E-mail</option>
            <option value="recontato" ${CRM_STATE.agendaFiltroTipo === 'recontato' ? 'selected' : ''}>⏰ Recontato</option>
          </select>

          <select class="crm-form-select" style="min-width:150px; padding:0.35rem 0.65rem; font-size:0.78rem;" onchange="filtrarAgendaResponsavel(this.value)">
            <option value="todos" ${CRM_STATE.agendaFiltroResponsavel === 'todos' ? 'selected' : ''}>Todos os Responsáveis</option>
            ${usuarios.map(u => `<option value="${u.id}" ${CRM_STATE.agendaFiltroResponsavel === u.id ? 'selected' : ''}>👤 ${u.nome || u.id}</option>`).join('')}
          </select>

          <select class="crm-form-select" style="min-width:140px; padding:0.35rem 0.65rem; font-size:0.78rem;" onchange="filtrarAgendaStatus(this.value)">
            <option value="todos" ${CRM_STATE.agendaFiltroStatus === 'todos' ? 'selected' : ''}>Todos os Status</option>
            <option value="pendente" ${CRM_STATE.agendaFiltroStatus === 'pendente' ? 'selected' : ''}>🟡 Apenas Pendentes</option>
            <option value="concluida" ${CRM_STATE.agendaFiltroStatus === 'concluida' ? 'selected' : ''}>🟢 Apenas Concluídas</option>
          </select>
        </div>

        <div class="crm-agenda-summary-badges">
          <span class="crm-day-summary-badge">Total: <strong>${total}</strong></span>
          <span class="crm-day-summary-badge" style="color:#fbbf24; border-color:rgba(245,158,11,0.3);">Pendentes: <strong>${pendentes}</strong></span>
          <span class="crm-day-summary-badge" style="color:#34d399; border-color:rgba(16,185,129,0.3);">Concluídas: <strong>${concluidas}</strong></span>
        </div>
      </div>
    </div>

    <!-- Conteúdo Principal: Calendário ou Tabela -->
    <div class="crm-calendar-viewport">
      ${CRM_STATE.agendaModo === 'lista'
        ? renderizarTabelaAtividadesLista(ativsFiltradas)
        : (CRM_STATE.agendaVisao === 'semana'
            ? renderizarCalendarioSemana(ativsFiltradas)
            : (CRM_STATE.agendaVisao === 'dia'
                ? renderizarCalendarioDia(ativsFiltradas)
                : renderizarCalendarioMes(ativsFiltradas)))}
    </div>
  `;
}

// ==================== VISÃO MÊS ====================
function renderizarCalendarioMes(ativs) {
  const ref = CRM_STATE.agendaDataRef || new Date();
  const ano = ref.getFullYear();
  const mes = ref.getMonth();
  const primeiroDia = new Date(ano, mes, 1);
  const startDayOfWeek = (primeiroDia.getDay() + 6) % 7; // Segunda = 0
  const diasNoMes = new Date(ano, mes + 1, 0).getDate();
  const diasNoMesAnt = new Date(ano, mes, 0).getDate();

  const hojeStr = formatarIsoDate(new Date());

  // Mapear atividades por data YYYY-MM-DD
  const ativsPorDia = {};
  ativs.forEach(a => {
    if (!a.data_hora) return;
    const diaKey = a.data_hora.slice(0, 10);
    if (!ativsPorDia[diaKey]) ativsPorDia[diaKey] = [];
    ativsPorDia[diaKey].push(a);
  });

  // Ordenar atividades por horário dentro de cada dia
  Object.keys(ativsPorDia).forEach(k => {
    ativsPorDia[k].sort((a, b) => (a.data_hora || '').localeCompare(b.data_hora || ''));
  });

  const cells = [];
  // Dias do mês anterior
  for (let i = startDayOfWeek - 1; i >= 0; i--) {
    const d = new Date(ano, mes - 1, diasNoMesAnt - i);
    cells.push({ date: d, iso: formatarIsoDate(d), outroMes: true });
  }
  // Dias do mês atual
  for (let d = 1; d <= diasNoMes; d++) {
    const cur = new Date(ano, mes, d);
    cells.push({ date: cur, iso: formatarIsoDate(cur), outroMes: false });
  }
  // Dias do próximo mês para completar semanas
  const resto = (7 - (cells.length % 7)) % 7;
  for (let nextD = 1; nextD <= resto; nextD++) {
    const d = new Date(ano, mes + 1, nextD);
    cells.push({ date: d, iso: formatarIsoDate(d), outroMes: true });
  }

  return `
    <div class="crm-month-viewport">
      <div class="crm-month-container">
        <div class="crm-month-header">
          ${DIAS_SEMANA_CURTO.map((d, idx) => `
            <div class="crm-month-header-cell ${idx >= 5 ? 'weekend' : ''}">${d}</div>
          `).join('')}
        </div>
        <div class="crm-month-grid">
          ${cells.map(c => {
            const diaEvents = ativsPorDia[c.iso] || [];
            const isHoje = c.iso === hojeStr;
            const totalDia = diaEvents.length;
            const pendentesDia = diaEvents.filter(a => a.status !== 'concluida').length;
            const concluidasDia = diaEvents.filter(a => a.status === 'concluida').length;
            const tooltipText = totalDia > 0 ? `${totalDia} atividade(s): ${pendentesDia} pendente(s), ${concluidasDia} concluída(s)` : 'Nenhuma atividade (clique para adicionar)';

            const visiveis = diaEvents.slice(0, 3);
            const ocultosCount = diaEvents.length - 3;

            return `
              <div class="crm-month-day ${c.outroMes ? 'outro-mes' : ''} ${isHoje ? 'hoje' : ''}" 
                   data-agenda-tooltip="${tooltipText}" 
                   title="${tooltipText}"
                   onclick="aoClicarDiaMes(event, '${c.iso}')">
                <div class="crm-month-day-top">
                  <span class="crm-month-day-num">${c.date.getDate()}</span>
                  <button type="button" class="crm-month-day-add-btn" 
                          title="Agendar atividade em ${c.date.getDate()}/${c.date.getMonth() + 1}"
                          onclick="event.stopPropagation(); abrirModalNovaAtividadeComData('${c.iso}', 9, 0)">+</button>
                </div>

                <div class="crm-month-day-events">
                  ${visiveis.map(a => {
                    const cor = corTipoAtividade(a.tipo);
                    const icone = iconeTipoAtividade(a.tipo);
                    const horaCurta = formatarHoraCurta(a.data_hora);
                    const isConcluida = a.status === 'concluida';
                    return `
                      <div class="crm-event-pill ${isConcluida ? 'concluida' : ''}"
                           style="background:${cor.bg}; border-color:${cor.border}; color:${cor.text};"
                           onclick="event.stopPropagation(); abrirModalDetalhesAtividade('${a.id}')"
                           title="${icone} ${a.titulo} (${horaCurta}) - ${isConcluida ? 'Concluída' : 'Pendente'}">
                        <span>${icone}</span>
                        <span class="crm-event-pill-time">${horaCurta}</span>
                        <span class="crm-event-pill-title">${escapeHtml(a.titulo || 'Atividade')}</span>
                      </div>
                    `;
                  }).join('')}

                  ${ocultosCount > 0 ? `
                    <div class="crm-events-more-btn" onclick="event.stopPropagation(); abrirDiaCalendario('${c.iso}')">
                      +${ocultosCount} mais...
                    </div>
                  ` : ''}
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    </div>
  `;
}

function aoClicarDiaMes(e, diaIso) {
  // Se clicou na célula vazia, abre visão de dia
  abrirDiaCalendario(diaIso);
}

// ==================== VISÃO SEMANA ====================
function renderizarCalendarioSemana(ativs) {
  const ref = CRM_STATE.agendaDataRef || new Date();
  const currentDay = ref.getDay();
  const diffToMonday = (currentDay + 6) % 7;
  const monday = new Date(ref);
  monday.setDate(monday.getDate() - diffToMonday);
  monday.setHours(0, 0, 0, 0);

  const hojeStr = formatarIsoDate(new Date());

  const diasSemana = [];
  for (let i = 0; i < 7; i++) {
    const d = new Date(monday);
    d.setDate(d.getDate() + i);
    diasSemana.push({ date: d, iso: formatarIsoDate(d), diaSemanaNome: DIAS_SEMANA_CURTO[i] });
  }

  // Horários de 08:00 a 20:00
  const horas = [];
  for (let h = 8; h <= 20; h++) {
    horas.push(h);
  }

  // Indexar atividades por dia e hora
  const ativsPorDiaHora = {};
  ativs.forEach(a => {
    if (!a.data_hora) return;
    const diaKey = a.data_hora.slice(0, 10);
    let hora = 9;
    try {
      const d = new Date(a.data_hora);
      if (!isNaN(d.getHours())) hora = d.getHours();
    } catch (e) {}
    // Ajustar se fora do range
    if (hora < 8) hora = 8;
    if (hora > 20) hora = 20;

    const slotKey = `${diaKey}_${hora}`;
    if (!ativsPorDiaHora[slotKey]) ativsPorDiaHora[slotKey] = [];
    ativsPorDiaHora[slotKey].push(a);
  });

  return `
    <div class="crm-week-viewport">
      <table class="crm-week-table">
        <thead>
          <tr class="crm-week-header-row">
            <th class="crm-week-time-col" style="color:#94a3b8; font-weight:700;">Hora</th>
            ${diasSemana.map(d => {
              const isHoje = d.iso === hojeStr;
              return `
                <th class="crm-week-header-cell ${isHoje ? 'hoje' : ''}">
                  <div>${d.diaSemanaNome}</div>
                  <div style="font-size:0.95rem; font-weight:700; margin-top:2px;">
                    ${d.date.getDate()}/${d.date.getMonth() + 1}
                  </div>
                </th>
              `;
            }).join('')}
          </tr>
        </thead>
        <tbody>
          ${horas.map(h => {
            const horaLabel = `${String(h).padStart(2, '0')}:00`;
            return `
              <tr class="crm-week-slot-row">
                <td class="crm-week-time-col">${horaLabel}</td>
                ${diasSemana.map(d => {
                  const slotKey = `${d.iso}_${h}`;
                  const slotEvents = ativsPorDiaHora[slotKey] || [];
                  const isHoje = d.iso === hojeStr;
                  return `
                    <td class="crm-week-slot-cell ${isHoje ? 'hoje' : ''}" 
                        onclick="abrirModalNovaAtividadeComData('${d.iso}', ${h}, 0)"
                        title="Clique para agendar às ${horaLabel} em ${d.date.getDate()}/${d.date.getMonth() + 1}">
                      ${slotEvents.map(a => {
                        const cor = corTipoAtividade(a.tipo);
                        const icone = iconeTipoAtividade(a.tipo);
                        const horaStr = formatarHoraCurta(a.data_hora);
                        const empNome = obterNomeEmpresa(a.empresa_id);
                        const isConcluida = a.status === 'concluida';

                        return `
                          <div class="crm-week-event-card ${isConcluida ? 'concluida' : ''}" 
                               style="border-left-color:${cor.border};"
                               onclick="event.stopPropagation(); abrirModalDetalhesAtividade('${a.id}')"
                               title="${icone} ${a.titulo} - ${empNome}">
                            <div class="crm-week-event-card-header">
                              <span style="color:${cor.text};">${icone} ${horaStr}</span>
                              ${!isConcluida ? `
                                <button type="button" class="btn-crm btn-crm-success" 
                                        style="padding:1px 5px; font-size:0.65rem; border-radius:4px;" 
                                        title="Concluir atividade"
                                        onclick="event.stopPropagation(); concluirAtividade('${a.id}')">✓</button>
                              ` : '<span style="color:#34d399; font-size:0.65rem;">✓ Concluída</span>'}
                            </div>
                            <div class="crm-week-event-card-title">${escapeHtml(a.titulo)}</div>
                            <div class="crm-week-event-card-meta">🏢 ${escapeHtml(empNome)}</div>
                          </div>
                        `;
                      }).join('')}
                    </td>
                  `;
                }).join('')}
              </tr>
            `;
          }).join('')}
        </tbody>
      </table>
    </div>
  `;
}

// ==================== VISÃO DIA ====================
function renderizarCalendarioDia(ativs) {
  const ref = CRM_STATE.agendaDataRef || new Date();
  const diaIso = formatarIsoDate(ref);
  const diaSemanaNome = DIAS_SEMANA_NOMES[(ref.getDay() + 6) % 7];

  const eventosDia = ativs.filter(a => (a.data_hora || '').startsWith(diaIso));
  eventosDia.sort((a, b) => (a.data_hora || '').localeCompare(b.data_hora || ''));

  const pendentesDia = eventosDia.filter(a => a.status !== 'concluida').length;
  const concluidasDia = eventosDia.filter(a => a.status === 'concluida').length;

  return `
    <div class="crm-day-view-container">
      <div class="crm-day-summary-banner">
        <div>
          <button onclick="trocarVisaoAgenda('mes')" class="btn-crm" style="margin-bottom:0.4rem; padding:0.25rem 0.6rem; font-size:0.75rem;">
            ← Voltar à Visão Mensal
          </button>
          <h2 style="font-size:1.25rem; font-weight:700; color:#fff; margin:0;">
            ${diaSemanaNome}, ${ref.getDate()} de ${MESES_NOMES[ref.getMonth()]} de ${ref.getFullYear()}
          </h2>
          <div style="font-size:0.82rem; color:#94a3b8; margin-top:3px;">
            ${eventosDia.length} compromisso(s) agendado(s) neste dia · 
            <span style="color:#fbbf24;">${pendentesDia} pendente(s)</span> · 
            <span style="color:#34d399;">${concluidasDia} concluído(s)</span>
          </div>
        </div>

        <button onclick="abrirModalNovaAtividadeComData('${diaIso}', 9, 0)" class="btn-crm btn-crm-primary" style="font-weight:700;">
          + Nova Atividade neste Dia
        </button>
      </div>

      <div class="crm-day-timeline-list">
        ${eventosDia.length === 0 ? `
          <div style="text-align:center; padding:3rem 1.5rem; background:#0d1527; border:1px dashed var(--crm-border); border-radius:10px;">
            <div style="font-size:2.2rem; margin-bottom:0.75rem;">📅</div>
            <div style="font-size:1rem; font-weight:700; color:#f8fafc;">Nenhum compromisso marcado para este dia</div>
            <p style="font-size:0.82rem; color:#94a3b8; margin:0.35rem 0 1rem 0;">Aproveite para prospectar novos clientes ou agendar reuniões.</p>
            <button onclick="abrirModalNovaAtividadeComData('${diaIso}', 10, 0)" class="btn-crm btn-crm-primary">+ Agendar Compromisso</button>
          </div>
        ` : eventosDia.map(a => {
          const cor = corTipoAtividade(a.tipo);
          const icone = iconeTipoAtividade(a.tipo);
          const horaStr = formatarHoraCurta(a.data_hora);
          const empNome = obterNomeEmpresa(a.empresa_id);
          const isConcluida = a.status === 'concluida';

          return `
            <div class="crm-day-event-row ${isConcluida ? 'concluida' : ''}" style="border-left-color:${cor.border};">
              <div class="crm-day-event-time">
                <span>${horaStr}</span>
                <span style="font-size:0.65rem; color:#94a3b8; font-weight:400;">${a.duracao_minutos || 60} min</span>
              </div>

              <div class="crm-day-event-details">
                <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.35rem;">
                  <span class="badge-ent" style="background:${cor.badgeBg}; color:${cor.text}; border:1px solid ${cor.border};">
                    ${icone} ${(a.tipo || 'geral').toUpperCase()}
                  </span>
                  <span class="badge-ent ${isConcluida ? 'badge-ganho' : 'badge-aberto'}">
                    ${isConcluida ? '✓ CONCLUÍDO' : 'PENDENTE'}
                  </span>
                </div>

                <h4 style="${isConcluida ? 'text-decoration:line-through; color:#94a3b8;' : ''}">${escapeHtml(a.titulo)}</h4>

                <div class="crm-day-event-tags">
                  <span onclick="abrirModalDetalhesEmpresa('${a.empresa_id}')" style="cursor:pointer; color:#38bdf8; text-decoration:underline;">
                    🏢 ${escapeHtml(empNome)}
                  </span>
                  <span>👤 Responsável: ${escapeHtml(a.responsavel_id || 'usr-admin')}</span>
                </div>

                ${a.notas ? `
                  <div class="crm-day-event-notes">
                    <strong>Pauta / Anotação:</strong> ${escapeHtml(a.notas)}
                  </div>
                ` : ''}
              </div>

              <div style="display:flex; flex-direction:column; gap:0.4rem; align-items:flex-end;">
                ${!isConcluida ? `
                  <button onclick="concluirAtividade('${a.id}')" class="btn-crm btn-crm-success" style="font-size:0.75rem; padding:0.4rem 0.8rem; font-weight:700;">
                    ✓ Concluir
                  </button>
                ` : `
                  <span style="color:#34d399; font-weight:700; font-size:0.8rem;">✓ Concluída</span>
                `}
                <button onclick="abrirModalDetalhesAtividade('${a.id}')" class="btn-crm" style="font-size:0.72rem; padding:0.3rem 0.6rem;">
                  Detalhes
                </button>
              </div>
            </div>
          `;
        }).join('')}
      </div>
    </div>
  `;
}

// ==================== VISÃO LISTA / TABELA ====================
function renderizarTabelaAtividadesLista(ativs) {
  return `
    <div class="crm-table-container">
      <table class="crm-table crm-table-empresas">
        <thead>
          <tr>
            <th style="width:140px;">Tipo</th>
            <th>Título da Tarefa</th>
            <th>Empresa / Negociação</th>
            <th style="width:170px;">Data / Horário</th>
            <th style="width:130px;">Responsável</th>
            <th style="width:120px; text-align:center;">Status</th>
            <th style="width:140px; text-align:center;">Ações</th>
          </tr>
        </thead>
        <tbody>
          ${ativs.length === 0 ? `
            <tr>
              <td colspan="7" style="text-align:center; padding:2.5rem; color:#94a3b8;">
                Nenhuma atividade encontrada com os filtros selecionados.
              </td>
            </tr>
          ` : ativs.map(a => {
            const empNome = obterNomeEmpresa(a.empresa_id);
            const icone = iconeTipoAtividade(a.tipo);
            const cor = corTipoAtividade(a.tipo);
            const isConcluida = a.status === 'concluida';

            return `
              <tr>
                <td style="white-space:nowrap;">
                  <span class="badge-ent" style="background:${cor.badgeBg}; color:${cor.text}; border:1px solid ${cor.border};">
                    ${icone} ${(a.tipo || 'geral').toUpperCase()}
                  </span>
                </td>
                <td>
                  <div style="font-weight:600; color:#f8fafc; ${isConcluida ? 'text-decoration:line-through; opacity:0.6;' : ''}">
                    ${escapeHtml(a.titulo)}
                  </div>
                  ${a.notas ? `<div style="font-size:0.75rem; color:#94a3b8; margin-top:2px;">${escapeHtml(a.notas)}</div>` : ''}
                </td>
                <td>
                  <span onclick="abrirModalDetalhesEmpresa('${a.empresa_id}')" style="cursor:pointer; color:#38bdf8; text-decoration:underline; font-size:0.85rem;">
                    ${escapeHtml(empNome)}
                  </span>
                </td>
                <td style="font-family:'JetBrains Mono', monospace; font-size:0.8rem; color:#cbd5e1; white-space:nowrap;">
                  ${formatarDataHora(a.data_hora)}
                </td>
                <td style="font-size:0.82rem; color:#94a3b8;">${escapeHtml(a.responsavel_id || 'usr-admin')}</td>
                <td style="text-align:center; white-space:nowrap;">
                  <span class="badge-ent ${isConcluida ? 'badge-ganho' : 'badge-aberto'}">
                    ${isConcluida ? '✓ CONCLUÍDA' : 'PENDENTE'}
                  </span>
                </td>
                <td style="text-align:center; white-space:nowrap;">
                  <div class="crm-actions-group" style="justify-content:center;">
                    ${!isConcluida ? `
                      <button onclick="concluirAtividade('${a.id}')" class="btn-crm btn-crm-success" style="padding:0.25rem 0.6rem; font-size:0.72rem; font-weight:700;">
                        ✓ Concluir
                      </button>
                    ` : `
                      <span style="font-size:0.72rem; color:#34d399;">✓ Concluída</span>
                    `}
                    <button onclick="abrirModalDetalhesAtividade('${a.id}')" class="btn-crm-icon btn-action-view" data-tooltip="Visualizar Detalhes" title="Visualizar">
                      <svg viewBox="0 0 24 24"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                    </button>
                    <button onclick="excluirAtividade('${a.id}')" class="btn-crm-icon" data-tooltip="Excluir Ação" title="Excluir Ação" style="color:#f87171; border-color:rgba(239,68,68,0.3); background:rgba(239,68,68,0.1);">
                      <svg viewBox="0 0 24 24" style="width:13px; height:13px; fill:none; stroke:currentColor; stroke-width:2;"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                    </button>
                  </div>
                </td>
              </tr>
            `;
          }).join('')}
        </tbody>
      </table>
    </div>
  `;
}

// ==================== NAVEGAÇÃO E FILTROS DA AGENDA ====================
function navegarAgenda(direcao) {
  if (!CRM_STATE.agendaDataRef) CRM_STATE.agendaDataRef = new Date();
  
  if (direcao === 'hoje') {
    CRM_STATE.agendaDataRef = new Date();
  } else if (CRM_STATE.agendaVisao === 'mes') {
    const d = new Date(CRM_STATE.agendaDataRef);
    d.setMonth(d.getMonth() + (direcao === 'prox' ? 1 : -1));
    CRM_STATE.agendaDataRef = d;
  } else if (CRM_STATE.agendaVisao === 'semana') {
    const d = new Date(CRM_STATE.agendaDataRef);
    d.setDate(d.getDate() + (direcao === 'prox' ? 7 : -7));
    CRM_STATE.agendaDataRef = d;
  } else {
    const d = new Date(CRM_STATE.agendaDataRef);
    d.setDate(d.getDate() + (direcao === 'prox' ? 1 : -1));
    CRM_STATE.agendaDataRef = d;
  }
  renderizarAtividades();
}

function alterarMesAgenda(novoMes) {
  if (!CRM_STATE.agendaDataRef) CRM_STATE.agendaDataRef = new Date();
  const d = new Date(CRM_STATE.agendaDataRef);
  const diaOriginal = d.getDate();
  d.setDate(1); // Previne pular mês por dias excedentes (ex: dia 31)
  d.setMonth(parseInt(novoMes, 10));
  const ultimoDia = new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate();
  d.setDate(Math.min(diaOriginal, ultimoDia));
  CRM_STATE.agendaDataRef = d;
  renderizarAtividades();
}

function alterarAnoAgenda(novoAno) {
  if (!CRM_STATE.agendaDataRef) CRM_STATE.agendaDataRef = new Date();
  const d = new Date(CRM_STATE.agendaDataRef);
  const diaOriginal = d.getDate();
  d.setDate(1);
  d.setFullYear(parseInt(novoAno, 10));
  const ultimoDia = new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate();
  d.setDate(Math.min(diaOriginal, ultimoDia));
  CRM_STATE.agendaDataRef = d;
  renderizarAtividades();
}

function irParaDataAgenda(isoDate) {
  if (!isoDate) return;
  try {
    const parts = isoDate.split('-');
    if (parts.length === 3) {
      CRM_STATE.agendaDataRef = new Date(parseInt(parts[0], 10), parseInt(parts[1], 10) - 1, parseInt(parts[2], 10), 12, 0, 0);
      renderizarAtividades();
    }
  } catch (e) {
    console.error('Erro ao ir para data selecionada:', e);
  }
}

function trocarVisaoAgenda(visao) {
  CRM_STATE.agendaVisao = visao;
  CRM_STATE.agendaModo = 'calendario';
  renderizarAtividades();
}

function trocarModoAgenda(modo) {
  CRM_STATE.agendaModo = modo;
  renderizarAtividades();
}

function abrirDiaCalendario(diaIso) {
  try {
    CRM_STATE.agendaDataRef = new Date(diaIso + 'T12:00:00');
  } catch (e) {
    CRM_STATE.agendaDataRef = new Date();
  }
  CRM_STATE.agendaVisao = 'dia';
  CRM_STATE.agendaModo = 'calendario';
  renderizarAtividades();
}

function abrirModalNovaAtividadeComData(diaIso, hora = 9, minuto = 0) {
  abrirModalNovaAtividade();
  const pad = n => String(n).padStart(2, '0');
  const dhInput = document.getElementById('ativ-dh');
  if (dhInput && diaIso) {
    dhInput.value = `${diaIso}T${pad(hora)}:${pad(minuto)}`;
  }
}

function filtrarAgendaTipo(tipo) {
  CRM_STATE.agendaFiltroTipo = tipo;
  renderizarAtividades();
}

function filtrarAgendaResponsavel(resp) {
  CRM_STATE.agendaFiltroResponsavel = resp;
  renderizarAtividades();
}

function filtrarAgendaStatus(status) {
  CRM_STATE.agendaFiltroStatus = status;
  renderizarAtividades();
}

function filtrarAgendaBusca(e) {
  CRM_STATE.agendaFiltroBusca = e.target.value.trim();
  renderizarAtividades();
}

// ==================== MODAL DE DETALHES DE ATIVIDADE ====================
function abrirModalDetalhesAtividade(ativId) {
  const ativ = (CRM_STATE.dados?.atividades || []).find(a => a.id === ativId);
  if (!ativ) return;

  const modal = document.getElementById('modal-detalhes-atividade');
  if (!modal) return;

  const icone = iconeTipoAtividade(ativ.tipo);
  const cor = corTipoAtividade(ativ.tipo);
  const empNome = obterNomeEmpresa(ativ.empresa_id);
  const isConcluida = ativ.status === 'concluida';

  const badgeTipo = document.getElementById('det-ativ-tipo-badge');
  if (badgeTipo) {
    badgeTipo.innerHTML = `${icone} ${(ativ.tipo || 'geral').toUpperCase()}`;
    badgeTipo.style.background = cor.badgeBg;
    badgeTipo.style.color = cor.text;
    badgeTipo.style.border = `1px solid ${cor.border}`;
  }

  const elTit = document.getElementById('det-ativ-titulo');
  if (elTit) elTit.textContent = ativ.titulo || 'Atividade sem título';

  const elEmp = document.getElementById('det-ativ-empresa');
  if (elEmp) {
    elEmp.innerHTML = `<span onclick="fecharModalDetalhesAtividade(); abrirModalDetalhesEmpresa('${ativ.empresa_id}')" style="color:#38bdf8; cursor:pointer; text-decoration:underline;">${escapeHtml(empNome)}</span>`;
  }

  const elDh = document.getElementById('det-ativ-dh');
  if (elDh) elDh.textContent = `${formatarDataHora(ativ.data_hora)} (${ativ.duracao_minutos || 60} min)`;

  const elResp = document.getElementById('det-ativ-resp');
  if (elResp) elResp.textContent = ativ.responsavel_id || 'usr-admin';

  const elSt = document.getElementById('det-ativ-status');
  if (elSt) {
    elSt.innerHTML = `<span class="badge-ent ${isConcluida ? 'badge-ganho' : 'badge-aberto'}">${isConcluida ? '✓ CONCLUÍDA' : '🟡 PENDENTE'}</span>`;
  }

  const elNotas = document.getElementById('det-ativ-notas');
  const wrapNotas = document.getElementById('det-ativ-notas-wrap');
  if (elNotas && wrapNotas) {
    if (ativ.notas) {
      elNotas.textContent = ativ.notas;
      wrapNotas.style.display = 'block';
    } else {
      wrapNotas.style.display = 'none';
    }
  }

  const acoesLeft = document.getElementById('det-ativ-acoes-left');
  if (acoesLeft) {
    if (!isConcluida) {
      acoesLeft.innerHTML = `
        <button onclick="concluirAtividade('${ativ.id}')" class="btn-crm btn-crm-success" style="font-weight:700;">
          ✓ Concluir Esta Atividade
        </button>
        <button onclick="fecharModalDetalhesAtividade(); excluirAtividade('${ativ.id}')" class="btn-crm" style="margin-left:0.5rem; font-weight:600; background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.4); color:#f87171;">
          🗑️ Excluir
        </button>
      `;
    } else {
      acoesLeft.innerHTML = `
        <span style="color:#34d399; font-weight:700; font-size:0.85rem;">✓ Atividade Concluída</span>
        <button onclick="fecharModalDetalhesAtividade(); excluirAtividade('${ativ.id}')" class="btn-crm" style="margin-left:0.75rem; font-weight:600; background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.4); color:#f87171;">
          🗑️ Excluir
        </button>
      `;
    }
  }

  modal.classList.remove('hidden');
}

function fecharModalDetalhesAtividade() {
  const modal = document.getElementById('modal-detalhes-atividade');
  if (modal) modal.classList.add('hidden');
}

// ==================== CONCLUIR ATIVIDADE ====================
async function concluirAtividade(id) {
  const ativ = (CRM_STATE.dados?.atividades || []).find(a => a.id === id);
  if (!ativ) return;
  
  ativ.status = 'concluida';
  try {
    const res = await fetch('/api/crm/v2/atividade', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Usuario-Id': CRM_STATE.usuarioAtivo.id },
      body: JSON.stringify(ativ)
    });
    const json = await res.json();
    if (json.sucesso) {
      fecharModalDetalhesAtividade();
      renderizarAtividades();
      mostrarToastCRM('✓ Atividade concluída com sucesso!', 'sucesso');
    } else {
      mostrarToastCRM('Erro ao concluir atividade: ' + (json.erro || 'Falha na API'), 'erro');
    }
  } catch (e) {
    console.error('Erro ao concluir atividade:', e);
    mostrarToastCRM('Erro de conexão ao concluir atividade.', 'erro');
  }
}

// ==================== EXCLUIR ATIVIDADE ====================
async function excluirAtividade(id) {
  if (!confirm('Deseja realmente excluir esta ação/tarefa agendada?')) return;
  try {
    const res = await fetch('/api/crm/v2/atividade/excluir', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Usuario-Id': (CRM_STATE.usuarioAtivo && CRM_STATE.usuarioAtivo.id) || 'usr-admin' },
      body: JSON.stringify({ id })
    });
    const json = await res.json();
    if (json.sucesso) {
      if (CRM_STATE.dados && CRM_STATE.dados.atividades) {
        CRM_STATE.dados.atividades = CRM_STATE.dados.atividades.filter(a => a.id !== id);
      }
      fecharModalDetalhesAtividade();
      renderizarAtividades();
      mostrarToastCRM('✓ Ação/tarefa excluída com sucesso!', 'sucesso');
    } else {
      mostrarToastCRM('Erro ao excluir: ' + (json.erro || 'Falha na API'), 'erro');
    }
  } catch (e) {
    console.error('Erro ao excluir atividade:', e);
    mostrarToastCRM('Erro de conexão ao excluir atividade.', 'erro');
  }
}

// ==================== LIMPAR TODAS AS ATIVIDADES ====================
async function limparTodasAtividades() {
  const total = (CRM_STATE.dados?.atividades || []).length;
  if (total === 0) {
    mostrarToastCRM('Não há nenhuma tarefa de ação ou agendamento para remover.', 'aviso');
    return;
  }
  if (!confirm(`Tem certeza que deseja remover TODAS as ${total} tarefas de ações e agendamentos? Esta ação removerá a lista completa.`)) return;
  try {
    const res = await fetch('/api/crm/v2/atividade/limpar_todas', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Usuario-Id': (CRM_STATE.usuarioAtivo && CRM_STATE.usuarioAtivo.id) || 'usr-admin' },
      body: JSON.stringify({})
    });
    const json = await res.json();
    if (json.sucesso) {
      if (CRM_STATE.dados) {
        CRM_STATE.dados.atividades = [];
      }
      renderizarAtividades();
      mostrarToastCRM('✓ Todas as tarefas de ações e agendamento foram removidas!', 'sucesso');
    } else {
      mostrarToastCRM('Erro ao limpar tarefas: ' + (json.erro || 'Falha na API'), 'erro');
    }
  } catch (e) {
    console.error('Erro ao limpar atividades:', e);
    mostrarToastCRM('Erro de conexão ao limpar atividades.', 'erro');
  }
}

// ==================== EXPORTAR ICS ====================
function exportarCalendarioICS() {
  const ativs = CRM_STATE.dados?.atividades || [];
  let ics = "BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//TruData//CRM Enterprise//PT-BR\r\nCALSCALE:GREGORIAN\r\nMETHOD:PUBLISH\r\n";
  ativs.forEach(a => {
    let dtStart = '';
    let dtEnd = '';
    try {
      const d = new Date(a.data_hora);
      const pad = n => String(n).padStart(2, '0');
      const startStr = `${d.getUTCFullYear()}${pad(d.getUTCMonth() + 1)}${pad(d.getUTCDate())}T${pad(d.getUTCHours())}${pad(d.getUTCMinutes())}00Z`;
      const dur = a.duracao_minutos || 60;
      const dEnd = new Date(d.getTime() + dur * 60000);
      const endStr = `${dEnd.getUTCFullYear()}${pad(dEnd.getUTCMonth() + 1)}${pad(dEnd.getUTCDate())}T${pad(dEnd.getUTCHours())}${pad(dEnd.getUTCMinutes())}00Z`;
      dtStart = startStr;
      dtEnd = endStr;
    } catch (e) {
      dtStart = '20260924T120000Z';
      dtEnd = '20260924T130000Z';
    }
    const empNome = obterNomeEmpresa(a.empresa_id);
    ics += "BEGIN:VEVENT\r\n";
    ics += `UID:${a.id}@trudata.com.br\r\n`;
    ics += `DTSTART:${dtStart}\r\n`;
    ics += `DTEND:${dtEnd}\r\n`;
    ics += `SUMMARY:${(a.titulo || 'Atividade TruData').replace(/[\r\n]/g, ' ')}\r\n`;
    ics += `DESCRIPTION:${((a.notas || '') + (empNome ? ' - Empresa: ' + empNome : '')).replace(/[\r\n]/g, ' ')}\r\n`;
    ics += `STATUS:${a.status === 'concluida' ? 'CONFIRMED' : 'TENTATIVE'}\r\n`;
    ics += "END:VEVENT\r\n";
  });
  ics += "END:VCALENDAR\r\n";

  const blob = new Blob([ics], { type: 'text/calendar;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `trudata_agenda_${new Date().toISOString().slice(0, 10)}.ics`;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  mostrarToastCRM('Agenda exportada em formato .ICS!', 'sucesso');
}

// ==================== 6. AUTOMAÇÕES & GATILHOS ====================
function renderizarAutomacoes() {
  const container = document.getElementById('view-automacoes');
  if (!container) return;

  const autos = CRM_STATE.dados.automacoes;

  container.innerHTML = `
    <div class="dash-box" style="margin-bottom:1.5rem;">
      <div class="dash-box-title">⚡ Regras de Automação Ativas no Pipeline</div>
      <div style="display:flex; flex-direction:column; gap:1rem;">
        ${autos.map(a => `
          <div style="background:#090e18; border:1px solid rgba(255,255,255,0.08); padding:1rem; border-radius:8px; display:flex; justify-content:space-between; align-items:center;">
            <div>
              <div style="font-size:0.95rem; font-weight:700; color:#fff;">${a.nome}</div>
              <div style="font-size:0.8rem; color:#94a3b8; margin-top:0.25rem;">
                Gatilho: <code style="color:#38bdf8;">${a.gatilho}</code> | Ação: <code style="color:#34d399;">${a.acao}</code>
              </div>
            </div>
            <span class="badge-ent badge-ganho">ATIVO</span>
          </div>
        `).join('')}
      </div>
    </div>
  `;
}

// ==================== 7. GESTÃO DE USUÁRIOS & PERMISSÕES ====================
function renderizarUsuarios() {
  const container = document.getElementById('view-usuarios');
  if (!container) return;

  const usrs = CRM_STATE.dados.usuarios;

  container.innerHTML = `
    <div class="dash-box">
      <div class="dash-box-title">👥 Usuários, Equipes e Níveis de Visibilidade</div>
      <table class="crm-table">
        <thead>
          <tr>
            <th>Nome</th>
            <th>Login</th>
            <th>E-mail</th>
            <th>Perfil de Acesso</th>
            <th>Equipe</th>
            <th>Visibilidade dos Dados</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          ${usrs.map(u => `
            <tr>
              <td><strong>${u.nome}</strong></td>
              <td><code>${u.login}</code></td>
              <td>${u.email}</td>
              <td><span class="badge-ent badge-pj">${u.perfil.toUpperCase()}</span></td>
              <td>${u.equipe}</td>
              <td>${u.visibilidade === 'todos' ? '🌐 Todos os Registros' : '🔒 Próprios Registros'}</td>
              <td><span class="badge-ent badge-ganho">ATIVO</span></td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `;
}

// ==================== 8. INTEGRAÇÕES, SWAGGER API & DIAGRAMA ER ====================
function renderizarIntegracoes() {
  const container = document.getElementById('view-integracoes_api');
  if (!container) return;

  container.innerHTML = `
    <div class="dash-columns-2">
      <!-- Diagrama ER Interativo -->
      <div class="dash-box">
        <div class="dash-box-title">📐 Diagrama Entidade-Relacionamento (Modelo de Dados)</div>
        <div style="background:#090e18; padding:1rem; border-radius:8px; font-family:'JetBrains Mono', monospace; font-size:0.75rem; color:#38bdf8; overflow-x:auto; line-height:1.6;">
          <strong>[EMPRESAS]</strong> 1 ─── N <strong>[CONTATOS]</strong><br>
          &nbsp;&nbsp;&nbsp;│<br>
          &nbsp;&nbsp;&nbsp;└─── 1 ─── N <strong>[NEGOCIACOES]</strong> ─── N ─── 1 <strong>[FUNIS/ETAPAS]</strong><br>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├─── 1 ─── N <strong>[ATIVIDADES]</strong><br>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├─── 1 ─── N <strong>[HISTORICO_INTERACOES]</strong><br>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─── N ─── N <strong>[PRODUTOS/SERVICOS]</strong>
        </div>
      </div>

      <!-- OpenAPI / Swagger Explorer -->
      <div class="dash-box">
        <div class="dash-box-title">
          <span>Documentação REST OpenAPI v2</span>
          <a href="/api/crm/v2/openapi.json" target="_blank" class="btn-crm" style="font-size:0.72rem;">JSON Raw</a>
        </div>
        <div style="display:flex; flex-direction:column; gap:0.5rem;">
          <div style="background:#090e18; padding:0.6rem; border-radius:6px; font-size:0.8rem;">
            <span style="color:#10b981; font-weight:700;">GET</span> <code>/api/crm/v2/estado</code> — Carrega dados e métricas
          </div>
          <div style="background:#090e18; padding:0.6rem; border-radius:6px; font-size:0.8rem;">
            <span style="color:#0284c7; font-weight:700;">POST</span> <code>/api/crm/v2/mover_etapa</code> — Mover deal no Kanban
          </div>
          <div style="background:#090e18; padding:0.6rem; border-radius:6px; font-size:0.8rem;">
            <span style="color:#0284c7; font-weight:700;">POST</span> <code>/api/crm/v2/empresa</code> — Salvar empresa PF/PJ
          </div>
          <div style="background:#090e18; padding:0.6rem; border-radius:6px; font-size:0.8rem;">
            <span style="color:#0284c7; font-weight:700;">POST</span> <code>/api/crm/v2/atividade</code> — Agendar tarefa
          </div>
          <div style="background:#090e18; padding:0.6rem; border-radius:6px; font-size:0.8rem;">
            <span style="color:#10b981; font-weight:700;">GET</span> <code>/api/crm/v2/deduplicar</code> — Scanner de duplicações
          </div>
          <div style="background:#090e18; padding:0.6rem; border-radius:6px; font-size:0.8rem;">
            <span style="color:#10b981; font-weight:700;">GET</span> <code>/api/crm/v2/lgpd/exportar</code> — Dossiê titular LGPD
          </div>
        </div>
      </div>
    </div>
  `;
}

// ==================== DOSSIÊ LGPD ====================
async function exportarDossieLGPD(termo) {
  try {
    const res = await fetch(`/api/crm/v2/lgpd/exportar?termo=${encodeURIComponent(termo)}`);
    const json = await res.json();
    if (json.sucesso) {
      const blob = new Blob([JSON.stringify(json.relatorio_lgpd, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `dossie_lgpd_${termo.replace(/[^a-zA-Z0-9]/g, '_')}.json`;
      link.click();
      alert('Dossiê LGPD exportado em conformidade com o Artigo 18 da LGPD!');
    }
  } catch (e) {
    console.error('Erro ao exportar LGPD:', e);
  }
}

// ==================== MODAIS ====================
function abrirModalNovaEmpresa() {
  document.getElementById('modal-empresa').classList.remove('hidden');
}

function fecharModalEmpresa() {
  document.getElementById('modal-empresa').classList.add('hidden');
}

async function salvarEmpresaForm() {
  const tipo = document.getElementById('emp-tipo').value;
  const nome = document.getElementById('emp-nome').value.trim();
  const doc = document.getElementById('emp-doc').value.trim();
  const tel = document.getElementById('emp-tel').value.trim();
  const email = document.getElementById('emp-email').value.trim();
  const cidade = document.getElementById('emp-cidade').value.trim();
  const segmento = document.getElementById('emp-segmento').value;
  const pdvs = document.getElementById('emp-pdvs').value || '1';

  if (!nome) {
    alert('Informe o nome da empresa.');
    return;
  }

  try {
    const res = await fetch('/api/crm/v2/empresa', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Usuario-Id': CRM_STATE.usuarioAtivo.id },
      body: JSON.stringify({
        tipo,
        razao_social: nome,
        nome_fantasia: nome,
        documento: doc,
        telefone: tel,
        whatsapp: tel,
        email,
        cidade: cidade || 'Sarandi - RS',
        uf: 'RS',
        segmento,
        pdvs_estimados: parseInt(pdvs)
      })
    });
    const json = await res.json();
    if (json.sucesso) {
      fecharModalEmpresa();
      await carregarEstadoCRM();
    }
  } catch (e) {
    console.error('Erro ao salvar empresa:', e);
  }
}

// ==================== MODAIS: NOVO LEAD COMPLETO ====================
function abrirModalNovoLead() {
  const modal = document.getElementById('modal-novo-lead');
  if (!modal) return;
  // Preencher data prevista padrão (+15 dias) se vazio
  const prevInput = document.getElementById('nl-previsao');
  if (prevInput && !prevInput.value) {
    const d = new Date();
    d.setDate(d.getDate() + 15);
    prevInput.value = d.toISOString().split('T')[0];
  }
  atualizarEstimativaNovoLead();
  modal.classList.remove('hidden');
}

function fecharModalNovoLead() {
  const modal = document.getElementById('modal-novo-lead');
  if (modal) modal.classList.add('hidden');
}

function atualizarEstimativaNovoLead() {
  const pdvsInput = document.getElementById('nl-pdvs');
  const segSelect = document.getElementById('nl-segmento');
  const mrrInput = document.getElementById('nl-mrr');
  const setupInput = document.getElementById('nl-setup');

  if (!pdvsInput || !mrrInput) return;

  const pdvs = Math.max(1, parseInt(pdvsInput.value) || 1);
  const seg = segSelect ? segSelect.value.toLowerCase() : '';

  let mrr = 180.0 + Math.max(0, pdvs - 1) * 60.0;
  let setup = Math.max(0, pdvs - 1) * 200.0;

  if (seg.includes('contabil') || seg.includes('contabilidade')) {
    mrr = 750.0;
    setup = 0.0;
  }

  mrrInput.value = mrr.toFixed(2);
  if (setupInput) setupInput.value = setup.toFixed(2);
}

async function salvarNovoLeadForm() {
  const nome = (document.getElementById('nl-nome')?.value || '').trim();
  const razao = (document.getElementById('nl-razao')?.value || '').trim() || nome;
  const tipoDoc = document.getElementById('nl-tipo-doc')?.value || 'PJ';
  const doc = (document.getElementById('nl-doc')?.value || '').trim();
  const cidade = (document.getElementById('nl-cidade')?.value || '').trim() || 'Sarandi - RS';
  const segmento = document.getElementById('nl-segmento')?.value || 'Comércio Geral';
  const pdvs = parseInt(document.getElementById('nl-pdvs')?.value) || 1;
  const endereco = (document.getElementById('nl-endereco')?.value || '').trim();

  const contatoNome = (document.getElementById('nl-contato-nome')?.value || '').trim();
  const contatoCargo = (document.getElementById('nl-contato-cargo')?.value || '').trim() || 'Proprietário';
  const contatoTel = (document.getElementById('nl-contato-tel')?.value || '').trim();
  const contatoEmail = (document.getElementById('nl-contato-email')?.value || '').trim();

  const funilId = document.getElementById('nl-funil-sel')?.value || 'funil-vendas-novas';
  const etapaId = document.getElementById('nl-etapa-sel')?.value || 'etapa-lead';
  const mrr = parseFloat(document.getElementById('nl-mrr')?.value) || 180.0;
  const setup = parseFloat(document.getElementById('nl-setup')?.value) || 0.0;
  const previsao = document.getElementById('nl-previsao')?.value || '';
  const notas = (document.getElementById('nl-notas')?.value || '').trim();

  if (!nome) {
    alert('Por favor, informe o Nome do Estabelecimento / Empresa.');
    document.getElementById('nl-nome')?.focus();
    return;
  }
  if (!contatoNome) {
    alert('Por favor, informe o Nome do Decisor / Responsável.');
    document.getElementById('nl-contato-nome')?.focus();
    return;
  }
  if (!contatoTel) {
    alert('Por favor, informe o Telefone / WhatsApp de contato.');
    document.getElementById('nl-contato-tel')?.focus();
    return;
  }

  const payload = {
    empresa: {
      tipo: tipoDoc,
      razao_social: razao,
      nome_fantasia: nome,
      documento: doc,
      telefone: contatoTel,
      whatsapp: contatoTel,
      email: contatoEmail,
      cidade: cidade,
      uf: 'RS',
      endereco: endereco,
      segmento: segmento,
      pdvs_estimados: pdvs,
      origem: 'Prospecção Manual'
    },
    contato: {
      nome: contatoNome,
      cargo: contatoCargo,
      telefone: contatoTel,
      whatsapp: contatoTel,
      email: contatoEmail
    },
    negociacao: {
      titulo: `Implantação TruData ERP - ${nome}`,
      funil_id: funilId,
      etapa_id: etapaId,
      responsavel_id: CRM_STATE.usuarioAtivo?.id || 'usr-admin',
      valor_mrr: mrr,
      valor_setup_produtos: setup,
      data_prevista: previsao
    },
    notas: notas
  };

  try {
    const res = await fetch('/api/crm/v2/lead/adicionar_completo', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Usuario-Id': CRM_STATE.usuarioAtivo?.id || 'usr-admin'
      },
      body: JSON.stringify(payload)
    });

    const json = await res.json();
    if (json.sucesso) {
      fecharModalNovoLead();
      // Limpar campos
      const formFields = ['nl-nome', 'nl-razao', 'nl-doc', 'nl-endereco', 'nl-contato-nome', 'nl-contato-tel', 'nl-contato-email', 'nl-notas'];
      formFields.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = '';
      });

      // Recarregar CRM e direcionar para o funil no Kanban
      await carregarEstadoCRM();
      CRM_STATE.funilAtivoId = funilId;
      trocarSubAba('kanban');

      alert(`✅ Lead "${nome}" cadastrado com sucesso e adicionado ao Pipeline!`);
    } else {
      alert('Erro ao cadastrar lead: ' + (json.erro || 'Falha desconhecida'));
    }
  } catch (err) {
    console.error('Erro na requisição de cadastro de lead:', err);
    alert('Erro de conexão ao salvar o lead.');
  }
}

function abrirModalNovoDeal() {
  document.getElementById('modal-deal').classList.remove('hidden');
}

function fecharModalDeal() {
  document.getElementById('modal-deal').classList.add('hidden');
}

async function salvarDealForm() {
  const titulo = document.getElementById('deal-titulo').value.trim();
  const empId = document.getElementById('deal-empresa-sel').value;
  const mrr = parseFloat(document.getElementById('deal-mrr').value) || 180.0;
  const setup = parseFloat(document.getElementById('deal-setup').value) || 0.0;

  if (!titulo || !empId) {
    alert('Preencha título e selecione a empresa.');
    return;
  }

  try {
    const res = await fetch('/api/crm/v2/negociacao', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Usuario-Id': CRM_STATE.usuarioAtivo.id },
      body: JSON.stringify({
        titulo,
        empresa_id: empId,
        funil_id: CRM_STATE.funilAtivoId,
        etapa_id: 'etapa-lead',
        responsavel_id: CRM_STATE.usuarioAtivo.id,
        valor_mrr: mrr,
        valor_setup_produtos: setup,
        probabilidade: 20,
        data_prevista: (new Date(Date.now() + 15*86400000)).toISOString().split('T')[0]
      })
    });
    const json = await res.json();
    if (json.sucesso) {
      fecharModalDeal();
      await carregarEstadoCRM();
    }
  } catch (e) {
    console.error('Erro ao salvar deal:', e);
  }
}

function abrirModalNovaAtividade(dealId = null, empresaId = null) {
  const modal = document.getElementById('modal-atividade');
  if (!modal) return;

  const dealHidden = document.getElementById('ativ-deal-id');
  if (dealHidden) dealHidden.value = dealId || '';

  // Popular select de empresas
  const selEmp = document.getElementById('ativ-empresa-sel');
  if (selEmp && CRM_STATE.dados?.empresas) {
    selEmp.innerHTML = CRM_STATE.dados.empresas.map(e => 
      `<option value="${e.id}">${e.nome_fantasia || e.razao_social || 'Empresa'} (📍 ${e.cidade || 'RS'})</option>`
    ).join('');
  }

  // Pre-selecionar empresa ou deal
  let suggestedTitle = '';
  if (dealId && CRM_STATE.dados?.negociacoes) {
    const deal = CRM_STATE.dados.negociacoes.find(d => d.id === dealId);
    if (deal) {
      if (selEmp) selEmp.value = deal.empresa_id;
      const emp = (CRM_STATE.dados.empresas || []).find(e => e.id === deal.empresa_id);
      suggestedTitle = `📞 Follow-up: ${emp?.nome_fantasia || deal.titulo}`;
    }
  } else if (empresaId && selEmp) {
    selEmp.value = empresaId;
  }

  const inputTit = document.getElementById('ativ-titulo');
  if (inputTit) {
    inputTit.value = suggestedTitle || '';
    if (!suggestedTitle) inputTit.placeholder = 'Ex: Demonstração presencial do PDV com contingência offline';
  }

  // Definir data padrão (Amanhã às 09:30)
  definirHorarioAtividade(1, 9, 30);

  modal.classList.remove('hidden');
}

function fecharModalAtividade() {
  const modal = document.getElementById('modal-atividade');
  if (modal) modal.classList.add('hidden');
}

function preencherAcaoRapida(titulo, tipo) {
  const inputTit = document.getElementById('ativ-titulo');
  const selTipo = document.getElementById('ativ-tipo');
  if (inputTit) inputTit.value = titulo;
  if (selTipo && tipo) selTipo.value = tipo;
}

function definirHorarioAtividade(diasAFrente, hora, minuto = 0) {
  const d = new Date();
  d.setDate(d.getDate() + diasAFrente);
  d.setHours(hora, minuto, 0, 0);

  const pad = (n) => String(n).padStart(2, '0');
  const str = `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
  
  const inputDh = document.getElementById('ativ-dh');
  if (inputDh) inputDh.value = str;
}

function formatarDataHoraCurta(dh) {
  if (!dh) return '';
  try {
    const d = new Date(dh);
    const dia = String(d.getDate()).padStart(2, '0');
    const mes = String(d.getMonth() + 1).padStart(2, '0');
    const hora = String(d.getHours()).padStart(2, '0');
    const min = String(d.getMinutes()).padStart(2, '0');
    return `${dia}/${mes} ${hora}:${min}`;
  } catch (e) {
    return dh;
  }
}

async function salvarAtividadeForm() {
  const titulo = document.getElementById('ativ-titulo').value.trim();
  const tipo = document.getElementById('ativ-tipo').value;
  const empId = document.getElementById('ativ-empresa-sel').value;
  const dh = document.getElementById('ativ-dh').value;
  const duracao = parseInt(document.getElementById('ativ-duracao')?.value || '60', 10);
  const dealId = document.getElementById('ativ-deal-id')?.value || null;
  const notas = document.getElementById('ativ-notas')?.value.trim() || '';

  if (!titulo || !empId || !dh) {
    mostrarToastCRM('Preencha o título, selecione a empresa e defina data e horário.', 'erro');
    return;
  }

  try {
    const res = await fetch('/api/crm/v2/atividade', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Usuario-Id': CRM_STATE.usuarioAtivo.id },
      body: JSON.stringify({
        titulo,
        tipo,
        empresa_id: empId,
        deal_id: dealId,
        data_hora: dh,
        duracao_minutos: duracao,
        notas,
        responsavel_id: CRM_STATE.usuarioAtivo.id,
        status: 'pendente'
      })
    });
    const json = await res.json();
    if (json.sucesso) {
      fecharModalAtividade();
      await carregarEstadoCRM();
      renderizarAtividades();
      mostrarToastCRM(`✓ Ação agendada com sucesso! (${formatarDataHora(dh)})`, 'sucesso');
    } else {
      mostrarToastCRM('Erro ao salvar atividade: ' + (json.erro || 'Erro desconhecido'), 'erro');
    }
  } catch (e) {
    console.error('Erro ao salvar atividade:', e);
    mostrarToastCRM('Erro de conexão ao agendar atividade.', 'erro');
  }
}

async function importarPlanilhaCSV(e) {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = async (event) => {
    const texto = event.target.result;
    try {
      const res = await fetch('/api/crm/v2/importar_csv', {
        method: 'POST',
        headers: { 'Content-Type': 'text/csv', 'X-Usuario-Id': CRM_STATE.usuarioAtivo.id },
        body: texto
      });
      const json = await res.json();
      if (json.sucesso) {
        alert(`Sucesso! ${json.total_importados} registros importados.`);
        await carregarEstadoCRM();
      } else {
        alert('Erro ao importar: ' + json.erro);
      }
    } catch (err) {
      console.error('Erro na importação:', err);
    }
  };
  reader.readAsText(file);
}

// ==================== DETALHES DE EMPRESA & TIMELINE ====================
function abrirModalDetalhesEmpresa(empId) {
  const emp = CRM_STATE.dados.empresas.find(e => e.id === empId);
  if (!emp) return;

  const contatos = CRM_STATE.dados.contatos.filter(c => c.empresa_id === empId);
  const interacoes = CRM_STATE.dados.historico_interacoes.filter(h => h.empresa_id === empId);
  const deals = CRM_STATE.dados.negociacoes.filter(d => d.empresa_id === empId);

  let modalEl = document.getElementById('modal-detalhes-empresa-dinamico');
  if (!modalEl) {
    modalEl = document.createElement('div');
    modalEl.id = 'modal-detalhes-empresa-dinamico';
    modalEl.className = 'crm-modal';
    document.body.appendChild(modalEl);
  }

  modalEl.classList.remove('hidden');
  modalEl.innerHTML = `
    <div class="crm-modal-box" style="max-width:760px;">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:1rem; border-bottom:1px solid var(--crm-border); padding-bottom:0.75rem;">
        <div>
          <h3 style="color:#fff; font-size:1.3rem;">🏢 ${emp.nome_fantasia || emp.razao_social}</h3>
          <p style="font-size:0.8rem; color:#94a3b8;">${emp.tipo || 'PJ'} · Doc: ${emp.documento || 'Não informado'} · 📍 ${emp.cidade} - ${emp.uf || 'RS'}</p>
        </div>
        <button onclick="document.getElementById('modal-detalhes-empresa-dinamico').classList.add('hidden')" class="btn-crm">✕ Fechar</button>
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-bottom:1rem;">
        <div style="background:#090e18; padding:0.85rem; border-radius:8px; font-size:0.82rem;">
          <div style="color:#38bdf8; font-weight:700; margin-bottom:0.4rem;">Informações Comerciais</div>
          <div>Segmento: <strong>${emp.segmento}</strong></div>
          <div>PDVs Estimados: <strong>${emp.pdvs_estimados || 1}</strong></div>
          <div>Telefone: <strong>${emp.telefone || '-'}</strong></div>
          <div>E-mail: <strong>${emp.email || '-'}</strong></div>
          <div style="margin-top:0.5rem;">
            <button onclick="abrirWhatsAppLead('${emp.telefone}', '${emp.nome_fantasia}', '${contatos[0]?.nome || ''}')" class="btn-crm btn-crm-success" style="font-size:0.75rem;">
              💬 Chamar no WhatsApp
            </button>
          </div>
        </div>

        <div style="background:#090e18; padding:0.85rem; border-radius:8px; font-size:0.82rem;">
          <div style="color:#34d399; font-weight:700; margin-bottom:0.4rem;">Oportunidades (${deals.length})</div>
          ${deals.length === 0 ? '<div style="color:#64748b;">Nenhum deal ativo.</div>' : deals.map(d => `
            <div style="border-bottom:1px solid rgba(255,255,255,0.06); padding:0.3rem 0;">
              <div><strong>${d.titulo}</strong></div>
              <div style="font-size:0.72rem; color:#34d399;">MRR: R$ ${d.valor_mrr}/mês · Etapa: ${d.etapa_id}</div>
            </div>
          `).join('')}
        </div>
      </div>

      <!-- Timeline de Interações -->
      <div style="background:#090e18; padding:0.85rem; border-radius:8px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
          <strong style="color:#fff; font-size:0.85rem;">Histórico de Interações</strong>
          <button onclick="adicionarNotaRapida('${emp.id}')" class="btn-crm" style="font-size:0.72rem; padding:0.25rem 0.6rem;">+ Adicionar Nota / Contato</button>
        </div>
        <div style="max-height:180px; overflow-y:auto; display:flex; flex-direction:column; gap:0.5rem;">
          ${interacoes.length === 0 ? '<div style="color:#64748b; font-size:0.8rem;">Nenhum histórico registrado ainda.</div>' : interacoes.map(h => `
            <div class="timeline-item-ent">
              <div class="timeline-meta">${formatarDataHora(h.data_hora)} · <strong>${h.canal || h.tipo}</strong> (${h.responsavel_id || 'Sistema'})</div>
              <div class="timeline-desc">${h.descricao}</div>
            </div>
          `).join('')}
        </div>
      </div>
    </div>
  `;
}

// ==================== MODAL DE EDIÇÃO DE EMPRESA ====================
function abrirModalEditarEmpresa(empId) {
  const emp = CRM_STATE.dados.empresas.find(e => e.id === empId);
  if (!emp) {
    mostrarToastCRM('Empresa não encontrada.', 'erro');
    return;
  }

  // Se o modal de detalhes estiver aberto, oculta-o
  const detalhesModal = document.getElementById('modal-detalhes-empresa-dinamico');
  if (detalhesModal) detalhesModal.classList.add('hidden');

  let modalEl = document.getElementById('modal-editar-empresa-dinamico');
  if (!modalEl) {
    modalEl = document.createElement('div');
    modalEl.id = 'modal-editar-empresa-dinamico';
    modalEl.className = 'crm-modal';
    document.body.appendChild(modalEl);
  }

  const tipo = (emp.tipo || 'PJ').toUpperCase();
  const lgpdAtivo = emp.consentimento_lgpd ? !!emp.consentimento_lgpd.autorizado : true;

  modalEl.classList.remove('hidden');
  modalEl.innerHTML = `
    <div class="crm-modal-box" style="max-width:680px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.25rem; border-bottom:1px solid var(--crm-border); padding-bottom:0.75rem;">
        <h3 style="color:#fff; font-size:1.25rem; display:flex; align-items:center; gap:0.5rem; margin:0;">
          <span>✏️</span> Editar Dados da Empresa
        </h3>
        <button type="button" onclick="fecharModalEditarEmpresa()" class="btn-crm" style="padding:0.3rem 0.6rem;">✕</button>
      </div>

      <div id="alert-erro-editar-empresa" style="display:none; color:#ef4444; background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.3); padding:0.65rem; border-radius:6px; font-size:0.82rem; margin-bottom:1rem;"></div>

      <form id="form-editar-empresa" onsubmit="salvarEdicaoEmpresa(event, '${emp.id}')">
        <div style="display:grid; grid-template-columns:1fr 2fr; gap:0.75rem; margin-bottom:0.75rem;">
          <div class="crm-form-group" style="margin-bottom:0;">
            <label style="font-size:0.78rem; color:#94a3b8; font-weight:600;">Tipo de Pessoa</label>
            <select id="edit-emp-tipo" class="crm-form-select">
              <option value="PJ" ${tipo === 'PJ' ? 'selected' : ''}>Pessoa Jurídica (PJ)</option>
              <option value="PF" ${tipo === 'PF' ? 'selected' : ''}>Pessoa Física (PF)</option>
              <option value="MEI" ${tipo === 'MEI' ? 'selected' : ''}>Microempreendedor (MEI)</option>
              <option value="Outro" ${!['PJ', 'PF', 'MEI'].includes(tipo) ? 'selected' : ''}>Outro / Produtor Rural</option>
            </select>
          </div>
          <div class="crm-form-group" style="margin-bottom:0;">
            <label style="font-size:0.78rem; color:#94a3b8; font-weight:600;">Nome Fantasia *</label>
            <input type="text" id="edit-emp-nome-fantasia" class="crm-form-input" value="${escapeHtml(emp.nome_fantasia || '')}" required placeholder="Ex: Mercado Central">
          </div>
        </div>

        <div class="crm-form-group" style="margin-bottom:0.75rem;">
          <label style="font-size:0.78rem; color:#94a3b8; font-weight:600;">Razão Social</label>
          <input type="text" id="edit-emp-razao-social" class="crm-form-input" value="${escapeHtml(emp.razao_social || '')}" placeholder="Ex: Mercado Central Alimentos Ltda">
        </div>

        <div style="display:grid; grid-template-columns:1.5fr 1fr; gap:0.75rem; margin-bottom:0.75rem;">
          <div class="crm-form-group" style="margin-bottom:0;">
            <label style="font-size:0.78rem; color:#94a3b8; font-weight:600;">Documento (CNPJ / CPF)</label>
            <input type="text" id="edit-emp-doc" class="crm-form-input" value="${escapeHtml(emp.documento || '')}" placeholder="00.000.000/0001-00">
          </div>
          <div class="crm-form-group" style="margin-bottom:0;">
            <label style="font-size:0.78rem; color:#94a3b8; font-weight:600;">Inscrição Estadual</label>
            <input type="text" id="edit-emp-ie" class="crm-form-input" value="${escapeHtml(emp.inscricao_estadual || '')}" placeholder="Isento ou Nº">
          </div>
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem; margin-bottom:0.75rem;">
          <div class="crm-form-group" style="margin-bottom:0;">
            <label style="font-size:0.78rem; color:#94a3b8; font-weight:600;">Telefone Principal</label>
            <input type="text" id="edit-emp-tel" class="crm-form-input" value="${escapeHtml(emp.telefone || '')}" placeholder="(54) 3361-0000">
          </div>
          <div class="crm-form-group" style="margin-bottom:0;">
            <label style="font-size:0.78rem; color:#94a3b8; font-weight:600;">WhatsApp Comercial</label>
            <input type="text" id="edit-emp-wpp" class="crm-form-input" value="${escapeHtml(emp.whatsapp || '')}" placeholder="(54) 99999-9999">
          </div>
        </div>

        <div class="crm-form-group" style="margin-bottom:0.75rem;">
          <label style="font-size:0.78rem; color:#94a3b8; font-weight:600;">E-mail Comercial</label>
          <input type="email" id="edit-emp-email" class="crm-form-input" value="${escapeHtml(emp.email || '')}" placeholder="contato@empresa.com.br">
        </div>

        <div style="display:grid; grid-template-columns:2fr 1fr; gap:0.75rem; margin-bottom:0.75rem;">
          <div class="crm-form-group" style="margin-bottom:0;">
            <label style="font-size:0.78rem; color:#94a3b8; font-weight:600;">Cidade *</label>
            <input type="text" id="edit-emp-cidade" class="crm-form-input" value="${escapeHtml(emp.cidade || '')}" required placeholder="Ex: Sarandi">
          </div>
          <div class="crm-form-group" style="margin-bottom:0;">
            <label style="font-size:0.78rem; color:#94a3b8; font-weight:600;">UF</label>
            <input type="text" id="edit-emp-uf" class="crm-form-input" value="${escapeHtml(emp.uf || 'RS')}" maxlength="2" placeholder="RS">
          </div>
        </div>

        <div class="crm-form-group" style="margin-bottom:0.75rem;">
          <label style="font-size:0.78rem; color:#94a3b8; font-weight:600;">Endereço Completo</label>
          <input type="text" id="edit-emp-endereco" class="crm-form-input" value="${escapeHtml(emp.endereco || '')}" placeholder="Rua, Número, Bairro">
        </div>

        <div style="display:grid; grid-template-columns:2fr 1fr; gap:0.75rem; margin-bottom:1rem;">
          <div class="crm-form-group" style="margin-bottom:0;">
            <label style="font-size:0.78rem; color:#94a3b8; font-weight:600;">Segmento de Atuação</label>
            <select id="edit-emp-segmento" class="crm-form-select">
              ${['Supermercados & Mercearias', 'Escritórios de Contabilidade', 'Autopeças & Oficinas', 'Farmácias & Drogarias', 'Lojas de Roupas & Calçados', 'Agropecuárias & Pet Shops', 'Materiais de Construção', 'Restaurantes & Lanchonetes', 'Geral / Outros'].map(seg => `
                <option value="${seg}" ${emp.segmento === seg ? 'selected' : ''}>${seg}</option>
              `).join('')}
            </select>
          </div>
          <div class="crm-form-group" style="margin-bottom:0;">
            <label style="font-size:0.78rem; color:#94a3b8; font-weight:600;">PDVs Estimados</label>
            <input type="number" id="edit-emp-pdvs" class="crm-form-input" value="${emp.pdvs_estimados || 1}" min="1" max="99">
          </div>
        </div>

        <div style="background:rgba(255,255,255,0.03); border:1px solid var(--crm-border); padding:0.75rem; border-radius:8px; margin-bottom:1.25rem;">
          <label style="display:flex; align-items:center; gap:0.6rem; cursor:pointer; font-size:0.82rem; color:#cbd5e1; user-select:none;">
            <input type="checkbox" id="edit-emp-lgpd" ${lgpdAtivo ? 'checked' : ''} style="width:16px; height:16px; accent-color:var(--crm-primary);">
            <span>Consentimento LGPD Ativo (Base legal: Art. 7º V/IX da Lei 13.709/2018)</span>
          </label>
        </div>

        <div style="display:flex; justify-content:flex-end; gap:0.75rem; border-top:1px solid var(--crm-border); padding-top:1rem;">
          <button type="button" onclick="fecharModalEditarEmpresa()" class="btn-crm">Cancelar</button>
          <button type="submit" id="btn-submit-editar-empresa" class="btn-crm btn-crm-primary" style="display:flex; align-items:center; gap:0.4rem;">
            <span>💾</span> Salvar Alterações
          </button>
        </div>
      </form>
    </div>
  `;
}

function fecharModalEditarEmpresa() {
  const modal = document.getElementById('modal-editar-empresa-dinamico');
  if (modal) modal.classList.add('hidden');
}

async function salvarEdicaoEmpresa(e, empId) {
  e.preventDefault();
  const btn = document.getElementById('btn-submit-editar-empresa');
  const alertEl = document.getElementById('alert-erro-editar-empresa');
  if (alertEl) alertEl.style.display = 'none';

  const nomeFantasia = document.getElementById('edit-emp-nome-fantasia').value.trim();
  const razaoSocial = document.getElementById('edit-emp-razao-social').value.trim();
  const tipo = document.getElementById('edit-emp-tipo').value;
  const doc = document.getElementById('edit-emp-doc').value.trim();
  const ie = document.getElementById('edit-emp-ie').value.trim();
  const tel = document.getElementById('edit-emp-tel').value.trim();
  const wpp = document.getElementById('edit-emp-wpp').value.trim();
  const email = document.getElementById('edit-emp-email').value.trim();
  const cidade = document.getElementById('edit-emp-cidade').value.trim();
  const uf = (document.getElementById('edit-emp-uf').value.trim() || 'RS').toUpperCase();
  const endereco = document.getElementById('edit-emp-endereco').value.trim();
  const segmento = document.getElementById('edit-emp-segmento').value;
  const pdvs = parseInt(document.getElementById('edit-emp-pdvs').value) || 1;
  const lgpdAtivo = document.getElementById('edit-emp-lgpd').checked;

  if (!nomeFantasia && !razaoSocial) {
    if (alertEl) {
      alertEl.textContent = 'Por favor, informe ao menos o Nome Fantasia ou Razão Social.';
      alertEl.style.display = 'block';
    }
    return;
  }

  const payload = {
    id: empId,
    tipo,
    nome_fantasia: nomeFantasia || razaoSocial,
    razao_social: razaoSocial || nomeFantasia,
    documento: doc,
    inscricao_estadual: ie,
    telefone: tel,
    whatsapp: wpp || tel,
    email,
    cidade: cidade || 'Sarandi',
    uf,
    endereco,
    segmento,
    pdvs_estimados: pdvs,
    consentimento_lgpd: {
      autorizado: lgpdAtivo,
      data_consentimento: new Date().toISOString(),
      base_legal: "Art. 7º V/IX da LGPD (Relação Comercial B2B)"
    }
  };

  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '<span>⏳</span> Salvando...';
  }

  try {
    const res = await fetch('/api/crm/v2/empresa', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Usuario-Id': CRM_STATE.usuarioAtivo?.id || 'usr-admin'
      },
      body: JSON.stringify(payload)
    });
    const json = await res.json();
    if (json.sucesso) {
      // Atualização reativa em memória sem reload
      const empIdx = CRM_STATE.dados.empresas.findIndex(emp => emp.id === empId);
      if (empIdx !== -1) {
        CRM_STATE.dados.empresas[empIdx] = {
          ...CRM_STATE.dados.empresas[empIdx],
          ...json.empresa,
          ...payload
        };
      }
      fecharModalEditarEmpresa();
      renderizarContatosEmpresas();
      mostrarToastCRM('Empresa atualizada com sucesso!', 'sucesso');
    } else {
      throw new Error(json.erro || 'Falha ao salvar as alterações.');
    }
  } catch (err) {
    console.error('Erro ao atualizar empresa:', err);
    if (alertEl) {
      alertEl.textContent = 'Erro ao salvar alterações: ' + (err.message || 'Verifique a conexão.');
      alertEl.style.display = 'block';
    } else {
      mostrarToastCRM('Erro ao salvar: ' + err.message, 'erro');
    }
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = '<span>💾</span> Salvar Alterações';
    }
  }
}

// ==================== MODAL DE EXCLUSÃO DE EMPRESA ====================
function confirmarExcluirEmpresa(empId) {
  const emp = CRM_STATE.dados.empresas.find(e => e.id === empId);
  if (!emp) {
    mostrarToastCRM('Empresa não encontrada.', 'erro');
    return;
  }

  const contatos = CRM_STATE.dados.contatos.filter(c => c.empresa_id === empId);
  const deals = CRM_STATE.dados.negociacoes.filter(d => d.empresa_id === empId);

  let modalEl = document.getElementById('modal-confirmar-exclusao-dinamico');
  if (!modalEl) {
    modalEl = document.createElement('div');
    modalEl.id = 'modal-confirmar-exclusao-dinamico';
    modalEl.className = 'crm-modal';
    document.body.appendChild(modalEl);
  }

  const nome = emp.nome_fantasia || emp.razao_social || 'esta empresa';
  let alertaVinculos = '';
  if (contatos.length > 0 || deals.length > 0) {
    alertaVinculos = `
      <div style="background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.3); border-radius:6px; padding:0.6rem; margin-bottom:1rem; font-size:0.78rem; color:#fbbf24;">
        ⚠️ <strong>Atenção:</strong> Existem <strong>${contatos.length} contato(s)</strong> e <strong>${deals.length} oportunidade(s)</strong> associados a este registro.
      </div>
    `;
  }

  modalEl.classList.remove('hidden');
  modalEl.innerHTML = `
    <div class="crm-modal-box crm-delete-box">
      <div class="crm-delete-icon-wrap">
        <svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
      </div>
      <h3 style="color:#fff; font-size:1.2rem; margin-bottom:0.5rem;">Excluir Empresa?</h3>
      <p style="color:#94a3b8; font-size:0.85rem; line-height:1.45; margin-bottom:1rem;">
        Tem certeza de que deseja remover permanentemente o registro de <strong style="color:#f8fafc;">"${escapeHtml(nome)}"</strong> da base?
      </p>
      ${alertaVinculos}
      <div id="erro-exclusao-empresa" style="display:none; color:#ef4444; background:rgba(239,68,68,0.12); border:1px solid rgba(239,68,68,0.3); padding:0.6rem; border-radius:6px; font-size:0.8rem; margin-bottom:1rem;"></div>
      <div style="display:flex; justify-content:flex-end; gap:0.65rem;">
        <button type="button" onclick="fecharModalExcluirEmpresa()" class="btn-crm">Cancelar</button>
        <button type="button" id="btn-confirmar-excluir" onclick="executarExclusaoEmpresa('${emp.id}')" class="btn-crm btn-crm-danger">
          🗑️ Confirmar Exclusão
        </button>
      </div>
    </div>
  `;
}

function fecharModalExcluirEmpresa() {
  const modal = document.getElementById('modal-confirmar-exclusao-dinamico');
  if (modal) modal.classList.add('hidden');
}

async function executarExclusaoEmpresa(empId) {
  const btn = document.getElementById('btn-confirmar-excluir');
  const alertEl = document.getElementById('erro-exclusao-empresa');
  if (alertEl) alertEl.style.display = 'none';

  if (btn) {
    btn.disabled = true;
    btn.textContent = 'Excluindo...';
  }

  try {
    const res = await fetch('/api/crm/v2/empresa/excluir', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Usuario-Id': CRM_STATE.usuarioAtivo?.id || 'usr-admin'
      },
      body: JSON.stringify({ id: empId })
    });
    const json = await res.json();
    if (json.sucesso) {
      // Remoção reativa em memória sem reload
      CRM_STATE.dados.empresas = CRM_STATE.dados.empresas.filter(e => e.id !== empId);
      fecharModalExcluirEmpresa();
      renderizarContatosEmpresas();
      mostrarToastCRM('Empresa excluída com sucesso!', 'sucesso');
    } else {
      throw new Error(json.erro || 'Falha ao excluir empresa.');
    }
  } catch (err) {
    console.error('Erro ao excluir empresa:', err);
    if (alertEl) {
      alertEl.textContent = 'Erro ao excluir: ' + (err.message || 'Verifique a conexão.');
      alertEl.style.display = 'block';
    } else {
      mostrarToastCRM('Erro ao excluir empresa: ' + err.message, 'erro');
    }
    if (btn) {
      btn.disabled = false;
      btn.textContent = '🗑️ Confirmar Exclusão';
    }
  }
}

// ==================== TOAST & FEEDBACK REATIVO ====================
function mostrarToastCRM(mensagem, tipo = 'sucesso') {
  let container = document.getElementById('crm-toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'crm-toast-container';
    container.style.cssText = 'position:fixed; top:20px; right:20px; z-index:99999; display:flex; flex-direction:column; gap:0.5rem; pointer-events:none;';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  const isSucesso = tipo === 'sucesso';
  const corBorda = isSucesso ? '#10b981' : '#ef4444';
  const corBg = isSucesso ? 'rgba(16,185,129,0.2)' : 'rgba(239,68,68,0.2)';
  const icone = isSucesso ? '✓' : '⚠️';

  toast.style.cssText = `
    background: #0f172a;
    background-color: ${corBg};
    backdrop-filter: blur(8px);
    border: 1px solid ${corBorda};
    color: #f8fafc;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    pointer-events: auto;
    transition: opacity 0.3s ease, transform 0.3s ease;
  `;
  toast.innerHTML = `<span style="color:${corBorda}; font-weight:700;">${icone}</span> <span>${escapeHtml(mensagem)}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-10px)';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// ==================== DETALHES DO DEAL ====================
function abrirModalDetalhesDeal(dealId) {
  const deal = CRM_STATE.dados.negociacoes.find(d => d.id === dealId);
  if (!deal) return;

  const emp = CRM_STATE.dados.empresas.find(e => e.id === deal.empresa_id) || {};

  let modalEl = document.getElementById('modal-detalhes-deal-dinamico');
  if (!modalEl) {
    modalEl = document.createElement('div');
    modalEl.id = 'modal-detalhes-deal-dinamico';
    modalEl.className = 'crm-modal';
    document.body.appendChild(modalEl);
  }

  modalEl.classList.remove('hidden');
  modalEl.innerHTML = `
    <div class="crm-modal-box" style="max-width:600px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; border-bottom:1px solid var(--crm-border); padding-bottom:0.75rem;">
        <h3 style="color:#fff; font-size:1.2rem;">Editar Oportunidade</h3>
        <button onclick="document.getElementById('modal-detalhes-deal-dinamico').classList.add('hidden')" class="btn-crm">✕</button>
      </div>

      <div class="crm-form-group">
        <label>Título do Deal</label>
        <input type="text" id="edit-deal-titulo" class="crm-form-input" value="${deal.titulo || ''}">
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
        <div class="crm-form-group">
          <label>Mensalidade MRR (R$)</label>
          <input type="number" id="edit-deal-mrr" class="crm-form-input" value="${deal.valor_mrr || 180}">
        </div>
        <div class="crm-form-group">
          <label>Setup / Produtos (R$)</label>
          <input type="number" id="edit-deal-setup" class="crm-form-input" value="${deal.valor_setup_produtos || 0}">
        </div>
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.75rem;">
        <div class="crm-form-group">
          <label>Probabilidade (%)</label>
          <input type="number" id="edit-deal-prob" class="crm-form-input" value="${deal.probabilidade || 50}" min="0" max="100">
        </div>
        <div class="crm-form-group">
          <label>Data Prevista de Fechamento</label>
          <input type="date" id="edit-deal-data" class="crm-form-input" value="${deal.data_prevista || ''}">
        </div>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; gap:0.5rem; margin-top:1.5rem; border-top:1px solid var(--crm-border); padding-top:1rem;">
        <button onclick="confirmarRemoverDeal('${deal.id}', event)" class="btn-crm" style="color:#ef4444; border-color:rgba(239,68,68,0.4); background:rgba(239,68,68,0.12);" title="Remover esta oportunidade">🗑️ Remover do Kanban</button>
        <div style="display:flex; gap:0.5rem;">
          <button onclick="document.getElementById('modal-detalhes-deal-dinamico').classList.add('hidden')" class="btn-crm">Cancelar</button>
          <button onclick="salvarEdicaoDeal('${deal.id}')" class="btn-crm btn-crm-primary">💾 Salvar Alterações</button>
        </div>
      </div>
    </div>
  `;
}

async function salvarEdicaoDeal(dealId) {
  const deal = CRM_STATE.dados.negociacoes.find(d => d.id === dealId);
  if (!deal) return;

  deal.titulo = document.getElementById('edit-deal-titulo').value.trim() || deal.titulo;
  deal.valor_mrr = parseFloat(document.getElementById('edit-deal-mrr').value) || deal.valor_mrr;
  deal.valor_setup_produtos = parseFloat(document.getElementById('edit-deal-setup').value) || deal.valor_setup_produtos;
  deal.probabilidade = parseInt(document.getElementById('edit-deal-prob').value) || deal.probabilidade;
  deal.data_prevista = document.getElementById('edit-deal-data').value || deal.data_prevista;

  try {
    const res = await fetch('/api/crm/v2/negociacao', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Usuario-Id': CRM_STATE.usuarioAtivo.id },
      body: JSON.stringify(deal)
    });
    const json = await res.json();
    if (json.sucesso) {
      document.getElementById('modal-detalhes-deal-dinamico').classList.add('hidden');
      await carregarEstadoCRM();
    }
  } catch (e) {
    console.error('Erro ao editar deal:', e);
  }
}

async function confirmarRemoverDeal(dealId, e) {
  if (e) {
    e.stopPropagation();
    e.preventDefault();
  }
  const deal = (CRM_STATE.dados?.negociacoes || []).find(d => d.id === dealId);
  const titulo = deal ? deal.titulo : 'esta negociação';

  if (!confirm(`Deseja remover "${titulo}" do Kanban?`)) {
    return;
  }

  try {
    const res = await fetch('/api/crm/v2/negociacao/excluir', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Usuario-Id': CRM_STATE.usuarioAtivo.id
      },
      body: JSON.stringify({ deal_id: dealId })
    });
    const json = await res.json();
    if (json.sucesso) {
      const modal = document.getElementById('modal-detalhes-deal-dinamico');
      if (modal) modal.classList.add('hidden');
      await carregarEstadoCRM();
    } else {
      alert('Não foi possível remover: ' + (json.erro || 'Erro desconhecido'));
    }
  } catch (err) {
    console.error('Falha ao remover oportunidade:', err);
    alert('Erro de conexão ao remover a oportunidade.');
  }
}

// ==================== DISPARO DE WHATSAPP ====================
function abrirWhatsAppLead(tel, empresa, nome) {
  if (!tel) {
    alert('Telefone não cadastrado para esta empresa.');
    return;
  }
  const limpo = tel.replace(/\D/g, '');
  const numFinal = limpo.startsWith('55') ? limpo : ('55' + limpo);
  const msg = encodeURIComponent(
    `Olá, ${nome || 'tudo bem'}! Aqui é da equipe comercial da TruData ERP (Sarandi/RS). 🤝\n` +
    `Gostaríamos de conversar sobre as soluções para a *${empresa || 'sua empresa'}* com emissão fiscal rápida e contingência 100% offline.\nPodemos falar nesta semana?`
  );
  window.open(`https://wa.me/${numFinal}?text=${msg}`, '_blank');
}

async function adicionarNotaRapida(empId) {
  const texto = prompt('Digite o resumo do contato / interação:');
  if (!texto || !texto.trim()) return;

  try {
    const res = await fetch('/api/crm/v2/interacao', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Usuario-Id': CRM_STATE.usuarioAtivo.id },
      body: JSON.stringify({
        empresa_id: empId,
        tipo: 'ligacao',
        canal: 'Contato Telefônico',
        descricao: texto.trim()
      })
    });
    const json = await res.json();
    if (json.sucesso) {
      alert('Interação adicionada à timeline com sucesso!');
      await carregarEstadoCRM();
      abrirModalDetalhesEmpresa(empId);
    }
  } catch (e) {
    console.error('Erro ao adicionar nota:', e);
  }
}

// ==================== ITEM 1: PROPOSTA COMERCIAL RASTREÁVEL (1-CLICK) ====================

async function gerarProposta1Click(dealId) {
  try {
    const res = await fetch('/api/crm/v2/proposta/gerar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Usuario-Id': CRM_STATE.usuarioAtivo.id },
      body: JSON.stringify({ deal_id: dealId })
    });
    const json = await res.json();
    if (json.sucesso) {
      const prop = json.proposta;
      const urlCompleta = `${window.location.origin}/proposta-digital?p=${prop.hash}`;
      
      const inputLink = document.getElementById('prop-link-input');
      if (inputLink) inputLink.value = urlCompleta;
      
      const openBtn = document.getElementById('prop-open-btn');
      if (openBtn) openBtn.href = urlCompleta;
      
      const wppBtn = document.getElementById('prop-wpp-btn');
      if (wppBtn) {
        const msg = encodeURIComponent(`Olá, ${prop.contato_nome || ''}! Segue a sua Proposta Comercial Oficial TruData: ${urlCompleta}\nVocê pode visualizar os detalhes técnicos e assinar digitalmente.`);
        const fone = (prop.contato_telefone || '54999887766').replace(/\D/g, '');
        const numFinal = fone.startsWith('55') ? fone : ('55' + fone);
        wppBtn.href = `https://wa.me/${numFinal}?text=${msg}`;
      }

      document.getElementById('modal-proposta').classList.remove('hidden');
      await carregarEstadoCRM();
    } else {
      alert('Erro ao gerar proposta: ' + (json.erro || 'Falha ao processar'));
    }
  } catch (e) {
    console.error('Erro na geração da proposta:', e);
    alert('Erro de conexão com o servidor.');
  }
}

function abrirLinkProposta(hash) {
  window.open(`/proposta-digital?p=${encodeURIComponent(hash)}`, '_blank');
}

function copiarLinkProposta() {
  const input = document.getElementById('prop-link-input');
  if (!input) return;
  input.select();
  navigator.clipboard.writeText(input.value).then(() => {
    alert('✓ Link copiado para a área de transferência!');
  }).catch(() => {
    document.execCommand('copy');
    alert('✓ Link copiado!');
  });
}

function fecharModalProposta() {
  document.getElementById('modal-proposta').classList.add('hidden');
}

// ==================== ITEM 2: ONBOARDING TÉCNICO (6 ETAPAS) ====================

function renderizarOnboarding() {
  const container = document.getElementById('view-onboarding');
  if (!container) return;

  const onboardings = CRM_STATE.dados.onboarding_checklists || [];

  if (onboardings.length === 0) {
    container.innerHTML = `
      <div class="dash-box" style="text-align:center; padding:3rem 1rem;">
        <div style="font-size:2.5rem; margin-bottom:1rem;">🚀</div>
        <h3 style="color:#fff; margin-bottom:0.5rem;">Nenhum Onboarding em Andamento</h3>
        <p style="color:#94a3b8; max-width:500px; margin:0 auto 1.5rem;">
          Quando uma proposta comercial for assinada digitalmente ou um negócio for marcado como "Ganho" no Kanban, o checklist de 6 etapas técnicas de homologação é disparado automaticamente.
        </p>
        <button onclick="trocarSubAba('kanban')" class="btn-crm btn-crm-primary">Ver Pipeline Kanban</button>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.5rem; flex-wrap:wrap; gap:1rem;">
      <div>
        <h2 style="font-family:'Outfit',sans-serif; font-size:1.35rem; color:#fff; margin:0;">🚀 Implantação & Onboarding Homologado (6 Etapas)</h2>
        <p style="color:#94a3b8; font-size:0.85rem; margin-top:0.25rem;">
          Acompanhamento técnico pós-venda: auditoria de PDVs, instalação remota do agente e treinamento assistido.
        </p>
      </div>
      <span class="badge-ent badge-pj" style="font-size:0.8rem; padding:0.4rem 0.8rem;">
        Total: ${onboardings.length} Clientes em Implantação
      </span>
    </div>

    <div class="onboarding-grid">
      ${onboardings.map(onb => {
        const isConcluido = onb.status === 'concluido' || onb.progresso_pct >= 100;
        return `
          <div class="onboarding-card">
            <div class="onboarding-card-header">
              <div>
                <div class="onboarding-title">🏢 ${onb.empresa_nome}</div>
                <div style="font-size:0.75rem; color:#94a3b8; margin-top:0.2rem;">
                  Início: ${new Date(onb.data_inicio).toLocaleDateString('pt-BR')} · Prazo Go-Live: ${onb.prazo_final_estimado || '7 dias'}
                </div>
              </div>
              <span class="badge-proposal ${isConcluido ? 'signed' : ''}">
                ${isConcluido ? '✓ Go-Live Concluído' : '⚡ ' + onb.progresso_pct + '%'}
              </span>
            </div>

            <!-- Barra de Progresso -->
            <div class="onboarding-progress-bar">
              <div class="onboarding-progress-fill" style="width:${Math.max(5, onb.progresso_pct)}%;"></div>
            </div>

            <!-- Lista das 6 Etapas Técnicas -->
            <div class="onboarding-steps-list">
              ${onb.etapas.map(et => `
                <div class="onboarding-step-item ${et.concluida ? 'concluida' : ''}" onclick="toggleEtapaOnboardingClick(event, '${onb.id}', '${et.id}', ${!et.concluida})">
                  <input type="checkbox" class="step-checkbox" ${et.concluida ? 'checked' : ''} onchange="toggleEtapaOnboarding(event, '${onb.id}', '${et.id}', this.checked)">
                  <div class="step-details">
                    <span class="step-name">${et.nome}</span>
                    <span class="step-desc">${et.descricao}</span>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.3rem;">
                      <span class="step-resp-badge">👤 ${et.responsavel} (Prazo: D+${et.prazo_dias})</span>
                      ${et.concluida && et.data_conclusao ? `
                        <span style="font-size:0.68rem; color:#10b981;">✓ ${new Date(et.data_conclusao).toLocaleDateString('pt-BR')}</span>
                      ` : ''}
                    </div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        `;
      }).join('')}
    </div>
  `;
}

function toggleEtapaOnboardingClick(e, onboardingId, etapaId, novaConcluida) {
  if (e.target.tagName === 'INPUT') return;
  toggleEtapaOnboarding(null, onboardingId, etapaId, novaConcluida);
}

async function toggleEtapaOnboarding(e, onboardingId, etapaId, isConcluida) {
  if (e) e.stopPropagation();
  try {
    const res = await fetch('/api/crm/v2/onboarding/atualizar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Usuario-Id': CRM_STATE.usuarioAtivo.id },
      body: JSON.stringify({
        onboarding_id: onboardingId,
        etapa_id: etapaId,
        concluida: isConcluida
      })
    });
    const json = await res.json();
    if (json.sucesso) {
      await carregarEstadoCRM();
    } else {
      alert('Erro ao atualizar etapa: ' + (json.erro || 'Falha'));
    }
  } catch (err) {
    console.error('Erro ao atualizar onboarding:', err);
  }
}

function irParaOnboardingDeal(dealId) {
  trocarSubAba('onboarding');
}

// ==================== ITEM 3: METAS COMERCIAIS & COMISSÕES ====================

function renderizarMetas() {
  const container = document.getElementById('view-metas');
  if (!container) return;

  const m = CRM_STATE.dados.metricas;
  const metas = m.metas_painel || {};
  const ranking = metas.ranking_vendedores || [];

  container.innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.5rem; flex-wrap:wrap; gap:1rem;">
      <div>
        <h2 style="font-family:'Outfit',sans-serif; font-size:1.35rem; color:#fff; margin:0;">🎯 Painel de Metas & Simulador de Comissões</h2>
        <p style="color:#94a3b8; font-size:0.85rem; margin-top:0.25rem;">
          Acompanhamento de metas corporativas, projeção run-rate diária e apuração transparente de comissões.
        </p>
      </div>
      <button onclick="abrirModalConfigMetas()" class="btn-crm btn-crm-primary">⚙️ Ajustar Metas da Equipe</button>
    </div>

    <!-- Termômetro Principal -->
    <div class="metas-thermometer-box">
      <div class="thermo-stats-grid">
        <div class="thermo-stat-card">
          <div class="thermo-stat-label">Meta Global MRR</div>
          <div class="thermo-stat-val" style="color:#38bdf8;">R$ ${(metas.mrr_atingido || 0).toLocaleString('pt-BR', {minimumFractionDigits: 2})} / R$ ${(metas.meta_mrr_empresa || 15000).toLocaleString('pt-BR', {minimumFractionDigits: 2})}</div>
          <div style="font-size:0.75rem; color:#cbd5e1;">Atingimento: <strong>${metas.pct_meta_mrr || 0}%</strong></div>
        </div>
        <div class="thermo-stat-card">
          <div class="thermo-stat-label">Meta PDVs Homologados</div>
          <div class="thermo-stat-val" style="color:#34d399;">${metas.pdvs_atingidos || 0} / ${metas.meta_pdvs_empresa || 50} PDVs</div>
          <div style="font-size:0.75rem; color:#cbd5e1;">Atingimento: <strong>${metas.pct_meta_pdvs || 0}%</strong></div>
        </div>
        <div class="thermo-stat-card">
          <div class="thermo-stat-label">Projeção Fechamento (Run-Rate)</div>
          <div class="thermo-stat-val" style="color:#facc15;">R$ ${(metas.projecao_run_rate_mrr || 0).toLocaleString('pt-BR', {minimumFractionDigits: 2})}</div>
          <div style="font-size:0.75rem; color:#cbd5e1;">Ritmo projetado para 30 dias</div>
        </div>
        <div class="thermo-stat-card">
          <div class="thermo-stat-label">Comissão Total Calculada</div>
          <div class="thermo-stat-val" style="color:#a855f7;">R$ ${(metas.total_comissao_equipe || 0).toLocaleString('pt-BR', {minimumFractionDigits: 2})}</div>
          <div style="font-size:0.75rem; color:#cbd5e1;">Estimativa variável para a equipe</div>
        </div>
      </div>

      <div>
        <div style="display:flex; justify-content:space-between; font-size:0.8rem; margin-bottom:0.4rem;">
          <span style="font-weight:700; color:#cbd5e1;">Progresso da Meta Global:</span>
          <span style="font-weight:800; color:#38bdf8;">${metas.pct_meta_mrr || 0}%</span>
        </div>
        <div class="thermo-progress-container">
          <div class="thermo-progress-fill" style="width:${Math.min(100, Math.max(8, metas.pct_meta_mrr || 0))}%;">
            ${metas.pct_meta_mrr || 0}%
          </div>
        </div>
      </div>
    </div>

    <!-- Tabela Detalhada por Consultor -->
    <div class="dash-box">
      <div class="dash-box-title">
        <span>Classificação & Comissionamento Individual</span>
        <span style="font-size:0.75rem; color:#94a3b8;">Base de cálculo: 12% MRR + 10% Setup</span>
      </div>
      <table class="crm-table">
        <thead>
          <tr>
            <th>Posição</th>
            <th>Consultor Comercial</th>
            <th>Equipe</th>
            <th>Deals Fechados</th>
            <th>MRR Fechado</th>
            <th>Meta Individual</th>
            <th>% Atingimento</th>
            <th>Comissão Estimada</th>
          </tr>
        </thead>
        <tbody>
          ${ranking.map(r => `
            <tr>
              <td><strong>${r.posicao}</strong></td>
              <td><strong>${r.nome}</strong></td>
              <td><span class="badge-ent badge-pj">${r.equipe}</span></td>
              <td><strong style="color:#34d399;">${r.ganhos}</strong></td>
              <td style="color:#34d399; font-family:'JetBrains Mono'; font-weight:700;">R$ ${r.mrr_ganho.toFixed(2)}</td>
              <td style="color:#94a3b8; font-family:'JetBrains Mono';">R$ ${r.meta_mrr.toFixed(2)}</td>
              <td>
                <span class="badge-proposal ${r.pct_meta >= 100 ? 'signed' : ''}">
                  ${r.pct_meta}%
                </span>
              </td>
              <td style="color:#fbbf24; font-family:'JetBrains Mono'; font-weight:800;">
                R$ ${r.comissao_estimada.toFixed(2)}
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>
  `;
}

function abrirModalConfigMetas() {
  const m = CRM_STATE.dados.metricas;
  const metas = m.metas_painel || {};
  document.getElementById('meta-mrr-emp').value = metas.meta_mrr_empresa || 15000;
  document.getElementById('meta-pdvs-emp').value = metas.meta_pdvs_empresa || 50;
  document.getElementById('meta-mes-ref').value = metas.mes_referencia || 'Setembro/2026';
  document.getElementById('modal-config-metas').classList.remove('hidden');
}

function fecharModalConfigMetas() {
  document.getElementById('modal-config-metas').classList.add('hidden');
}

async function salvarConfigMetasForm() {
  const payload = {
    meta_mrr_empresa: parseFloat(document.getElementById('meta-mrr-emp').value) || 15000,
    meta_pdvs_empresa: parseInt(document.getElementById('meta-pdvs-emp').value) || 50,
    mes_referencia: document.getElementById('meta-mes-ref').value
  };

  try {
    const res = await fetch('/api/crm/v2/metas/salvar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Usuario-Id': CRM_STATE.usuarioAtivo.id },
      body: JSON.stringify(payload)
    });
    const json = await res.json();
    if (json.sucesso) {
      fecharModalConfigMetas();
      await carregarEstadoCRM();
      alert('✓ Metas comerciais atualizadas com sucesso!');
    }
  } catch (e) {
    console.error('Erro ao salvar metas:', e);
  }
}

// ==================== DROPDOWN DE FERRAMENTAS RÁPIDAS ====================
function toggleMenuFerramentasCRM(e) {
  if (e) e.stopPropagation();
  const el = document.getElementById('dropdown-ferramentas-content');
  if (el) el.classList.toggle('hidden');
}

document.addEventListener('click', function(e) {
  const el = document.getElementById('dropdown-ferramentas-content');
  const btn = document.getElementById('btn-menu-ferramentas');
  if (el && !el.classList.contains('hidden')) {
    if (!el.contains(e.target) && (!btn || !btn.contains(e.target))) {
      el.classList.add('hidden');
    }
  }
});

