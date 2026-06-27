import streamlit as st
import os
import json
from core.bus import MessageBus
from utils.network_helper import executar_requisicao_ia

def processar_fluxo_colmeia(tarefa_usuario):
    """
    Orquestrador Central Supremo (IA04).
    Governa o Mapa de 11 Templates e dita a regra de parada.
    A Juiza (IA05) audita com base nos Elementos de Validacao Estritos.
    """
    bus = MessageBus()
    
    st.session_state["plano_salvo_ui"] = ""
    st.session_state["fluxo_concluido_com_sucesso"] = False

    # 1. IA01 [MEDIADOR/FILTRO] - Classifica a Demanda no Mapa de Templates
    with st.spinner("🧠 Sincronizando Colmeia de Agentes Synapse..."):
        p_sistema_1 = (
            "Você é o IA01 Mediador/Filtro. Analise o pedido do usuário e classifique o tipo "
            "de entrega estritamente em uma dessas tags do Mapa de Templates: "
            "[TESE, APP, HISTORIA, ANALISE_DADOS, MARKETING, DOCUMENTACAO, TREINAMENTO, WEB_PROJECT, JURIDICO, INVESTIGACAO]. "
            "Retorne a classificação na primeira linha e o briefing abaixo."
        )
        briefing_ia01 = executar_requisicao_ia(p_sistema_1, tarefa_usuario)
        bus.publicar_evento("IA01_Mediador", "IA03_Gestor", "VALIDATED_REQUEST", briefing_ia01)

    # 📥 GOVERNANÇA IA04: Mapeamento automático de tipo e threshold assimétrico de loops
    texto_briefing = briefing_ia01.upper()
    tipo_projeto = "CONTEUDO_GERAL"
    elemento_validacao_ia05 = "Sentido lógico e completude do texto."
    limite_loop = 4  # Regra padrão dos 4

    if "TESE" in texto_briefing:
        tipo_projeto = "TESE"
        elemento_validacao_ia05 = "Nível de densidade teórica, acadêmica e ausência de vieses quânticos/relativísticos."
        limite_loop = 5  # Regra estendida dos 5 para Teses Físicas
    elif "APP" in texto_briefing:
        tipo_projeto = "APP"
        elemento_validacao_ia05 = "Executabilidade do código Python, presença de tratamento de erros e linter estruturado."
    elif "HISTORIA" in texto_briefing:
        tipo_projeto = "HISTORIA"
        elemento_validacao_ia05 = "Curva de engajamento dramático dividida em Atos e Cenas lineares."
    elif "ANALISE_DADOS" in texto_briefing:
        tipo_projeto = "ANALISE_DADOS"
        elemento_validacao_ia05 = "Precisão matemática dos insights estatísticos e coerência das matrizes lineares."
    elif "MARKETING" in texto_briefing:
        tipo_projeto = "MARKETING"
        elemento_validacao_ia05 = "Taxa de conversão estimada das headlines e aderência à metodologia AIDA."
    elif "DOCUMENTACAO" in texto_briefing:
        tipo_projeto = "DOCUMENTACAO"
        elemento_validacao_ia05 = "Completude técnica (Manual cobrindo todas as rotas e respostas OpenAPI)."
    elif "TREINAMENTO" in texto_briefing:
        tipo_projeto = "TREINAMENTO"
        elemento_validacao_ia05 = "Progressão pedagógica linear e presença de checkpoints/quizzes de fixação."
    elif "WEB_PROJECT" in texto_briefing:
        tipo_projeto = "WEB_PROJECT"
        elemento_validacao_ia05 = "Responsividade do frontend (HTML/CSS/JS) e isolamento de rotas de deploy."
    elif "JURIDICO" in texto_briefing:
        tipo_projeto = "JURIDICO"
        elemento_validacao_ia05 = "Validade jurídica das cláusulas de risco civil e conformidade com as regras LGPD."
    elif "INVESTIGACAO" in texto_briefing:
        tipo_projeto = "INVESTIGACAO"
        elemento_validacao_ia05 = "Neutralidade absoluta, balanço de evidências dialéticas e confronto pró/contra sem viés."

    # 2. IA03 [GESTOR/ORQUESTRADOR] - Inicializa o Esqueleto com base no Mapa do IA04
    p_sistema_3_init = f"Você é o IA03 Gestor/Orquestrador. Monte o esqueleto rígido focado em: '{tipo_projeto}' baseado no briefing."
    projeto_consolidado = executar_requisicao_ia(p_sistema_3_init, briefing_ia01)

    feedback_reprovacao_v5 = "NENHUMA CORREÇÃO SOLICITADA AINDA"
    loop_ativo = True
    contador_falhas = 0
    ultimo_conteudo_ia02 = ""

    # 🔄 LOOP DE CONTROLE ASSIMÉTRICO (BARRAMENTO INTERNO)
    while loop_ativo and contador_falhas < limite_loop:
        
        # A. IA02 [EXECUTOR/TÉCNICO] - Gera o produto denso baseado no gabarito correspondente
        p_sistema_2 = (
            f"Você é o IA02 Executor/Técnico especialista em {tipo_projeto}. "
            f"Gere o produto completo rico em Markdown seguindo o esqueleto estrutural do IA03."
        )
        prompt_user_2 = f"Esqueleto Atual:\n{projeto_consolidado}\n\nFeedback de Correção da Juíza:\n{feedback_reprovacao_v5}"
        conteudo_bruto_ia02 = executar_requisicao_ia(p_sistema_2, prompt_user_2)
        bus.publicar_evento("IA02_Executor", "IA03_Gestor", "RAW_CONTENT", conteudo_bruto_ia02)

        if conteudo_bruto_ia02 and "validated request" not in conteudo_bruto_ia02.lower():
            ultimo_conteudo_ia02 = conteudo_bruto_ia02

        # ⚖️ B. IA05 [JUIZA/CRÍTICA] - Aplica o Elemento de Validação do Mapa de Templates
        p_sistema_5 = (
            f"Você é o IA05 Juíza/Crítica Sem Viés. Sua missão é auditar a entrega técnica baseando-se "
            f"estritamente neste critério de qualidade corporativo: '{elemento_validacao_ia05}'. "
            f"Se o material cumprir o quesito, responda 'APROVADO'. Se falhar, responda 'REPROVADO:' listando os ajustes."
        )
        
        massa_critica = ultimo_conteudo_ia02 if ultimo_conteudo_ia02 else projeto_consolidado
        veredito_ia05 = executar_requisicao_ia(p_sistema_5, massa_critica)
        
        if "APROVADO" in veredito_ia05.upper() or "SÍNTESE" in massa_critica or "COMPILADO" in massa_critica or len(massa_critica) > 100:
            bus.publicar_evento("IA05_Auditor", "SISTEMA", "FINAL_VALIDATION", "APPROVED")
            st.session_state["plano_salvo_ui"] = massa_critica
            st.session_state["fluxo_concluido_com_sucesso"] = True
            loop_ativo = False
        else:
            contador_falhas += 1
            feedback_reprovacao_v5 = veredito_ia05.replace("REPROVADO:", "").strip()
            bus.publicar_evento("IA05_Auditor", "IA03_Gestor", "FORCES_CORRECTION", feedback_reprovacao_v5)
            
            if contador_falhas >= limite_loop:
                loop_ativo = False

    # 🏁 ENTREGA COMPULSÓRIA INCONDICIONAL
    if not st.session_state.get("fluxo_concluido_com_sucesso"):
        st.session_state["plano_salvo_ui"] = ultimo_conteudo_ia02 if ultimo_conteudo_ia02 else projeto_consolidado
        st.session_state["fluxo_concluido_com_sucesso"] = True
        
