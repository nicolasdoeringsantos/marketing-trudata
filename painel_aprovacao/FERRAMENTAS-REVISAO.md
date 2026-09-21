# Revisão da central de ferramentas

68 destinos únicos no catálogo anterior; 14 entradas na nova central.

## Critério

Manter operações reais. Reunir tarefas equivalentes. Retirar confirmações simuladas, métricas sem fonte e condições comerciais ou fiscais sem validação documentada. Nenhum registro de cliente ou arquivo de negócio foi alterado.

## Ferramentas reformuladas

- `checkup_loja.html`: Diagnóstico da loja.
- `tco_roi.html`: Comparar custos.
- `gerador_proposta.html`: Preparar proposta.
- `cadencia_sdr.html`: Preparar uma conversa.
- `checklist_implantacao.html`: Planejar implantação.
- `auditor_xml.html`: Ler arquivo XML.
- `teleprompter.html`: Teleprompter.
- `demo_pdv.html`: Demonstração de caixa.

## Decisão para cada destino anterior

| Página | Decisão | Alternativa |
|---|---|---|
| cadencia_omnichannel.html | Reunida em Preparar uma conversa | cadencia_sdr.html |
| copiloto_audio.html | Reunida em Preparar uma conversa | cadencia_sdr.html |
| copiloto_vendas.html | Reunida em Preparar uma conversa | cadencia_sdr.html |
| objecoes.html | Reunida em Preparar uma conversa | cadencia_sdr.html |
| script_coldcall.html | Reunida em Preparar uma conversa | cadencia_sdr.html |
| disparador_whatsapp.html | Reunida em Preparar uma conversa | cadencia_sdr.html |
| calculadora_troca.html | Reunida em Comparar custos | tco_roi.html |
| calculadora_ruptura.html | Reunida em Comparar custos | tco_roi.html |
| calculadora_tef.html | Reunida em Comparar custos | tco_roi.html |
| simulador_tef_multibandeira.html | Reunida em Comparar custos | tco_roi.html |
| payback_hardware.html | Reunida em Comparar custos | tco_roi.html |
| perdas_caixa.html | Reunida em Comparar custos | tco_roi.html |
| dossie_portabilidade.html | Reunida em Comparar custos | tco_roi.html |
| dossie_contador.html | Reunida em Comparar custos | tco_roi.html |
| hardware.html | Reunida em Comparar custos | tco_roi.html |
| proposta_online.html | Reunida em Preparar proposta | gerador_proposta.html |
| proposta_rastreavel.html | Reunida em Preparar proposta | gerador_proposta.html |
| fechamento_rapido.html | Reunida em Preparar proposta | gerador_proposta.html |
| migracao_concorrentes.html | Reunida em Planejar implantação | checklist_implantacao.html |
| mercados.html | Reunida em Planejar implantação | checklist_implantacao.html |
| gps_campo.html | Reunida no Radar de clientes | radar_clientes.html |
| contadores.html | Reunida no Radar de contadores | radar_clientes.html?modo=contadores |
| simulador_contingencia.html | Reunida na Demonstração de caixa | demo_pdv.html |
| emulador_cupom_termica.html | Reunida na Demonstração de caixa | demo_pdv.html |
| showroom_virtual.html | Reunida na Demonstração de caixa | demo_pdv.html |
| painel_telemetria_propostas.html | Retirada: integração não implementada | crm.html |
| pesquisa_nps_ativa.html | Retirada: integração não implementada | crm.html |
| termometro_churn.html | Retirada: integração não implementada | crm.html |
| produtividade_comissoes.html | Retirada: integração não implementada | crm.html |
| conector_bi_openapi.html | Retirada: integração não implementada | crm.html |
| auditor_sped_efd.html | Retirada: validação não implementada | auditor_xml.html |
| portal_contador_xml.html | Retirada: validação não implementada | auditor_xml.html |
| calculadora_difal_st.html | Retirada: requer validação fiscal | checklist_implantacao.html |
| simulador_simples.html | Retirada: requer validação fiscal | checklist_implantacao.html |
| reforma-tributaria.html | Retirada: requer validação fiscal | checklist_implantacao.html |
| simulador_tributario_2026.html | Retirada: requer validação fiscal | checklist_implantacao.html |
| simulador_cesta_basica_rs.html | Retirada: requer validação fiscal | checklist_implantacao.html |
| status_sefaz.html | Retirada: status não consultado | ferramentas.html |
| homologador_balancas.html | Retirada: equipamento não conectado | checklist_implantacao.html |
| contrato_digital.html | Retirada: condições sem validação | gerador_proposta.html |
| garantia_blindada.html | Retirada: condições sem validação | gerador_proposta.html |
| programa_indicacao.html | Retirada: condições sem validação | gerador_proposta.html |
| prova_social_regional.html | Retirada: prova social sem comprovação | index.html |
| simulador_print_whatsapp.html | Retirada: prova social sem comprovação | index.html |
| stories.html | Material preservado na biblioteca | biblioteca.html |
| carrosseis_feed.html | Material preservado na biblioteca | biblioteca.html |
| roteiros_reels.html | Material preservado na biblioteca | biblioteca.html |
| spots_radio.html | Material preservado na biblioteca | biblioteca.html |
| estudio_brolls.html | Material preservado na biblioteca | biblioteca.html |
| campanhas_ads.html | Material preservado na biblioteca | biblioteca.html |
| campanhas_trafego.html | Material preservado na biblioteca | biblioteca.html |
| figurinhas.html | Material preservado na biblioteca | biblioteca.html |
| gerador_reels.html | Material preservado na biblioteca | biblioteca.html |
| gerador_carrosseis_916.html | Material preservado na biblioteca | biblioteca.html |
| spots_radio_trilha.html | Material preservado na biblioteca | biblioteca.html |
| vitrine_comercios_rs.html | Material preservado na biblioteca | biblioteca.html |
| pitch.html | Material preservado na biblioteca | biblioteca.html |

Radar, CRM e calendário mantidos. Aprovação integrada por link.

## Evidências da revisão

- SPED: `executarAuditoria` mostrava 1.428 documentos aprovados, sem ler arquivo.
- Portal XML: os botões de download apenas executavam `alert`.
- Balanças: o peso vinha de `Math.random`, sem comunicação com dispositivo.
- Retenção e NPS: os alertas confirmavam agendamento e ações remotas inexistentes.
- Telemetria: os registros vinham de `DADOS_MOCK`.
- Contrato: `gerarHashSimulado` e confirmação de pagamento simulada.
- Calculadoras: economia limitada por `Math.max`, recuperação presumida de 90% e perda fixa de 0,4%.
- Proposta: economia anual fixa, sem relação com valores fornecidos pelo cliente.

## Recuperação de referências

Os HTMLs anteriores estão preservados em `qa/ferramentas-fontes-antes.zip`. Conteúdo criativo não foi apagado do arquivo de referência. A nova central não o apresenta como pronto para publicação.

## Validação

Os resumos e rascunhos da oficina são locais. Nenhuma ferramenta nova envia mensagens, processa pagamentos ou modifica o CRM. Valores de propostas são preenchidos pelo usuário; não há preços ou garantias predefinidos.

## Direção visual

Tokens compartilhados: marca #009FE3, ação #075985, texto #0F172A,
secundário #475569, fundo #F1F5F9 e superfície #FFFFFF. Família Inter.
A faixa de próximos passos concentra o destaque; o catálogo usa linhas e
hierarquia tipográfica, com busca e categorias. Formulários e resumos ficam
lado a lado no desktop e empilhados no tablet.

## Verificação concluída

- Quatro testes de regressão em `python -m unittest test_painel -v`.
- 71 endereços HTTP verificados, sem falhas.
- Catálogo inspecionado em 768, 1366 e 1920 px, sem rolagem horizontal.
- Busca por acento/categoria, resultado vazio e limpeza dos filtros.
- Comparação de custos: aumento e redução reais, zero válido, valores em centavos.
- Proposta: total de R$ 750 para R$ 250 mensais + R$ 500 de implantação.
- Alterar entradas invalida o resumo; exportação fica desativada até atualizar.
- Rascunho salvo e recuperado no navegador; preenchimento obrigatório validado.
- XML com namespace lido; arquivo incompleto rejeitado com orientação.
- Checklist de 9 conferências e diagnóstico geram resumos consistentes.
- Demo de caixa bloqueia carrinho vazio e mostra conclusão explicitamente simulada.
- Teleprompter rola, pausa e retorna ao início; movimento começa por ação do usuário.
- Biblioteca pesquisada e aberta com textos editáveis; original completo preservado.
- Sintaxe de JavaScript conferida; interação no navegador interno do Codex.

Capturas: `qa/ferramentas-antes.png`, `qa/ferramentas-depois-1366.png`,
`qa/ferramentas-tablet-768.png`, `qa/ferramentas-monitor-1920.png` e
`qa/ferramentas-proposta-tablet.png`.

A oficina não tem integração de envio ou escrita no CRM. O botão Imprimir / PDF
usa a impressão do navegador. Biblioteca preserva textos para referência;
layouts e fontes originais completos estão no ZIP. A revisão não homologa regras
fiscais, equipamentos, garantias, descontos ou depoimentos.
