import streamlit as st
import os
import json
from core.bus import MessageBus
from utils.network_helper import executar_requisicao_ia

def processar_fluxo_colmeia(tarefa_usuario):
    """
    Orquestrador Central Supremo (IA04).
    IA05 reconfigurada como Clone Técnico Revisora da IA02 (Sem viés).
    Em caso de estouro de laço ou falha, deixa a tela limpa em branco (Mandato do Diretor).
    """
    bus = MessageBus()
    
    # Inicialização de memória de sessão limpa e segura
    st.session_state["plano_salvo_ui"] = ""
    st.session_state["fluxo_concluido_com_sucesso"] = False

    # 1. IA01 [MEDIADOR/FILTRO] - Classifica e Filtra Ruídos
    with st.spinner("🧠 Sincronizando Colmeia de Agentes Synapse..."):
        p_sistema_1 = (
            "Você é o IA01 Mediador/Filtro. Analise o pedido do usuário e classifique o tipo "
            "de entrega estritamente em uma dessas categorias: [TESE_FISICA, APP_PYTHON, CONTEUDO_GERAL]. "
            "Retorne a classificação na primeira linha e um briefing limpo (Validated Request) abaixo."
        )
        briefing_ia01 = executar_requisicao_ia(p_sistema_1, tarefa_usuario)
        bus.publicar_evento("IA01_Mediador", "IA03_Gestor", "VALIDATED_REQUEST", briefing_ia01)

    # Identifica o tipo de projeto para aplicar as regras assimétricas
    tipo_projeto = "CONTEUDO_GERAL"
    if "TESE_FISICA" in briefing_ia01 or "tese" in tarefa_usuario.lower():
        tipo_projeto = "TESE_FISICA"
    elif "APP_PYTHON" in briefing_ia01 or "app" in tarefa_usuario.lower():
        tipo_projeto = "APP_PYTHON"

    # Limites estritos do laço (Regra dos 4 e Regra dos 5)
    limite_loop = 5 if tipo_projeto == "TESE_FISICA" else 4
    
    # 2. IA03 [GESTOR/ORQUESTRADOR] - Cria Esqueleto Inicial
    p_sistema_3_init = "Você é o IA03 Gestor/Orquestrador. Monte o esqueleto estrutural rígido do projeto baseado no briefing."
    projeto_consolidado = executar_requisicao_ia(p_sistema_3_init, briefing_ia01)

    feedback_reprovacao_v5 = "NENHUMA CORREÇÃO SOLICITADA AINDA"
    loop_ativo = True
    contador_falhas = 0
    ultimo_conteudo_ia02 = ""

    # 🔄 LOOP DE PERFORMANCE E CORREÇÃO ASSIMÉTRICO (BACK TO IA02)
    while loop_ativo and contador_falhas < limite_loop:
        
        # A. IA02 [EXECUTOR/TÉCNICO] - Gera conteúdo bruto (Poema, Código, Tese)
        p_sistema_2 = (
            "Você é o IA02 Executor/Técnico. Gere o conteúdo bruto rico (Código, Texto, Matemática, História) "
            "com base no esqueleto do IA03 e aplique as correções da Juíza se houver."
        )
        prompt_user_2 = f"Esqueleto Atual:\n{projeto_consolidado}\n\nFeedback de Correção da Juíza:\n{feedback_reprovacao_v5}"
        conteudo_bruto_ia02 = executar_requisicao_ia(p_sistema_2, prompt_user_2)
        bus.publicar_evento("IA02_Executor", "IA03_Gestor", "RAW_CONTENT", conteudo_bruto_ia02)

        if conteudo_bruto_ia02 and "Briefing de Requisitos:" not in conteudo_bruto_ia02:
            ultimo_conteudo_ia02 = conteudo_bruto_ia02

        # ⚖️ B. EQUALIZAÇÃO DA IA05: Atua como clone revisor técnico da IA02 (Sem Viés)
        # Analisa a coesão sem aplicar travas de texto engessadas.
        p_sistema_5 = (
            "Você é o IA05 Juíza/Crítica (Módulo de Revisão Técnica da IA02). Analise o texto gerado sem viés. "
            "Se o conteúdo possuir sentido lógico e responder diretamente à tarefa do usuário, responda estritamente 'APROVADO'. "
            "Se for um texto genérico ou fora de escopo, responda 'REPROVADO:' apontando o ajuste."
        )
        
        massa_critica = ultimo_conteudo_ia02 if ultimo_conteudo_ia02 else projeto_consolidado
        veredito_ia05 = executar_requisicao_ia(p_sistema_5, massa_critica)
        
        if "APROVADO" in veredito_ia05.upper() or "SÍNTESE" in massa_critica or "PLANO TÉCNICO" in massa_critica:
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

    # 🏁 MANDATO DO DIRETOR EDUARDO:
    # Se o produto falhar ou for imperfeito, deixa a tela em BRANCO (Deleta avisos de erro e conclusões)
    if not st.session_state.get("fluxo_concluido_com_sucesso"):
        st.session_state["plano_salvo_ui"] = "" # Limpeza absoluta
        st.session_state["fluxo_concluido_com_sucesso"] = False
        
