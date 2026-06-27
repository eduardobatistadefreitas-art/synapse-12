import streamlit as st

def renderizar_ui_principal():
    """
    Camada Exclusiva de UI e Design.
    Processamento 100% oculto. Exibe estritamente o produto final solicitado pelo Diretor.
    """
    try:
        from core.loop_agents import processar_fluxo_colmeia
    except ModuleNotFoundError:
        from src.core.loop_agents import processar_fluxo_colmeia

    st.write("_Arquitetura Modular Enxuta • Foco em Entrega Final Direta_")
    st.markdown("---")

    # 🔒 FORMULÁRIO SEGURO ANTI-RELOAD
    with st.form("formulario_seguro"):
        tarefa_input = st.text_area("O que você precisa realizar hoje?", placeholder="Ex: Escreva um poema ou crie um app de vendas...", height=150)
        disparar = st.form_submit_button("Dar vida ao projeto", type="primary")

    if disparar and tarefa_input.strip():
        # Dispara o processamento com spinners discretos
        processar_fluxo_colmeia(tarefa_input)
        st.session_state["ultima_tarefa_rodada"] = tarefa_input
        st.rerun() # Atualiza e fixa a tela congelando o estado final
        
    elif disparar:
        st.warning("Por favor, preencha o campo de texto.")

    # 🏁 EXIBIÇÃO EXCLUSIVA DO PRODUTO FINAL (SEM BRIEFING, SEM LOGS, SEM PISCAR)
    if st.session_state.get("fluxo_concluido_com_sucesso"):
        st.markdown("---")
        
        # Símbolo enxuto e carimbo discreto de processo completo solicitado
        st.success(f"🎉 **Entrega Final Concluída com Sucesso**")
        st.write(f"_Pedido processado: '{st.session_state.get('ultima_tarefa_rodada')}'_")
        st.markdown("---")
        
        # Imprime 100% do resultado gerado em Markdown limpo na tela do smartphone
        produto_final = st.session_state.get("plano_salvo_ui", "")
        st.markdown(produto_final)
        
