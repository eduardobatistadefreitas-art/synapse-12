import streamlit as st

def renderizar_ui_principal():
    """
    Camada Exclusiva de UI e Design.
    Sem painel de testes e estabilizada contra limpezas de tela automáticas.
    """
    try:
        from core.loop_agents import processar_fluxo_colmeia
        from utils.context_analyzer import ContextAnalyzer
    except ModuleNotFoundError:
        from src.core.loop_agents import processar_fluxo_colmeia
        from src.utils.context_analyzer import ContextAnalyzer

    st.write("_Arquitetura Corporativa Desacoplada Baseada em Barramento (Bus)._")
    st.markdown("---")

    st.write("### 🎬 Iniciar Nova Orquestração")
    
    # 🔒 FORMULÁRIO SEGURO ANTI-RELOAD
    with st.form("formulario_seguro"):
        tarefa_input = st.text_area("O que você precisa realizar hoje?", placeholder="Crie um app para vendas", height=150)
        disparar = st.form_submit_button("Dar vida ao projeto", type="primary")

    if disparar and tarefa_input.strip():
        analisador = ContextAnalyzer()
        st.session_state["intencao_identificada_ui"] = analisador.extrair_intencao(tarefa_input)
        st.session_state["ultima_tarefa_rodada"] = tarefa_input
        
        # Executa o processamento salvando direto na sessão segura do navegador
        processar_fluxo_colmeia(tarefa_input)
        st.session_state["fluxo_concluido_com_sucesso"] = True
        st.rerun()
        
    elif disparar:
        st.warning("Por favor, descreva o comando.")

    # 📋 EXIBIÇÃO TRAVADA EM TELA (NÃO APAGA MAIS)
    if st.session_state.get("intencao_identificada_ui"):
        st.info(f"🔍 **Análise do Barramento**: Contexto Identificado -> `{st.session_state['intencao_identificada_ui']}`")

    if st.session_state.get("fluxo_concluido_com_sucesso"):
        st.markdown("---")
        
        # 1. Renderiza o histórico de briefings validados
        for rodada_info in st.session_state.get("historico_rodadas_ui", []):
            st.markdown(f"### 🧠 Briefing Gerado (Rodada {rodada_info['rodada']})")
            st.write(rodada_info["texto"])
            if rodada_info["aprovado"]:
                st.success("✅ Briefing validado e aprovado pelo validador SMART!")
            else:
                st.warning(f"⚠️ Briefing Reprovado. Lacunas: {', '.join(rodada_info['lacunas'])}")
            st.markdown("---")

        # 2. Renderiza a entrega técnica ou o poema real fixado em tela
        plano_final = st.session_state.get("plano_salvo_ui", "")
        if plano_final:
            st.markdown("### 🏁 Entrega Final Homologada")
            st.markdown(plano_final)
            st.success(f"🎉 Processo concluído com sucesso para: '{st.session_state.get('ultima_tarefa_rodada')}'!")
            
