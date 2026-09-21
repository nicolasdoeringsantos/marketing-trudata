# Radar de clientes — extensão do design system

## Direção definida antes da implementação

Conceito: território à esquerda, empresas no centro e mapa como apoio para a próxima conversa comercial.

```text
TruData     Aprovação · Calendário · Radar · Ferramentas
O próximo cliente está por perto.          CSV · CRM
Empresas     Fora do CRM     Cidades     Contatos
┌ Território ┐ ┌ Mapa regional ────────┬ Cidades ┐
│ Origem    │ └───────────────────────┴─────────┘
│ Raio      │ Empresas para conhecer      Busca
│ Cidade    │ Todas · Fora do CRM · No CRM · 50 prioridades
│ Segmento  │ Seleção · Telefones · Rota · Adicionar ao CRM
│ + filtros │ Empresa / contato / etapa / abrir ficha
└───────────┘
```

Tokens compartilhados: marca `#009FE3`, ação `#075985`, texto `#0F172A`,
texto secundário `#475569`, fundo `#F1F5F9`, superfície `#FFFFFF`.
Inter em 400/500/600/700; escala e espaçamento de `design-system.css`.
Estados semânticos reutilizam os tokens existentes.

O mapa é o elemento de maior presença. Contadores, divisórias e linhas de
empresas ficam discretos. A personalidade vem do território regional e da
hierarquia tipográfica, sem radar animado, porcentagem inventada de conversão
ou decoração de painel genérico.

## Implementação

- `radar_clientes.html`: estrutura, filtros, mapa e diálogo acessível.
- `radar.css`: composição responsiva do radar sobre os componentes compartilhados.
- `radar.js`: seleção consistente entre lista, cards, mapa, CSV e ações em lote.
- `radar-dados.js`: opções geográficas e modelos de abordagem preservados.
- Aprovação e calendário agora têm acesso direto ao radar na navegação.
- Assets versionados para superar o cache de 24 horas do servidor local.

Fora do CRM significa que a empresa ainda não está na base comercial, sem
inferir data de criação ou histórico de contato. Etapas existentes, inclusive
`contato`, `demo` e `proposta`, são preservadas. Importação só confirma sucesso
após a resposta da API. O modo de e-mail assistido confirma preparação; SMTP
confirma envio apenas quando a resposta do servidor o informa.

As informações cadastrais continuam vindo da base existente. Coordenadas são
agrupadas por cidade, sem deslocamento aleatório; pontos próximos são agrupados
no mapa. A prioridade é um indicador cadastral, não previsão de venda.

O fundo do mapa usa a camada padrão do OpenStreetMap, com atribuição visível,
conforme https://operations.osmfoundation.org/policies/tiles/ . O mapa depende
de rede; falhas mostram aviso e mantêm a lista de empresas utilizável.

## Verificação em 21/09/2026

- Capturas e inspeção em 768, 1366 e 1920 pixels; sem overflow horizontal.
- Ficha de empresa no tablet; Tab/Shift+Tab contidos no diálogo e Esc fecha.
- Lista/cards, filtros, busca sem resultados e CSV das 50 prioridades.
- Base simulada isolada: importação individual e de duas empresas, etapa
  legada preservada e alterada, rota saindo da origem selecionada.
- Configuração preserva senha quando o campo está vazio.
- E-mail assistido e SMTP têm mensagens distintas, ambos testados com simulação.
- Falha de API desativa exportação; a ação Buscar novamente recupera a lista.
- Nenhuma escrita foi encaminhada ao CRM real nem houve envio de e-mail.
- Inspeção inicial em Chrome e final no navegador interno do Codex. A conexão
  CUA com Chrome não estava disponível para repetir a bateria final nele.

Servidor reproduzível para QA: `python painel_aprovacao/qa/radar_fixture_server.py`.
Ele funciona somente em localhost:8877 e mantém dados de teste em memória.
Capturas em `qa/radar-antes.png`, `qa/radar-depois-1366.png`,
`qa/radar-tablet-768.png`, `qa/radar-ficha-tablet.png` e `qa/radar-desktop-1920.png`.
