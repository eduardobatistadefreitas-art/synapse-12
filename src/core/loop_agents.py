import streamlit as st
import os
import json
from core.bus import MessageBus
from agents.mediador import MediadorAgent
from agents.executor import ExecutorAgent
from agents.auditor import AuditorAgent

def processar_fluxo_colmeia(tarefa_usuario):
    """
    Orquestrador Central baseado em Barramento (Bus).
    Garante o encaminhamento correto do prompt do Diretor Eduardo para os Especialistas.
    """
    bus = MessageBus()
    mediador = MediadorAgent()
    executor = ExecutorAgent()
    auditor = AuditorAgent()
    
    # Inicializa variáveis de sessão de segurança limpas
    st.session_state["plano_salvo_ui"] = ""
    st.session_state["fluxo_concluido_com_sucesso"] = False

    # 1. Recupera as diretrizes adaptativas salvas do arquivo de aprendizado (.json)
    diretriz_sistema = "NORMAL"
    caminho_config = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config_adaptativa.json")
    if os.path.exists(caminho_config):
        try:
            with open(caminho_config, "r", encoding="utf-8") as f:
                config = json.load(f)
                if config.get("erros_acumulados", 0) >= 3:
                    diretriz_sistema = "FORCAR_METRICAS_ESTRITAS_SMART"
        except Exception: pass

    # 2. IA01 [Mediador] monta o briefing técnico com base na tarefa do usuário
    with st.spinner("🧠 IA01 [Mediador] estruturando briefing estratégico..."):
        dados_mediador = {
            "tarefa_usuario": tarefa_usuario, 
            "diretriz_optimizer": diretriz_sistema, 
            "rodada": 1
        }
        briefing_gerado = mediador.executar(dados_mediador)
        bus.publicar_evento(mediador.name, "SISTEMA", "BRIEFING_TEXTO", briefing_gerado)

    # 3. CORREÇÃO DA MÁQUINA: O IA02 [Executor] recebe a tarefa real do usuário casada com o briefing
    if briefing_gerado and not briefing_gerado.startswith("RAIZ_ERRO:"):
        with st.spinner("🛠️ IA02 [Executor Sênior] gerando e refinando seu projeto real..."):
            dados_executor = {
                "tarefa_usuario": tarefa_usuario,  # Alinha o foco no pedido original do Diretor
                "briefing": briefing_gerado
            }
            projeto_final = executor.executar(dados_executor)
            bus.publicar_evento(executor.name, "SISTEMA", "PRODUTO_FINAL", projeto_final)
            
            # Trava o resultado final legítimo gerado pela inteligência na tela
            st.session_state["plano_salvo_ui"] = projeto_final
            st.session_state["fluxo_concluido_com_sucesso"] = True
            
            # 4. IA05 [Auditor] executa a validação em segundo plano e salva o log
            auditor.executar({"briefing": briefing_gerado})
    else:
        st.session_state["plano_salvo_ui"] = f"💥 Falha de comunicação na malha do servidor. Detalhes: {briefing_gerado[:50]}"
        st.session_state["fluxo_concluido_com_sucesso"] = True
        
