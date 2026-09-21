# -*- coding: utf-8 -*-
"""
Script de montagem e injeção do Cockpit Executivo TruData (36 Ferramentas)
em painel_aprovacao/ferramentas.html com garantia de 0 mojibake UTF-8.
"""
import re

INDEX_PATH = "painel_aprovacao/ferramentas.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

if 'id="secao-cockpit"' not in html:
    raise SystemExit("A central foi reformulada. Edite ferramentas.js; a injeção do cockpit antigo foi desativada.")

# Construção do HTML do Cockpit
COCKPIT_HTML = """    <!-- ============================================================ -->
    <!-- SEÇÃO 0: COCKPIT EXECUTIVO TRUDATA (36 FERRAMENTAS & MOTORES) -->
    <!-- ============================================================ -->
    <section id="secao-cockpit" class="space-y-8">
      
      <!-- HERO DO COCKPIT & INDICADORES DE IMPACTO -->
      <div class="bg-gradient-to-r from-slate-900 via-slate-900/90 to-emerald-950/40 border border-emerald-500/30 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden">
        <div class="absolute -right-16 -top-16 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div class="absolute -left-16 -bottom-16 w-64 h-64 bg-teal-500/10 rounded-full blur-3xl pointer-events-none"></div>
        
        <div class="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 mb-3">
              <span>🚀</span>
              <span>Suíte Comercial & Operacional 360°</span>
              <span class="bg-emerald-400 text-slate-950 text-[10px] font-black px-2 py-0.5 rounded-full">36 Motores</span>
            </div>
            <h1 class="text-2xl sm:text-3xl lg:text-4xl font-black font-display text-white tracking-tight">
              Central Executiva de Vendas & Operações <span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-300">TruData ERP</span>
            </h1>
            <p class="text-slate-300 text-xs sm:text-sm mt-2 max-w-3xl leading-relaxed">
              Ambiente unificado para prospecção regional, diagnóstico no balcão da loja, quebra de objeções ao vivo, simulação de ROI e fechamento imediato no Norte Gaúcho.
            </p>
          </div>

          <!-- Mini Badges de Status -->
          <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-2 gap-2.5 shrink-0">
            <div class="bg-slate-950/80 border border-slate-800 px-3.5 py-2.5 rounded-xl">
              <div class="text-[10px] uppercase font-bold text-slate-400">Total Ferramentas</div>
              <div class="text-lg font-black text-white font-display">36 Ativas</div>
            </div>
            <div class="bg-slate-950/80 border border-emerald-500/30 px-3.5 py-2.5 rounded-xl">
              <div class="text-[10px] uppercase font-bold text-emerald-400">Ultra-Conversão</div>
              <div class="text-lg font-black text-emerald-400 font-display">6 Motores</div>
            </div>
            <div class="bg-slate-950/80 border border-sky-500/30 px-3.5 py-2.5 rounded-xl">
              <div class="text-[10px] uppercase font-bold text-sky-400">Raio de Atuação</div>
              <div class="text-lg font-black text-sky-400 font-display">100 km RS</div>
            </div>
            <div class="bg-slate-950/80 border border-teal-500/30 px-3.5 py-2.5 rounded-xl">
              <div class="text-[10px] uppercase font-bold text-teal-400">SLA Presencial</div>
              <div class="text-lg font-black text-teal-400 font-display">Até 2h</div>
            </div>
          </div>
        </div>
      </div>

      <!-- TOP-6 QUICK DOCK: AÇÕES RÁPIDAS DE FECHAMENTO NO BALCÃO -->
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-sm font-black uppercase tracking-wider text-emerald-400 font-display">⚡ Quick Dock de Balcão</span>
            <span class="text-[11px] text-slate-400">— As 6 ferramentas de fechamento imediato para o vendedor em campo</span>
          </div>
          <span class="text-[11px] font-bold text-slate-400 hidden sm:inline">1-Click Fast Launch</span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <!-- Quick 1: Check-up 15min -->
          <a href="checkup_loja.html" class="bg-slate-900/90 hover:bg-emerald-950/40 border border-emerald-500/40 hover:border-emerald-400 p-3.5 rounded-2xl transition duration-200 group flex flex-col justify-between shadow-lg hover:shadow-emerald-500/10">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-2xl">📋</span>
                <span class="text-[9px] font-black uppercase bg-emerald-500/20 text-emerald-300 px-1.5 py-0.5 rounded border border-emerald-500/30">Laudo A4</span>
              </div>
              <div class="text-xs font-bold text-white group-hover:text-emerald-300 transition">Check-up 15 Min</div>
              <div class="text-[10px] text-slate-400 mt-1 line-clamp-2">Diagnóstico de gargalos e perdas no caixa</div>
            </div>
            <div class="mt-3 pt-2 border-t border-slate-800 text-[10px] font-bold text-emerald-400 flex items-center justify-between">
              <span>Auditar Loja</span>
              <span class="group-hover:translate-x-0.5 transition">↗</span>
            </div>
          </a>

          <!-- Quick 2: Fechador de Bolso -->
          <a href="fechamento_rapido.html" class="bg-slate-900/90 hover:bg-sky-950/40 border border-sky-500/40 hover:border-sky-400 p-3.5 rounded-2xl transition duration-200 group flex flex-col justify-between shadow-lg hover:shadow-sky-500/10">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-2xl">⚡</span>
                <span class="text-[9px] font-black uppercase bg-sky-500/20 text-sky-300 px-1.5 py-0.5 rounded border border-sky-500/30">Fast-Close</span>
              </div>
              <div class="text-xs font-bold text-white group-hover:text-sky-300 transition">Fechador Mobile</div>
              <div class="text-[10px] text-slate-400 mt-1 line-clamp-2">Parcelas, Pix Sicredi e toque na tela</div>
            </div>
            <div class="mt-3 pt-2 border-t border-slate-800 text-[10px] font-bold text-sky-400 flex items-center justify-between">
              <span>Fechar Agora</span>
              <span class="group-hover:translate-x-0.5 transition">↗</span>
            </div>
          </a>

          <!-- Quick 3: Prova Social RS -->
          <a href="prova_social_regional.html" class="bg-slate-900/90 hover:bg-amber-950/40 border border-amber-500/40 hover:border-amber-400 p-3.5 rounded-2xl transition duration-200 group flex flex-col justify-between shadow-lg hover:shadow-amber-500/10">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-2xl">🌟</span>
                <span class="text-[9px] font-black uppercase bg-amber-500/20 text-amber-300 px-1.5 py-0.5 rounded border border-amber-500/30">Áudio RS</span>
              </div>
              <div class="text-xs font-bold text-white group-hover:text-amber-300 transition">Prova Social RS</div>
              <div class="text-[10px] text-slate-400 mt-1 line-clamp-2">Depoimentos reais da região em áudio</div>
            </div>
            <div class="mt-3 pt-2 border-t border-slate-800 text-[10px] font-bold text-amber-400 flex items-center justify-between">
              <span>Tocar Áudios</span>
              <span class="group-hover:translate-x-0.5 transition">↗</span>
            </div>
          </a>

          <!-- Quick 4: Garantia Blindada -->
          <a href="garantia_blindada.html" class="bg-slate-900/90 hover:bg-teal-950/40 border border-teal-500/40 hover:border-teal-400 p-3.5 rounded-2xl transition duration-200 group flex flex-col justify-between shadow-lg hover:shadow-teal-500/10">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-2xl">🛡️</span>
                <span class="text-[9px] font-black uppercase bg-teal-500/20 text-teal-300 px-1.5 py-0.5 rounded border border-teal-500/30">Risco Zero</span>
              </div>
              <div class="text-xs font-bold text-white group-hover:text-teal-300 transition">Garantia Blindada</div>
              <div class="text-[10px] text-slate-400 mt-1 line-clamp-2">Certificado 30 dias e SLA 2h presencial</div>
            </div>
            <div class="mt-3 pt-2 border-t border-slate-800 text-[10px] font-bold text-teal-400 flex items-center justify-between">
              <span>Ver Garantia</span>
              <span class="group-hover:translate-x-0.5 transition">↗</span>
            </div>
          </a>

          <!-- Quick 5: CRM Pipeline -->
          <a href="crm.html" class="bg-slate-900/90 hover:bg-indigo-950/40 border border-indigo-500/40 hover:border-indigo-400 p-3.5 rounded-2xl transition duration-200 group flex flex-col justify-between shadow-lg hover:shadow-indigo-500/10">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-2xl">💼</span>
                <span class="text-[9px] font-black uppercase bg-indigo-500/20 text-indigo-300 px-1.5 py-0.5 rounded border border-indigo-500/30">Kanban</span>
              </div>
              <div class="text-xs font-bold text-white group-hover:text-indigo-300 transition">CRM Pipeline</div>
              <div class="text-[10px] text-slate-400 mt-1 line-clamp-2">Gestão de leads e negociações ativas</div>
            </div>
            <div class="mt-3 pt-2 border-t border-slate-800 text-[10px] font-bold text-indigo-400 flex items-center justify-between">
              <span>Abrir Funil</span>
              <span class="group-hover:translate-x-0.5 transition">↗</span>
            </div>
          </a>

          <!-- Quick 6: TCO & ROI -->
          <a href="tco_roi.html" class="bg-slate-900/90 hover:bg-cyan-950/40 border border-cyan-500/40 hover:border-cyan-400 p-3.5 rounded-2xl transition duration-200 group flex flex-col justify-between shadow-lg hover:shadow-cyan-500/10">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-2xl">📊</span>
                <span class="text-[9px] font-black uppercase bg-cyan-500/20 text-cyan-300 px-1.5 py-0.5 rounded border border-cyan-500/30">Economia</span>
              </div>
              <div class="text-xs font-bold text-white group-hover:text-cyan-300 transition">TCO & ROI 36M</div>
              <div class="text-[10px] text-slate-400 mt-1 line-clamp-2">Comparador de custos vs Linx, Hiper, Totvs</div>
            </div>
            <div class="mt-3 pt-2 border-t border-slate-800 text-[10px] font-bold text-cyan-400 flex items-center justify-between">
              <span>Calcular ROI</span>
              <span class="group-hover:translate-x-0.5 transition">↗</span>
            </div>
          </a>
        </div>
      </div>

      <!-- BARRA DE CONTROLE: FILTROS DE CATEGORIA & BUSCA EM TEMPO REAL -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 sm:p-5 shadow-xl flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        
        <!-- Chips de Categoria -->
        <div class="flex items-center gap-2 flex-wrap" id="filtros-cockpit-chips">
          <button onclick="filtrarCockpit('todos', this)" id="btn-cockpit-todos" class="btn-cockpit-chip px-3.5 py-2 rounded-xl text-xs font-bold transition bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20 whitespace-nowrap cursor-pointer">
            Todos (36)
          </button>
          <button onclick="filtrarCockpit('conversao', this)" id="btn-cockpit-conversao" class="btn-cockpit-chip px-3.5 py-2 rounded-xl text-xs font-semibold bg-slate-950 hover:bg-slate-800 text-slate-300 border border-slate-800 transition whitespace-nowrap cursor-pointer">
            🎯 1. Ultra-Conversão (6)
          </button>
          <button onclick="filtrarCockpit('b2b', this)" id="btn-cockpit-b2b" class="btn-cockpit-chip px-3.5 py-2 rounded-xl text-xs font-semibold bg-slate-950 hover:bg-slate-800 text-slate-300 border border-slate-800 transition whitespace-nowrap cursor-pointer">
            🛰️ 2. Vendas B2B & Expansão (10)
          </button>
          <button onclick="filtrarCockpit('operacoes', this)" id="btn-cockpit-operacoes" class="btn-cockpit-chip px-3.5 py-2 rounded-xl text-xs font-semibold bg-slate-950 hover:bg-slate-800 text-slate-300 border border-slate-800 transition whitespace-nowrap cursor-pointer">
            ⚙️ 3. Operações & Fiscal (10)
          </button>
          <button onclick="filtrarCockpit('midia', this)" id="btn-cockpit-midia" class="btn-cockpit-chip px-3.5 py-2 rounded-xl text-xs font-semibold bg-slate-950 hover:bg-slate-800 text-slate-300 border border-slate-800 transition whitespace-nowrap cursor-pointer">
            📣 4. Mídia & Tráfego (10)
          </button>
        </div>

        <!-- Campo de Busca em Tempo Real e Contador -->
        <div class="flex items-center gap-3 w-full lg:w-auto">
          <div class="relative flex-1 lg:w-72">
            <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500 text-xs">🔍</span>
            <input type="text" id="busca-cockpit" oninput="filtrarCockpitBusca()" placeholder="Buscar ferramenta, objetivo ou tag..." class="w-full pl-9 pr-3 py-2 bg-slate-950 border border-slate-700/80 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 transition" />
          </div>
          <div class="text-[11px] font-bold text-slate-400 bg-slate-950 border border-slate-800 px-3 py-2 rounded-xl shrink-0">
            <span id="cockpit-contador" class="text-emerald-400">36</span> visíveis
          </div>
        </div>

      </div>

      <!-- CONTAINER PRINCIPAL DOS 4 PILARES DO COCKPIT -->
      <div id="container-pilares-cockpit" class="space-y-8">

        <!-- ========================================================= -->
        <!-- PILAR 1: MOTORES DE ULTRA-CONVERSÃO & BALCÃO (6 FERRAMENTAS) -->
        <!-- ========================================================= -->
        <div class="cockpit-pilar-bloco space-y-4" data-pilar="conversao">
          <div class="flex items-center justify-between border-b border-emerald-500/20 pb-3">
            <div class="flex items-center gap-2.5">
              <div class="h-8 w-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-base border border-emerald-500/30">
                🎯
              </div>
              <div>
                <h3 class="text-base font-bold text-white font-display">Pilar 1 — Motores de Ultra-Conversão & Balcão Comercial</h3>
                <p class="text-[11px] text-slate-400">Ferramentas de combate comercial para diagnóstico rápido, quebra de objeções e fechamento no mesmo dia</p>
              </div>
            </div>
            <span class="text-[10px] font-extrabold uppercase tracking-wider bg-emerald-500/10 text-emerald-400 px-2.5 py-1 rounded-full border border-emerald-500/20">6 Motores Ativos</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            
            <!-- Card 1: Checkup Loja -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-emerald-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="checkup auditoria frente caixa pdv sangria laudo a4 perdas sarandi">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    📋
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-emerald-500/15 text-emerald-300 px-2 py-0.5 rounded border border-emerald-500/30">Laudo Técnico A4</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-emerald-300 transition">Check-up de Frente de Caixa (15 Minutos)</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Auditoria prática de 10 perguntas objetivas com cálculo de prejuízo anual em reais e geração instantânea de laudo executivo A4 para o dono da loja.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Perdas Anuais</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Impressão PDF</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Gargalos PDV</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">checkup_loja.html</span>
                <a href="checkup_loja.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-emerald-950">
                  <span>Abrir Check-up</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 2: Fechador de Bolso -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-sky-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="fechamento rapido bolso mobile fast close parcelamento pix sicredi assinatura touch balcao contrato">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-sky-500/10 border border-sky-500/30 text-sky-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    ⚡
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-sky-500/15 text-sky-300 px-2 py-0.5 rounded border border-sky-500/30">Mobile Fast-Close</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-sky-300 transition">Fechador de Bolso (Fast-Close Mobile)</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Interface touch de alta velocidade para celular: simulador de parcelamento em até 12x, chave Pix Sicredi Hansen e assinatura do contrato direto na tela.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Pix Sicredi</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Assinatura Touch</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">WhatsApp 1-Click</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">fechamento_rapido.html</span>
                <a href="fechamento_rapido.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-sky-600 hover:bg-sky-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-sky-950">
                  <span>Abrir Fechador</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 3: Prova Social RS -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-amber-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="prova social regional mural confianca depoimentos audios whatsapp sarandi passo fundo marau carazinho clientes">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🌟
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-amber-500/15 text-amber-300 px-2 py-0.5 rounded border border-amber-500/30">Áudios Reais RS</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-amber-300 transition">Mural de Confiança Regional RS (Prova Social)</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Depoimentos reais de lojistas vizinhos em áudio com waveform interativo, métricas de crescimento e mapa de clientes ativos em Sarandi, Passo Fundo e Marau.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Player de Áudio</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Métricas Auditadas</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Filtro por Cidade</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">prova_social_regional.html</span>
                <a href="prova_social_regional.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-amber-950">
                  <span>Ver Depoimentos</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 4: Garantia Blindada -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-teal-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="garantia blindada risco zero 30 dias sla 2h suporte presencial reversa certificado impressao">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-teal-500/10 border border-teal-500/30 text-teal-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🛡️
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-teal-500/15 text-teal-300 px-2 py-0.5 rounded border border-teal-500/30">Risco Zero 30D</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-teal-300 transition">Certificado de Garantia Blindada & SLA 2h</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Eliminador de risco para o cliente: 30 dias de teste incondicional com devolução total, migração reversa gratuita e compromisso formal de atendimento presencial em até 2 horas.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">100% Reembolsável</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">SLA 2h In-Loco</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Certificado Impresso</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">garantia_blindada.html</span>
                <a href="garantia_blindada.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-teal-950">
                  <span>Ver Certificado</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 5: Máquina de Indicação -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-emerald-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="indicacao lojista amigo bonus pix 250 desconto mensalidade member get viral">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🤝
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-emerald-500/15 text-emerald-300 px-2 py-0.5 rounded border border-emerald-500/30">Bônus R$ 250 Pix</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-emerald-300 transition">Máquina de Indicação (Lojista Amigo)</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Sistema de indicação entre comerciantes: R$ 250 de crédito Pix na fatura para quem indica e 50% de desconto no setup de implantação para o lojista indicado.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Pix Automático</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Mensagens WhatsApp</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">50% Off Setup</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">programa_indicacao.html</span>
                <a href="programa_indicacao.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-emerald-950">
                  <span>Abrir Programa</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 6: Oráculo de Objeções 2.0 -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-rose-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="oraculo objecoes modo batalha respostas caras internet cai ja tenho sistema migracao concorrentes voz">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    ⚔️
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-rose-500/15 text-rose-300 px-2 py-0.5 rounded border border-rose-500/30">Modo Batalha</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-rose-300 transition">Oráculo de Objeções 2.0 (Modo Batalha)</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Respostas matadoras para as maiores resistências do lojista gaúcho: "Tá caro", "Já tenho sistema", "Minha internet oscila" e "Tenho medo de parar a loja".
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">12 Scripts de Choque</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Áudio Speech</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Role-Play Comercial</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">objecoes.html</span>
                <a href="objecoes.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-rose-600 hover:bg-rose-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-rose-950">
                  <span>Entrar em Batalha</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

          </div>
        </div>

        <!-- ========================================================= -->
        <!-- PILAR 2: PROSPECÇÃO B2B, VENDAS & EXPANSÃO RS (10 FERRAMENTAS) -->
        <!-- ========================================================= -->
        <div class="cockpit-pilar-bloco space-y-4" data-pilar="b2b">
          <div class="flex items-center justify-between border-b border-sky-500/20 pb-3">
            <div class="flex items-center gap-2.5">
              <div class="h-8 w-8 rounded-lg bg-sky-500/20 text-sky-400 flex items-center justify-center font-bold text-base border border-sky-500/30">
                🛰️
              </div>
              <div>
                <h3 class="text-base font-bold text-white font-display">Pilar 2 — Vendas B2B, Prospecção Ativa & Expansão Regional RS</h3>
                <p class="text-[11px] text-slate-400">Inteligência de mercado hiperlocal, radar geográfico, propostas comerciais e cadências de primeiro contato</p>
              </div>
            </div>
            <span class="text-[10px] font-extrabold uppercase tracking-wider bg-sky-500/10 text-sky-400 px-2.5 py-1 rounded-full border border-sky-500/20">10 Ferramentas</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            
            <!-- Card 7: Radar B2B -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-sky-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="radar b2b 600 clientes rfb sintegra cnae qsa passo fundo sarandi mapa street view">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-sky-500/10 border border-sky-500/30 text-sky-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🗺️
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-sky-500/15 text-sky-300 px-2 py-0.5 rounded border border-sky-500/30">600 Empresas RS</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-sky-300 transition">Radar B2B Regional (600 Clientes)</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Mapeamento em raio de 100km de Sarandi com CNPJs ativos, sócios no QSA, CNAE detalhado, rota no Google Maps e visualização do comércio via Street View.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Sintegra RS</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Raio 100km</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Street View</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">radar_clientes.html</span>
                <a href="radar_clientes.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-sky-600 hover:bg-sky-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-sky-950">
                  <span>Abrir Radar</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 8: Proposta Online -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-emerald-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="proposta online url rastreavel aceite 1 clique whatsapp parcelamento simulador">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    ⚡
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-emerald-500/15 text-emerald-300 px-2 py-0.5 rounded border border-emerald-500/30">Aceite em 1 Clique</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-emerald-300 transition">Proposta Online Interativa (Link Único)</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Página web personalizada para envio pelo WhatsApp com simulador dinâmico de investimento, termos claros de SLA e botão de aceite instantâneo.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Link Rastreável</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Sem Burocracia</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Responsivo</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">proposta_online.html</span>
                <a href="proposta_online.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-emerald-950">
                  <span>Abrir Proposta</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 9: Gerador de Proposta One-Pager -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-indigo-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="gerador proposta one pager a4 pdf impressao orcamento personalizado modulos">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    📄
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-indigo-500/15 text-indigo-300 px-2 py-0.5 rounded border border-indigo-500/30">One-Pager A4</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-indigo-300 transition">Gerador de Propostas B2B One-Pager</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Gerador profissional de proposta comercial executiva em 1 folha A4 com composição modular de valores, cálculo de payback e exportação para PDF.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Layout A4</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Exportar PDF</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Personalizado</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">gerador_proposta.html</span>
                <a href="gerador_proposta.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-indigo-950">
                  <span>Gerar Proposta</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 10: Migração Concorrentes -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-violet-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="migracao concorrentes linx hiper bling totvs zero dia parado importacao cadastro xml">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-violet-500/10 border border-violet-500/30 text-violet-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🚀
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-violet-500/15 text-violet-300 px-2 py-0.5 rounded border border-violet-500/30">Zero Dia Parado</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-violet-300 transition">Migração Blindada de Concorrentes</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Roteiro de substituição rápida dos principais sistemas do mercado (Linx, Hiper, Bling, Totvs) importando cadastros por XML sem interromper as vendas.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Sem Travar Caixa</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Importador XML</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Histórico Seguro</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">migracao_concorrentes.html</span>
                <a href="migracao_concorrentes.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-violet-600 hover:bg-violet-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-violet-950">
                  <span>Ver Migração</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 11: Cadência SDR WhatsApp -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-emerald-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="cadencia sdr whatsapp mensagens roteiros primeiro contato lojistas supermercados contabilidade">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    📲
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-emerald-500/15 text-emerald-300 px-2 py-0.5 rounded border border-emerald-500/30">Scripts Validados</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-emerald-300 transition">Cadência SDR WhatsApp Regional</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Sequências testadas de mensagens com abordagem regional gaúcha, ganchos de dor fiscal, envio de áudios e convite para café presencial em 15 minutos.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">D-0 a D-7</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">1-Click Copiar</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Tom Humano</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">cadencia_sdr.html</span>
                <a href="cadencia_sdr.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-[#25D366] hover:bg-[#20ba59] text-slate-950 text-xs font-black rounded-lg transition shadow-md shadow-emerald-950">
                  <span>Abrir Cadência</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 12: Copiloto de Vendas IA -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-purple-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="copiloto vendas ia simulador pitch role play negociacao respostas ao vivo sarandi">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-purple-500/10 border border-purple-500/30 text-purple-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🧠
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-purple-500/15 text-purple-300 px-2 py-0.5 rounded border border-purple-500/30">IA Assistente</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-purple-300 transition">Copiloto Comercial IA & Role-Play</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Assistente para treino prático de vendas com pontuação de persuasão, gerador de mensagens por perfil de cliente e quebra contextual de objeções.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Simulador de Pitch</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Score de Venda</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Respostas Rápidas</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">copiloto_vendas.html</span>
                <a href="copiloto_vendas.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-purple-950">
                  <span>Abrir Copiloto</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 13: CRM Pipeline -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-indigo-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="crm pipeline kanban leads mrr financeiro propostas visitas cadencia">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    💼
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-indigo-500/15 text-indigo-300 px-2 py-0.5 rounded border border-indigo-500/30">Pipeline Ativo</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-indigo-300 transition">CRM Pipeline Kanban & Finanças</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Kanban completo do funil de prospecção da região: novos leads, contatos agendados, demonstrações realizadas, fechamentos e cálculo de MRR potencial.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Funil 5 Etapas</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">MRR Acumulado</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Exportar CSV</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">crm.html</span>
                <a href="crm.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-indigo-950">
                  <span>Abrir CRM</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 14: TCO & ROI -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-cyan-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="tco roi calculadora comparador custos linx hiper totvs bling payback economia 36 meses">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    💰
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-cyan-500/15 text-cyan-300 px-2 py-0.5 rounded border border-cyan-500/30">Payback em Meses</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-cyan-300 transition">Calculadora Executiva de TCO & ROI</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Comparador financeiro em horizonte de 36 meses contra Linx, Hiper e Totvs com cálculo de payback e laudo executivo A4 comprovando a economia real.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Economia 36M</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Laudo Financeiro</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Sem Pegadinhas</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">tco_roi.html</span>
                <a href="tco_roi.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-cyan-950">
                  <span>Calcular TCO</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 15: Simulador Simples -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-amber-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="simulador simples nacional faturamento pequeno comerciante mensalidade investimento calculo">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🧮
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-amber-500/15 text-amber-300 px-2 py-0.5 rounded border border-amber-500/30">Micro & Pequenos</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-amber-300 transition">Simulador de Faturamento Simples Nacional</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Cálculo transparente de custo x benefício para comércios locais enquadrados no Simples Nacional, eliminando o receio de custos fixos elevados.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Simples Nacional</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Clareza de Preço</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Zero Surpresas</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">simulador_simples.html</span>
                <a href="simulador_simples.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-amber-950">
                  <span>Abrir Simulador</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 16: Pitch Deck Executivo -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-blue-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="pitch deck apresentacao comercial slides reunioes projetor fullscreen vendas">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-blue-500/10 border border-blue-500/30 text-blue-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🎯
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-blue-500/15 text-blue-300 px-2 py-0.5 rounded border border-blue-500/30">Fullscreen Slides</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-blue-300 transition">Pitch Deck Comercial Executivo</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Apresentação interativa em 8 lâminas com timer integrado, projetada para reuniões presenciais, demonstrações em projetor e televendas executivas.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">8 Lâminas</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Timer Dinâmico</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Modo Reunião</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">pitch.html</span>
                <a href="pitch.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-blue-950">
                  <span>Abrir Slides</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

          </div>
        </div>

        <!-- ========================================================= -->
        <!-- PILAR 3: OPERAÇÕES, FISCAL & HARDWARE (10 FERRAMENTAS) -->
        <!-- ========================================================= -->
        <div class="cockpit-pilar-bloco space-y-4" data-pilar="operacoes">
          <div class="flex items-center justify-between border-b border-indigo-500/20 pb-3">
            <div class="flex items-center gap-2.5">
              <div class="h-8 w-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold text-base border border-indigo-500/30">
                ⚙️
              </div>
              <div>
                <h3 class="text-base font-bold text-white font-display">Pilar 3 — Operações, Fiscal & Hardware Especializado</h3>
                <p class="text-[11px] text-slate-400">Kits de PDV homologados, contingência offline, conformidade fiscal e integração com contadores</p>
              </div>
            </div>
            <span class="text-[10px] font-extrabold uppercase tracking-wider bg-indigo-500/10 text-indigo-400 px-2.5 py-1 rounded-full border border-indigo-500/20">10 Ferramentas</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            
            <!-- Card 17: Orçamentador Hardware -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-slate-700 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="hardware orcamentador kits pdv impressora epson elgin leitor gaveta balanca">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-slate-800 border border-slate-700 text-slate-200 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🖥️
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-slate-800 text-slate-300 px-2 py-0.5 rounded border border-slate-700">Kits Homologados</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-brand-azure transition">Orçamentador de Hardware & Kits PDV</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Montador de kits completos de frente de caixa: terminais touch, leitores barcode 2D/QR Code, gavetas automáticas e impressoras EPSON/Elgin.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">EPSON / Elgin</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Dimensionador</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Orçamento Rápido</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">hardware.html</span>
                <a href="hardware.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-bold rounded-lg transition">
                  <span>Montar Kit</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 18: Simulador Contingência Offline -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-amber-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="contingencia offline internet caiu nfce sefaz sincronizacao pdv nao para banco local">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🔌
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-amber-500/15 text-amber-300 px-2 py-0.5 rounded border border-amber-500/30">Offline Real</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-amber-300 transition">Simulador de Contingência Offline</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Demonstração visual para provar ao lojista que o caixa continua emitindo NFC-e e vendendo normalmente mesmo quando o provedor de internet do interior cai.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Emissão Offline</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Sync Automático</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Fila Fiscal</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">simulador_contingencia.html</span>
                <a href="simulador_contingencia.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-amber-950">
                  <span>Simular Offline</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 19: Supermercados & Toledo -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-cyan-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="supermercados toledo balancas acougue hortifruti etiquetas checkout pesagem">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🛒
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-cyan-500/15 text-cyan-300 px-2 py-0.5 rounded border border-cyan-500/30">Balanças Toledo</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-cyan-300 transition">Módulo Supermercados & Balanças Toledo</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Homologação de balanças de checkout e etiquetas de açougue/hortifruti (Toledo Prix, Filizola) com carga rápida de preços e pesagem automática.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Toledo Prix 4/5/6</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Checkout Veloz</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Etiquetas Código</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">mercados.html</span>
                <a href="mercados.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-cyan-700 hover:bg-cyan-600 text-white text-xs font-bold rounded-lg transition shadow-md shadow-cyan-950">
                  <span>Ver Módulo</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 20: Reforma Tributária -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-rose-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="reforma tributaria cbs ibs 2026 impostos simulador sefaz contabilidade simples icms">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    ⚖️
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-rose-500/15 text-rose-300 px-2 py-0.5 rounded border border-rose-500/30">Transição 2026</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-rose-300 transition">Guia Reforma Tributária CBS/IBS 2026</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Matriz de impacto das novas regras fiscais no comércio gaúcho, simulador de alíquotas e garantia de que o ERP já nasce adaptado às novas obrigações.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">CBS / IBS</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Auditoria Fiscal</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Pronto p/ 2026</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">reforma-tributaria.html</span>
                <a href="reforma-tributaria.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-rose-700 hover:bg-rose-600 text-white text-xs font-bold rounded-lg transition shadow-md shadow-rose-950">
                  <span>Abrir Guia</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 21: Dossiê Contador -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-teal-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="dossie contador sped fiscal sefaz rs escritorios contabeis parceria xml lote">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-teal-500/10 border border-teal-500/30 text-teal-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🏛️
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-teal-500/15 text-teal-300 px-2 py-0.5 rounded border border-teal-500/30">Pacto Contábil</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-teal-300 transition">Dossiê Técnico para Contadores (SPED)</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Documentação formal de conformidade com o SPED Fiscal e SEFAZ-RS para apresentar a escritórios contábeis e transformar o contador em parceiro promotor.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">SPED Sem Erro</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">XMLs em Lote</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Zero Retrabalho</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">dossie_contador.html</span>
                <a href="dossie_contador.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-teal-700 hover:bg-teal-600 text-white text-xs font-bold rounded-lg transition shadow-md shadow-teal-950">
                  <span>Abrir Dossiê</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 22: Auditor XML Fiscal -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-amber-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="auditor xml fiscal sefaz nfe nfce rejeicoes icms monofasico upload validador">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🔍
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-amber-500/15 text-amber-300 px-2 py-0.5 rounded border border-amber-500/30">Validador XML</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-amber-300 transition">Auditor e Validador de XML Fiscal</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Ferramenta para upload e diagnóstico de arquivos XML: identifica bitributação em produtos monofásicos, erros de CFOP e riscos de rejeição na SEFAZ.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Upload Drag&Drop</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Bitributação</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Laudo Executivo</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">auditor_xml.html</span>
                <a href="auditor_xml.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-amber-950">
                  <span>Auditar XML</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 23: Status SEFAZ-RS -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-emerald-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="status sefaz rs tempo real servidores autorizacao nfe nfce contingencia disponibilidade">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    📡
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-emerald-500/15 text-emerald-300 px-2 py-0.5 rounded border border-emerald-500/30">Live SEFAZ</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-emerald-300 transition">Monitor Status SEFAZ-RS em Tempo Real</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Painel de monitoramento da disponibilidade dos servidores estaduais do Rio Grande do Sul (NFC-e e NF-e) com alerta de instabilidades e contingência.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Servidores RS</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Alerta de Queda</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Status Verde</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">status_sefaz.html</span>
                <a href="status_sefaz.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-emerald-950">
                  <span>Ver Servidores</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 24: Checklist Implantação 48h -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-teal-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="checklist implantacao 48h virada campo tecnicos instalacao homologacao assinatura a4">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-teal-500/10 border border-teal-500/30 text-teal-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🛠️
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-teal-500/15 text-teal-300 px-2 py-0.5 rounded border border-teal-500/30">Roteiro de Campo</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-teal-300 transition">Checklist de Implantação 48h & Termo A4</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Roteiro operacional passo a passo para o técnico de campo: do backup do banco antigo à homologação da primeira venda com assinatura na tela.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">48h sem Atrito</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Termo Assinado</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Qualidade 100%</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">checklist_implantacao.html</span>
                <a href="checklist_implantacao.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-teal-950">
                  <span>Abrir Checklist</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 25: Perdas no Caixa -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-rose-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="perdas caixa calculadora sangria erros digitacao pesagem dinheiro vazamentos">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    💸
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-rose-500/15 text-rose-300 px-2 py-0.5 rounded border border-rose-500/30">Stop Loss</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-rose-300 transition">Calculadora de Prejuízos por Erro de Caixa</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Demonstrativo financeiro para mostrar ao lojista quanto dinheiro escorre pelo ralo por erros manuais de digitação e falta de fechamento cego no caixa.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Fechamento Cego</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Prevenção Perdas</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Cálculo em R$</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">perdas_caixa.html</span>
                <a href="perdas_caixa.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-rose-700 hover:bg-rose-600 text-white text-xs font-bold rounded-lg transition shadow-md shadow-rose-950">
                  <span>Calcular Perdas</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 26: Calculadora TEF -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-emerald-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="calculadora tef integrado pos maquininhas conciliacao taxas economia cartao">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    💳
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-emerald-500/15 text-emerald-300 px-2 py-0.5 rounded border border-emerald-500/30">Conciliação 100%</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-emerald-300 transition">Auditor de Cartões & TEF Integrado</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Simulador de economia eliminando o aluguel de várias maquininhas POS e evitando fraudes de digitação através do TEF integrado direto ao PDV.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">TEF Homologado</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Fim de Fraudes</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Sem Erro Digitação</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">calculadora_tef.html</span>
                <a href="calculadora_tef.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-emerald-950">
                  <span>Auditar Cartões</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

          </div>
        </div>

        <!-- ========================================================= -->
        <!-- PILAR 4: MÍDIA, CRIATIVOS & PRESENÇA REGIONAL (10 FERRAMENTAS) -->
        <!-- ========================================================= -->
        <div class="cockpit-pilar-bloco space-y-4" data-pilar="midia">
          <div class="flex items-center justify-between border-b border-pink-500/20 pb-3">
            <div class="flex items-center gap-2.5">
              <div class="h-8 w-8 rounded-lg bg-pink-500/20 text-pink-400 flex items-center justify-center font-bold text-base border border-pink-500/30">
                📣
              </div>
              <div>
                <h3 class="text-base font-bold text-white font-display">Pilar 4 — Mídia, Campanhas & Presença Regional</h3>
                <p class="text-[11px] text-slate-400">Criativos para redes sociais, roteiros de Reels/TikTok, campanhas de Meta Ads no RS e figurinhas WhatsApp</p>
              </div>
            </div>
            <span class="text-[10px] font-extrabold uppercase tracking-wider bg-pink-500/10 text-pink-400 px-2.5 py-1 rounded-full border border-pink-500/20">10 Ferramentas</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            
            <!-- Card 27: Estúdio Stories 9:16 -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-pink-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="stories 9 16 52 cards instagram status whatsapp celular download zip png hd svg">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-pink-500/10 border border-pink-500/30 text-pink-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    📱
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-pink-500/15 text-pink-300 px-2 py-0.5 rounded border border-pink-500/30">52 Cards HD</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-pink-300 transition">Estúdio de Stories 9:16 (52 Cards PNG/SVG)</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Simulador de smartphone com 52 lâminas verticais prontas no padrão visual mestre com download em lote (.ZIP em PNG HD e SVG vetorizado).
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">1080x1920</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Download ZIP</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Stories & Status</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">stories.html</span>
                <a href="stories.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-pink-600 hover:bg-pink-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-pink-950">
                  <span>Abrir Stories</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 28: Carrosséis Feed Instagram -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-purple-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="carrosseis feed instagram 4 5 laminas educativas autoridade postagens carrossel">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-purple-500/10 border border-purple-500/30 text-purple-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    📚
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-purple-500/15 text-purple-300 px-2 py-0.5 rounded border border-purple-500/30">Formato 4:5 Feed</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-purple-300 transition">Carrosséis para Feed do Instagram (4:5)</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  5 carrosséis completos de 1080x1350 com navegação lâmina a lâmina, focados em autoridade técnica, redução de impostos e diferenciais frente à concorrência.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">1080x1350</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Alta Retenção</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Autoridade B2B</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">carrosseis_feed.html</span>
                <a href="carrosseis_feed.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-purple-950">
                  <span>Ver Carrosséis</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 29: Roteiros Vídeos Reels -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-red-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="roteiros reels tiktok videos gravacao equipe sarandi aida gancho teleprompter">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🎬
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-red-500/15 text-red-300 px-2 py-0.5 rounded border border-red-500/30">20 Scripts Vídeo</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-red-300 transition">20 Roteiros para Vídeos & Reels (AIDA)</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Roteiros estruturados de 30 a 50 segundos com ganchos de 3s para a equipe de Sarandi gravar em lojas parceiras e alimentar as redes com conteúdo autêntico.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Gancho 3 Segundos</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Fórmula AIDA</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Lojas Reais</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">roteiros_reels.html</span>
                <a href="roteiros_reels.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-red-600 hover:bg-red-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-red-950">
                  <span>Abrir Roteiros</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 30: Spots de Rádio -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-amber-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="spots radio locucao audio podcast sarandi interior carros som metronomo">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🎙️
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-amber-500/15 text-amber-300 px-2 py-0.5 rounded border border-amber-500/30">Áudio & Rádio</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-amber-300 transition">Estúdio de Spots de Rádio & Mensagens Vocais</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Scripts e metrônomo de locução (30s e 45s) com marcações de ênfase para veiculação em emissoras de rádio do Norte Gaúcho e carros de som locais.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Metrônomo 30s/45s</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Rádios do Norte RS</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Locução Comercial</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">spots_radio.html</span>
                <a href="spots_radio.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-amber-950">
                  <span>Abrir Estúdio</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 31: Teleprompter Digital -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-teal-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="teleprompter gravacao celular rolagem texto velocidade scripts reels suporte">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-teal-500/10 border border-teal-500/30 text-teal-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🎬
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-teal-500/15 text-teal-300 px-2 py-0.5 rounded border border-teal-500/30">Gravação Fluida</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-teal-300 transition">Teleprompter Digital de Bolso</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Prompter profissional com ajuste suave de rolagem, tamanho de fonte e carregamento dos roteiros de Reels para gravar vídeos perfeitos de primeira.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Rolagem Suave</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Controle WPM</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Mobile Friendly</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">teleprompter.html</span>
                <a href="teleprompter.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-teal-600 hover:bg-teal-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-teal-950">
                  <span>Usar Prompter</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 32: Estúdio B-Rolls -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-sky-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="estudio brolls claquete takes enquadramento 9 16 gravacao cortes dinamicos">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-sky-500/10 border border-sky-500/30 text-sky-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🎥
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-sky-500/15 text-sky-300 px-2 py-0.5 rounded border border-sky-500/30">Claquete Digital</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-sky-300 transition">Estúdio de B-Rolls & Reels (Claquete)</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Contagem regressiva sonora de takes com guias de enquadramento 9:16 e catálogo dos 5 takes essenciais de loja física para edições dinâmicas.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">5 Takes Essenciais</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Beep Sonoro</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Cortes Rápidos</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">estudio_brolls.html</span>
                <a href="estudio_brolls.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-sky-600 hover:bg-sky-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-sky-950">
                  <span>Abrir Claquete</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 33: Central Meta Ads RS -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-indigo-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="campanhas ads meta google facebook instagram publicos anuncios copys sarandi rs">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    🎯
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-indigo-500/15 text-indigo-300 px-2 py-0.5 rounded border border-indigo-500/30">Meta & Google</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-indigo-300 transition">Central de Tráfego Pago & Anúncios B2B RS</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Conjunto pronto de anúncios segmentados por nicho (mercados, farmácias, moda) com copies persuasivas, criativos e simulador de retorno em leads.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Segmentação RS</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Copies por Nicho</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Simulador Leads</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">campanhas_ads.html</span>
                <a href="campanhas_ads.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-indigo-950">
                  <span>Ver Anúncios</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 34: Gerador Tráfego Hiperlocal -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-emerald-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="gerador trafego hiperlocal raio 30km 100km sarandi utms orcamento leads">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    📍
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-emerald-500/15 text-emerald-300 px-2 py-0.5 rounded border border-emerald-500/30">Raio 30km / 100km</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-emerald-300 transition">Gerador de Tráfego Hiperlocal RS</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Configurador de campanhas geolocalizadas em raio de 30km e 100km de Sarandi com parâmetros UTM de rastreamento e projeção de custo por aquisição.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Geolocalização</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Links com UTM</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Custo por Lead</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">campanhas_trafego.html</span>
                <a href="campanhas_trafego.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-emerald-950">
                  <span>Gerar Tráfego</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 35: Calendário Editorial -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-amber-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="calendario editorial 2026 datas comemorativas fiscais postagens agendamento">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    📅
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-amber-500/15 text-amber-300 px-2 py-0.5 rounded border border-amber-500/30">108 Pautas RS</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-amber-300 transition">Calendário Editorial 2026 (108 Datas)</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Planejamento estratégico de 108 datas comemorativas regionais gaúchas, prazos fiscais da SEFAZ-RS e campanhas comerciais sincronizadas para o ano todo.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Semana Farroupilha</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Prazos Fiscais</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Visão Anual</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">calendario.html</span>
                <a href="calendario.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-amber-950">
                  <span>Abrir Calendário</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Card 36: Pack de Figurinhas WhatsApp -->
            <div class="cockpit-card bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800/90 hover:border-emerald-500/40 rounded-2xl p-5 shadow-lg transition duration-200 flex flex-col justify-between group" data-tags="figurinhas whatsapp stickers conversao suporte atendimento humano amigavel">
              <div>
                <div class="flex items-start justify-between gap-3 mb-3">
                  <div class="h-10 w-10 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center justify-center text-xl shrink-0 group-hover:scale-110 transition">
                    💬
                  </div>
                  <span class="text-[10px] font-extrabold uppercase tracking-wider bg-emerald-500/15 text-emerald-300 px-2 py-0.5 rounded border border-emerald-500/30">Stickers WhatsApp</span>
                </div>
                <h4 class="text-sm font-bold text-white group-hover:text-emerald-300 transition">Pack de Figurinhas WhatsApp TruData</h4>
                <p class="text-xs text-slate-400 mt-1.5 leading-relaxed">
                  Pacote de stickers com frases e ganchos gaúchos de aproximação comercial para quebrar o gelo e humanizar o atendimento ao cliente no WhatsApp.
                </p>
                <div class="flex items-center gap-1.5 mt-3 flex-wrap">
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Stickers Prontos</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Atendimento Humanizado</span>
                  <span class="text-[10px] bg-slate-950 text-slate-400 px-2 py-0.5 rounded border border-slate-800">Quebra de Gelo</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <span class="text-[11px] text-slate-500 font-medium">figurinhas.html</span>
                <a href="figurinhas.html" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-lg transition shadow-md shadow-emerald-950">
                  <span>Ver Stickers</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

          </div>
        </div>

      </div>
"""

# Alvo de inserção: Inserir COCKPIT_HTML logo após `<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">`
# e envolver o Hub B2B e o Banner Fiscal dentro do secao-cockpit, fechando </section> antes do secao-galeria.

# 1. Localizar o início de <main
main_target = '<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">'
if main_target not in html:
    raise ValueError("Tag <main> alvo não encontrada!")

# 2. Localizar o início de <section id="secao-galeria"
galeria_target = '<section id="secao-galeria"'
if galeria_target not in html:
    raise ValueError("Tag <section id=\"secao-galeria\" não encontrada!")

partes_antes_galeria, partes_depois_galeria = html.split(galeria_target, 1)

# Na parte antes da galeria, substituímos a abertura de main para incluir o cockpit
split_main = partes_antes_galeria.split(main_target, 1)
cabecalho_html = split_main[0] + main_target + "\n\n" + COCKPIT_HTML + "\n\n"
corpo_b2b_e_fiscal = split_main[1]

# Fechar </section> do cockpit antes de iniciar secao-galeria
# E certificar que secao-galeria tenha class="hidden mb-12"
galeria_atualizada = '<section id="secao-galeria" class="hidden mb-12"' + partes_depois_galeria[partes_depois_galeria.find('>'):]

novo_html = cabecalho_html + corpo_b2b_e_fiscal.rstrip() + "\n    </section>\n\n    " + galeria_atualizada

# 3. Atualizar alternarAba e funções do Cockpit no JS
# Vamos procurar a função alternarAba
js_antigo = """    function alternarAba(aba) {
      const secaoGaleria = document.getElementById('secao-galeria');
      const secaoPosts = document.getElementById('secao-posts');
      const secaoAuditoria = document.getElementById('secao-auditoria');
      const secaoStories = document.getElementById('secao-stories');
      const btnGaleria = document.getElementById('btn-aba-galeria');
      const btnPosts = document.getElementById('btn-aba-posts');
      const btnAuditoria = document.getElementById('btn-aba-auditoria');
      const btnStories = document.getElementById('btn-aba-stories');

      // Reset botões

      secaoGaleria.classList.add('hidden');
      secaoPosts.classList.add('hidden');
      secaoAuditoria.classList.add('hidden');

      if (aba === 'galeria') {
        secaoGaleria.classList.remove('hidden');
        btnGaleria.className = "inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-bold rounded-lg bg-indigo-600 text-white shadow-lg shadow-indigo-600/20 transition";
      } else if (aba === 'posts') {
        secaoPosts.classList.remove('hidden');
        btnPosts.className = "inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-bold rounded-lg bg-brand-azure text-white shadow-lg shadow-brand-azure/20 transition";
      } else if (aba === 'auditoria') {
        secaoAuditoria.classList.remove('hidden');
        btnAuditoria.className = "inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-bold rounded-lg bg-brand-azure text-white shadow-lg shadow-brand-azure/20 transition";
      }
    }"""

js_novo = """    // --- CONTROLE DE ABAS PRINCIPAIS DO PAINEL TRUDATA ---
    function alternarAba(aba) {
      const secaoCockpit = document.getElementById('secao-cockpit');
      const secaoGaleria = document.getElementById('secao-galeria');
      const secaoPosts = document.getElementById('secao-posts');
      const secaoAuditoria = document.getElementById('secao-auditoria');
      const secaoStories = document.getElementById('secao-stories');

      const btnCockpit = document.getElementById('btn-aba-cockpit');
      const btnGaleria = document.getElementById('btn-aba-galeria');
      const btnPosts = document.getElementById('btn-aba-posts');
      const btnStories = document.getElementById('btn-aba-stories');
      const btnAuditoria = document.getElementById('btn-aba-auditoria');

      // Ocultar todas as seções
      if (secaoCockpit) secaoCockpit.classList.add('hidden');
      if (secaoGaleria) secaoGaleria.classList.add('hidden');
      if (secaoPosts) secaoPosts.classList.add('hidden');
      if (secaoAuditoria) secaoAuditoria.classList.add('hidden');
      if (secaoStories) secaoStories.classList.add('hidden');

      // Estilo neutro inativo para os botões do cabeçalho
      const estiloInativo = "px-4 py-2 rounded-xl text-xs font-semibold bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 transition flex items-center gap-2 whitespace-nowrap cursor-pointer";
      if (btnCockpit) btnCockpit.className = estiloInativo;
      if (btnGaleria) btnGaleria.className = estiloInativo;
      if (btnPosts) btnPosts.className = estiloInativo;
      if (btnStories) btnStories.className = estiloInativo;
      if (btnAuditoria) btnAuditoria.className = estiloInativo;

      // Ativar a seção e o botão correspondente
      if (aba === 'cockpit' && secaoCockpit) {
        secaoCockpit.classList.remove('hidden');
        if (btnCockpit) btnCockpit.className = "px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 shadow-lg shadow-emerald-500/20 whitespace-nowrap cursor-pointer";
      } else if (aba === 'galeria' && secaoGaleria) {
        secaoGaleria.classList.remove('hidden');
        if (btnGaleria) btnGaleria.className = "px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-gradient-to-r from-teal-500 to-cyan-500 text-slate-950 shadow-lg shadow-teal-500/20 whitespace-nowrap cursor-pointer";
      } else if (aba === 'posts' && secaoPosts) {
        secaoPosts.classList.remove('hidden');
        if (btnPosts) btnPosts.className = "px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-lg shadow-blue-500/20 whitespace-nowrap cursor-pointer";
      } else if (aba === 'stories' && secaoStories) {
        secaoStories.classList.remove('hidden');
        if (btnStories) btnStories.className = "px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-gradient-to-r from-pink-500 to-rose-500 text-white shadow-lg shadow-pink-500/20 whitespace-nowrap cursor-pointer";
      } else if (aba === 'auditoria' && secaoAuditoria) {
        secaoAuditoria.classList.remove('hidden');
        if (btnAuditoria) btnAuditoria.className = "px-4 py-2 rounded-xl text-xs font-bold transition flex items-center gap-2 bg-gradient-to-r from-amber-500 to-orange-500 text-slate-950 shadow-lg shadow-amber-500/20 whitespace-nowrap cursor-pointer";
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // --- FILTRAGEM & BUSCA INSTANTÂNEA DO COCKPIT ---
    let categoriaCockpitAtual = 'todos';

    function filtrarCockpit(categoria, botaoElemento) {
      categoriaCockpitAtual = categoria;
      
      // Atualizar estilo visual dos chips
      const chips = document.querySelectorAll('.btn-cockpit-chip');
      chips.forEach(chip => {
        chip.className = 'btn-cockpit-chip px-3.5 py-2 rounded-xl text-xs font-semibold bg-slate-950 hover:bg-slate-800 text-slate-300 border border-slate-800 transition whitespace-nowrap cursor-pointer';
      });
      if (botaoElemento) {
        botaoElemento.className = 'btn-cockpit-chip px-3.5 py-2 rounded-xl text-xs font-bold transition bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20 whitespace-nowrap cursor-pointer';
      }

      aplicarFiltrosCockpit();
    }

    function filtrarCockpitBusca() {
      aplicarFiltrosCockpit();
    }

    function aplicarFiltrosCockpit() {
      const termo = (document.getElementById('busca-cockpit')?.value || '').toLowerCase().trim();
      const blocos = document.querySelectorAll('.cockpit-pilar-bloco');
      const cards = document.querySelectorAll('.cockpit-card');
      let totalVisiveis = 0;

      cards.forEach(card => {
        const pilar = card.closest('.cockpit-pilar-bloco')?.getAttribute('data-pilar');
        const tags = (card.getAttribute('data-tags') || '').toLowerCase();
        const texto = card.innerText.toLowerCase();

        const matchCat = categoriaCockpitAtual === 'todos' || pilar === categoriaCockpitAtual;
        const matchTermo = !termo || tags.includes(termo) || texto.includes(termo);

        if (matchCat && matchTermo) {
          card.classList.remove('hidden');
          totalVisiveis++;
        } else {
          card.classList.add('hidden');
        }
      });

      // Ocultar blocos de pilar inteiros se nenhum card estiver visível nele
      blocos.forEach(bloco => {
        const pilar = bloco.getAttribute('data-pilar');
        const cardsNoBloco = bloco.querySelectorAll('.cockpit-card:not(.hidden)');
        const matchCat = categoriaCockpitAtual === 'todos' || pilar === categoriaCockpitAtual;

        if (matchCat && cardsNoBloco.length > 0) {
          bloco.classList.remove('hidden');
        } else {
          bloco.classList.add('hidden');
        }
      });

      // Atualizar o contador no painel
      const contador = document.getElementById('cockpit-contador');
      if (contador) contador.textContent = totalVisiveis;
    }"""

if js_antigo not in novo_html:
    raise ValueError("Bloco js_antigo não encontrado para substituição!")

novo_html = novo_html.replace(js_antigo, js_novo)

# 4. Atualizar init() para iniciar na aba 'cockpit'
init_antigo = """    async function init() {
      posts = POSTS_INICIAIS;
      carregarPostsLocalStorage();
      await carregarStatusBackend();
      atualizarStats();
      renderizarPosts();
      await carregarStoriesCards();
    }"""

init_novo = """    async function init() {
      posts = POSTS_INICIAIS;
      carregarPostsLocalStorage();
      await carregarStatusBackend();
      atualizarStats();
      renderizarPosts();
      await carregarStoriesCards();
      alternarAba('cockpit');
    }"""

if init_antigo not in novo_html:
    raise ValueError("Bloco init_antigo não encontrado para substituição!")

novo_html = novo_html.replace(init_antigo, init_novo)

# Salvar o novo arquivo UTF-8 limpo
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(novo_html)

print("OK: Cockpit Executivo injetado com sucesso em painel_aprovacao/ferramentas.html!")
