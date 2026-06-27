import streamlit as st
import os
import json
from core.bus import MessageBus
from utils.network_helper import executar_requisicao_ia

def processar_fluxo_colmeia(tarefa_usuario):
    """
    Orquestrador Central Supremo (IA04).
    Implementa estritamente o workflow multi-agent do infográfico Synapse 24 OS.
    Suporta classificacao IA01, barramento IA03 <-> IA02 e a Juiza IA05 (Regras 4 e 5).
    """
    bus = MessageBus()
    
    # Inicialização de memória de sessão limpa e segura
    st.session_state["plano_salvo_ui"] = ""
    st.session_state["fluxo_concluido_com_sucesso"] = False

    # ---------------------------------------------------------------------
    # PASSO 1: IA01 [MEDIADOR/FILTRO] - Classifica e Filtra Ruídos
    # ---------------------------------------------------------------------
    with st.spinner("🧠 IA01 [Mediador] classificando projeto e filtrando ruidos..."):
        p_sistema_1 = (
            "Você é o IA01 Mediador/Filtro. Analise o pedido do usuário e classifique o tipo "
            "de entrega estritamente em uma dessas categorias: [TESE_FISICA, APP_PYTHON, CONTEUDO_GERAL]. "
            "Retorne a classificação na primeira linha e um briefing limpo (Validated Request) abaixo."
        )
        briefing_ia01 = executar_requisicao_ia(p_sistema_1, tarefa_usuario)
        bus.publicar_evento("IA01_Mediador", "IA03_Gestor", "VALIDATED_REQUEST", briefing_ia01)

    # Identifica o tipo de projeto para aplicar as travas assimétricas da Juíza (IA05)
    tipo_projeto = "CONTEUDO_GERAL"
    if "TESE_FISICA" in briefing_ia01:
        tipo_projeto = "TESE_FISICA"
    elif "APP_PYTHON" in briefing_ia01 or "app" in tarefa_usuario.lower():
        tipo_projeto = "APP_PYTHON"

    # Define os limites estritos de estouro do laço (Regra dos 4 e Regra dos 5)
    limite_loop = 5 if tipo_projeto == "TESE_FISICA" else 4
    
    # ---------------------------------------------------------------------
    # PASSO 2: IA03 [GESTOR/ORQUESTRADOR] - Cria Esqueleto Inicial
    # ---------------------------------------------------------------------
    with st.spinner("📋 IA03 [Gestor] estruturando esqueleto base do projeto..."):
        p_sistema_3_init = "Você é o IA03 Gestor/Orquestrador. Com base na Validated Request do IA01, monte o esqueleto/esqueleto estrutural rígido do projeto."
        projeto_consolidado = executar_requisicao_ia(p_sistema_3_init, briefing_ia01)

    # Variáveis de controle do laço de performance gerenciado pelo IA04
    loop_ativo = True
    contador_falhas = 0
    feedback_juiza_ia05 = "NENHUMA CORREÇÃO REQUERIDA AINDA"

    # 🔄 LOOP DE PERFORMANCE E CORREÇÃO ASSIMÉTRICO (BACK TO IA02)
    while loop_ativo and contador_falhas < limite_loop:
        
        # A. IA02 [EXECUTOR/TÉCNICO] - Gera conteúdo bruto com base no esqueleto e correções
        with st.spinner(f"⚡ [Tentativa {contador_falhas + 1}/{limite_loop}] IA02 [Executor] processando conteudo bruto..."):
            p_sistema_2 = (
                "Você é o IA02 Executor/Técnico. Gere o conteúdo bruto rico (Código, Texto, Matemática, História) "
                "com base no esqueleto do IA03 e aplique as correções exigidas pela Juíza se houver."
            )
            prompt_user_2 = f"Esqueleto Atual:\n{projeto_consolidado}\n\nFeedback de Correção da Juíza:\n{feedback_reprovacao_v5 if 'feedback_reprovacao_v5' in locals() else 'Nenhum'}"
            conteudo_bruto_ia02 = executar_requisicao_ia(p_sistema_2, prompt_user_2)
            bus.publicar_evento("IA02_Executor", "IA03_Gestor", "RAW_CONTENT", conteudo_bruto_ia02)

        # B. IA03 [GESTOR] - Consolida e formata os dados brutos recebidos do IA02
        projeto_consolidado = f"{projeto_consolidado}\n\n{conteudo_bruto_ia02}"

        # C. IA05 [JUIZA/CRÍTICA] - Analisa sem Viés / Positividade
        with st.spinner(f"⚖️ [Avaliação {contador_falhas + 1}/{limite_loop}] IA05 [Juíza] aplicando crivo de qualidade..."):
            p_sistema_5 = (
                "Você é o IA05 Juíza/Crítica. Analise o projeto consolidado sem viés. "
                "Se o material estiver completo e atender perfeitamente à demanda, responda estritamente 'APROVADO'. "
                "Se faltar profundidade, qualidade ou estrutura, responda 'REPROVADO:' seguido detalhadamente das falhas encontradas."
            )
            veredito_ia05 = executar_requisicao_ia(p_sistema_5, projeto_consolidado)
            
            if "APROVADO" in veredito_ia05.upper():
                bus.publicar_evento("IA05_Auditor", "SISTEMA", "FINAL_VALIDATION", "APPROVED")
                st.session_state["plano_salvo_ui"] = projeto_consolidado
                st.session_state["fluxo_concluido_com_sucesso"] = True
                loop_ativo = False # Interrompe o fluxo - Delivers final product to user
            else:
                contador_falhas += 1
                feedback_reprovacao_v5 = veredito_ia05.replace("REPROVADO:", "").strip()
                bus.publicar_evento("IA05_Auditor", "IA03_Gestor", "FORCES_CORRECTION", feedback_reprovacao_v5)
                
                # Se atingir o limite exato de falhas da Regra, força a entrega no estado atual
                if contador_falhas >= limite_loop:
                    loop_ativo = False

    # 🏁 TRATAMENTO DE SAÍDA BASEADO NAS REGRAS DO INFOGRÁFICO
    if not st.session_state.get("fluxo_concluido_com_sucesso"):
        if tipo_projeto == "TESE_FISICA":
            # Regra dos 5 para tese física
            st.session_state["plano_salvo_ui"] = f"{projeto_consolidado}\n\n💥 **TESE QUEBRADA (VALIDATED ONLY)**\n_Nota do Orquestrador: O projeto falhou em 5 validações consecutivas da Juíza IA05._"
        else:
            # Regra dos 4 para Apps / Conteúdo Geral
            st.session_state["plano_salvo_ui"] = f"{projeto_consolidado}\n\n🔴 **PRODUTO IMPERFEITO**\n_Nota do Orquestrador: Entrega forçada após o estouro do limite de 4 correções da Regra dos 4._"
        
        st.session_state["fluxo_concluido_com_sucesso"] = True
        
