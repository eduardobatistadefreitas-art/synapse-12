# app.py
import os
os.system("pip install openai streamlit")

try:
    import openai
except ImportError:
    os.system("pip install openai")

import streamlit as st
import sys

# Garante que o Streamlit encontre a pasta 'src' no servidor em nuvem
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from bus.message_bus import MessageBus
from core.kernel import SynapseKernel
from agents.ia01_mediador import AgenteMediador
from agents.ia02_executor import AgenteExecutor
from agents.ia03_critico import AgenteCritico
from agents.ia04_supervisor import AgenteSupervisor
from agents.ia05_auditor import AgenteAuditor

# Configuração da página para o navegador do celular
st.set_page_config(page_title="Synapse 12 OS", page_icon="🧠", layout="centered")

st.title("🧠 Synapse 12 - Sistema Operacional")
st.subheader("Fábrica de Agentes Autónomos Orquestrados")

# Inicialização da infraestrutura na memória do app se não existir
if "bus" not in st.session_state:
    st.session_state.bus = MessageBus()
    st.session_state.kernel = SynapseKernel(st.session_state.bus)
    
    # Instancia e registra a colmeia de agentes
    ia01 = AgenteMediador("IA01", "Mediador", st.session_state.bus, user_plan="BASIC")
    ia02 = AgenteExecutor("IA02", "Executor", st.session_state.bus)
    ia03 = AgenteCritico("IA03", "Critico", st.session_state.bus, user_tier="BASIC")
    ia04 = AgenteSupervisor("IA04", "Supervisor", st.session_state.bus)
    ia05 = AgenteAuditor("IA05", "Auditor", st.session_state.bus)
    
    # 🎭 CONFIGURAÇÃO DOS 4 CÉREBROS REAIS E CONCORRENTES (POLIGLOTA GRÁTIS)
    ia01.model = "gemma2-9b-it"                     # Google via Groq
    ia02.model = "deepseek-r1-distill-llama-70b"    # DeepSeek via Groq
    ia03.model = "gemini-1.5-flash"                 # Google AI Studio direto
    ia05.model = "llama-3.3-70b-specdec"            # Meta via Groq
    
    # Registra a colmeia conectada no barramento
    st.session_state.bus.registrar(ia01)
    st.session_state.bus.registrar(ia02)
    st.session_state.bus.registrar(ia03)
    st.session_state.bus.registrar(ia04)
    st.session_state.bus.registrar(ia05)

st.markdown("---")

# Painel de Entrada do Usuário (Cliente 01)
st.write("### 🎬 Disparar Nova Orquestração")
tarefa_input = st.text_area("O que você deseja que a colmeia de agentes construa?", 
                            placeholder="Ex: Crie um script de automação para leads imobiliários...")

checklist_input = st.text_input("Definição de escopo (Requisito do Mediador):", 
                                 value="conclusao e escopo bem definidos.")

if st.button("Ativar Synapse Kernel", type="primary"):
    if tarefa_input.strip():
        with st.spinner("🤖 Conectando APIs gratuitas e iniciando debate entre as IAs..."):
            # Monta o payload conforme as regras do nosso ecossistema
            payload_usuario = {
                "tarefa": tarefa_input,
                "status": checklist_input
            }
            
            # Dispara através do Kernel oficial
            resultado = st.session_state.kernel.start_pipeline(payload_usuario)
            
            st.success("🏁 Pipeline Executado com Sucesso!")
            st.info(f"📊 **Retorno Final da Orquestração:** {resultado}")
            st.toast("Fluxo concluído!")
    else:
        st.warning("Por favor, digite uma tarefa para os agentes executarem.")

st.markdown("---")
st.caption("Synapse 12 • Modo de Operação Poliglota Ativo • Executando via Streamlit Engine")
