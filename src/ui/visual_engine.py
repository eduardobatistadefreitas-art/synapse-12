import streamlit as st

def renderizar_ui_principal():
    """
    Camada de Aparência e Exibição.
    Oculta o debate interno dos agentes e exibe estritamente o produto final homologado.
    """
    try:
        from core.loop_agents import processar_fluxo_colmeia
    except ModuleNotFoundError:
        from src.core.loop_agents import processar_fluxo_colmeia

    st.write("_Arquitetura Corporativa Baseada na Colmeia Estrita do Diretor Eduardo._")
    st.markdown("---")

    st.write("### 🎬 Iniciar Nova Orquestração")
    
    with st.form("formulario_seguro"):
        tarefa_input = st.text_area("O que você precisa realizar hoje?", placeholder="Ex: Crie um poema sobre tecnologia...", height=150)
        disparar = st.form_submit_button("Dar vida ao projeto", type="primary")

    if disparar and tarefa_input.strip():
        # Dispara o processamento invisível baseado no barramento
        processar_fluxo_colmeia(tarefa_input)
        st.session_state["ultima_tarefa_rodada"] = tarefa_input
        st.rerun()
    elif disparar:
        st.warning("Por favor, preencha o campo de texto.")

    # 🏁 ENTREGA EXCLUSIVA NA TELA (NÃO APAGA, NÃO EXPÕE BRIEFINGS INTERMÉDIOS)
    if st.session_state.get("fluxo_concluido_com_sucesso"):
        st.markdown("---")
        st.success(f"🎉 **Entrega Final Homologada com Sucesso**")
        st.write(f"_Projeto processado: '{st.session_state.get('ultima_tarefa_rodada')}'_")
        st.markdown("---")
        
        # Cospe estritamente o produto final lapidado pelo IA03 em Markdown puro
        produto_final = st.session_state.get("plano_salvo_ui", "")
        st.markdown(produto_final)
        
