import streamlit as st

def renderizar_ui_principal():
    """
    Camada Exclusiva de UI e Design.
    Lê os dados estáveis da memória da sessão, travando a renderização no smartphone.
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
    
    with st.form("formulario_seguro"):
        tarefa_input = st.text_area("O que você precisa realizar hoje?", placeholder="Crie um app para vendas", height=150)
        disparar = st.form_submit_button("Dar vida ao projeto", type="primary")

    if disparar and tarefa_input.strip():
        analisador = ContextAnalyzer()
        st.session_state["intencao_identificada_ui"] = analisador.extrair_intencao(tarefa_input)
        st.session_state["ultima_tarefa_rodada"] = tarefa_input
        
        # Executa o processamento em background (salvando na memória da sessão)
        processar_fluxo_colmeia(tarefa_input)
        st.session_state["fluxo_concluido_com_sucesso"] = True
        st.rerun()  # Força a interface a renderizar os dados guardados
        
    elif disparar:
        st.warning("Por favor, descreva o comando.")

    # 📋 RENDERIZAÇÃO ESTÁVEL E FIXA NA TELA DO SMARTPHONE
    if st.session_state.get("intencao_identificada_ui"):
        st.info(f"🔍 **Análise do Barramento**: Contexto Identificado -> `{st.session_state['intencao_identificada_ui']}`")

    if st.session_state.get("fluxo_concluido_com_sucesso"):
        st.markdown("---")
        
        # 1. Desenha o histórico das rodadas que você viu piscando
        for rodada_info in st.session_state.get("historico_rodadas_ui", []):
            st.markdown(f"### 🧠 Briefing Gerado (Rodada {rodada_info['rodada']})")
            st.write(rodada_info["texto"])
            if rodada_info["aprovado"]:
                st.success("✅ Briefing validado e aprovado pelo validador SMART!")
            else:
                st.warning(f"⚠️ Briefing Reprovado. Lacunas: {', '.join(rodada_info['lacunas'])}")
            st.markdown("---")

        # 2. Desenha a entrega técnica final estável
        plano_final = st.session_state.get("plano_salvo_ui", "")
        if plano_final:
            st.markdown("### 🏁 Plano Técnico Final Homologado")
            st.markdown(plano_final)
            st.success(f"🎉 Processo concluído com sucesso para: '{st.session_state.get('ultima_tarefa_rodada')}'!")
            
            with st.expander("👁️ Ver Logs do Auditor Adaptativo", expanded=False):
                st.json(st.session_state.get("dados_log_auditor", {}))
                
