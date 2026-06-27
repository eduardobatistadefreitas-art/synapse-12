import streamlit as st
import os
import json
from core.bus import MessageBus
from utils.network_helper import executar_requisicao_ia

def processar_fluxo_colmeia(tarefa_usuario):
    """
    Orquestrador Central Supremo (IA04).
    Workflow corrigido contra NameError e crash de memoria.
    Garante a entrega compulsoria do que estiver na mesa do IA03.
    """
    bus = MessageBus()
    
    # Inicializacao de memoria de sessao limpa e segura
    st.session_state["plano_salvo_ui"] = ""
    st.session_state["fluxo_concluido_com_sucesso"] = False

    # 1. IA01 [MEDIADOR/FILTRO] - Classifica e Filtra Ruidos
    with st.spinner("🧠 Sincronizando Colmeia de Agentes Synapse..."):
        p_sistema_1 = (
            "Você é o IA01 Mediador/Filtro. Analise o pedido do usuário e classifique o tipo "
            "de entrega estritamente em uma dessas categorias: [TESE_FISICA, APP_PYTHON, CONTEUDO_GERAL]. "
            "Retorne a classificação na primeira linha e um briefing limpo (Validated Request) abaixo."
        )
        briefing_ia01 = executar_requisicao_ia(p_sistema_1, tarefa_usuario)
        bus.publicar_evento("IA01_Mediador", "IA03_Gestor", "VALIDATED_REQUEST", briefing_ia01)

    # Identifica o tipo de projeto para aplicar as travas da Juiza (IA05)
    tipo_projeto = "CONTEUDO_GERAL"
    if "TESE_FISICA" in briefing_ia01:
        tipo_projeto = "TESE_FISICA"
    elif "APP_PYTHON" in briefing_ia01 or "app" in tarefa_usuario.lower():
        tipo_projeto = "APP_PYTHON"

    # Define os limites estritos de estouro do laco (Regra dos 4 e Regra dos 5)
    limite_loop = 5 if tipo_projeto == "TESE_FISICA" else 4
    
    # 2. IA03 [GESTOR/ORQUESTRADOR] - Cria Esqueleto Inicial
    p_sistema_3_init = "Você é o IA03 Gestor/Orquestrador. Monte o esqueleto estrutural rigido do projeto baseado no briefing."
    projeto_consolidado = executar_requisicao_ia(p_sistema_3_init, briefing_ia01)

    # 🛠️ CURA DO BUG: Inicializa a variavel obrigatoriamente para evitar NameError no primeiro boot
    feedback_reprovacao_v5 = "NENHUMA CORREÇÃO SOLICITADA AINDA"
    loop_ativo = True
    contador_falhas = 0
    ultimo_conteudo_ia02 = ""

    # 🔄 LOOP DE PERFORMANCE E CORREÇÃO ASSIMÉTRICO (BACK TO IA02)
    while loop_ativo and contador_falhas < limite_loop:
        
        # A. IA02 [EXECUTOR/TÉCNICO] - Gera conteudo bruto (Poema, Codigo, etc.)
        p_sistema_2 = (
            "Você é o IA02 Executor/Técnico. Gere o conteúdo bruto rico (Código, Texto, Matemática, História) "
            "com base no esqueleto do IA03 e aplique as correções da Juíza se houver."
        )
        prompt_user_2 = f"Esqueleto Atual:\n{projeto_consolidado}\n\nFeedback de Correção da Juíza:\n{feedback_reprovacao_v5}"
        conteudo_bruto_ia02 = executar_requisicao_ia(p_sistema_2, prompt_user_2)
        bus.publicar_evento("IA02_Executor", "IA03_Gestor", "RAW_CONTENT", conteudo_bruto_ia02)

        # Salvaguarda de dados para o IA03 nao perder o miolo da IA
        if conteudo_bruto_ia02 and "Esqueleto Atual:" not in conteudo_bruto_ia02:
            ultimo_conteudo_ia02 = conteudo_bruto_ia02

        # C. IA05 [JUIZA/CRÍTICA] - Analisa sem Vies / Positividade
        p_sistema_5 = (
            "Você é o IA05 Juíza/Crítica. Analise o projeto consolidado sem viés. "
            "Se o material estiver completo e atender perfeitamente à demanda, responda 'APROVADO'. "
            "Se faltar profundidade, responda 'REPROVADO:' seguido das falhas encontradas."
        )
        
        massa_critica = ultimo_conteudo_ia02 if ultimo_conteudo_ia02 else projeto_consolidado
        veredito_ia05 = executar_requisicao_ia(p_sistema_5, massa_critica)
        
        if "APROVADO" in veredito_ia05.upper():
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

    # 🏁 ENTREGA COMPULSÓRIA SEM QUEDAS (MANDATO DO DIRETOR)
    if not st.session_state.get("fluxo_concluido_com_sucesso"):
        entrega_final = ultimo_conteudo_ia02 if ultimo_conteudo_ia02 else projeto_consolidado
        
        if tipo_projeto == "TESE_FISICA":
            st.session_state["plano_salvo_ui"] = f"{entrega_final}\n\n_⚠️ Tese validada parcialmente (Limite de 5 falhas atingido)._"
        else:
            st.session_state["plano_salvo_ui"] = f"{entrega_final}\n\n_⚠️ Produto final com imperfeições identificadas (Limite de 4 falhas atingido)._"
        
        st.session_state["fluxo_concluido_com_sucesso"] = True
        
