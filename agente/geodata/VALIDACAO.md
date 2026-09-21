# Resultado atualizado — Geoapify

Foram consultados os 661 cadastros pendentes. A validação de componentes aceitou 179 endereços de prédio; somados aos 2 estabelecimentos revisados anteriormente, são 181 localizações na base de 663 registros. Os 482 restantes continuam pendentes. No raio padrão de 100 km, o radar retorna 172 pontos localizados em uma seleção de 633 cadastros.

Critério: confiança mínima de 0,95 no endereço, cidade, rua e prédio; país, UF, município, rua e número compatíveis; sem CEP específico divergente, posições ambíguas ou conflito de filial conhecido. Os novos pontos localizam o endereço cadastrado, sem confirmar ocupação pela empresa, funcionamento atual ou entrada.

Motivos das 482 pendências: 202 por confiança insuficiente, 156 sem número identificável, 80 por resposta sem prédio, 11 com CEP divergente, 11 com rua divergente, 11 com município divergente, 7 não encontrados e 4 com conflito conhecido. Os resultados completos e a justificativa por cadastro estão em `relatorio-geoapify.json`; a resposta da API está em `geoapify-candidatos.json`.

A base foi atualizada com cópia anterior e teste de preservação dos dados comerciais. Nove testes passaram (cinco da validação geográfica e quatro do painel). A revisão é reproduzível com `python agente/geodata/validar_geoapify.py`; para aplicar, use `--aplicar`.

## Registro da primeira revisão, antes da consulta Geoapify

# Validação de localização — 21/09/2026

Base: 663 estabelecimentos. Cruzamento com 7.188 objetos públicos do OpenStreetMap em consulta pontual Overpass, armazenada em `osm-regional.json`. Os 47 candidatos por similaridade NÃO são resultados validados.

Foram aceitas duas correspondências de nome e endereço:

- L.P. Minerais do Brasil: Avenida Bento Gonçalves, 1900, Ametista do Sul. Nome, rua e número coincidem no [ponto OSM](https://www.openstreetmap.org/node/7969535885). Posição do estabelecimento, sem levantamento da entrada.
- Rhriss Combustíveis: BR-386, km 178, Carazinho. [Área OSM](https://www.openstreetmap.org/way/548424422), com nome, rodovia e referência 178. Endereço também consta na [relação da SEFAZ-RS](https://nfg.sefaz.rs.gov.br/arquivos/relacao_emitentes_nfe.pdf) para o CNPJ da base. Essa relação é antiga e apenas corrobora o endereço, sem confirmar funcionamento atual. Coordenada corresponde ao centro da área do posto, não à entrada.

661 localizações permanecem pendentes, inclusive nomes encontrados sem número/filial conclusivos. Não foi validada a exatidão de todas as coordenadas, o funcionamento atual, contatos ou situação cadastral. Há divergências de endereço e estabelecimentos identificados como antigos.

O mapa exclui coordenadas pendentes; a lista conserva os cadastros e identifica suas distâncias como estimativas. O filtro de raio e a ordenação ainda usam as coordenadas antigas desses cadastros: não devem ser interpretados como cobertura geográfica validada. As coordenadas corrigidas são usadas pelo cálculo de distância do servidor.

`base-antes-validacao.json` preserva a base original. `aplicar_validacao.py` registra apenas as duas correspondências revisadas; não executa busca automática nem consulta pública recorrente. Cada cadastro recebe status, data de consulta e observação; localizados também recebem URL da fonte e precisão. Nenhuma chave de serviço de geocodificação foi disponibilizada nesta tarefa.
