import streamlit as st

def renderizar_ui_principal():
    """
    Camada Exclusiva de UI e Design.
    """
    try:
        from core.loop_agents import processar_fluxo_colmeia, rodar_teste_estresse_direto
        from utils.context_analyzer import ContextAnalyzer
    except ModuleNotFoundError:
        from src.core.loop_agents import processar_fluxo_colmeia, rodar_teste_estresse_direto
        from src.utils.context_analyzer import ContextAnalyzer

    st.write("_Arquitetura Corporativa Desacoplada Baseada em Barramento (Bus)._")
    st.markdown("---")

    st.write("### 🛠️ Painel de Testes Estruturados")
    if st.button("🔥 Forçar Estouro de Limites (Simulação)", type="secondary"):
        rodar_teste_estresse_direto()

    st.write("### 🎬 Iniciar Nova Orquestração")
    
    with st.form("formulario_seguro"):
        tarefa_input = st.text_area("O que você precisa realizar hoje?", placeholder="Crie um app para vendas", height=150)
        disparar = st.form_submit_button("Dar vida ao projeto", type="primary")

    if disparar and tarefa_input.strip():
        analisador = ContextAnalyzer()
        st.info(f"🔍 **Análise do Barramento**: Contexto Identificado -> `{analisador.extrair_intencao(tarefa_input)}`")
        processar_fluxo_colmeia(tarefa_input)
    elif disparar:
        st.warning("Por favor, descreva o comando.")
      
