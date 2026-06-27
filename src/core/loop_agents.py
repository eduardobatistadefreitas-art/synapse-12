import streamlit as st
import os
import json
from core.bus import MessageBus
from agents.mediador import MediadorAgent
from agents.executor import ExecutorAgent
from agents.auditor import AuditorAgent

def processar_fluxo_colmeia(tarefa_usuario):
    """
    Orquestrador Central baseado na arquitetura de Barramento de Mensagens (Bus).
    """
    bus = MessageBus()
    mediador = MediadorAgent()
    executor = ExecutorAgent()
    auditor = AuditorAgent()
    
    # Carrega diretrizes adaptativas do Optimizer em disco
    diretriz_sistema = "NORMAL"
    caminho_config = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config_adaptativa.json")
    if os.path.exists(caminho_config):
        try:
            with open(caminho_config, "r", encoding="utf-8") as f:
                config = json.load(f)
                if config.get("erros_acumulados", 0) >= 3:
                    diretriz_sistema = f"FORCAR_METRICAS_ESTRITAS_SMART (Alerta: {config.get('ultima_lacuna')})"
                    st.warning(f"🚨 **Auto-Otimização Acionada**: Diretriz do Mediador enrijecida automaticamente pelo barramento.")
        except Exception: pass

    loop_ativo, rodada = True, 1
    briefing_final = ""
    
    # 🔄 Loop de Validação do Mediador
    while loop_ativo and rodada <= 2:
        with st.spinner(f"🧠 [Rodada {rodada}] {mediador.name} processando briefing..."):
            dados_envio = {"tarefa_usuario": tarefa_usuario, "diretriz_optimizer": diretriz_sistema, "rodada": rodada}
            briefing_final = mediador.executar(dados_envio)
            
            bus.publicar_evento(mediador.name, "SISTEMA", "BRIEFING_TEXTO", briefing_final)
            
            # Auditor analisa o briefing gerado via Barramento
            resultado_auditoria = auditor.executar({"briefing": briefing_final})
            
            st.markdown(f"### 🧠 Briefing Gerado (Rodada {rodada})")
            st.write(briefing_final)
            
            if resultado_auditoria["is_smart"]:
                st.success("✅ Briefing validado e aprovado pelo validador SMART!")
                loop_ativo = False
            else:
                st.warning(f"⚠️ Briefing Reprovado. Lacunas: {', '.join(resultado_auditoria['lacunas'])}")
                
        rodada += 1

    # Execução do Plano Técnico Final
    if briefing_final:
        with st.spinner(f"🛠️ {executor.name} compilando plano técnico final..."):
            plano_tecnico = executor.executar({"briefing": briefing_final})
            bus.publicar_evento(executor.name, "SISTEMA", "PLANO_FINAL", plano_tecnico)
            
            st.markdown("### 🏁 Plano Técnico Final Homologado")
            st.markdown(plano_tecnico)
            st.success("🎉 Processo modular concluído via Barramento de Mensagens!")
            
            # Mostra estado final do JSON
            st.json(auditor.executar({"briefing": briefing_final})["dados_log"])

def rodar_teste_estresse_direto():
    """Simula injeção forçada de erros no JSON corporativo."""
    auditor = AuditorAgent()
    for _ in range(3):
        auditor.executar({"briefing": "Prompt ruim sem nada de dados quantificados."})
    st.success("🎉 Sandbox: 3 erros injetados. Abra uma nova orquestração para ver o Optimizer agir!")
          
