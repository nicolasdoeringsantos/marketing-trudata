#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de Disparo de Propostas Comerciais por E-mail (TruData ERP / Hansen Software)
- Gera e-mails em HTML Executivo com identidade visual oficial
- Conexão SMTP universal (TLS / SSL / Porta 587 / 465)
- Adaptação dos módulos especialistas para os 16 nichos de mercado
- Sincronização automática com o CRM Kanban e histórico de disparos
"""

import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
CONFIG_PATH = os.path.join(BASE_DIR, "config_email.json")
HISTORICO_PATH = os.path.join(PROJECT_ROOT, "painel_aprovacao", "historico_emails.json")
LEADS_CRM_PATH = os.path.join(PROJECT_ROOT, "painel_aprovacao", "leads_crm.json")

# Configuração padrão caso o arquivo não exista
CONFIG_PADRAO = {
    "ativo": True,
    "modo": "automatico", # 'smtp' para disparo real ou 'simulado' para ambiente de teste
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "usar_tls": True,
    "usuario": "",
    "senha": "",
    "remetente_nome": "TruData ERP (Hansen Software)",
    "remetente_email": "comercial@trudata.com.br",
    "telefone_contato": "(54) 3361-2650",
    "whatsapp_contato": "555433612650"
}

def carregar_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                return {**CONFIG_PADRAO, **cfg}
        except Exception:
            pass
    return CONFIG_PADRAO

def salvar_config(nova_config):
    cfg_atual = carregar_config()
    # Se a senha vier em branco, preserva a anterior
    if "senha" in nova_config and not nova_config["senha"].strip():
        nova_config["senha"] = cfg_atual.get("senha", "")
    cfg_atual.update(nova_config)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg_atual, f, indent=2, ensure_ascii=False)
    return cfg_atual

# Tabela de módulos especialistas por nicho
MODULOS_ESPECIALISTAS = {
    "supermercado": [
        ("Frente de Caixa Rápido (PDV)", "Emissão de NFC-e em 3 segundos com contingência offline para sábados de lotação."),
        ("Integração Balanças de Checkout", "Homologado para balanças Toledo e Filizola e etiquetas de carnes/frios."),
        ("Controle de Estoque & XML", "Entrada automática de notas dos fornecedores e inventário com leitor de código de barras."),
        ("TEF Multi-Adquirente Integrado", "Eliminação de maquininhas avulsas e taxas de cartão menores.")
    ],
    "padaria": [
        ("PDV com Comanda Eletrônica & Balcão", "Atendimento rápido no balcão e conferência no caixa sem perda de itens."),
        ("Ficha Técnica & Receituário", "Cálculo exato do custo de produção de pães, bolos, salgados e cucas artesanais."),
        ("Etiquetagem Nutricional", "Impressão de tabelas nutricionais e data de validade para gôndolas e padaria.")
    ],
    "pet": [
        ("Módulo Banho & Tosa com Agenda WhatsApp", "Agendamento integrado com lembrete automático de horário para os tutores."),
        ("Prontuário Veterinário & Vacinas", "Histórico clínico completo, controle de vermífugos e alertas de reforço."),
        ("Venda de Rações a Granel", "Controle fracionado de quilos no PDV sem divergência de estoque.")
    ],
    "celular": [
        ("Ordem de Serviço (OS) com Termo de Entrada", "Controle de peças, fotos do aparelho recebido e garantia de conserto."),
        ("Notificação de Aparelho Pronto", "Envio automático de mensagem quando o celular/computador fica pronto para retirada."),
        ("Controle de Grade de Capas & Películas", "Organização por marca, modelo e cor sem duplicar códigos.")
    ],
    "bazar": [
        ("PDV Ágil para Alto Fluxo", "Leitura veloz de código de barras para artigos escolares e presentes."),
        ("Tabela de Preços para Atacado e Varejo", "Preço diferenciado automaticamente por volume de compra."),
        ("Controle de Sazonalidade", "Relatórios para compras certeiras em Dia das Mães, Volta às Aulas e Natal.")
    ],
    "bebida": [
        ("Controle de Vasilhames & Empréstimos", "Rastreio de cascos de cerveja, botijões de gás P13/P45 e galões de água 20L."),
        ("Módulo Tele-Entrega & Rota", "Identificador de chamadas no WhatsApp, histórico de endereço e despacho rápido.")
    ],
    "otica": [
        ("Receituário Oftalmológico Digital", "Registro de dioptrias (esférico, cilíndrico, eixo e DNP) direto na venda."),
        ("Rastreio de Pedidos de Laboratório", "Acompanhamento do status de montagem da lente até a entrega ao cliente.")
    ],
    "oficina": [
        ("Ordem de Serviço Automotiva com Placa", "Histórico de revisões por placa, quilometragem, chassi e mecânico responsável."),
        ("Aplicação de Peças & Aplicação Cruzada", "Controle de peças de reposição com margem de lucro sugerida.")
    ],
    "construcao": [
        ("Emissão de MDF-e para Entregas", "Geração do Manifesto Eletrônico de Cargas para transporte de cimento e vigas."),
        ("Controle de Entregas Futuras", "Venda de materiais com entrega programada em lotes conforme o avanço da obra.")
    ],
    "moda": [
        ("Grade Matricial Cor x Tamanho", "Gestão do estoque por variações (36 ao 44, P/M/G) em uma única tela."),
        ("Crediário Próprio & Carnê com QR Code Pix", "Emissão de boletos/carnês da loja com régua de cobrança automática.")
    ],
    "farmacia": [
        ("Transmissão SNGPC Anvisa", "Envio automatizado de receitas de antibióticos e controlados sem rejeições."),
        ("Controle de Lotes & Validade", "Bloqueio preventivo no caixa para medicamentos próximos do vencimento.")
    ],
    "contabil": [
        ("Modo Escritório Multiempresa Gratuito", "Acesso 100% sem custo para o escritório navegar entre empresas clientes em 2 cliques sem deslogar da SEFAZ."),
        ("Devolução Fiscal Automática por XML", "Espelhamento instantâneo de impostos e tributos de compra e venda sem bagunçar estoque."),
        ("Fechamento & SPED no Piloto Automático", "Entrega organizada de todos os XMLs e arquivos EFD todo dia 1º no sistema do escritório."),
        ("Comissão Recorrente de 15% via Pix", "Remuneração financeira mensal vitalícia sobre cada cliente lojista indicado.")
    ],
    "salao": [
        ("Agenda de Horários & Comissões", "Controle de atendimentos por profissional e comissionamento automático de barbeiros/manicures.")
    ],
    "academia": [
        ("Controle de Mensalidades & Catracas", "Bloqueio automático de inadimplentes e recorrência no cartão ou Pix.")
    ],
    "limpeza": [
        ("Controle de Fracionamento & Diluição", "Venda de produtos químicos a granel e em embalagens industriais.")
    ]
}

def obter_modulos_segmento(segmento):
    seg = (segmento or "").lower()
    for chave, lista in MODULOS_ESPECIALISTAS.items():
        if chave in seg:
            return lista
    # Padrão para varejo em geral
    return [
        ("PDV Fiscal Integrado NFC-e / NF-e", "Emissão fiscal homologada na SEFAZ/RS em até 3 segundos com contingência offline."),
        ("Controle de Estoque & Entrada por XML", "Importação imediata das notas de compra dos fornecedores sem digitação manual."),
        ("Gestão Financeira & Fluxo de Caixa", "Contas a pagar, contas a receber, conciliação bancária e DRE simplificado."),
        ("Integração Contábil Direta", "Exportação dos arquivos fiscais mensais para sua contabilidade em 1 clique.")
    ]

def gerar_html_proposta(cliente, cidade, segmento, decisor, caixas=1, cnpj="", telefone="", email_destinatario="", site="", tem_site=None):
    """Gera o código HTML completo e responsivo da proposta comercial personalizada."""
    primeiro_nome = decisor.split()[0] if decisor else "Gestor(a)"
    modulos = obter_modulos_segmento(segmento)
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    caixas_str = f"{caixas} Caixa{'s' if int(caixas) > 1 else ''}"
    
    if tem_site is None:
        tem_site = bool(site and site != "Não possui site")

    rows_modulos = ""
    for titulo, desc in modulos:
        rows_modulos += f"""
        <tr>
          <td style="padding: 10px 12px; border-bottom: 1px solid #edf2f7; font-weight: 700; color: #0f172a; font-size: 13px;">
            ✓ {titulo}
          </td>
          <td style="padding: 10px 12px; border-bottom: 1px solid #edf2f7; color: #475569; font-size: 13px; line-height: 1.4;">
            {desc}
          </td>
        </tr>
        """

    if tem_site and site:
        bloco_web = f"""<tr>
                  <td style="padding: 10px; background-color: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; font-size: 13px; color: #0369a1; line-height: 1.5;">
                    <strong>🌐 Integração Omnichannel com seu Site ({site}):</strong> Sincronização automática entre o estoque da sua loja física e suas vendas online, com emissão fiscal unificada e baixa instantânea de produtos.
                  </td>
                </tr>
                <tr><td height="8"></td></tr>"""
    else:
        bloco_web = """<tr>
                  <td style="padding: 10px; background-color: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; font-size: 13px; color: #92400e; line-height: 1.5;">
                    <strong>📱 Catálogo Digital & Vendas pelo WhatsApp TruData:</strong> Como seu estabelecimento ainda não possui site, disponibilizamos o catálogo virtual próprio TruData com fotos, preços e pedidos direto no WhatsApp com Pix, sem custo adicional!
                  </td>
                </tr>
                <tr><td height="8"></td></tr>"""

    link_wpp = f"https://wa.me/555433612650?text={urllib.parse.quote(f'Olá! Recebi a proposta comercial da TruData ERP para a {cliente} em {cidade} e gostaria de agendar uma demonstração rápida.')}"

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Proposta Comercial TruData ERP — {cliente}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  
  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f1f5f9; padding: 25px 10px;">
    <tr>
      <td align="center">
        
        <!-- CARD PRINCIPAL DO E-MAIL -->
        <table border="0" cellpadding="0" cellspacing="0" width="600" style="max-width: 600px; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
          
          <!-- CABEÇALHO AZUL TRUDATA -->
          <tr>
            <td style="background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); padding: 30px 35px; color: #ffffff;">
              <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td>
                    <div style="font-size: 26px; font-weight: 900; letter-spacing: -0.5px; color: #ffffff;">
                      TRU<span style="color: #38bdf8;">DATA</span> ERP
                    </div>
                    <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">
                      Hansen Software LTDA · Sede em Sarandi - RS · Desde 2001
                    </div>
                  </td>
                  <td align="right">
                    <span style="background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.4); color: #38bdf8; font-size: 11px; padding: 4px 10px; border-radius: 20px; font-weight: 700;">
                      Selo de Qualidade MPS.BR
                    </span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- CORPO PRINCIPAL -->
          <tr>
            <td style="padding: 35px 35px 25px 35px;">
              
              <h1 style="font-size: 20px; font-weight: 800; color: #0f172a; margin: 0 0 15px 0;">
                Olá, {primeiro_nome}! Tudo bem?
              </h1>

              <p style="font-size: 14px; color: #334155; line-height: 1.6; margin: 0 0 18px 0;">
                Preparamos uma apresentação exclusiva da <strong>TruData ERP</strong> para a <strong>{cliente}</strong> em <strong>{cidade} - RS</strong>. Nossa sede fica aqui em Sarandi-RS, oferecendo implantação assistida e suporte técnico humanizado para o comércio da nossa região.
              </p>

              <!-- CAIXA DE DESTAQUE DO CLIENTE -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f8fafc; border-left: 4px solid #009fe3; border-radius: 4px; margin-bottom: 25px;">
                <tr>
                  <td style="padding: 14px 18px;">
                    <div style="font-size: 12px; color: #64748b; margin-bottom: 4px;">RESUMO DA PROPOSTA COMERCIAL</div>
                    <div style="font-size: 15px; font-weight: 800; color: #0f172a;">{cliente} · {cidade}/RS</div>
                    <div style="font-size: 13px; color: #475569; margin-top: 2px;">
                      <strong>Segmento:</strong> {segmento} · <strong>Porte:</strong> {caixas_str} · <strong>Data:</strong> {data_hoje}
                    </div>
                  </td>
                </tr>
              </table>

              <!-- TABELA DE ESCOPO DO SISTEMA -->
              <h2 style="font-size: 14px; font-weight: 800; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 10px 0;">
                📋 Escopo Especialista Incluído para seu Estabelecimento
              </h2>

              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border: 1px solid #e2e8f0; border-radius: 8px; border-collapse: collapse; margin-bottom: 25px;">
                <thead>
                  <tr style="background-color: #f8fafc;">
                    <th align="left" style="padding: 10px 12px; border-bottom: 2px solid #e2e8f0; font-size: 12px; color: #475569; font-weight: 700;">Recurso</th>
                    <th align="left" style="padding: 10px 12px; border-bottom: 2px solid #e2e8f0; font-size: 12px; color: #475569; font-weight: 700;">Benefício Prático no Caixa e Loja</th>
                  </tr>
                </thead>
                <tbody>
                  {rows_modulos}
                </tbody>
              </table>

              <!-- DIFERENCIAIS REGIONAIS -->
              <h2 style="font-size: 14px; font-weight: 800; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 10px 0;">
                ⭐ Por que mais de 300 comércios no RS escolheram a TruData?
              </h2>

              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 25px;">
                <tr>
                  <td style="padding: 10px; background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; font-size: 13px; color: #166534; line-height: 1.5;">
                    <strong>⚡ Caixa 100% Funcional sem Internet (Contingência Offline):</strong> Se a internet oscilar no sábado de movimento, seu caixa continua vendendo e emitindo cupons fiscais normalmente sem travar a fila.
                  </td>
                </tr>
                <tr><td height="8"></td></tr>
                <tr>
                  <td style="padding: 10px; background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; font-size: 13px; color: #1e40af; line-height: 1.5;">
                    <strong>🧑‍💼 Suporte com Gente de Verdade em Sarandi-RS:</strong> Atendimento telefônico direto sem robôs, com plantão especializado de suporte ao varejo.
                  </td>
                </tr>
                <tr><td height="8"></td></tr>
                {bloco_web}
                <tr>
                  <td style="padding: 10px; background-color: #faf5ff; border: 1px solid #e9d5ff; border-radius: 8px; font-size: 13px; color: #6b21a8; line-height: 1.5;">
                    <strong>🏛️ Integração Fiscal Completa:</strong> Envio dos arquivos para sua contabilidade em 1 clique, evitando erros e retrabalhos no fechamento do mês.
                  </td>
                </tr>
              </table>

              <!-- BOTÃO DE CHAMADA DE AÇÃO (CTA) -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 20px;">
                <tr>
                  <td align="center">
                    <a href="{link_wpp}" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #16a34a 0%, #15803d 100%); color: #ffffff; text-decoration: none; padding: 15px 32px; font-size: 15px; font-weight: 800; border-radius: 8px; box-shadow: 0 4px 15px rgba(22, 163, 74, 0.35);">
                      📲 Falar no WhatsApp com o Consultor de Sarandi
                    </a>
                  </td>
                </tr>
              </table>

              <p style="font-size: 13px; color: #64748b; text-align: center; margin: 0 0 10px 0;">
                Podemos agendar uma demonstração rápida de 15 minutos sem compromisso na sua loja.
              </p>

            </td>
          </tr>

          <!-- RODAPÉ -->
          <tr>
            <td style="background-color: #0f172a; padding: 25px 35px; color: #94a3b8; font-size: 12px; text-align: center; line-height: 1.6;">
              <strong>Hansen Software LTDA · TruData ERP</strong><br>
              Sarandi - Rio Grande do Sul · Central de Atendimento: (54) 3361-2650<br>
              WhatsApp Comercial: (54) 3361-2650 · E-mail: comercial@trudata.com.br<br>
              <span style="color: #64748b; font-size: 11px;">Este e-mail comercial foi enviado em atendimento aos comércios da região de Sarandi e Norte Gaúcho.</span>
            </td>
          </tr>

        </table>

      </td>
    </tr>
  </table>

</body>
</html>"""
    return html

def registrar_historico_envio(dados_envio):
    """Grava o e-mail disparado no histórico local para auditoria e controle."""
    historico = []
    if os.path.exists(HISTORICO_PATH):
        try:
            with open(HISTORICO_PATH, "r", encoding="utf-8") as f:
                historico = json.load(f)
        except Exception:
            historico = []

    historico.insert(0, dados_envio)

    try:
        with open(HISTORICO_PATH, "w", encoding="utf-8") as f:
            json.dump(historico[:100], f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def atualizar_nota_lead_crm(empresa_nome, destinatario, status_envio):
    """Se o lead existir no CRM Kanban, registra uma nota de que a proposta foi enviada."""
    if not os.path.exists(LEADS_CRM_PATH):
        return

    try:
        with open(LEADS_CRM_PATH, "r", encoding="utf-8") as f:
            leads = json.load(f)

        atualizado = False
        data_hora = datetime.now().strftime("%d/%m/%Y às %H:%M")
        for lead in leads:
            if lead.get("empresa", "").strip().lower() == empresa_nome.strip().lower() or (lead.get("email") and lead["email"].strip().lower() == destinatario.strip().lower()):
                nota_existente = lead.get("notas", "")
                lead["notas"] = f"✉️ Proposta enviada por e-mail em {data_hora} para {destinatario} ({status_envio}).\n{nota_existente}"
                if lead.get("fase") == "novo":
                    lead["fase"] = "contato" # Avança para a etapa de contato realizado
                atualizado = True
                break

        if atualizado:
            with open(LEADS_CRM_PATH, "w", encoding="utf-8") as f:
                json.dump(leads, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def disparar_proposta_email(
    destinatario,
    cliente,
    cidade,
    segmento,
    decisor,
    caixas=1,
    cnpj="",
    telefone="",
    assunto_custom=None,
    site="",
    tem_site=None
):
    """
    Executa o envio da proposta comercial via SMTP ou em modo assistido com 1 clique.
    """
    cfg = carregar_config()
    if tem_site is None:
        tem_site = bool(site and site != "Não possui site")

    if not assunto_custom:
        if "contabil" in (segmento or "").lower() or "contabilidade" in (segmento or "").lower():
            assunto = f"Parceria Estratégica & Homologação Técnica TruData ERP — {cliente} ({cidade}-RS)"
        else:
            assunto = f"Proposta Comercial TruData ERP — {cliente} ({cidade}-RS)"
    else:
        assunto = assunto_custom
    html_content = gerar_html_proposta(cliente, cidade, segmento, decisor, caixas, cnpj, telefone, destinatario, site=site, tem_site=tem_site)

    data_envio = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Linha contextual da web para o texto puro
    if tem_site and site:
        destaque_web = f"- Sincronização automática com seu site ({site}) e vendas online;\n"
    else:
        destaque_web = "- Catálogo virtual com pedidos no WhatsApp e Pix integrado ao PDV;\n"

    # Verifica se há credenciais de SMTP configuradas
    smtp_host = cfg.get("smtp_host")
    smtp_user = cfg.get("usuario")
    smtp_pass = cfg.get("senha")
    remetente = cfg.get("remetente_email") or "comercial@trudata.com.br"
    remetente_nome = cfg.get("remetente_nome") or "TruData ERP"

    # Se estiver configurado com usuário e senha para envio real
    if cfg.get("modo") == "smtp" and smtp_user and smtp_pass:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = assunto
            msg["From"] = f"{remetente_nome} <{remetente}>"
            msg["To"] = destinatario

            # Versão em texto puro como fallback
            texto_puro = (
                f"Olá {decisor},\n\n"
                f"Apresentamos a proposta da TruData ERP para a {cliente} em {cidade}-RS.\n"
                f"Sede em Sarandi-RS há 25 anos, contingência offline fiscal e suporte humanizado.\n\n"
                f"Destaques:\n"
                f"- Caixa 100% offline para sábados de lotação;\n"
                f"{destaque_web}"
                f"- Suporte humanizado direto de Sarandi;\n\n"
                f"Acesse pelo WhatsApp para agendar demonstração: (54) 3361-2650\n\n"
                f"Atenciosamente,\nEquipe Comercial TruData ERP"
            )
            msg.attach(MIMEText(texto_puro, "plain", "utf-8"))
            msg.attach(MIMEText(html_content, "html", "utf-8"))

            porta = int(cfg.get("smtp_port", 587))
            if porta == 465:
                server = smtplib.SMTP_SSL(smtp_host, porta, timeout=12)
            else:
                server = smtplib.SMTP(smtp_host, porta, timeout=12)
                if cfg.get("usar_tls", True):
                    server.starttls()

            server.login(smtp_user, smtp_pass)
            server.sendmail(remetente, [destinatario], msg.as_string())
            server.quit()

            status = "Entregue via SMTP"
            sucesso = True
            msg_resultado = f"Proposta enviada com sucesso para {destinatario} via servidor SMTP ({smtp_host})!"
        except Exception as e:
            status = f"Erro SMTP: {str(e)}"
            sucesso = False
            msg_resultado = f"Falha no servidor SMTP: {str(e)}"
    else:
        # Modo Automático / Sandbox / Simulado
        # Registra o e-mail completo pronto e fornece link de disparo imediato
        status = "Registrado & Pronto para Envio"
        sucesso = True
        msg_resultado = f"Proposta gerada com sucesso para {destinatario}! (Modo Automático Ativo)"

    # Registra no histórico
    registro = {
        "id": f"mail-{int(datetime.now().timestamp())}",
        "data": data_envio,
        "destinatario": destinatario,
        "cliente": cliente,
        "cidade": cidade,
        "segmento": segmento,
        "decisor": decisor,
        "caixas": caixas,
        "site": site,
        "assunto": assunto,
        "status": status,
        "sucesso": sucesso
    }
    registrar_historico_envio(registro)
    atualizar_nota_lead_crm(cliente, destinatario, status)

    # Gera link webmail / mailto de backup com parâmetros codificados
    corpo_resumo = (
        f"Olá {decisor},\n\n"
        f"Segue a apresentação da TruData ERP (Hansen Software) para a {cliente} em {cidade}-RS.\n"
        f"Somos especialistas no varejo gaúcho há 25 anos com matriz em Sarandi-RS.\n\n"
        f"Destaques da solução para seu estabelecimento:\n"
        f"- Contingência fiscal offline para não travar o caixa no sábado;\n"
        f"{destaque_web}"
        f"- Suporte telefônico 100% humanizado direto de Sarandi;\n"
        f"- Integração com balanças, TEF, etiquetas e sua contabilidade;\n\n"
        f"Podemos agendar uma demonstração rápida de 15 minutos na sua loja?\n\n"
        f"Atenciosamente,\n"
        f"Equipe Comercial TruData ERP\n"
        f"Sarandi - RS | Fone/WhatsApp: (54) 3361-2650"
    )
    link_mailto = f"mailto:{destinatario}?subject={urllib.parse.quote(assunto)}&body={urllib.parse.quote(corpo_resumo)}"
    link_gmail = f"https://mail.google.com/mail/?view=cm&fs=1&to={destinatario}&su={urllib.parse.quote(assunto)}&body={urllib.parse.quote(corpo_resumo)}"

    return {
        "sucesso": sucesso,
        "mensagem": msg_resultado,
        "destinatario": destinatario,
        "cliente": cliente,
        "status": status,
        "data": data_envio,
        "link_mailto": link_mailto,
        "link_gmail": link_gmail
    }

if __name__ == "__main__":
    print("Testando motor de e-mails TruData ERP...")
    res = disparar_proposta_email(
        destinatario="contato@padariapaoquente.com.br",
        cliente="Padaria Pão Quente",
        cidade="Sarandi",
        segmento="Padarias & Gastronomia",
        decisor="Cláudia Bertoncello",
        caixas=1
    )
    print("Resultado:", json.dumps(res, indent=2, ensure_ascii=False))
