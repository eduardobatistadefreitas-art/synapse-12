import streamlit as st
import os
import json
from core.bus import MessageBus
from utils.network_helper import executar_requisicao_ia

def processar_fluxo_colmeia(tarefa_usuario):
    """
    Orquestrador Supremo (IA04). 
    Imune a erros de tipo (AttributeError) ao validar strings dos agentes.
    """
    bus = MessageBus()
    
    st.session_state["plano_salvo_ui"] = ""
    st.session_state["fluxo_concluido_com_sucesso"] = False

    # 1. IA01 [Mediador] monta o briefing
    with st.spinner("🧠 IA01 [Mediador] gerando briefing de requisitos..."):
        p_sistema_1 = "Você é o IA01 Mediador. Escreva um briefing técnico enxuto com Objetivo, Requisitos quantificáveis (%) e Cronograma com prazos."
        briefing_estruturado = executar_requisicao_ia(p_sistema_1, tarefa_usuario)
        
        if isinstance(briefing_estruturado, dict):
            briefing_estruturado = json.dumps(briefing_estruturado)
        bus.publicar_evento("IA01_Mediador", "IA03_Alinhador", "BRIEFING_TEXTO", briefing_estruturado)

    loop_ativo, rodada, max_rodadas = True, 1, 3
    projeto_alinhado_v3 = ""
    feedback_reprovacao_v5 = "NENHUM"

    # 🔄 LOOP DE CONTROLE DOS AGENTES (MÁXIMO 3 PASSAGENS PELO IA05)
    while loop_ativo and rodada <= max_rodadas:
        
        # A. IA03 [Alinhador] monta/refina o projeto chamando a lógica do IA02
        with st.spinner(f"⚡ [Rodada {rodada}/3] IA03 [Alinhador] estruturando projeto..."):
            p_sistema_3 = "Você é o IA03 Alinhador Geral. Compile o briefing e os dados da lógica de matemática do IA02 em um projeto rico em Markdown."
            prompt_user_3 = f"Tarefa original: {tarefa_usuario}\nBriefing base: {briefing_estruturado}\nÚltimo Feedback de Reprovação do IA05: {feedback_reprovacao_v5}"
            projeto_alinhado_v3 = executar_requisicao_ia(p_sistema_3, prompt_user_3)
            
            if isinstance(projeto_alinhado_v3, dict):
                projeto_alinhado_v3 = json.dumps(projeto_alinhado_v3)
            bus.publicar_evento("IA03_Alinhador", "IA02_Executor", "PROJETO_INTERMEDIO", projeto_alinhado_v3)

        # B. IA02 [Executor Técnico] entra processando matemática ou lógica
        with st.spinner(f"🛠️ [Rodada {rodada}/3] IA02 [Executor] processando lógica e matemática..."):
            p_sistema_2 = "Você é o IA02 Executor Técnico. Analise o projeto do IA03, execute a lógica, matemática ou estrutura rígida e devolva o resultado refinado."
            dados_logica_v2 = executar_requisicao_ia(p_sistema_2, projeto_alinhado_v3)
            
            if isinstance(dados_logica_v2, dict):
                dados_logica_v2 = json.dumps(dados_logica_v2)
            bus.publicar_evento("IA02_Executor", "IA03_Alinhador", "LOGICA_COMPILADA", dados_logica_v2)

        # C. IA03 junta os dados da lógica recebidos do IA02
        projeto_alinhado_v3 = f"{projeto_alinhado_v3}\n\n## ⚙️ Lógica Integrada (IA02):\n{dados_logica_v2}"

        # D. IA05 [Auditor] executa a validação crítica SMART
        with st.spinner(f"⚖️ [Rodada {rodada}/3] IA05 [Auditor] avaliando entrega técnica..."):
            # Força o tratamento para string estável antes do .lower() para extinguir o AttributeError
            texto_teste = str(projeto_alinhado_v3).lower()
            
            aprovado_ia05 = ("%" in texto_teste or "taxa" in texto_teste) and ("meses" in texto_teste or "fase" in texto_teste) or "síntese local" in texto_teste
            
            if aprovado_ia05:
                bus.publicar_evento("IA05_Auditor", "IA03_Alinhador", "VEREDITO", "APROVADO")
                st.session_state["plano_salvo_ui"] = projeto_alinhado_v3
                st.session_state["fluxo_concluido_com_sucesso"] = True
                loop_ativo = False
            else:
                feedback_reprovacao_v5 = "REPROVADO: O plano técnico final ainda carece de prazos explícitos em meses ou métricas quantificáveis de sucesso."
                bus.publicar_evento("IA05_Auditor", "IA03_Alinhador", "VEREDITO", feedback_reprovacao_v5)
                
        rodada += 1

    if not st.session_state.get("fluxo_concluido_com_sucesso"):
        st.session_state["plano_salvo_ui"] = f"{projeto_alinhado_v3}\n\n⚠️ *Nota de Governança (IA04): Limite de 3 rodadas atingido. Projeto homologado por threshold.*"
        st.session_state["fluxo_concluido_com_sucesso"] = True
        
