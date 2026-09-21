# Rotina comercial integrada

Cinco ferramentas acessíveis pela central:

- `revisao_enderecos.html`: lista os cadastros pendentes, permite editar os componentes e consultar a Geoapify. Só aplica resultados de prédio com correspondência suficiente, após a confirmação da empresa/filial. Mantém cópia da base anterior e rejeita consultas expiradas ou cadastros alterados durante a revisão.
- `planejar_visitas.html`: agenda até oito empresas localizadas com ordem e horários, salva no servidor, abre trajetos em grupos de até quatro paradas e registra visitas realizadas. O trajeto respeita a ordem escolhida, sem prometer otimização ou tempo de deslocamento.
- `proximos_contatos.html`: usa a lista atual do CRM; organiza retornos atrasados, de hoje, futuros e sem data. Guarda próxima ação, última conversa e histórico compartilhado.
- `gerador_proposta.html`: preenche a empresa pelo radar, permite serviços mensais ou únicos, edição de rascunhos, impressão/PDF, texto e registro de apresentação, aceite ou recusa. Não envia propostas ou registra pagamentos automaticamente.
- `resultado_prospeccao.html`: conta atividades registradas nas novas ferramentas por período e mostra separadamente a distribuição atual do CRM. Não inventa histórico a partir das etapas atuais.

Os registros de agenda, acompanhamento e propostas ficam em `comercial_registros.json`, criado no primeiro salvamento real. Não ficam apenas no navegador. A origem dos clientes é `base_clientes_regional.json`; a dos contatos é `leads_crm.json`. Os eventos das ferramentas são mantidos separadamente dos campos antigos do CRM; não reclassificam automaticamente a fase do lead. A chave Geoapify continua fora da pasta publicada.

API: `/api/comercial/dados` e operações específicas de POST em `/api/comercial/`. Validação no servidor, gravação atômica e exclusão mútua entre operações destas ferramentas. As APIs antigas de escrita do CRM continuam com o comportamento anterior.

Verificação: 14 testes automatizados aprovados, incluindo validação geográfica e integridade da central. Os cinco fluxos foram exercitados no navegador com dados isolados, incluindo consulta/aplicação simulada, contato, visita, proposta, aceite e contadores. Dados fictícios não foram inseridos na base real. Capturas foram inspecionadas para corrigir formulário e rolagem horizontal. A versão anterior da proposta foi preservada em `qa/gerador_proposta-antes-integracao.html`.
