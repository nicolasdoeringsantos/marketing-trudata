# 🚀 Marketing TruData — Gestão de Imagem, Redes Sociais e Agente IA V2.0

Bem-vindo ao projeto central de Marketing e Gestão de Imagem da **TruData** (desenvolvido pela **Hansen Software LTDA**).

Este repositório reúne toda a inteligência de marca, estratégia de redes sociais, acervo de postagens prontas, campanhas de vendas e ferramentas de IA para posicionar o **Trudata ERP** com máxima autoridade no mercado.

---

## 🏢 Sobre a TruData (Hansen Software)

- **Sede**: Sarandi — RS
- **História**: Mais de 25 anos de solidez e inovação contínua.
- **Autoridade**: +300 clientes no Brasil, +4.000.000 de NFC-e emitidas, 98% de índice de satisfação no suporte.
- **Soluções**: Trudata ERP (Desktop e Nuvem) e Trudata Easy (Emissão Fiscal Web).
- **Proposta de Valor Inegociável**: **Suporte humano e consultivo de verdade**, domínio fiscal regional/nacional e facilidade operacional para o comércio e serviços.

---

## 🌐 Interfaces Web Interativas (Acesso Local)

O projeto conta com duas aplicações web completas rodando localmente na porta 8080:

1. **📅 Calendário Editorial Visual 2026**:
   - URL: [http://localhost:8080/calendario.html](http://localhost:8080/calendario.html)
   - 108 dias de planejamento diário (Setembro a Dezembro de 2026).
   - 324 telas de Stories às 08:00 com simulador de enquetes.
   - 17 pautas de Feed/Reels com roteiros cena a cena e legendas prontas.
   - Recursos: Simulador de Feed 3x3 do Instagram, Exportação CSV/Excel, Exportação Notion/Markdown, Disparo Direto para WhatsApp e download do pacote do dia em `.txt`.

2. **🖼️ Painel de Aprovação & Gestão de Posts**:
   - URL: [http://localhost:8080/index.html](http://localhost:8080/index.html)
   - Galeria oficial de cards publicitários gerados em alta resolução.
   - Fila de aprovação de posts com persistência em LocalStorage (`Aprovado`, `Pendente`, `Publicado`).
   - Diagnóstico estratégico completo das redes sociais da empresa (@trudata_ e Facebook).

---

## 📂 Estrutura Completa do Projeto

```text
marketing_trudata/
├── README.md                                  # Este guia central
├── brand/
│   ├── manual_marca_posicionamento.md         # Diretrizes de tom de voz, cores e mensagens
│   └── personas_clientes.md                   # Perfil dos clientes ideais (varejo, farmácia, etc.)
├── estrategia/
│   ├── banco_ganchos_reels.md                 # 🎯 50 Ganchos de alta retenção categorizados
│   ├── roteiros_reels_prontos.md              # 🎬 10 Roteiros prontos cena a cena
│   ├── dicionario_fiscal_varejo.md            # 📚 Dicionário fiscal descomplicado para lojistas
│   ├── manual_respostas_crise.md              # 🛡️ Manual de SAC, respostas rápidas e gestão de crise
│   ├── cadencia_whatsapp_contadores.md        # 💬 Cadência de 3 toques para prospecção de escritórios
│   ├── checklist_pre_publicacao.md            # ✅ Checklist obrigatório de 8 pontos pré-postagem
│   ├── diagnostico_redes_sociais.md           # 📊 Auditoria do Instagram (@trudata_) e Facebook
│   ├── calendario_comemorativo_e_feriados.md  # 📅 Calendário de feriados e datas comemorativas
│   ├── pilares_de_conteudo.md                 # 5 pilares estratégicos de postagem
│   └── funil_de_vendas_conteudo.md            # Jornada de compra do cliente ERP
├── campanhas/
│   ├── parceria_contadores_locais.md          # 💼 Campanha "Modo Escritório" para contadores
│   ├── reforma_tributaria.md                  # Campanha de conformidade fiscal (IBS/CBS)
│   ├── black_friday_varejo.md                 # Preparação de PDV e estoque para o varejo
│   └── suporte_humanizado.md                  # Posicionamento contra robôs do mercado
├── conteudo_pronto/
│   ├── card_tela_real_anonimizada.jpg         # Card oficial baseado na interface real do ERP
│   ├── card_devolucao_xml.jpg                 # Card de devolução fiscal por XML
│   ├── card_honorarios.jpg                    # Card de honorários e cobrança automática
│   ├── card_suporte_humano.jpg                # Card institucional de suporte humano
│   └── card_reforma_tributaria.jpg            # Card de autoridade sobre a Reforma Tributária
├── painel_aprovacao/
│   ├── index.html                             # Painel web de aprovação de posts e galeria
│   ├── calendario.html                        # Calendário editorial visual de 108 dias
│   ├── calendario_dados.js / .json            # Base de dados estruturada do calendário
│   └── servidor_painel.py                     # Servidor HTTP local (porta 8080)
└── agente/
    ├── prompt_sistema_agente.md               # Prompt mestre V2.0 do Agente com 50 melhorias
    ├── gerador_conteudo.py                    # CLI V2.0 (Frameworks AIDA/PAS/BAB, Prompts IA, etc.)
    ├── avaliador_qualidade.py                 # Auditor automático de qualidade editorial (0-100)
    └── sincronizar_marketing.py               # Auditoria de sincronização do ecossistema
```

---

## 🤖 Ferramentas CLI do Agente TruData

Execute diretamente no terminal dentro da pasta do projeto:

```bash
# Gerar post no framework PAS para o segmento de Moda:
python agente/gerador_conteudo.py --framework PAS --segmento 2

# Ver os top ganchos magnéticos para Reels:
python agente/gerador_conteudo.py --ganchos

# Gerar cadência de 3 mensagens para WhatsApp de contadores:
python agente/gerador_conteudo.py --formato whatsapp

# Gerar prompt para criar imagens fotográficas em ferramentas de IA (Flux/Midjourney):
python agente/gerador_conteudo.py --formato ia-prompt --segmento 1

# Avaliar a qualidade de um post (Nota 0 a 100):
python agente/avaliador_qualidade.py

# Auditar a sincronização de todos os arquivos e banco de dados:
python agente/sincronizar_marketing.py
```
