# Ativar geolocalização

A integração de consulta está preparada, mas precisa de uma conta e chave Geoapify. Não é executada ao carregar o radar e não cria despesas recorrentes automaticamente.

1. Crie sua conta em https://myprojects.geoapify.com/ e escolha o plano gratuito.
2. Crie um projeto e copie a API key. Para este uso no servidor, não use uma restrição de HTTP referrer de navegador. Se restringir por IP, use o IP público da conexão que fará as consultas.
3. No terminal, na pasta do projeto, execute:

```powershell
python agente/configurar_geolocalizacao.py configurar
```

Cole a chave quando solicitada. A entrada fica oculta e a chave é gravada em `%LOCALAPPDATA%\TruData\geolocalizacao.json`, fora da pasta publicada. Não cole a chave no chat, HTML, JavaScript ou repositório. Alternativamente, o processo pode receber `GEOAPIFY_API_KEY` do ambiente.

Para verificar presença da configuração sem mostrar a chave:

```powershell
python agente/configurar_geolocalizacao.py status
```

Para testar acesso real com um endereço:

```powershell
python agente/configurar_geolocalizacao.py consultar --limite 1
```

Depois, pode-se consultar os pendentes em lote:

```powershell
python agente/configurar_geolocalizacao.py consultar --limite 663
```

Somente endereço, cidade, UF e CEP são enviados à Geoapify. Resultados ficam em `geoapify-candidatos.json`, com cache por endereço e salvamento após cada consulta. A execução para em falhas ou limite de cota, sem perder os resultados já salvos. Reexecutar não repete endereços concluídos. Não execute dois lotes simultaneamente.

Antes de publicar coordenadas, conferir município, rua, número, tipo do resultado, confiança e eventuais filiais ou mudanças de endereço. Geocodificação de prédio não comprova empresa em funcionamento nem entrada exata. Pontos de rua, bairro, CEP ou cidade não são localizações exatas. O mapa continua mostrando apenas os pontos já revisados. Resultados publicados da Geoapify devem incluir atribuição do serviço e das fontes retornadas.

Referências: [documentação](https://apidocs.geoapify.com/docs/geocoding/), [plano e limites](https://www.geoapify.com/pricing/). Em 21/09/2026, o plano gratuito anuncia 3.000 créditos/dia; uma consulta simples de geocodificação usa um crédito. Confira os termos ao criar a conta.
