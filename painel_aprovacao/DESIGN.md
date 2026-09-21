# TruData — mesa editorial

## Leitura do produto

O manual de marca define Azure `#009FE3`, ciano `#169FDB`, navy
`#0F172A`/`#302D7F`, gelo e branco. Os cards existentes reforçam azul e
tipografia sem serifa. O tom é próximo, consultivo e respeita o tempo do
comerciante. As personas incluem varejo, moda, serviços e contabilidade.

As duas telas anteriores repetiam configurações Tailwind, estilos, modais,
toasts e filtros. Fundos escuros diferentes, gradientes, emojis e numerosas
ações competiam pela atenção. O calendário já possuía grade, mas seus
filtros de conteúdo só afetavam a lista. A página inicial também abrigava
um portal comercial com 68 ferramentas; esse portal está preservado em
`ferramentas.html`, acessível pela navegação das duas telas.

## Direção definida antes da implementação

Uma mesa editorial clara: a arte protagoniza a revisão e a grade mensal
organiza a produção, com controles silenciosos ao redor.

```text
TruData     Aprovação · Calendário · Ferramentas
──────────────────────────────────────────────
Aprovação de conteúdo       Pendentes / Aprovados / Publicados
Status                     Canal · Busca
[ arte ]  [ arte ]  [ arte ]     Diagnóstico
[ações]   [ações]   [ações]      dos canais

Calendário editorial       Progresso do plano
Mês · Pilar · Segmento      Exportar · Prévia do feed
Dom     Seg     Ter     Qua     Qui     Sex     Sáb
[        grade mensal com pautas reais          ]
Detalhe: Stories + roteiro + legenda + ações
```

O plano foi revisto para evitar um dashboard genérico: estatísticas usam
divisórias em vez de cards; a lateral é um diagnóstico editorial; a grade
respeita a semana e o intervalo real do plano. Não há animação de entrada.

## Tokens e componentes

| Token base | Valor | Papel |
|---|---|---|
| Azure | `#009FE3` | Identidade e marcação do feed |
| Navy | `#0F172A` | Texto e Stories |
| Azul de ação | `#075985` | Botões com texto branco e links |
| Gelo | `#F1F5F9` | Fundo da área de trabalho |
| Branco | `#FFFFFF` | Superfícies e contraste |
| Cinza de texto | `#475569` | Metadados e legendas |

Estados adicionam verde `#166534`, amarelo `#854D0E` e vermelho `#991B1B`,
sempre acompanhados por texto e ícone. Valores ficam centralizados no CSS.
O azul oficial não recebe texto branco pequeno: a variante de ação alcança
contraste de 7,56:1. Os pares de texto medidos variam de 6,01:1 a 17,85:1;
o relatório está em `qa/contraste.json`.

Inter é a única família, com fallback Arial. Corpo 400/500, ações 600,
títulos 700 e marca 800. Escala: 12, 14, 16, 20 e 32 px, com token de 48 px
reservado. Espaçamentos: 4, 8, 12, 16, 24, 32 e 48 px. Prosa até 76ch.

Um pequeno conjunto SVG de traço uniforme atende às duas telas. Botões,
badges, campos, diálogo nativo, feedback e estados vazios compartilham
estilos e comportamento. A galeria usa borda discreta; o calendário usa
linhas contínuas. Sombras ficam restritas a sobreposições.

## Comportamento e compatibilidade

- As 22 publicações originais estão em `posts-dados.js`, com IDs, imagens,
  legendas e briefings preservados. Os 108 dias e 17 feeds continuam vindo
  de `calendario_dados.js`.
- Aprovar, marcar publicado, reprovar e reabrir revisão atualizam a fila e
  os contadores. Reprovar leva ao estado existente `ajuste`.
- As chaves `trudata_posts_marketing` e `trudata_status_dias` permanecem.
  Aprovações também usam `/api/status` quando o servidor está disponível;
  falhas de armazenamento e sincronização têm feedback explícito.
- CSV, CSV importável no Notion, Markdown e XLSX real usam o mês e os
  filtros selecionados. XLSX é OOXML/ZIP, sem dependência de CDN. O pacote
  TXT do dia inclui Stories, enquete e todos os campos do feed disponível.
- WhatsApp abre um rascunho para o usuário escolher o destinatário e
  confirmar o envio. O simulador de enquete não registra votos reais.
- Tab permanece no diálogo, Esc fecha e o foco retorna ao controle de
  origem. A preferência por movimento reduzido é respeitada.
- `atualizar_cockpit.py` agora atualiza `ferramentas.html`, preservando o
  estúdio editorial. O service worker usa a rede primeiro nessas telas,
  evitando servir uma versão antiga quando existe conexão.

## Pontos editoriais para validação

1. Diversas pautas já associavam a mesma arte a temas diferentes. Essas
   referências foram preservadas e sinalizadas na prévia/detalhes; o time
   deve revisar a associação antes de publicar.
2. O diagnóstico original não tinha métricas reais de seguidores ou
   alcance. O novo painel compara a fila por canal e declara a ausência
   dessas medições. Nenhuma métrica de audiência foi inventada.
3. As pautas não possuem metadados estruturados de pilar/segmento. Os
   filtros usam classificação por palavras-chave do conteúdo. O time pode
   validar essa classificação antes de torná-la metadado explícito.
4. O redesenho cobre aprovação e calendário. As páginas comerciais do
   portal preservado mantêm suas interfaces anteriores.

## Validação

`qa/verify_ui.py` testa Chrome e Edge, 768/1366/1920 px, ações da fila,
persistência, filtros, 108 dias, foco/teclado, enquetes, downloads, estrutura
XLSX e falha de armazenamento. Intercepta a API de status e o WhatsApp;
nenhum conteúdo é enviado. Resultado em `qa/validation.json`.

Screenshots anteriores e posteriores estão em `qa/`. Os comparativos
`comparativo-aprovacao.jpg` e `comparativo-calendario.jpg` mostram as telas
lado a lado. O snapshot `index-antes.png` registra o portal original na
entrada; `aprovacao-antes.png` registra sua aba de aprovação.

Execute o servidor existente e os testes:

```powershell
python painel_aprovacao/servidor_painel.py
python painel_aprovacao/qa/verify_ui.py
```

Os testes exigem o pacote Python `playwright` e Chrome/Edge instalados.
As telas não precisam de build nem de dependências JavaScript de terceiros.
