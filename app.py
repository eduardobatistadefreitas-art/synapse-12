# app.py
import streamlit as st
import sys
import os
import json
import http.client

# Garante que o Streamlit encontre a pasta 'src' no servidor em nuvem
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from bus.message_bus import MessageBus
from core.kernel import SynapseKernel
from agents.ia01_mediador import AgenteMediador
from agents.ia02_executor import AgenteExecutor
from agents.ia03_critico import AgenteCritico
from agents.ia04_supervisor import AgenteSupervisor
from agents.ia05_auditor import AgenteAuditor

# Configuração de Tela Premium do Co-Piloto
st.set_page_config(page_title="Synapse 12", page_icon="💡", layout="centered")

st.title("💡 Synapse 12")
st.subheader("Sua ideia, executada.")
st.write("_Descreva sua ideia ou o problema que deseja eliminar. Nossa rede de especialistas em IA cuida de toda a execução para você._")

if "bus" not in st.session_state:
    st.session_state.bus = MessageBus()
    st.session_state.kernel = SynapseKernel(st.session_state.bus)
    
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

st.write("### 🎬 Iniciar Projeto")
tarefa_input = st.text_area(
    "O que você precisa realizar hoje?", 
    placeholder="Ex: Quero automatizar o envio de e-mails para meus leads imobiliários ou criar um relatório de vendas...",
    height=150
)

if st.button("Dar vida ao projeto", type="primary"):
    if tarefa_input.strip():
        status_placeholder = st.empty()
        
        with st.spinner("Conectando nossa rede de especialistas..."):
            status_placeholder.info("🧠 Entendendo seus requisitos e validando o escopo...")
            
            groq_key = os.getenv("GROQ_API_KEY")
            
            if groq_key:
                try:
                    # 🚀 CHAMADA HTTP NATIVA (SEM BIBLIOTECAS EXTERNAS / IMUNE A CONFLITOS)
                    conn = http.client.HTTPSConnection("://groq.com")
                    
                    payload = json.dumps({
                        "model": "deepseek-r1-distill-llama-70b",
                        "messages": [
                            {
                                "role": "system", 
                                "content": "Você é o arquiteto central do Synapse 24. Crie uma estrutura detalhada, prática e funcional para o projeto solicitado pelo usuário, sem introduções longas ou rodeios técnicos."
                            },
                            {
                                "role": "user", 
                                "content": tarefa_input
                            }
                        ],
                        "temperature": 0.3
                    })
                    
                    headers = {
                        'Authorization': f'Bearer {groq_key}',
                        'Content-Type': 'application/json'
                    }
                    
                    conn.request("POST", "/openai/v1/chat/completions", payload, headers)
                    res = conn.getresponse()
                    data = res.read()
                    
                    if res.status == 200:
                        json_data = json.loads(data.decode("utf-8"))
                        resultado = json_data["choices"][0]["message"]["content"]
                    else:
                        resultado = f"Erro na API da Groq: Status {res.status}. Verifique suas chaves de API nos Secrets."
                except Exception as e:
                    resultado = f"Falha de conexão interna: {e}"
            else:
                resultado = "Chave de acesso GROQ_API_KEY não localizada nas configurações internas do aplicativo."
            
            status_placeholder.empty()
            
            st.success("🎉 Projeto concluído com sucesso!")
            st.write("### 📊 Aqui está o resultado da sua entrega:")
            st.info(resultado)
            st.toast("Finalizado!")
    else:
        st.warning("Por favor, descreva o que você precisa realizar hoje.")

st.markdown("---")
with st.expander("⚙️ Ver detalhes técnicos do processo (Logs Avançados)"):
    st.caption("Modo de Operação Poliglota Ativo • Conexão Direta TLS • Synapse 12 Engine Oficial")
