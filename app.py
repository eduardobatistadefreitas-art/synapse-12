# app.py
import streamlit as st
import sys
import os
from rest_client import orquestrar_chamada_rest

PATH_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(PATH_SRC)

st.set_page_config(page_title="Synapse 12 OS", page_icon="🧠", layout="centered")
st.title("🧠 Synapse 12 OS")
st.subheader("Sua ideia, executada por uma rede de agentes.")
st.write("_Sistema operando em Malha de Redundância Quádrupla Automática (NVIDIA/OpenRouter/Groq/Gemini)._")
st.markdown("---")

st.write("### 🎬 Iniciar Nova Orquestração")
tarefa_input = st.text_area("O que você precisa realizar hoje?", placeholder="Ex: Escreva uma tese sobre física quântica...", height=150)

def carregar_contexto_extensao(nome_arquivo):
    caminho = os.path.join(PATH_SRC, "agents", nome_arquivo)
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return "".join([l for l in f.readlines() if not l.startswith("import")][:20])
        except Exception: return ""
    return ""

if st.button("Dar vida ao projeto", type="primary"):
    if tarefa_input.strip():
        st.write("### ⚙️ Debate e Orquestração em Tempo Real:")
        ctx_manager = carregar_contexto_extensao("ia02_executor_manager.py")
        ctx_monitor = carregar_contexto_extensao("ia02_executor_monitor.py")
        ctx_generator = carregar_contexto_extensao("ia02_executor_content_generator.py")
        
        with st.status("🧠 IA01 [Mediador] analisando e montando briefing técnico...", expanded=True) as s1:
            p_sistema_1 = "Você é o IA01 Mediador. Escreva um briefing enxuto com 3 requisitos baseados no objetivo final do usuário."
            briefing = orquestrar_chamada_rest(p_sistema_1, tarefa_input)
            st.write(briefing)
            s1.update(label="🧠 IA01 [Mediador] concluiu o Briefing!", state="complete")
        
        if "[Erro" not in briefing:
            regras_ia2 = f"\nDiretrizes Administrativas:\n{ctx_manager}\nManual de Qualidade:\n{ctx_monitor}\nGerador Base:\n{ctx_generator}"
            p_sistema_2 = f"Você é o IA02 Executor Sênior. Siga estas regras: {regras_ia2}\nExecute o briefing. Se o usuário pediu código, forneça código Python puro. Se pediu uma tese, livro ou história, entregue em Markdown limpo."
            p_sistema_3 = "Você é o IA03 Crítico Geral. Avalie a entrega e aponte falhas de forma enxuta."
            p_sistema_4 = "Você é o IA04 Supervisor. Responda estritamente 'APROVADO' se o material atende ao briefing, ou 'REPROVADO' se precisa de ajustes."
            
            with st.status("🛠️ IA02 [Executor] gerando versão inicial...", expanded=True) as s2:
                codigo_v1 = orquestrar_chamada_rest(p_sistema_2, briefing)
                st.markdown(codigo_v1)
                s2.update(label="🛠️ IA02 [Executor] gerou a Versão Inicial!", state="complete")

            loop_ativo, rodada, max_rodadas = True, 1, 2
            while loop_ativo and rodada <= max_rodadas and "[Erro" not in codigo_v1:
                st.markdown(f"#### 🔄 Rodada {rodada} de Ajuste")
                with st.status(f"🗺️ Rodada {rodada}: IA03 [Crítico] analisando entrega...", expanded=True) as s3:
                    critica = orquestrar_chamada_rest(p_sistema_3, codigo_v1)
                    st.write(critica)
                    s3.update(label=f"🗺️ Rodada {rodada}: Análise do Crítico Emitida!", state="complete")
                
                with st.status(f"⚖️ Rodada {rodada}: IA04 [Supervisor] julgando...", expanded=True) as s_super:
                    contexto_supervisao = f"Briefing:\n{briefing}\n\nEntrega:\n{codigo_v1}\n\nCrítica:\n{critica}"
                    veredito = orquestrar_chamada_rest(p_sistema_4, contexto_supervisao).strip().upper()
                    st.write(f"Veredito do Supervisor: **{veredito}**")
                    if "APROVADO" in veredito:
                        s_super.update(label=f"✅ Rodada {rodada}: Aprovado!", state="complete")
                        loop_ativo = False
                    else:
                        s_super.update(label=f"⚠️ Rodada {rodada}: Reprovado! Refatorando.", state="complete")
                        with st.status(f"🛠️ Rodada {rodada}: IA02 corrigindo...", expanded=True) as s_exec_fix:
                            prompt_reajuste = f"Briefing:\n{briefing}\n\nEntrega:\n{codigo_v1}\n\nErros:\n{critica}"
                            codigo_v1 = orquestrar_chamada_rest(p_sistema_2, prompt_reajuste)
                            st.markdown(codigo_v1)
                            s_exec_fix.update(label=f"🛠️ Rodada {rodada}: Reescrito!", state="complete")
                        rodada += 1

            if "[Erro" not in codigo_v1:
                with st.status("⚖️ IA05 [Auditor] revisando qualidade final...", expanded=True) as s4:
                    p_sistema_5 = "Você é o IA05 Auditor. Analise a entrega final e aponte se ela está segura e coesa."
                    auditoria = orquestrar_chamada_rest(p_sistema_5, codigo_v1)
                    st.write(auditoria)
                    s4.update(label="⚖️ IA05 [Auditor] finalizou!", state="complete")
                st.success("🎉 Concluído pela Colmeia!")
                st.write("### 🏁 Entrega Final Homologada:")
                st.info(f"**Requisitos:**\n{briefing}")
                st.markdown(codigo_v1)
            else: st.error(codigo_v1)
        else: st.error(briefing)
    else: st.warning("Por favor, descreva o que deseja realizar.")

st.markdown("---")
with st.expander("⚙️ Ver Arquitetura"):
    st.caption("Synapse 24 OS Engine • Redundância Quádrupla Ativa • Custo Zero")
    
