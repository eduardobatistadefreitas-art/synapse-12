import streamlit as st

def renderizar_ui_principal():
    """
    Camada Exclusiva de UI e Design.
    Estabilizada com persistência de estado para evitar apagamentos na tela.
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
        st.session_state["teste_estresse_rodado"] = True
        st.rerun()

    if st.session_state.get("teste_estresse_rodado"):
        st.success("🎉 Sandbox: 3 erros injetados com sucesso!")
        st.markdown("---")

    st.write("### 🎬 Iniciar Nova Orquestração")
    
    #🔒 FORMULÁRIO COM PERSISTÊNCIA: Isola o clique e impede que a tela limpe sozinha
    with st.form("formulario_seguro"):
        tarefa_input = st.text_area("O que você precisa realizar hoje?", placeholder="Crie um app para vendas", height=150)
        disparar = st.form_submit_button("Dar vida ao projeto", type="primary")

    # Se clicar no botão principal, inicializa a flag de processamento
    if disparar and tarefa_input.strip():
        analisador = ContextAnalyzer()
        st.info(f"🔍 **Análise do Barramento**: Contexto Identificado -> `{analisador.extrair_intencao(tarefa_input)}`")
        
        # Roda o processamento e sinaliza que temos um resultado para fixar
        processar_fluxo_colmeia(tarefa_input)
        st.session_state["ultima_tarefa_rodada"] = tarefa_input
        st.session_state["fluxo_concluido_com_sucesso"] = True
        st.rerun()  # Força a interface a congelar o estado renderizado
        
    elif disparar:
        st.warning("Por favor, descreva o comando.")

    # 📋 EXIBIÇÃO FIXA: Mantém o resultado grudado na tela mesmo após recarregamento automático
    if st.session_state.get("fluxo_concluido_com_sucesso"):
        st.markdown("---")
        st.success(f"🎉 Processo concluído para o pedido: '{st.session_state.get('ultima_tarefa_rodada')}'")
        st.info("💡 _Os detalhes completos do Briefing SMART e do Plano Técnico Final foram gerados acima no console de logs da colmeia e salvos na malha adaptativa._")
