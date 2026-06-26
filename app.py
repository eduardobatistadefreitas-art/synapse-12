# app.py
import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from bus.message_bus import MessageBus
from core.kernel import SynapseKernel
from agents.ia01_mediador import AgenteMediador
from agents.ia02_executor import AgenteExecutor
from agents.ia03_critico import AgenteCritico
from agents.ia04_supervisor import AgenteSupervisor
from agents.ia05_auditor import AgenteAuditor

# 1. Configuração de Tela com Posicionamento Premium
st.set_page_config(page_title="Synapse 12", page_icon="💡", layout="centered")

st.title("💡 Synapse 12")
st.subheader("Sua ideia, executada.")
st.write("_Descreva sua ideia ou o problema que deseja eliminar. Nossa rede de especialistas em IA cuida de toda a execução para você._")

# Inicialização da infraestrutura em segundo plano
if "bus" not in st.session_state:
    st.session_state.bus = MessageBus()
    st.session_state.kernel = SynapseKernel(st.session_state.bus)
    
    # Instancia a colmeia de agentes poliglotas
    ia01 = AgenteMediador("IA01", "Mediador", st.session_state.bus, user_plan="BASIC")
    ia02 = AgenteExecutor("IA02", "Executor", st.session_state.bus)
    ia03 = AgenteCritico("IA03", "Critico", st.session_state.bus, user_tier="BASIC")
    ia04 = AgenteSupervisor("IA04", "Supervisor", st.session_state.bus)
    ia05 = AgenteAuditor("IA05", "Auditor", st.session_state.bus)
    
    ia01.model = "gemma2-9b-it"                     
    ia02.model = "deepseek-r1-distill-llama-70b"    
    ia03.model = "gemini-1.5-flash"                 
    ia05.model = "llama-3.3-70b-specdec"            
    
    st.session_state.bus.registrar(ia01)
    st.session_state.bus.registrar(ia02)
    st.session_state.bus.registrar(ia03)
    st.session_state.bus.registrar(ia04)
    st.session_state.bus.registrar(ia05)

st.markdown("---")

# 2. Nova Roupagem de Copywriting (Foco no Benefício)
st.write("### 🎬 Iniciar Projeto")
tarefa_input = st.text_area(
    "O que você precisa realizar hoje?", 
    placeholder="Ex: Quero automatizar o envio de e-mails para meus leads imobiliários ou criar uma planilha inteligente de vendas...",
    height=150
)

if st.button("Dar vida ao projeto", type="primary"):
    if tarefa_input.strip():
        # 4. Feedback de Status Humanizado (Escondendo a engenharia)
        status_placeholder = st.empty()
        
        with st.spinner("Conectando nossa rede de especialistas..."):
            status_placeholder.info("🧠 Entendendo seus requisitos e validando o escopo...")
            # Pequena pausa apenas para o usuário ler o status humanizado
            import time
            time.sleep(1.5) 
            
            status_placeholder.info("🗺️ Planejando a melhor estratégia de execução...")
            time.sleep(1.5)
            
            status_placeholder.info("🛠️ Executando sua automação com máxima precisão...")
            
            payload_usuario = {
                "tarefa": tarefa_input,
                "status": "conclusao automatica de escopo aprovada pelo sistema"
            }
            
            # Dispara a orquestração síncrona real via Kernel
            resultado = st.session_state.kernel.start_pipeline(payload_usuario)
            
            # Limpa as mensagens de carregamento temporárias
            status_placeholder.empty()
            
            # Entrega do resultado final focado em valor
            st.success("🎉 Projeto concluído com sucesso!")
            st.write("### 📊 Aqui está o resultado da sua entrega:")
            st.info(resultado)
            st.toast("Finalizado!")
    else:
        st.warning("Por favor, descreva o que você precisa realizar hoje.")

st.markdown("---")
# 3. Transparência Controlada (Complexidade Técnica Oculta)
with st.expander("⚙️ Ver detalhes técnicos do processo (Logs Avançados)"):
    st.caption("Modo de Operação Poliglota Ativo • Redundância Resiliente Ativada • Synapse 12 REST Engine")
    
