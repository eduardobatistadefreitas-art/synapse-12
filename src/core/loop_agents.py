import streamlit as st
import os
import json
from core.bus import MessageBus
from agents.mediador import MediadorAgent
from agents.executor import ExecutorAgent
from agents.auditor import AuditorAgent

def processar_fluxo_colmeia(tarefa_usuario):
    """
    Orquestrador Central. Guarda as entregas no st.session_state 
    para impedir apagamentos causados pelo re-run da interface.
    """
    bus = MessageBus()
    mediador = MediadorAgent()
    executor = ExecutorAgent()
    auditor = AuditorAgent()
    
    # Inicializa variáveis de sessão de segurança
    st.session_state["briefing_salvo_ui"] = ""
    st.session_state["plano_salvo_ui"] = ""
    st.session_state["historico_rodadas_ui"] = []

    # Carrega diretrizes adaptativas
    diretriz_sistema = "NORMAL"
    caminho_config = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config_adaptativa.json")
    if os.path.exists(caminho_config):
        try:
            with open(caminho_config, "r", encoding="utf-8") as f:
                config = json.load(f)
                if config.get("erros_acumulados", 0) >= 3:
                    diretriz_sistema = f"FORCAR_METRICAS_ESTRITAS_SMART (Alerta: {config.get('ultima_lacuna')})"
        except Exception: pass

    loop_ativo, rodada = True, 1
    briefing_final = ""
    
    # 🔄 Loop de Validação do Mediador
    while loop_ativo and rodada <= 2:
        with st.spinner(f"🧠 [Rodada {rodada}] {mediador.name} processando..."):
            dados_envio = {"tarefa_usuario": tarefa_usuario, "diretriz_optimizer": diretriz_sistema, "rodada": rodada}
            briefing_final = mediador.executar(dados_envio)
            
            bus.publicar_evento(mediador.name, "SISTEMA", "BRIEFING_TEXTO", briefing_final)
            resultado_auditoria = auditor.executar({"briefing": briefing_final})
            
            # Registra o histórico da rodada na memória estável
            st.session_state["historico_rodadas_ui"].append({
                "rodada": rodada,
                "texto": briefing_final,
                "aprovado": resultado_auditoria["is_smart"],
                "lacunas": resultado_auditoria["lacunas"]
            })
            
            if resultado_auditoria["is_smart"]:
                loop_ativo = False
                
        rodada += 1

    # Salva o Briefing Final consolidado
    st.session_state["briefing_salvo_ui"] = briefing_final

    # Execução do Plano Técnico Final
    if briefing_final:
        with st.spinner(f"🛠️ {executor.name} compilando plano técnico final..."):
            plano_tecnico = executor.executar({"briefing": briefing_final})
            bus.publicar_evento(executor.name, "SISTEMA", "PLANO_FINAL", plano_tecnico)
            
            # Salva o Plano Técnico Final consolidado na memória estável
            st.session_state["plano_salvo_ui"] = plano_tecnico
            st.session_state["dados_log_auditor"] = auditor.executar({"briefing": briefing_final})["dados_log"]
            
