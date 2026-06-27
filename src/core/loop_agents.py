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
    Executa o debate interno em silêncio e isola o produto final em sessão estável.
    """
    bus = MessageBus()
    mediador = MediadorAgent()
    executor = ExecutorAgent()
    auditor = AuditorAgent()
    
    # Inicializa variáveis de sessão de segurança limpas
    st.session_state["plano_salvo_ui"] = ""
    st.session_state["fluxo_concluido_com_sucesso"] = False

    # Carrega diretrizes adaptativas
    diretriz_sistema = "NORMAL"
    caminho_config = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config_adaptativa.json")
    if os.path.exists(caminho_config):
        try:
            with open(caminho_config, "r", encoding="utf-8") as f:
                config = json.load(f)
                if config.get("erros_acumulados", 0) >= 3:
                    diretriz_sistema = f"FORCAR_METRICAS_ESTRITAS_SMART"
        except Exception: pass

    # IA01 [Mediador] monta o briefing inicial em segundo plano
    with st.spinner("🧠 Sincronizando Colmeia de Agentes Synapse..."):
        dados_envio = {"tarefa_usuario": tarefa_usuario, "diretriz_optimizer": diretriz_sistema, "rodada": 1}
        briefing_final = mediador.executar(dados_envio)
        bus.publicar_evento(mediador.name, "SISTEMA", "BRIEFING_TEXTO", briefing_final)

    # IA02 [Executor] processa a entrega real com base no briefing
    if briefing_final and not briefing_final.startswith("RAIZ_ERRO:"):
        with st.spinner("⚡ Compilando e lapidando seu produto final..."):
            plano_tecnico = executor.executar({"briefing": briefing_final})
            bus.publicar_evento(executor.name, "SISTEMA", "PLANO_FINAL", plano_tecnico)
            
            # Trava o resultado bruto e real (poema, app, tese) na memória de sessão
            st.session_state["plano_salvo_ui"] = plano_tecnico
            st.session_state["fluxo_concluido_com_sucesso"] = True
            
            # Auditor atua em silêncio gravando as métricas adaptativas no JSON
            auditor.executar({"briefing": briefing_final})
    else:
        st.session_state["plano_salvo_ui"] = f"💥 Falha de comunicação na malha do servidor. Resposta bruta: {briefing_final[:50]}"
        st.session_state["fluxo_concluido_com_sucesso"] = True
        
