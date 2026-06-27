import streamlit as st

def renderizar_ui_principal():
    """
    Camada Exclusiva de UI e Design Rígido.
    Exibe UNICAMENTE o produto final gerado, eliminando qualquer texto ou carimbo extra.
    """
    try:
        from core.loop_agents import processar_fluxo_colmeia
    except ModuleNotFoundError:
        from src.core.loop_agents import processar_fluxo_colmeia

    # 🔒 FORMULÁRIO SEGURO ANTI-RELOAD
    with st.form("formulario_seguro"):
        tarefa_input = st.text_area("O que você precisa realizar hoje?", placeholder="Ex: Escreva um poema ou crie um app de vendas...", height=150)
        disparar = st.form_submit_button("Dar vida ao projeto", type="primary")

    if disparar and tarefa_input.strip():
        processar_fluxo_colmeia(tarefa_input)
        st.session_state["fluxo_concluido_com_sucesso"] = True
        st.rerun()
    elif disparar:
        st.warning("Por favor, preencha o campo de texto.")

    # 🏁 EXIBIÇÃO ABSOLUTA E EXCLUSIVA (NADA ALÉM DO PRODUTO SOLICITADO)
    if st.session_state.get("fluxo_concluido_com_sucesso"):
        produto_final = st.session_state.get("plano_salvo_ui", "")
        if produto_final:
            st.markdown(produto_final)
            
