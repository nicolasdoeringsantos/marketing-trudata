// Service Worker — TruData ERP Cockpit (Modo Estrada Offline-First)
const CACHE_NAME = 'trudata-cockpit-v2026-r3';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/checkup_loja.html',
  '/fechamento_rapido.html',
  '/prova_social_regional.html',
  '/garantia_blindada.html',
  '/programa_indicacao.html',
  '/objecoes.html',
  '/crm.html',
  '/tco_roi.html',
  '/dossie_portabilidade.html',
  '/proposta_rastreavel.html',
  '/gps_campo.html',
  '/gerador_reels.html',
  '/simulador_tributario_2026.html',
  // 20 Novas Ferramentas (Expansão 65)
  '/cadencia_omnichannel.html',
  '/calculadora_ruptura.html',
  '/simulador_tef_multibandeira.html',
  '/script_coldcall.html',
  '/painel_telemetria_propostas.html',
  '/auditor_sped_efd.html',
  '/simulador_cesta_basica_rs.html',
  '/emulador_cupom_termica.html',
  '/homologador_balancas.html',
  '/calculadora_difal_st.html',
  '/gerador_carrosseis_916.html',
  '/spots_radio_trilha.html',
  '/vitrine_comercios_rs.html',
  '/simulador_print_whatsapp.html',
  '/showroom_virtual.html',
  '/portal_contador_xml.html',
  '/pesquisa_nps_ativa.html',
  '/termometro_churn.html',
  '/payback_hardware.html',
  '/conector_bi_openapi.html',
  '/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Service Worker] Pré-carregando ferramentas críticas do Cockpit...');
      return cache.addAll(ASSETS_TO_CACHE).catch(err => {
        console.warn('[Service Worker] Falha ao pré-carregar alguns ativos:', err);
      });
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(
        keyList.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[Service Worker] Removendo cache antigo:', key);
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const requestUrl = new URL(event.request.url);

  // Não interceptar requisições para outros domínios ou websockets
  if (requestUrl.origin !== location.origin) {
    return;
  }

  // APIs: Network First com fallback gracioso
  if (requestUrl.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request)
        .catch(() => {
          return new Response(
            JSON.stringify({ 
              offline: true, 
              sucesso: false, 
              mensagem: 'Modo Estrada Ativo (Sem conexão no momento. Seus dados foram salvos na fila local para sincronização).' 
            }),
            { headers: { 'Content-Type': 'application/json' } }
          );
        })
    );
    return;
  }

  // Páginas e Ativos Estáticos: Cache First com Network Fallback
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        // Retorna do cache e atualiza o cache em segundo plano (Stale-While-Revalidate)
        fetch(event.request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, networkResponse));
          }
        }).catch(() => {});
        return cachedResponse;
      }

      return fetch(event.request).then((networkResponse) => {
        if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
          return networkResponse;
        }

        const responseToCache = networkResponse.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseToCache);
        });

        return networkResponse;
      }).catch(() => {
        // Fallback offline se a página não estiver no cache
        if (event.request.mode === 'navigate') {
          return caches.match('/index.html');
        }
      });
    })
  );
});
