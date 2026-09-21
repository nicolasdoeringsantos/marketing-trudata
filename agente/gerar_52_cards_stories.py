#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador dos 52 Cards Publicitários Verticais (1080x1920px, 9:16) — TruData ERP
Segue rigorosamente o PROMPT MESTRE:
- Fundo azul-petróleo escuro com gradiente sutil (#07141e -> #0f2b3c)
- Ícone principal flat/linear minimalista em branco (#ffffff) e verde-menta claro (#34d399 / #5eead4)
- Detalhes lineares discretos ao redor
- Título em sans-serif bold geométrico branco
- Subtítulo em regular com 80% de opacidade
- Logotipo 'Trudata' discreto e uniforme no rodapé
- Margens de segurança de ~250px no topo e na base
"""

import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(BASE_DIR, "conteudo_pronto", "cards_stories")
JSON_OUTPUT = os.path.join(BASE_DIR, "painel_aprovacao", "cards_stories_dados.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Definição dos 52 Cards
CARDS = [
    # 01 a 09: FISCAL & REFORMA TRIBUTÁRIA
    {
        "id": "01",
        "categoria": "Fiscal & Tributário",
        "cat_slug": "fiscal",
        "titulo": "Centro Fiscal Inteligente",
        "subtitulo": "Identifique e bloqueie erros antes de enviar à SEFAZ.",
        "icon_svg": """
            <!-- Documento Fiscal com Escudo e Check -->
            <rect x="-100" y="-130" width="200" height="260" rx="16" stroke="#ffffff" stroke-width="6" fill="none"/>
            <line x1="-65" y1="-80" x2="25" y2="-80" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>
            <line x1="-65" y1="-40" x2="65" y2="-40" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>
            <line x1="-65" y1="0" x2="0" y2="0" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>
            <line x1="-65" y1="40" x2="40" y2="40" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>
            <!-- Escudo Frontal -->
            <path d="M 30,20 Q 75,30 120,20 Q 125,90 75,145 Q 25,90 30,20 Z" stroke="#34d399" stroke-width="6" fill="#0b1e2c" stroke-linejoin="round"/>
            <path d="M 55,80 L 70,95 L 98,60" stroke="#34d399" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            <!-- Detalhes discretos de validação -->
            <circle cx="-140" cy="-60" r="4" fill="#5eead4"/>
            <line x1="-150" y1="20" x2="-120" y2="20" stroke="#5eead4" stroke-width="3" stroke-dasharray="4,4"/>
            <path d="M 140,-40 L 160,-40 M 150,-50 L 150,-30" stroke="#5eead4" stroke-width="3"/>
        """
    },
    {
        "id": "02",
        "categoria": "Fiscal & Tributário",
        "cat_slug": "fiscal",
        "titulo": "Reforma Tributária",
        "subtitulo": "IBS, CBS e novos impostos sempre atualizados.",
        "icon_svg": """
            <!-- Documento com Porcentagem e Conexões IBS / CBS -->
            <rect x="-100" y="-120" width="200" height="250" rx="16" stroke="#ffffff" stroke-width="6" fill="none"/>
            <!-- Símbolo de % -->
            <circle cx="-30" cy="-40" r="16" stroke="#34d399" stroke-width="6" fill="none"/>
            <line x1="-40" y1="45" x2="40" y2="-45" stroke="#34d399" stroke-width="6" stroke-linecap="round"/>
            <circle cx="30" cy="40" r="16" stroke="#34d399" stroke-width="6" fill="none"/>
            <!-- Conexões e Siglas IBS/CBS -->
            <line x1="100" y1="-30" x2="145" y2="-30" stroke="#5eead4" stroke-width="4"/>
            <text x="155" y="-22" font-family="'Inter', sans-serif" font-size="16" font-weight="700" fill="#34d399">IBS</text>
            <line x1="100" y1="30" x2="145" y2="30" stroke="#5eead4" stroke-width="4"/>
            <text x="155" y="38" font-family="'Inter', sans-serif" font-size="16" font-weight="700" fill="#34d399">CBS</text>
            <circle cx="-130" cy="20" r="3" fill="#5eead4"/>
            <line x1="-150" y1="-20" x2="-120" y2="-20" stroke="#5eead4" stroke-width="3" stroke-dasharray="4,4"/>
        """
    },
    {
        "id": "03",
        "categoria": "Fiscal & Tributário",
        "cat_slug": "fiscal",
        "titulo": "Contingência Offline",
        "subtitulo": "Continue emitindo NFC-e mesmo sem internet.",
        "icon_svg": """
            <!-- Documento Fiscal com Wi-Fi Desconectado e Seta de Sync -->
            <rect x="-90" y="-110" width="180" height="230" rx="16" stroke="#ffffff" stroke-width="6" fill="none"/>
            <!-- Linhas do cupom -->
            <line x1="-55" y1="-60" x2="55" y2="-60" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>
            <line x1="-55" y1="-25" x2="15" y2="-25" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>
            <!-- Símbolo Wi-Fi interrompido -->
            <path d="M 50,60 Q 95,20 140,60" stroke="#ffffff" stroke-width="5" fill="none" stroke-linecap="round"/>
            <path d="M 65,78 Q 95,50 125,78" stroke="#ffffff" stroke-width="5" fill="none" stroke-linecap="round"/>
            <circle cx="95" cy="100" r="6" fill="#ffffff"/>
            <!-- Linha de corte/interrupção -->
            <line x1="45" y1="110" x2="145" y2="30" stroke="#f43f5e" stroke-width="5" stroke-linecap="round"/>
            <!-- Seta de Sincronização Futura em Verde Menta -->
            <path d="M -40,30 Q -60,65 -30,85 Q 0,105 20,80" stroke="#34d399" stroke-width="6" fill="none" stroke-linecap="round"/>
            <polyline points="10,65 24,80 12,95" stroke="#34d399" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        """
    },
    {
        "id": "04",
        "categoria": "Fiscal & Tributário",
        "cat_slug": "fiscal",
        "titulo": "NF-e",
        "subtitulo": "Emissão e entrada de notas fiscais por XML.",
        "icon_svg": """
            <!-- Documento NF-e com Setas Bidirecionais e Badge XML -->
            <rect x="-90" y="-120" width="180" height="240" rx="16" stroke="#ffffff" stroke-width="6" fill="none"/>
            <!-- Dobra do topo -->
            <path d="M 40,-120 L 90,-70 L 40,-70 Z" stroke="#ffffff" stroke-width="5" fill="none"/>
            <!-- Seta Entrada (Esquerda para Dentro) -->
            <line x1="-150" y1="-30" x2="-50" y2="-30" stroke="#34d399" stroke-width="6" stroke-linecap="round"/>
            <polyline points="-70,-45 -50,-30 -70,-15" stroke="#34d399" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            <!-- Seta Saída (Dentro para Direita) -->
            <line x1="50" y1="30" x2="150" y2="30" stroke="#34d399" stroke-width="6" stroke-linecap="round"/>
            <polyline points="130,15 150,30 130,45" stroke="#34d399" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            <!-- Badge XML -->
            <rect x="-45" y="55" width="90" height="34" rx="8" stroke="#34d399" stroke-width="4" fill="none"/>
            <text x="0" y="78" font-family="'Inter', sans-serif" font-size="18" font-weight="800" fill="#34d399" text-anchor="middle">XML</text>
        """
    },
    {
        "id": "05",
        "categoria": "Fiscal & Tributário",
        "cat_slug": "fiscal",
        "titulo": "NFS-e Nacional",
        "subtitulo": "Emissão de serviços pelo padrão nacional DPS.",
        "icon_svg": """
            <!-- Documento de Serviço com Selo Digital DPS e Engrenagem -->
            <rect x="-85" y="-120" width="170" height="240" rx="16" stroke="#ffffff" stroke-width="6" fill="none"/>
            <line x1="-50" y1="-70" x2="50" y2="-70" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>
            <line x1="-50" y1="-35" x2="20" y2="-35" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>
            <!-- Selo Digital DPS -->
            <circle cx="0" cy="35" r="42" stroke="#34d399" stroke-width="6" fill="none"/>
            <polyline points="-18,35 -5,48 20,22" stroke="#34d399" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            <!-- Pequena engrenagem/ferramenta lateral -->
            <circle cx="120" cy="-40" r="18" stroke="#5eead4" stroke-width="4" stroke-dasharray="8,4" fill="none"/>
            <circle cx="120" cy="-40" r="6" fill="#5eead4"/>
        """
    },
    {
        "id": "06",
        "categoria": "Fiscal & Tributário",
        "cat_slug": "fiscal",
        "titulo": "MDF-e e CT-e",
        "subtitulo": "Documentos fiscais para transporte e logística.",
        "icon_svg": """
            <!-- Caminhão Linear Minimalista com Documento Fiscal -->
            <path d="M -130,40 L -130,-30 L -10,-30 L -10,40 Z" stroke="#ffffff" stroke-width="6" fill="none"/>
            <path d="M -10,-10 L 40,-10 L 65,15 L 65,40 L -10,40 Z" stroke="#ffffff" stroke-width="6" fill="none"/>
            <!-- Rodas -->
            <circle cx="-85" cy="50" r="18" stroke="#34d399" stroke-width="6" fill="#081722"/>
            <circle cx="35" cy="50" r="18" stroke="#34d399" stroke-width="6" fill="#081722"/>
            <!-- Documento no topo -->
            <rect x="-60" y="-125" width="120" height="80" rx="10" stroke="#34d399" stroke-width="5" fill="#081722"/>
            <line x1="-40" y1="-100" x2="0" y2="-100" stroke="#34d399" stroke-width="4" stroke-linecap="round"/>
            <line x1="-40" y1="-80" x2="35" y2="-80" stroke="#34d399" stroke-width="4" stroke-linecap="round"/>
            <!-- Linha de rota com pino -->
            <path d="M 85,-40 Q 120,-70 140,-40" stroke="#5eead4" stroke-width="3" stroke-dasharray="5,5" fill="none"/>
            <circle cx="140" cy="-40" r="5" fill="#34d399"/>
        """
    },
    {
        "id": "07",
        "categoria": "Fiscal & Tributário",
        "cat_slug": "fiscal",
        "titulo": "Assistente Fiscal",
        "subtitulo": "Emissão guiada em apenas três passos.",
        "icon_svg": """
            <!-- Documento com Sequência Linear 1 -> 2 -> 3 -->
            <rect x="-100" y="-120" width="200" height="240" rx="16" stroke="#ffffff" stroke-width="6" fill="none"/>
            <!-- Etapa 1 -->
            <circle cx="-45" cy="-40" r="16" stroke="#34d399" stroke-width="5" fill="none"/>
            <text x="-45" y="-33" font-family="'Inter', sans-serif" font-size="18" font-weight="700" fill="#34d399" text-anchor="middle">1</text>
            <line x1="-20" y1="-40" x2="20" y2="-40" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
            <!-- Etapa 2 -->
            <circle cx="45" cy="-40" r="16" stroke="#ffffff" stroke-width="5" fill="none"/>
            <text x="45" y="-33" font-family="'Inter', sans-serif" font-size="18" font-weight="700" fill="#ffffff" text-anchor="middle">2</text>
            <!-- Etapa 3 com Check -->
            <line x1="45" y1="-15" x2="45" y2="25" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
            <circle cx="45" cy="50" r="16" stroke="#34d399" stroke-width="5" fill="none"/>
            <text x="45" y="57" font-family="'Inter', sans-serif" font-size="18" font-weight="700" fill="#34d399" text-anchor="middle">3</text>
            <polyline points="-55,50 -40,65 -15,35" stroke="#34d399" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        """
    },
    {
        "id": "08",
        "categoria": "Fiscal & Tributário",
        "cat_slug": "fiscal",
        "titulo": "IBPT Automático",
        "subtitulo": "Transparência fiscal calculada automaticamente.",
        "icon_svg": """
            <!-- Calculadora Linear com Documento Fiscal e Símbolo de % -->
            <rect x="-90" y="-110" width="180" height="230" rx="18" stroke="#ffffff" stroke-width="6" fill="none"/>
            <!-- Visor da Calculadora -->
            <rect x="-65" y="-85" width="130" height="50" rx="8" stroke="#ffffff" stroke-width="5" fill="none"/>
            <text x="50" y="-50" font-family="'Inter', sans-serif" font-size="22" font-weight="700" fill="#34d399" text-anchor="end">% 0,00</text>
            <!-- Teclas em Grade -->
            <circle cx="-40" cy="-5" r="10" stroke="#ffffff" stroke-width="4" fill="none"/>
            <circle cx="0" cy="-5" r="10" stroke="#ffffff" stroke-width="4" fill="none"/>
            <circle cx="40" cy="-5" r="10" stroke="#34d399" stroke-width="4" fill="none"/>
            <circle cx="-40" cy="35" r="10" stroke="#ffffff" stroke-width="4" fill="none"/>
            <circle cx="0" cy="35" r="10" stroke="#ffffff" stroke-width="4" fill="none"/>
            <circle cx="40" cy="35" r="10" stroke="#ffffff" stroke-width="4" fill="none"/>
            <circle cx="-40" cy="75" r="10" stroke="#ffffff" stroke-width="4" fill="none"/>
            <circle cx="0" cy="75" r="10" stroke="#ffffff" stroke-width="4" fill="none"/>
            <rect x="25" y="65" width="30" height="20" rx="5" fill="#34d399"/>
        """
    },
    {
        "id": "09",
        "categoria": "Fiscal & Tributário",
        "cat_slug": "fiscal",
        "titulo": "Porta Única Fiscal",
        "subtitulo": "Só avance quando sua nota estiver correta.",
        "icon_svg": """
            <!-- Portal/Escudo com Semáforo de 3 Círculos -->
            <path d="M -110,-90 Q 0,-130 110,-90 L 110,30 Q 110,130 0,165 Q -110,130 -110,30 Z" stroke="#ffffff" stroke-width="6" fill="none" stroke-linejoin="round"/>
            <!-- Documento entrando pelo portal -->
            <rect x="-50" y="-60" width="100" height="130" rx="10" stroke="#ffffff" stroke-width="5" fill="#081722"/>
            <!-- Semáforo de Validação (3 Círculos verticais) -->
            <circle cx="0" cy="-25" r="9" stroke="#ffffff" stroke-width="3" fill="none"/>
            <circle cx="0" cy="5" r="9" stroke="#ffffff" stroke-width="3" fill="none"/>
            <circle cx="0" cy="35" r="12" fill="#34d399"/>
            <polyline points="-5,35 -1,39 6,31" stroke="#081722" stroke-width="3" fill="none" stroke-linecap="round"/>
        """
    },

    # 10 a 15: PDV & VENDAS
    {
        "id": "10",
        "categoria": "PDV & Vendas",
        "cat_slug": "pdv",
        "titulo": "PDV Rápido",
        "subtitulo": "Venda com agilidade no balcão ou tela touch.",
        "icon_svg": """
            <!-- Monitor de PDV com Código de Barras e Carrinho -->
            <rect x="-110" y="-100" width="220" height="145" rx="14" stroke="#ffffff" stroke-width="6" fill="none"/>
            <!-- Suporte do monitor -->
            <line x1="0" y1="45" x2="0" y2="90" stroke="#ffffff" stroke-width="6"/>
            <line x1="-50" y1="90" x2="50" y2="90" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>
            <!-- Código de barras na tela -->
            <line x1="-75" y1="-65" x2="-75" y2="10" stroke="#ffffff" stroke-width="4"/>
            <line x1="-60" y1="-65" x2="-60" y2="10" stroke="#ffffff" stroke-width="6"/>
            <line x1="-45" y1="-65" x2="-45" y2="10" stroke="#ffffff" stroke-width="3"/>
            <line x1="-30" y1="-65" x2="-30" y2="10" stroke="#ffffff" stroke-width="8"/>
            <line x1="-15" y1="-65" x2="-15" y2="10" stroke="#ffffff" stroke-width="4"/>
            <!-- Carrinho de Compras em Destaque Menta -->
            <path d="M 20,-30 L 35,-30 L 50,10 L 80,10" stroke="#34d399" stroke-width="5" fill="none" stroke-linecap="round"/>
            <circle cx="50" cy="22" r="5" fill="#34d399"/>
            <circle cx="75" cy="22" r="5" fill="#34d399"/>
            <!-- Raio de Agilidade -->
            <path d="M 125,-75 L 140,-55 L 130,-55 L 145,-30" stroke="#5eead4" stroke-width="4" fill="none" stroke-linejoin="round"/>
        """
    },
    {
        "id": "11",
        "categoria": "PDV & Vendas",
        "cat_slug": "pdv",
        "titulo": "PIX + TEF Integrado",
        "subtitulo": "Pagamentos rápidos com conciliação automática.",
        "icon_svg": """
            <!-- QR Code Estilizado com Cartão de Crédito e Chip -->
            <!-- Base QR Code -->
            <rect x="-125" y="-85" width="120" height="120" rx="12" stroke="#ffffff" stroke-width="6" fill="none"/>
            <rect x="-105" y="-65" width="35" height="35" rx="6" stroke="#ffffff" stroke-width="5" fill="none"/>
            <rect x="-95" y="-55" width="15" height="15" fill="#34d399"/>
            <rect x="-55" y="-20" width="20" height="20" fill="#34d399"/>
            <!-- Cartão TEF Sobreposto -->
            <rect x="-25" y="-20" width="155" height="105" rx="12" stroke="#34d399" stroke-width="6" fill="#0b1e2c"/>
            <rect x="-5" y="10" width="28" height="22" rx="4" stroke="#ffffff" stroke-width="4" fill="none"/>
            <line x1="40" y1="40" x2="105" y2="40" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
            <!-- Setas de Conciliação Automática -->
            <path d="M 50,-65 Q 85,-85 110,-55" stroke="#5eead4" stroke-width="4" fill="none"/>
            <polyline points="105,-70 110,-55 95,-55" stroke="#5eead4" stroke-width="4" fill="none"/>
        """
    },
    {
        "id": "12",
        "categoria": "PDV & Vendas",
        "cat_slug": "pdv",
        "titulo": "Cancelamento Inteligente",
        "subtitulo": "Estoque e financeiro estornados juntos.",
        "icon_svg": """
            <!-- Recibo com Seta de Retorno Conectando Estoque e Financeiro -->
            <rect x="-100" y="-120" width="110" height="150" rx="10" stroke="#ffffff" stroke-width="5" fill="none"/>
            <line x1="-80" y1="-90" x2="-20" y2="-90" stroke="#ffffff" stroke-width="4"/>
            <line x1="-80" y1="-65" x2="-40" y2="-65" stroke="#ffffff" stroke-width="4"/>
            <!-- Duas caixas conectadas (Estoque & Finanças) -->
            <rect x="25" y="-100" width="75" height="60" rx="8" stroke="#34d399" stroke-width="5" fill="none"/>
            <text x="62" y="-62" font-family="'Inter', sans-serif" font-size="16" font-weight="700" fill="#34d399" text-anchor="middle">EST</text>
            <rect x="25" y="0" width="75" height="60" rx="8" stroke="#ffffff" stroke-width="5" fill="none"/>
            <text x="62" y="38" font-family="'Inter', sans-serif" font-size="16" font-weight="700" fill="#ffffff" text-anchor="middle">FIN</text>
            <!-- Seta de Estorno Circular Reversa -->
            <path d="M 62,-25 C 105,-25 105,-70 105,-70" stroke="#5eead4" stroke-width="4" stroke-dasharray="4,4" fill="none"/>
            <path d="M -25,50 Q 10,95 62,75" stroke="#34d399" stroke-width="5" fill="none"/>
            <polyline points="-15,35 -28,52 -10,65" stroke="#34d399" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        """
    },
    {
        "id": "13",
        "categoria": "PDV & Vendas",
        "cat_slug": "pdv",
        "titulo": "Comissões Automáticas",
        "subtitulo": "Calcule por vendedor, produto ou meta.",
        "icon_svg": """
            <!-- Usuário/Vendedor com Símbolo % e Gráfico Ascendente -->
            <circle cx="-50" cy="-60" r="32" stroke="#ffffff" stroke-width="6" fill="none"/>
            <path d="M -95,30 C -95,-15 -5,-15 -5,30" stroke="#ffffff" stroke-width="6" fill="none" stroke-linecap="round"/>
            <!-- Símbolo de % em Destaque -->
            <circle cx="55" cy="-70" r="14" stroke="#34d399" stroke-width="5" fill="none"/>
            <line x1="45" y1="-30" x2="85" y2="-90" stroke="#34d399" stroke-width="5" stroke-linecap="round"/>
            <circle cx="75" cy="-50" r="14" stroke="#34d399" stroke-width="5" fill="none"/>
            <!-- Gráfico Crescente Simples -->
            <line x1="20" y1="50" x2="20" y2="25" stroke="#34d399" stroke-width="6" stroke-linecap="round"/>
            <line x1="50" y1="50" x2="50" y2="5" stroke="#34d399" stroke-width="6" stroke-linecap="round"/>
            <line x1="80" y1="50" x2="80" y2="-15" stroke="#34d399" stroke-width="6" stroke-linecap="round"/>
            <polyline points="10,35 40,15 80,-25" stroke="#5eead4" stroke-width="3" fill="none"/>
        """
    },
    {
        "id": "14",
        "categoria": "PDV & Vendas",
        "cat_slug": "pdv",
        "titulo": "Orçamento → Venda",
        "subtitulo": "Converta o orçamento aprovado com um clique.",
        "icon_svg": """
            <!-- Orçamento Transformando-se em Carrinho de Venda -->
            <rect x="-135" y="-70" width="100" height="140" rx="12" stroke="#ffffff" stroke-width="6" fill="none"/>
            <line x1="-115" y1="-40" x2="-55" y2="-40" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>
            <line x1="-115" y1="-15" x2="-70" y2="-15" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>
            <!-- Seta de Transformação Central -->
            <line x1="-20" y1="0" x2="35" y2="0" stroke="#34d399" stroke-width="6" stroke-linecap="round"/>
            <polyline points="15,-18 35,0 15,18" stroke="#34d399" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            <!-- Carrinho / Venda Aprovada -->
            <path d="M 55,-40 L 70,-40 L 85,10 L 125,10" stroke="#34d399" stroke-width="6" fill="none" stroke-linecap="round"/>
            <circle cx="85" cy="28" r="7" fill="#34d399"/>
            <circle cx="120" cy="28" r="7" fill="#34d399"/>
            <polyline points="90,-20 100,-10 120,-30" stroke="#5eead4" stroke-width="4" fill="none" stroke-linecap="round"/>
        """
    },
    {
        "id": "15",
        "categoria": "PDV & Vendas",
        "cat_slug": "pdv",
        "titulo": "PDV Completo",
        "subtitulo": "Comandas, delivery, pré-venda e devoluções.",
        "icon_svg": """
            <!-- Monitor Central com 4 Recursos Secundários Lineares -->
            <rect x="-80" y="-60" width="160" height="110" rx="12" stroke="#ffffff" stroke-width="6" fill="none"/>
            <line x1="0" y1="50" x2="0" y2="80" stroke="#ffffff" stroke-width="6"/>
            <line x1="-40" y1="80" x2="40" y2="80" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>
            <!-- 1. Wi-Fi Offline (Noroeste) -->
            <path d="M -135,-85 Q -115,-105 -95,-85" stroke="#34d399" stroke-width="4" fill="none"/>
            <circle cx="-115" cy="-75" r="3" fill="#34d399"/>
            <!-- 2. Mesa/Comanda (Nordeste) -->
            <rect x="95" y="-105" width="30" height="40" rx="4" stroke="#34d399" stroke-width="4" fill="none"/>
            <!-- 3. Delivery/Moto (Sudeste) -->
            <circle cx="105" cy="50" r="10" stroke="#34d399" stroke-width="4" fill="none"/>
            <circle cx="135" cy="50" r="10" stroke="#34d399" stroke-width="4" fill="none"/>
            <line x1="105" y1="50" x2="135" y2="50" stroke="#34d399" stroke-width="3"/>
            <!-- 4. Devolução/Troca (Sudoeste) -->
            <path d="M -135,40 Q -115,20 -95,40" stroke="#34d399" stroke-width="4" fill="none"/>
            <polyline points="-135,30 -135,45 -120,45" stroke="#34d399" stroke-width="4" fill="none"/>
        """
    },

    # 16 a 20: ESTOQUE
    {
        "id": "16",
        "categoria": "Estoque & Armazém",
        "cat_slug": "estoque",
        "titulo": "Grade de Produtos",
        "subtitulo": "Cor, tamanho e modelo em um único cadastro.",
        "icon_svg": """
            <!-- Camiseta Linear com Grade de Tamanhos P, M, G -->
            <path d="M -70,-80 L -35,-100 Q 0,-70 35,-100 L 70,-80 L 50,-35 L 35,-45 L 35,50 L -35,50 L -35,-45 L -50,-35 Z" stroke="#ffffff" stroke-width="6" fill="none" stroke-linejoin="round"/>
            <!-- Matriz de Grade P, M, G -->
            <rect x="-65" y="70" width="40" height="35" rx="6" stroke="#34d399" stroke-width="4" fill="none"/>
            <text x="-45" y="94" font-family="'Inter', sans-serif" font-size="16" font-weight="700" fill="#34d399" text-anchor="middle">P</text>
            <rect x="-20" y="70" width="40" height="35" rx="6" stroke="#34d399" stroke-width="4" fill="none"/>
            <text x="0" y="94" font-family="'Inter', sans-serif" font-size="16" font-weight="700" fill="#34d399" text-anchor="middle">M</text>
            <rect x="25" y="70" width="40" height="35" rx="6" stroke="#34d399" stroke-width="4" fill="none"/>
            <text x="45" y="94" font-family="'Inter', sans-serif" font-size="16" font-weight="700" fill="#34d399" text-anchor="middle">G</text>
        """
    },
    {
        "id": "17",
        "categoria": "Estoque & Armazém",
        "cat_slug": "estoque",
        "titulo": "Transferência entre Filiais",
        "subtitulo": "Movimente estoque com saldo atualizado na hora.",
        "icon_svg": """
            <!-- Duas Lojas/Depósitos com Setas Bidirecionais -->
            <!-- Loja 1 -->
            <path d="M -130,-20 L -90,-60 L -50,-20 L -50,60 L -130,60 Z" stroke="#ffffff" stroke-width="6" fill="none"/>
            <rect x="-100" y="15" width="20" height="45" stroke="#ffffff" stroke-width="4" fill="none"/>
            <!-- Loja 2 -->
            <path d="M 50,-20 L 90,-60 L 130,-20 L 130,60 L 50,60 Z" stroke="#ffffff" stroke-width="6" fill="none"/>
            <rect x="80" y="15" width="20" height="45" stroke="#ffffff" stroke-width="4" fill="none"/>
            <!-- Setas Bidirecionais de Transferência -->
            <line x1="-35" y1="-10" x2="35" y2="-10" stroke="#34d399" stroke-width="6" stroke-linecap="round"/>
            <polyline points="20,-22 35,-10 20,2" stroke="#34d399" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="35" y1="20" x2="-35" y2="20" stroke="#34d399" stroke-width="6" stroke-linecap="round"/>
            <polyline points="-20,8 -35,20 -20,32" stroke="#34d399" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            <!-- Pequena caixa sendo transferida -->
            <rect x="-12" y="-45" width="24" height="24" rx="4" stroke="#5eead4" stroke-width="3" fill="#081722"/>
        """
    },
    {
        "id": "18",
        "categoria": "Estoque & Armazém",
        "cat_slug": "estoque",
        "titulo": "Lote e Validade",
        "subtitulo": "Priorize automaticamente o que vence primeiro.",
        "icon_svg": """
            <!-- Caixa de Produto com Calendário e Relógio (FEFO) -->
            <!-- Caixa 3D linear -->
            <path d="M -80,-10 L 0,-50 L 80,-10 L 0,30 Z" stroke="#ffffff" stroke-width="5" fill="none"/>
            <path d="M -80,-10 L -80,60 L 0,100 L 0,30" stroke="#ffffff" stroke-width="5" fill="none"/>
            <path d="M 80,-10 L 80,60 L 0,100" stroke="#ffffff" stroke-width="5" fill="none"/>
            <!-- Calendário com Relógio no topo -->
            <rect x="-30" y="-120" width="60" height="50" rx="8" stroke="#34d399" stroke-width="5" fill="#081722"/>
            <line x1="-30" y1="-95" x2="30" y2="-95" stroke="#34d399" stroke-width="4"/>
            <circle cx="45" cy="-85" r="22" stroke="#34d399" stroke-width="4" fill="#081722"/>
            <polyline points="45,-95 45,-85 55,-85" stroke="#5eead4" stroke-width="3" stroke-linecap="round"/>
        """
    },
    {
        "id": "19",
        "categoria": "Estoque & Armazém",
        "cat_slug": "estoque",
        "titulo": "Estoque Multi-local",
        "subtitulo": "Controle lojas, depósitos, kits e composições.",
        "icon_svg": """
            <!-- 3 Depósitos Interligados em Formato Triangular -->
            <!-- Depósito Topo -->
            <rect x="-35" y="-120" width="70" height="60" rx="8" stroke="#34d399" stroke-width="5" fill="none"/>
            <line x1="-15" y1="-120" x2="-15" y2="-60" stroke="#34d399" stroke-width="3"/>
            <!-- Depósito Esquerda -->
            <rect x="-110" y="30" width="70" height="60" rx="8" stroke="#ffffff" stroke-width="5" fill="none"/>
            <line x1="-90" y1="30" x2="-90" y2="90" stroke="#ffffff" stroke-width="3"/>
            <!-- Depósito Direita -->
            <rect x="40" y="30" width="70" height="60" rx="8" stroke="#ffffff" stroke-width="5" fill="none"/>
            <line x1="60" y1="30" x2="60" y2="90" stroke="#ffffff" stroke-width="3"/>
            <!-- Linhas de Interconexão -->
            <line x1="0" y1="-60" x2="-65" y2="30" stroke="#5eead4" stroke-width="4" stroke-dasharray="6,4"/>
            <line x1="0" y1="-60" x2="65" y2="30" stroke="#5eead4" stroke-width="4" stroke-dasharray="6,4"/>
            <line x1="-40" y1="60" x2="40" y2="60" stroke="#5eead4" stroke-width="4" stroke-dasharray="6,4"/>
        """
    },
    {
        "id": "20",
        "categoria": "Estoque & Armazém",
        "cat_slug": "estoque",
        "titulo": "Inventário Inteligente",
        "subtitulo": "Conte, organize e analise seu estoque.",
        "icon_svg": """
            <!-- Leitor/Coletor de Código de Barras com Feixe e Caixas -->
            <!-- Coletor Portátil -->
            <rect x="-40" y="-120" width="80" height="130" rx="14" stroke="#ffffff" stroke-width="6" fill="none"/>
            <rect x="-25" y="-105" width="50" height="40" rx="6" stroke="#ffffff" stroke-width="4" fill="none"/>
            <circle cx="0" cy="-45" r="10" fill="#34d399"/>
            <!-- Feixe Laser de Leitura -->
            <polygon points="-5,10 5,10 60,60 -60,60" fill="none" stroke="#34d399" stroke-width="2" stroke-dasharray="4,4"/>
            <!-- Caixa sendo bipada -->
            <rect x="-65" y="65" width="130" height="60" rx="8" stroke="#ffffff" stroke-width="5" fill="none"/>
            <!-- Curva ABC discreta no fundo -->
            <text x="80" y="-70" font-family="'Inter', sans-serif" font-size="18" font-weight="800" fill="#5eead4">ABC</text>
        """
    },

    # 21 a 27: FINANCEIRO
    {
        "id": "21",
        "categoria": "Gestão Financeira",
        "cat_slug": "financeiro",
        "titulo": "Financeiro Inteligente",
        "subtitulo": "Fiscal e contábil integrados sem retrabalho.",
        "icon_svg": """
            <!-- Símbolo Financeiro Conectado a Documento Fiscal e Livro Contábil -->
            <circle cx="-65" cy="-30" r="45" stroke="#34d399" stroke-width="6" fill="none"/>
            <text x="-65" y="-15" font-family="'Inter', sans-serif" font-size="44" font-weight="700" fill="#34d399" text-anchor="middle">R$</text>
            <!-- Documento Fiscal -->
            <rect x="25" y="-80" width="75" height="100" rx="8" stroke="#ffffff" stroke-width="5" fill="none"/>
            <line x1="45" y1="-55" x2="85" y2="-55" stroke="#ffffff" stroke-width="4"/>
            <!-- Livro Contábil -->
            <path d="M -20,50 L 50,50 L 70,100 L 0,100 Z" stroke="#ffffff" stroke-width="5" fill="none"/>
            <!-- Setas de Sincronização Circular -->
            <path d="M -20,-30 Q 5,-40 25,-30" stroke="#5eead4" stroke-width="4" stroke-dasharray="4,4" fill="none"/>
            <path d="M 50,20 Q 30,50 0,40" stroke="#5eead4" stroke-width="4" stroke-dasharray="4,4" fill="none"/>
        """
    },
    {
        "id": "22",
        "categoria": "Gestão Financeira",
        "cat_slug": "financeiro",
        "titulo": "Gestão Financeira",
        "subtitulo": "Contas, caixa e conciliações em uma só tela.",
        "icon_svg": """
            <!-- Carteira Central com Setas de Entrada (Receita) e Saída (Despesa) -->
            <rect x="-85" y="-55" width="170" height="120" rx="16" stroke="#ffffff" stroke-width="6" fill="none"/>
            <path d="M -85,-20 L 45,-20 Q 85,-20 85,10 Q 85,40 45,40 L -85,40" stroke="#ffffff" stroke-width="5" fill="none"/>
            <circle cx="55" cy="10" r="6" fill="#34d399"/>
            <!-- Seta Entrada (Receita / Menta) -->
            <line x1="-125" y1="-100" x2="-65" y2="-65" stroke="#34d399" stroke-width="6" stroke-linecap="round"/>
            <polyline points="-95,-65 -65,-65 -65,-95" stroke="#34d399" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            <!-- Seta Saída (Despesa / Branco) -->
            <line x1="65" y1="65" x2="125" y2="100" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>
            <polyline points="95,100 125,100 125,70" stroke="#ffffff" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
        """
    },
    {
        "id": "23",
        "categoria": "Gestão Financeira",
        "cat_slug": "financeiro",
        "titulo": "DRE + Balancete",
        "subtitulo": "Informação contábil organizada e auditável.",
        "icon_svg": """
            <!-- Gráfico Contábil de Duas Colunas (Débito e Crédito) com Documento -->
            <rect x="-95" y="-110" width="190" height="220" rx="14" stroke="#ffffff" stroke-width="6" fill="none"/>
            <!-- Linha divisória contábil -->
            <line x1="0" y1="-70" x2="0" y2="80" stroke="#ffffff" stroke-width="4" stroke-dasharray="6,4"/>
            <!-- Coluna Débito -->
            <rect x="-70" y="0" width="50" height="70" fill="#ffffff"/>
            <text x="-45" y="-30" font-family="'Inter', sans-serif" font-size="16" font-weight="700" fill="#ffffff" text-anchor="middle">DÉB</text>
            <!-- Coluna Crédito -->
            <rect x="20" y="-20" width="50" height="90" fill="#34d399"/>
            <text x="45" y="-30" font-family="'Inter', sans-serif" font-size="16" font-weight="700" fill="#34d399" text-anchor="middle">CRÉD</text>
        """
    },
    {
        "id": "24",
        "categoria": "Gestão Financeira",
        "cat_slug": "financeiro",
        "titulo": "Do Simples ao Completo",
        "subtitulo": "Use apenas o nível de gestão que você precisa.",
        "icon_svg": """
            <!-- Interface em Dois Níveis com Chave Seletora Switch -->
            <!-- Nível Simples -->
            <rect x="-110" y="-95" width="220" height="65" rx="12" stroke="#ffffff" stroke-width="5" fill="none"/>
            <line x1="-80" y1="-62" x2="-20" y2="-62" stroke="#ffffff" stroke-width="4"/>
            <circle cx="65" cy="-62" r="10" stroke="#ffffff" stroke-width="4" fill="none"/>
            <!-- Chave Seletora (Toggle Switch) Central -->
            <rect x="-40" y="-12" width="80" height="34" rx="17" stroke="#34d399" stroke-width="5" fill="#081722"/>
            <circle cx="16" cy="5" r="10" fill="#34d399"/>
            <!-- Nível Completo / Avançado -->
            <rect x="-110" y="45" width="220" height="75" rx="12" stroke="#34d399" stroke-width="5" fill="none"/>
            <line x1="-80" y1="75" x2="30" y2="75" stroke="#34d399" stroke-width="4"/>
            <line x1="-80" y1="95" x2="-10" y2="95" stroke="#34d399" stroke-width="4"/>
            <rect x="55" y="65" width="25" height="30" rx="4" fill="#34d399"/>
        """
    },
    {
        "id": "25",
        "categoria": "Gestão Financeira",
        "cat_slug": "financeiro",
        "titulo": "Conciliação Bancária",
        "subtitulo": "Importe OFX e CNAB e reduza tarefas manuais.",
        "icon_svg": """
            <!-- Prédio de Banco com Setas Circulares e Checks -->
            <!-- Fachada do Banco -->
            <polygon points="-80,-40 0,-90 80,-40" stroke="#ffffff" stroke-width="6" fill="none"/>
            <rect x="-65" y="-40" width="130" height="85" stroke="#ffffff" stroke-width="6" fill="none"/>
            <line x1="-35" y1="-40" x2="-35" y2="45" stroke="#ffffff" stroke-width="5"/>
            <line x1="0" y1="-40" x2="0" y2="45" stroke="#ffffff" stroke-width="5"/>
            <line x1="35" y1="-40" x2="35" y2="45" stroke="#ffffff" stroke-width="5"/>
            <!-- Setas de Conciliação Circular -->
            <path d="M -115,10 A 120 120 0 0 1 115,10" stroke="#34d399" stroke-width="5" stroke-dasharray="8,6" fill="none"/>
            <circle cx="115" cy="10" r="14" stroke="#34d399" stroke-width="4" fill="#081722"/>
            <polyline points="109,10 114,15 122,5" stroke="#34d399" stroke-width="4" fill="none" stroke-linecap="round"/>
        """
    },
    {
        "id": "26",
        "categoria": "Gestão Financeira",
        "cat_slug": "financeiro",
        "titulo": "Cobranças Automatizadas",
        "subtitulo": "Boleto e PIX integrados ao seu financeiro.",
        "icon_svg": """
            <!-- Boleto com Código de Barras e QR Code PIX -->
            <rect x="-90" y="-110" width="180" height="230" rx="14" stroke="#ffffff" stroke-width="6" fill="none"/>
            <!-- Código de barras do boleto -->
            <line x1="-65" y1="-75" x2="65" y2="-75" stroke="#ffffff" stroke-width="4"/>
            <line x1="-65" y1="-50" x2="30" y2="-50" stroke="#ffffff" stroke-width="4"/>
            <!-- Logo PIX Estilizado -->
            <polygon points="0,-15 35,20 0,55 -35,20" stroke="#34d399" stroke-width="6" fill="none"/>
            <!-- Linhas de código de barras no rodapé -->
            <line x1="-60" y1="85" x2="-60" y2="105" stroke="#ffffff" stroke-width="3"/>
            <line x1="-48" y1="85" x2="-48" y2="105" stroke="#ffffff" stroke-width="6"/>
            <line x1="-32" y1="85" x2="-32" y2="105" stroke="#ffffff" stroke-width="2"/>
            <line x1="-20" y1="85" x2="-20" y2="105" stroke="#ffffff" stroke-width="5"/>
            <line x1="0" y1="85" x2="0" y2="105" stroke="#ffffff" stroke-width="4"/>
            <line x1="20" y1="85" x2="20" y2="105" stroke="#ffffff" stroke-width="6"/>
            <line x1="45" y1="85" x2="45" y2="105" stroke="#ffffff" stroke-width="4"/>
        """
    },
    {
        "id": "27",
        "categoria": "Gestão Financeira",
        "cat_slug": "financeiro",
        "titulo": "Centro de Custos",
        "subtitulo": "Analise resultados por setor, projeto ou filial.",
        "icon_svg": """
            <!-- Moeda Central Ramificada para 3 Setores -->
            <circle cx="0" cy="-60" r="38" stroke="#34d399" stroke-width="6" fill="none"/>
            <text x="0" y="-46" font-family="'Inter', sans-serif" font-size="34" font-weight="700" fill="#34d399" text-anchor="middle">$</text>
            <!-- Ramificações Lineares -->
            <line x1="0" y1="-22" x2="0" y2="25" stroke="#ffffff" stroke-width="5"/>
            <line x1="-90" y1="25" x2="90" y2="25" stroke="#ffffff" stroke-width="5"/>
            <!-- Setor 1 -->
            <line x1="-90" y1="25" x2="-90" y2="60" stroke="#ffffff" stroke-width="5"/>
            <rect x="-120" y="60" width="60" height="40" rx="8" stroke="#ffffff" stroke-width="4" fill="none"/>
            <!-- Setor 2 -->
            <line x1="0" y1="25" x2="0" y2="60" stroke="#ffffff" stroke-width="5"/>
            <rect x="-30" y="60" width="60" height="40" rx="8" stroke="#ffffff" stroke-width="4" fill="none"/>
            <!-- Setor 3 -->
            <line x1="90" y1="25" x2="90" y2="60" stroke="#ffffff" stroke-width="5"/>
            <rect x="60" y="60" width="60" height="40" rx="8" stroke="#ffffff" stroke-width="4" fill="none"/>
        """
    },

    # 28 a 31: CANAIS DE VENDA E COMUNICAÇÃO
    {
        "id": "28",
        "categoria": "Comunicação & Vendas",
        "cat_slug": "comunicacao",
        "titulo": "Integração Nuvemshop",
        "subtitulo": "Pedidos, estoque e faturamento sincronizados.",
        "icon_svg": """
            <!-- Sacola de E-commerce Conectada a Caixa e Documento Fiscal -->
            <rect x="-55" y="-50" width="110" height="120" rx="14" stroke="#ffffff" stroke-width="6" fill="none"/>
            <path d="M -25,-50 Q -25,-90 0,-90 Q 25,-90 25,-50" stroke="#ffffff" stroke-width="6" fill="none"/>
            <circle cx="0" cy="5" r="14" stroke="#34d399" stroke-width="4" fill="none"/>
            <!-- Caixa de Estoque (Noroeste) -->
            <rect x="-125" y="-95" width="45" height="40" rx="6" stroke="#34d399" stroke-width="4" fill="none"/>
            <line x1="-80" y1="-75" x2="-35" y2="-50" stroke="#5eead4" stroke-width="3" stroke-dasharray="4,4"/>
            <!-- Documento Fiscal (Nordeste) -->
            <rect x="80" y="-95" width="45" height="50" rx="6" stroke="#34d399" stroke-width="4" fill="none"/>
            <line x1="80" y1="-75" x2="35" y2="-50" stroke="#5eead4" stroke-width="3" stroke-dasharray="4,4"/>
        """
    },
    {
        "id": "29",
        "categoria": "Comunicação & Vendas",
        "cat_slug": "comunicacao",
        "titulo": "WhatsApp Inteligente",
        "subtitulo": "Atenda, venda e envie documentos em um só canal.",
        "icon_svg": """
            <!-- Balão de Mensagem com Robô Inteligente e Documento -->
            <path d="M -100,-70 Q -100,-110 0,-110 Q 100,-110 100,-70 Q 100,0 30,10 L 10,45 L -20,10 Q -100,10 -100,-70 Z" stroke="#ffffff" stroke-width="6" fill="none" stroke-linejoin="round"/>
            <!-- Cabeça do Robô Linear no Centro -->
            <rect x="-40" y="-85" width="80" height="55" rx="12" stroke="#34d399" stroke-width="5" fill="none"/>
            <circle cx="-18" cy="-58" r="6" fill="#34d399"/>
            <circle cx="18" cy="-58" r="6" fill="#34d399"/>
            <line x1="0" y1="-85" x2="0" y2="-98" stroke="#34d399" stroke-width="4"/>
            <circle cx="0" cy="-102" r="3" fill="#34d399"/>
            <!-- Documento e Carrinho ao Redor -->
            <rect x="85" y="20" width="30" height="40" rx="4" stroke="#5eead4" stroke-width="3" fill="none"/>
        """
    },
    {
        "id": "30",
        "categoria": "Comunicação & Vendas",
        "cat_slug": "comunicacao",
        "titulo": "Telegram + SMS",
        "subtitulo": "Notificações automáticas para seus clientes.",
        "icon_svg": """
            <!-- Dois Balões de Notificação com Avião de Papel Linear -->
            <rect x="-110" y="-80" width="130" height="90" rx="16" stroke="#ffffff" stroke-width="6" fill="none"/>
            <path d="M -70,10 L -90,35 L -45,10 Z" fill="#ffffff"/>
            <!-- Segundo balão com Avião de Papel -->
            <rect x="-10" y="-20" width="130" height="90" rx="16" stroke="#34d399" stroke-width="6" fill="#081722"/>
            <path d="M 15,20 L 75,0 L 45,45 L 35,28 Z" stroke="#34d399" stroke-width="4" fill="none" stroke-linejoin="round"/>
            <!-- Ondas de Sinal -->
            <path d="M 85,-60 Q 110,-40 120,-10" stroke="#5eead4" stroke-width="3" fill="none"/>
        """
    },
    {
        "id": "31",
        "categoria": "Comunicação & Vendas",
        "cat_slug": "comunicacao",
        "titulo": "E-mails Automatizados",
        "subtitulo": "Envie notas, boletos e pedidos automaticamente.",
        "icon_svg": """
            <!-- Envelope Aberto com Documento e Engrenagem -->
            <path d="M -100,-20 L -100,70 L 100,70 L 100,-20 L 0,40 Z" stroke="#ffffff" stroke-width="6" fill="none"/>
            <polyline points="-100,-20 0,-80 100,-20" stroke="#ffffff" stroke-width="6" fill="none"/>
            <!-- Documento saindo do envelope -->
            <rect x="-55" y="-115" width="110" height="90" rx="8" stroke="#34d399" stroke-width="5" fill="#081722"/>
            <line x1="-35" y1="-90" x2="35" y2="-90" stroke="#34d399" stroke-width="4"/>
            <line x1="-35" y1="-65" x2="10" y2="-65" stroke="#34d399" stroke-width="4"/>
            <!-- Pequena engrenagem discreta -->
            <circle cx="85" cy="-85" r="16" stroke="#5eead4" stroke-width="4" stroke-dasharray="6,4" fill="none"/>
        """
    },

    # 32 a 36: NUVEM & SEGURANÇA
    {
        "id": "32",
        "categoria": "Nuvem & Segurança",
        "cat_slug": "seguranca",
        "titulo": "Segurança em Duas Etapas",
        "subtitulo": "Mais proteção para usuários e dados.",
        "icon_svg": """
            <!-- Escudo com Cadeado e Código de 6 Dígitos -->
            <path d="M -90,-80 Q 0,-115 90,-80 L 90,20 Q 90,110 0,145 Q -90,110 -90,20 Z" stroke="#ffffff" stroke-width="6" fill="none" stroke-linejoin="round"/>
            <!-- Cadeado Central -->
            <rect x="-35" y="-15" width="70" height="55" rx="8" stroke="#34d399" stroke-width="5" fill="none"/>
            <path d="M -20,-15 L -20,-40 Q 0,-60 20,-40 L 20,-15" stroke="#34d399" stroke-width="5" fill="none"/>
            <circle cx="0" cy="12" r="5" fill="#34d399"/>
            <!-- Código 6 dígitos estilizado -->
            <text x="0" y="85" font-family="'Inter', sans-serif" font-size="20" font-weight="800" fill="#5eead4" text-anchor="middle" letter-spacing="4">● ● ● ● ● ●</text>
        """
    },
    {
        "id": "33",
        "categoria": "Nuvem & Segurança",
        "cat_slug": "seguranca",
        "titulo": "Controle de Acessos",
        "subtitulo": "Defina exatamente o que cada usuário pode acessar.",
        "icon_svg": """
            <!-- Usuário Central com Escudo e Níveis de Permissão -->
            <circle cx="0" cy="-60" r="30" stroke="#ffffff" stroke-width="6" fill="none"/>
            <path d="M -50,20 C -50,-20 50,-20 50,20" stroke="#ffffff" stroke-width="6" fill="none"/>
            <!-- 3 Chaves/Níveis Hierárquicos -->
            <rect x="-105" y="45" width="60" height="30" rx="6" stroke="#34d399" stroke-width="4" fill="none"/>
            <rect x="-30" y="45" width="60" height="30" rx="6" stroke="#34d399" stroke-width="4" fill="none"/>
            <rect x="45" y="45" width="60" height="30" rx="6" stroke="#34d399" stroke-width="4" fill="none"/>
            <circle cx="-75" cy="60" r="4" fill="#34d399"/>
            <circle cx="0" cy="60" r="4" fill="#34d399"/>
            <circle cx="75" cy="60" r="4" fill="#34d399"/>
        """
    },
    {
        "id": "34",
        "categoria": "Nuvem & Segurança",
        "cat_slug": "seguranca",
        "titulo": "Atualizações Automáticas",
        "subtitulo": "Sempre atualizado sem instalações manuais.",
        "icon_svg": """
            <!-- Nuvem com Engrenagem e Setas Circulares -->
            <path d="M -80,20 Q -115,20 -115,-15 Q -115,-45 -85,-50 Q -70,-95 -20,-95 Q 25,-95 45,-60 Q 75,-60 85,-40 Q 115,-30 115,10 Q 115,40 80,40 Z" stroke="#ffffff" stroke-width="6" fill="none"/>
            <!-- Setas Circulares de Sincronização no Centro -->
            <circle cx="0" cy="-10" r="28" stroke="#34d399" stroke-width="5" stroke-dasharray="12,6" fill="none"/>
            <polyline points="20,-20 28,-10 18,-4" stroke="#34d399" stroke-width="5" fill="none" stroke-linecap="round"/>
        """
    },
    {
        "id": "35",
        "categoria": "Nuvem & Segurança",
        "cat_slug": "seguranca",
        "titulo": "Backup Automático",
        "subtitulo": "Seus dados protegidos e sempre disponíveis.",
        "icon_svg": """
            <!-- Nuvem com Escudo e Servidores em Camadas -->
            <path d="M -60,-30 Q -95,-30 -95,-60 Q -95,-90 -65,-95 Q -50,-130 0,-130 Q 40,-130 60,-100 Q 95,-100 95,-60 Q 95,-30 60,-30 Z" stroke="#ffffff" stroke-width="5" fill="none"/>
            <!-- Dois Servidores Redundantes na Base -->
            <rect x="-80" y="0" width="160" height="40" rx="8" stroke="#34d399" stroke-width="5" fill="#081722"/>
            <circle cx="-50" cy="20" r="4" fill="#34d399"/>
            <line x1="-30" y1="20" x2="50" y2="20" stroke="#34d399" stroke-width="4"/>
            <rect x="-80" y="55" width="160" height="40" rx="8" stroke="#34d399" stroke-width="5" fill="#081722"/>
            <circle cx="-50" cy="75" r="4" fill="#34d399"/>
            <line x1="-30" y1="75" x2="50" y2="75" stroke="#34d399" stroke-width="4"/>
            <!-- Seta de Upload / Backup -->
            <polyline points="-18,-5 0,-25 18,-5" stroke="#5eead4" stroke-width="5" fill="none" stroke-linecap="round"/>
        """
    },
    {
        "id": "36",
        "categoria": "Nuvem & Segurança",
        "cat_slug": "seguranca",
        "titulo": "Gestão Multiempresa",
        "subtitulo": "Controle matriz, filiais e empresas em um só acesso.",
        "icon_svg": """
            <!-- Empresa Matriz Conectada a 3 Filiais -->
            <path d="M -40,-60 L 0,-95 L 40,-60 L 40,0 L -40,0 Z" stroke="#34d399" stroke-width="6" fill="none"/>
            <rect x="-12" y="-30" width="24" height="30" stroke="#34d399" stroke-width="4" fill="none"/>
            <!-- Linhas de Conexão -->
            <line x1="0" y1="0" x2="0" y2="45" stroke="#ffffff" stroke-width="5"/>
            <line x1="-90" y1="45" x2="90" y2="45" stroke="#ffffff" stroke-width="5"/>
            <!-- Filiais -->
            <rect x="-110" y="55" width="40" height="45" rx="6" stroke="#ffffff" stroke-width="4" fill="none"/>
            <rect x="-20" y="55" width="40" height="45" rx="6" stroke="#ffffff" stroke-width="4" fill="none"/>
            <rect x="70" y="55" width="40" height="45" rx="6" stroke="#ffffff" stroke-width="4" fill="none"/>
        """
    },

    # 37 a 41: TRUDATA BI
    {
        "id": "37",
        "categoria": "TruData BI",
        "cat_slug": "bi",
        "titulo": "Matriz RFV",
        "subtitulo": "Descubra seus melhores clientes e quem está se afastando.",
        "icon_svg": """
            <!-- Matriz 5x5 com Quadrados Destacados e Eixos R x F -->
            <!-- Eixos -->
            <line x1="-90" y1="90" x2="-90" y2="-90" stroke="#ffffff" stroke-width="5"/>
            <line x1="-90" y1="90" x2="90" y2="90" stroke="#ffffff" stroke-width="5"/>
            <text x="-90" y="-105" font-family="'Inter', sans-serif" font-size="16" font-weight="700" fill="#34d399">Frequência</text>
            <text x="85" y="115" font-family="'Inter', sans-serif" font-size="16" font-weight="700" fill="#34d399">Recência</text>
            <!-- Células da Matriz -->
            <rect x="-70" y="-70" width="26" height="26" rx="4" fill="#34d399"/>
            <rect x="-35" y="-70" width="26" height="26" rx="4" fill="#34d399"/>
            <rect x="0" y="-70" width="26" height="26" rx="4" stroke="#ffffff" stroke-width="3" fill="none"/>
            <rect x="35" y="-70" width="26" height="26" rx="4" stroke="#ffffff" stroke-width="3" fill="none"/>
            <rect x="-70" y="-35" width="26" height="26" rx="4" fill="#34d399"/>
            <rect x="-35" y="-35" width="26" height="26" rx="4" stroke="#ffffff" stroke-width="3" fill="none"/>
            <rect x="0" y="-35" width="26" height="26" rx="4" stroke="#ffffff" stroke-width="3" fill="none"/>
            <rect x="35" y="-35" width="26" height="26" rx="4" stroke="#ffffff" stroke-width="3" fill="none"/>
            <rect x="-70" y="0" width="26" height="26" rx="4" stroke="#ffffff" stroke-width="3" fill="none"/>
            <rect x="-35" y="0" width="26" height="26" rx="4" stroke="#ffffff" stroke-width="3" fill="none"/>
            <rect x="0" y="0" width="26" height="26" rx="4" stroke="#ffffff" stroke-width="3" fill="none"/>
            <rect x="35" y="0" width="26" height="26" rx="4" fill="#5eead4"/>
            <rect x="-70" y="35" width="26" height="26" rx="4" stroke="#ffffff" stroke-width="3" fill="none"/>
            <rect x="-35" y="35" width="26" height="26" rx="4" stroke="#ffffff" stroke-width="3" fill="none"/>
            <rect x="0" y="35" width="26" height="26" rx="4" stroke="#ffffff" stroke-width="3" fill="none"/>
            <rect x="35" y="35" width="26" height="26" rx="4" stroke="#ffffff" stroke-width="3" fill="none"/>
        """
    },
    {
        "id": "38",
        "categoria": "TruData BI",
        "cat_slug": "bi",
        "titulo": "Indicadores em Tempo Real",
        "subtitulo": "Faturamento, ticket, vendas e margem sempre atualizados.",
        "icon_svg": """
            <!-- Dashboard com Velocímetro e Gráfico de Linha Ascendente -->
            <rect x="-105" y="-95" width="210" height="190" rx="16" stroke="#ffffff" stroke-width="6" fill="none"/>
            <!-- Velocímetro -->
            <path d="M -60,-20 A 40 40 0 0 1 0,-20" stroke="#34d399" stroke-width="6" fill="none"/>
            <line x1="-30" y1="-20" x2="-10" y2="-45" stroke="#34d399" stroke-width="4" stroke-linecap="round"/>
            <!-- Gráfico de Linha Ascendente -->
            <polyline points="20,10 40,-15 65,-5 85,-45" stroke="#34d399" stroke-width="5" fill="none" stroke-linecap="round"/>
            <circle cx="85" cy="-45" r="5" fill="#34d399"/>
            <!-- Linhas de Métricas -->
            <line x1="-75" y1="35" x2="0" y2="35" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>
            <line x1="-75" y1="60" x2="55" y2="60" stroke="#ffffff" stroke-width="5" stroke-linecap="round"/>
        """
    },
    {
        "id": "39",
        "categoria": "TruData BI",
        "cat_slug": "bi",
        "titulo": "Curva ABC + Heatmaps",
        "subtitulo": "Entenda produtos, cores e tamanhos que mais vendem.",
        "icon_svg": """
            <!-- Gráfico Curva ABC com Matriz de Calor e Letras A, B, C -->
            <!-- Curva suave decrescente ABC -->
            <path d="M -90,-80 Q -30,-60 10,20 T 90,80" stroke="#34d399" stroke-width="6" fill="none"/>
            <!-- Barras A, B, C -->
            <rect x="-85" y="-30" width="35" height="110" fill="#34d399"/>
            <text x="-67" y="10" font-family="'Inter', sans-serif" font-size="20" font-weight="800" fill="#081722" text-anchor="middle">A</text>
            <rect x="-35" y="10" width="35" height="70" fill="#5eead4"/>
            <text x="-17" y="45" font-family="'Inter', sans-serif" font-size="18" font-weight="800" fill="#081722" text-anchor="middle">B</text>
            <rect x="15" y="45" width="35" height="35" fill="#ffffff"/>
            <text x="32" y="70" font-family="'Inter', sans-serif" font-size="16" font-weight="800" fill="#081722" text-anchor="middle">C</text>
        """
    },
    {
        "id": "40",
        "categoria": "TruData BI",
        "cat_slug": "bi",
        "titulo": "PivotGrid Interativo",
        "subtitulo": "Explore seus dados do seu jeito.",
        "icon_svg": """
            <!-- Tabela Dinâmica com Setas de Reorganização e Filtros -->
            <rect x="-95" y="-85" width="190" height="170" rx="12" stroke="#ffffff" stroke-width="6" fill="none"/>
            <line x1="-95" y1="-40" x2="95" y2="-40" stroke="#ffffff" stroke-width="5"/>
            <line x1="-30" y1="-85" x2="-30" y2="85" stroke="#ffffff" stroke-width="5"/>
            <line x1="30" y1="-85" x2="30" y2="85" stroke="#ffffff" stroke-width="5"/>
            <!-- Setas de Reorganização / Pivot -->
            <path d="M -5,15 L 15,-5 M 15,-5 L 5,-5 M 15,-5 L 15,5" stroke="#34d399" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M 5,-15 L -15,5 M -15,5 L -5,5 M -15,5 L -15,-5" stroke="#34d399" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
        """
    },
    {
        "id": "41",
        "categoria": "TruData BI",
        "cat_slug": "bi",
        "titulo": "Trudata BI",
        "subtitulo": "Dados sincronizados e disponíveis de qualquer lugar.",
        "icon_svg": """
            <!-- Dashboard Conectado à Nuvem e Multiempresas -->
            <rect x="-85" y="-30" width="170" height="120" rx="14" stroke="#ffffff" stroke-width="6" fill="none"/>
            <line x1="-60" y1="15" x2="-20" y2="15" stroke="#34d399" stroke-width="5"/>
            <line x1="-60" y1="45" x2="20" y2="45" stroke="#34d399" stroke-width="5"/>
            <!-- Nuvem de Dados no Topo -->
            <path d="M -45,-55 Q -75,-55 -75,-80 Q -75,-105 -50,-110 Q -35,-140 0,-140 Q 35,-140 50,-110 Q 75,-110 75,-80 Q 75,-55 45,-55 Z" stroke="#34d399" stroke-width="5" fill="#081722"/>
            <!-- Setas de Sincronização Contínua -->
            <polyline points="-10,-45 0,-30 10,-45" stroke="#5eead4" stroke-width="4" fill="none" stroke-linecap="round"/>
        """
    },

    # 42 e 43: MÓDULOS ESPECIALIZADOS
    {
        "id": "42",
        "categoria": "Módulos Especializados",
        "cat_slug": "modulos",
        "titulo": "Gestão para Farmácias",
        "subtitulo": "SNGPC, PBM, controlados, lote e validade.",
        "icon_svg": """
            <!-- Cruz Farmacêutica com Cápsula e Escudo ANVISA -->
            <!-- Cruz de Farmácia -->
            <path d="M -25,-110 L 25,-110 L 25,-60 L 75,-60 L 75,-10 L 25,-10 L 25,40 L -25,40 L -25,-10 L -75,-10 L -75,-60 L -25,-60 Z" stroke="#ffffff" stroke-width="6" fill="none" stroke-linejoin="round"/>
            <!-- Cápsula de Medicamento (Verde Menta) -->
            <rect x="-55" y="55" width="110" height="45" rx="22" stroke="#34d399" stroke-width="5" fill="none"/>
            <line x1="0" y1="55" x2="0" y2="100" stroke="#34d399" stroke-width="5"/>
            <!-- Escudo de Conformidade ANVISA -->
            <circle cx="85" cy="-75" r="15" stroke="#5eead4" stroke-width="4" fill="#081722"/>
            <polyline points="79,-75 83,-71 91,-79" stroke="#5eead4" stroke-width="3" fill="none" stroke-linecap="round"/>
        """
    },
    {
        "id": "43",
        "categoria": "Módulos Especializados",
        "cat_slug": "modulos",
        "titulo": "Ordem de Serviço",
        "subtitulo": "Veículo, peças, mão de obra e histórico completos.",
        "icon_svg": """
            <!-- Automóvel com Chave Inglesa e Prancheta de OS -->
            <!-- Carro Linear -->
            <path d="M -110,40 L -90,-5 L -50,-25 L 30,-25 L 70,-5 L 90,40 Z" stroke="#ffffff" stroke-width="6" fill="none"/>
            <circle cx="-65" cy="45" r="18" stroke="#ffffff" stroke-width="5" fill="#081722"/>
            <circle cx="45" cy="45" r="18" stroke="#ffffff" stroke-width="5" fill="#081722"/>
            <!-- Chave Inglesa em Menta -->
            <path d="M -15,-105 L 45,-45 L 30,-30 L -30,-90 Z" stroke="#34d399" stroke-width="5" fill="none"/>
            <circle cx="-25" cy="-95" r="14" stroke="#34d399" stroke-width="4" fill="none"/>
            <!-- Prancheta de OS -->
            <rect x="75" y="-85" width="50" height="65" rx="6" stroke="#5eead4" stroke-width="3" fill="none"/>
        """
    },

    # 44 a 49: SEGMENTOS ATENDIDOS
    {
        "id": "44",
        "categoria": "Segmentos Atendidos",
        "cat_slug": "segmentos",
        "titulo": "Confecção e Calçados",
        "subtitulo": "Grade completa, PDV rápido e vendas integradas.",
        "icon_svg": """
            <!-- Camiseta e Calçado com Grade -->
            <path d="M -100,-40 L -75,-60 Q -50,-40 -25,-60 L 0,-40 L -15,-5 L -30,-15 L -30,60 L -85,60 L -85,-15 L -100,-5 Z" stroke="#ffffff" stroke-width="5" fill="none" stroke-linejoin="round"/>
            <!-- Calçado / Sapato Linear -->
            <path d="M 15,20 Q 35,-10 65,-10 L 105,10 L 105,50 L 15,50 Z" stroke="#34d399" stroke-width="5" fill="none" stroke-linejoin="round"/>
            <line x1="85" y1="50" x2="85" y2="35" stroke="#34d399" stroke-width="4"/>
        """
    },
    {
        "id": "45",
        "categoria": "Segmentos Atendidos",
        "cat_slug": "segmentos",
        "titulo": "Comércio em Geral",
        "subtitulo": "Venda mais rápido e controle todas as suas lojas.",
        "icon_svg": """
            <!-- Fachada de Loja com Carrinho e Código de Barras -->
            <polygon points="-90,-30 0,-75 90,-30" stroke="#ffffff" stroke-width="6" fill="none"/>
            <rect x="-75" y="-30" width="150" height="100" stroke="#ffffff" stroke-width="6" fill="none"/>
            <!-- Toldo da Loja -->
            <path d="M -75,-30 Q -50,-10 -25,-30 Q 0,-10 25,-30 Q 50,-10 75,-30" stroke="#34d399" stroke-width="5" fill="none"/>
            <!-- Porta com Carrinho -->
            <rect x="-25" y="10" width="50" height="60" stroke="#34d399" stroke-width="4" fill="none"/>
        """
    },
    {
        "id": "46",
        "categoria": "Segmentos Atendidos",
        "cat_slug": "segmentos",
        "titulo": "Gestão para Oficinas",
        "subtitulo": "OS, veículos, peças e histórico em um só lugar.",
        "icon_svg": """
            <!-- Automóvel com Engrenagem e Chave -->
            <path d="M -80,30 L -60,-10 L -30,-25 L 30,-25 L 60,-10 L 80,30 Z" stroke="#ffffff" stroke-width="6" fill="none"/>
            <circle cx="-45" cy="35" r="16" stroke="#ffffff" stroke-width="5" fill="#081722"/>
            <circle cx="45" cy="35" r="16" stroke="#ffffff" stroke-width="5" fill="#081722"/>
            <!-- Engrenagem no Topo -->
            <circle cx="0" cy="-65" r="25" stroke="#34d399" stroke-width="5" stroke-dasharray="10,5" fill="none"/>
            <circle cx="0" cy="-65" r="8" fill="#34d399"/>
        """
    },
    {
        "id": "47",
        "categoria": "Segmentos Atendidos",
        "cat_slug": "segmentos",
        "titulo": "Escritórios Contábeis",
        "subtitulo": "Gerencie sua carteira de empresas com eficiência.",
        "icon_svg": """
            <!-- Prédio de Escritório Conectado a Documentos Fiscais -->
            <rect x="-45" y="-95" width="90" height="160" rx="8" stroke="#ffffff" stroke-width="6" fill="none"/>
            <!-- Janelas em grade -->
            <line x1="-25" y1="-70" x2="-10" y2="-70" stroke="#ffffff" stroke-width="4"/>
            <line x1="10" y1="-70" x2="25" y2="-70" stroke="#ffffff" stroke-width="4"/>
            <line x1="-25" y1="-40" x2="-10" y2="-40" stroke="#ffffff" stroke-width="4"/>
            <line x1="10" y1="-40" x2="25" y2="-40" stroke="#ffffff" stroke-width="4"/>
            <line x1="-25" y1="-10" x2="-10" y2="-10" stroke="#ffffff" stroke-width="4"/>
            <line x1="10" y1="-10" x2="25" y2="-10" stroke="#ffffff" stroke-width="4"/>
            <!-- Documentos fluindo -->
            <rect x="-115" y="-30" width="45" height="55" rx="6" stroke="#34d399" stroke-width="4" fill="none"/>
            <rect x="70" y="-30" width="45" height="55" rx="6" stroke="#34d399" stroke-width="4" fill="none"/>
        """
    },
    {
        "id": "48",
        "categoria": "Segmentos Atendidos",
        "cat_slug": "segmentos",
        "titulo": "Prestação de Serviços",
        "subtitulo": "OS, NFS-e e faturamento em uma gestão completa.",
        "icon_svg": """
            <!-- Maleta de Serviços com Engrenagem e Documento -->
            <rect x="-85" y="-45" width="170" height="120" rx="14" stroke="#ffffff" stroke-width="6" fill="none"/>
            <path d="M -35,-45 L -35,-80 L 35,-80 L 35,-45" stroke="#ffffff" stroke-width="6" fill="none"/>
            <!-- Fechadura Menta -->
            <rect x="-15" y="-15" width="30" height="25" rx="4" fill="#34d399"/>
            <!-- Engrenagem Lateral -->
            <circle cx="85" cy="-45" r="18" stroke="#5eead4" stroke-width="4" stroke-dasharray="6,3" fill="none"/>
        """
    },
    {
        "id": "49",
        "categoria": "Segmentos Atendidos",
        "cat_slug": "segmentos",
        "titulo": "Farmácias e Drogarias",
        "subtitulo": "Controle especializado para a rotina farmacêutica.",
        "icon_svg": """
            <!-- Cruz com Medicamento e Calendário SNGPC -->
            <rect x="-15" y="-95" width="30" height="110" rx="6" fill="#34d399"/>
            <rect x="-55" y="-55" width="110" height="30" rx="6" fill="#34d399"/>
            <!-- Frasco de Remédio -->
            <rect x="-45" y="35" width="90" height="70" rx="10" stroke="#ffffff" stroke-width="5" fill="none"/>
            <line x1="-25" y1="20" x2="25" y2="20" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>
        """
    },

    # 50 a 52: DESKTOP + NUVEM + BI
    {
        "id": "50",
        "categoria": "Ecossistema Completo",
        "cat_slug": "ecossistema",
        "titulo": "Trudata Desktop",
        "subtitulo": "Robustez e operação mesmo quando a internet falha.",
        "icon_svg": """
            <!-- Monitor de Computador Linear com Escudo e Símbolo Offline -->
            <rect x="-105" y="-95" width="210" height="145" rx="14" stroke="#ffffff" stroke-width="6" fill="none"/>
            <line x1="0" y1="50" x2="0" y2="90" stroke="#ffffff" stroke-width="6"/>
            <line x1="-55" y1="90" x2="55" y2="90" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>
            <!-- Escudo de Robustez no Centro -->
            <path d="M -30,-45 Q 0,-60 30,-45 L 30,-10 Q 30,25 0,40 Q -30,25 -30,-10 Z" stroke="#34d399" stroke-width="5" fill="none"/>
            <polyline points="-12,-10 -2,0 15,-15" stroke="#34d399" stroke-width="4" fill="none" stroke-linecap="round"/>
        """
    },
    {
        "id": "51",
        "categoria": "Ecossistema Completo",
        "cat_slug": "ecossistema",
        "titulo": "Trudata Nuvem",
        "subtitulo": "Acesse sua empresa de onde estiver.",
        "icon_svg": """
            <!-- Nuvem Conectada a Notebook e Tablet -->
            <path d="M -70,-30 Q -105,-30 -105,-60 Q -105,-90 -75,-95 Q -60,-135 -10,-135 Q 35,-135 55,-100 Q 95,-100 95,-60 Q 95,-30 65,-30 Z" stroke="#34d399" stroke-width="6" fill="none"/>
            <!-- Notebook no Centro -->
            <rect x="-55" y="10" width="110" height="70" rx="8" stroke="#ffffff" stroke-width="5" fill="none"/>
            <line x1="-75" y1="80" x2="75" y2="80" stroke="#ffffff" stroke-width="6" stroke-linecap="round"/>
        """
    },
    {
        "id": "52",
        "categoria": "Ecossistema Completo",
        "cat_slug": "ecossistema",
        "titulo": "Um Ecossistema Completo",
        "subtitulo": "Desktop + Nuvem + BI na combinação certa para sua empresa.",
        "icon_svg": """
            <!-- Trio Triangular: Desktop, Nuvem e Gráfico BI perfeitamente equilibrados -->
            <!-- Desktop (Topo) -->
            <rect x="-40" y="-125" width="80" height="55" rx="6" stroke="#ffffff" stroke-width="5" fill="none"/>
            <line x1="0" y1="-70" x2="0" y2="-55" stroke="#ffffff" stroke-width="4"/>
            <!-- Nuvem (Esquerda) -->
            <path d="M -105,65 Q -125,65 -125,45 Q -125,25 -105,25 Q -95,0 -70,0 Q -45,0 -40,20 Q -25,20 -25,45 Q -25,65 -45,65 Z" stroke="#34d399" stroke-width="5" fill="none"/>
            <!-- Gráfico BI (Direita) -->
            <rect x="35" y="10" width="75" height="55" rx="6" stroke="#ffffff" stroke-width="5" fill="none"/>
            <polyline points="45,45 60,30 75,38 95,22" stroke="#34d399" stroke-width="4" fill="none"/>
            <!-- Linhas de Interconexão Triangular -->
            <line x1="0" y1="-50" x2="-65" y2="10" stroke="#5eead4" stroke-width="4" stroke-dasharray="6,4"/>
            <line x1="0" y1="-50" x2="65" y2="10" stroke="#5eead4" stroke-width="4" stroke-dasharray="6,4"/>
            <line x1="-25" y1="45" x2="35" y2="45" stroke="#5eead4" stroke-width="4" stroke-dasharray="6,4"/>
        """
    }
]

def gerar_svg(card):
    # Template 1080x1920 (9:16)
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <defs>
    <!-- Gradiente Fundo Azul-Petróleo Escuro Elegante -->
    <radialGradient id="bg-grad-{card['id']}" cx="50%" cy="38%" r="65%">
      <stop offset="0%" stop-color="#0f2b3c"/>
      <stop offset="55%" stop-color="#091b26"/>
      <stop offset="100%" stop-color="#06121a"/>
    </radialGradient>
    <filter id="subtle-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="15" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Fundo Sólido Corporativo com Gradiente Sutil -->
  <rect width="1080" height="1920" fill="url(#bg-grad-{card['id']})"/>

  <!-- Guia Sutil de Categoria no Topo Seguro (y=280) -->
  <g transform="translate(540, 290)">
    <rect x="-140" y="-18" width="280" height="36" rx="18" fill="rgba(52, 211, 153, 0.08)" stroke="rgba(52, 211, 153, 0.25)" stroke-width="1.5"/>
    <text x="0" y="6" font-family="'Inter', -apple-system, sans-serif" font-size="14" font-weight="700" fill="#34d399" text-anchor="middle" letter-spacing="2">{card['categoria'].upper()} • {card['id']}</text>
  </g>

  <!-- Ícone Principal Flat/Linear Minimalista (Terço Superior, y=560) -->
  <g transform="translate(540, 560)">
    {card['icon_svg']}
  </g>

  <!-- Título Moderno Geométrico Bold em Branco (y=960) -->
  <text x="540" y="960" font-family="'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif" font-size="58" font-weight="800" fill="#ffffff" text-anchor="middle" letter-spacing="-0.5">
    {card['titulo']}
  </text>

  <!-- Subtítulo Regular Menor em Branco com 80% Opacidade (y=1040) -->
  <text x="540" y="1040" font-family="'Inter', -apple-system, sans-serif" font-size="32" font-weight="400" fill="rgba(255, 255, 255, 0.82)" text-anchor="middle">
    {card['subtitulo']}
  </text>

  <!-- Linha Decorativa Minimalista -->
  <line x1="490" y1="1120" x2="590" y2="1120" stroke="#34d399" stroke-width="3" stroke-linecap="round" opacity="0.6"/>

  <!-- Rodapé Padronizado com Logo Trudata (Margem de Segurança Base y=1720) -->
  <g transform="translate(540, 1720)">
    <text x="-8" y="0" font-family="'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif" font-size="32" font-weight="800" fill="rgba(255, 255, 255, 0.75)" text-anchor="middle" letter-spacing="6">TRUDATA</text>
    <circle cx="82" cy="-8" r="4.5" fill="#34d399"/>
    <text x="0" y="32" font-family="'Inter', -apple-system, sans-serif" font-size="13" font-weight="600" fill="rgba(255, 255, 255, 0.4)" text-anchor="middle" letter-spacing="3">SISTEMAS DE GESTÃO</text>
  </g>
</svg>
"""
    return svg_content

print(f"Gerando {len(CARDS)} cards de Stories em formato SVG (1080x1920)...")
cards_dados_json = []

for card in CARDS:
    svg_filename = f"card_story_{card['id']}_{card['cat_slug']}.svg"
    svg_path = os.path.join(OUTPUT_DIR, svg_filename)
    svg_code = gerar_svg(card)

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_code.strip())

    card_info = {
        "id": card["id"],
        "categoria": card["categoria"],
        "cat_slug": card["cat_slug"],
        "titulo": card["titulo"],
        "subtitulo": card["subtitulo"],
        "arquivo": svg_filename,
        "url": f"/conteudo_pronto/cards_stories/{svg_filename}",
        "dimensoes": "1080x1920 (9:16)"
    }
    cards_dados_json.append(card_info)

with open(JSON_OUTPUT, "w", encoding="utf-8") as f:
    json.dump(cards_dados_json, f, ensure_ascii=False, indent=2)

print(f"Sucesso! {len(CARDS)} arquivos SVG gerados em {OUTPUT_DIR}")
print(f"Arquivo JSON com dados salvos em {JSON_OUTPUT}")
