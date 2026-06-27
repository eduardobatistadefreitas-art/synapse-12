# app.py
import streamlit as st
import sys
import os
import json
import http.client

# Garante que o Streamlit encontre a pasta 'src' no servidor em nuvem
PATH_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(PATH_SRC)

st.set_page_config(page_title="Synapse 12 OS", page_icon="🧠", layout="centered")

st.title("🧠 Synapse 12 OS")
st.subheader("Sua ideia, executada por uma rede de agentes.")
st.write("_Descreva seu objetivo. Nossa colmeia de IAs vai planejar, codificar, criticar e auditar a entrega em tempo real._")

st.markdown("---")

# Painel de Entrada do Usuário (Cliente 01)
st.write("### 🎬 Iniciar Nova Orquestração")
tarefa_input = st.text_area(
    "O que você precisa realizar hoje?", 
    placeholder="Ex: Crie um sistema de automação para leads imobiliários que separe compradores de inquilinos...",
    height=150
)

def carregar_contexto_extensao(nome_arquivo):
    """Lê com segurança os arquivos criados pela IA2 para usá-los como manual de regras"""
    caminho = os.path.join(PATH_SRC, "agents", nome_arquivo)
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                linhas = f.readlines()
                return "".join([l for l in linhas if not l.startswith("import")][:20])
        except Exception:
            return ""
    return ""

def chamar_gemini_direto(api_key, prompt_sistema, prompt_usuario):
    """Executa a chamada REST nativa com timeout estendido e persistência de conexão"""
    try:
        host = "://googleapis.com"
        # 🚀 CORREÇÃO CRÍTICA: Removido o .http duplicado gerado pelo teclado móvel
        conn = http.client.HTTPSConnection(host, timeout=60)
        
        headers = {
            "Content-Type": "application/json",
            "Connection": "keep-alive"
        }
        
        payload = json.dumps({
            "contents": [{
                "parts": [{
                    "text": f"{prompt_sistema}\n\nComando do Usuário: {prompt_usuario}"
                }]
            }],
            "generationConfig": {"temperature": 0.2}
        })
        
        url = f"/v1/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
        conn.request("POST", url, payload, headers)
        
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        conn.close()
        
        if res.status == 200:
            json_data = json.loads(data)
            return json_data["candidates"][0]["content"]["parts"][0]["text"]
        return f"[Erro HTTP {res.status}]: {data[:100]}"
    except Exception as e:
        return f"[Falha de Conexão]: {e}"

if st.button("Dar vida ao projeto", type="primary"):
    if tarefa_input.strip():
        gemini_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")
        
        if not gemini_key:
            st.error("Chave GEMINI_API_KEY não localizada nos Secrets do Streamlit. Insira a chave para ativar as IAs.")
        else:
            st.write("### ⚙️ Debate e Orquestração da Synapse em Tempo Real:")
            
            # CARREGAMENTO AUTOMÁTICO DAS EXTENSÕES DO SEU PRINT
            ctx_manager = carregar_contexto_extensao("ia02_executor_manager.py")
            ctx_monitor = carregar_contexto_extensao("ia02_executor_monitor.py")
            ctx_generator = carregar_contexto_extensao("ia02_executor_content_generator.py")
            
            # --- CASO 1: IA01 MEDIADOR ---
            with st.status("🧠 IA01 [Mediador] está fazendo a triagem e estruturando o briefing...", expanded=True) as s1:
                p_sistema_1 = "Você é o IA01 Mediador. Escreva um briefing técnico ultra enxuto com 3 requisitos baseados na ideia do usuário."
                briefing = chamar_gemini_direto(gemini_key, p_sistema_1, tarefa_input)
                st.write(briefing)
                s1.update(label="🧠 IA01 [Mediador] concluiu o Briefing Técnico!", state="complete")
            
            # CONFIGURAÇÃO DOS PROMPTS COM AS DIRETRIZES REAIS DO SEU REPOSITÓRIO
            regras_ia2 = f"\nDiretrizes Administrativas:\n{ctx_manager}\nManual de Qualidade:\n{ctx_monitor}\nGerador Base:\n{ctx_generator}"
            
            p_sistema_2 = f"Você é o IA02 Executor, programador sênior. Siga estas regras internas desenvolvidas pelo seu sistema: {regras_ia2}\nEscreva um código Python estruturado para resolver o briefing ou corrigir as falhas apontadas. Mande apenas o código dentro de blocos markdown."
            p_sistema_3 = "Você é o IA03 Crítico Comercial. Avalie o código enviado pelo Executor e aponte erros técnicos ou de custo estruturais que precisam ser refeitos imediatamente."
            p_sistema_4 = "Você é o IA04 Supervisor. Analise o código e a crítica feita pelo IA03. Responda estritamente 'APROVADO' se o código está pronto e functional, ou 'REPROVADO' se ele ainda precisa passar por refinamento."
            
            # Geração da versão inicial (Rodada 0)
            with st.status("🛠️ IA02 [Executor] gerando versão inicial do código...", expanded=True) as s2:
                codigo_v1 = chamar_gemini_direto(gemini_key, p_sistema_2, briefing)
                st.code(codigo_v1, language="python")
                s2.update(label="🛠️ IA02 [Executor] gerou a Versão Inicial!", state="complete")

            # --- O LOOPING REAL SUPERVISIONADO ---
            loop_ativo = True
            rodada = 1
            max_rodadas = 2
            
            while loop_ativo and rodada <= max_rodadas:
                st.markdown(f"#### 🔄 Rodada {rodada} de Ajuste")
                
                # Turno do Crítico (IA03)
                with st.status(f"🗺️ Rodada {rodada}: IA03 [Crítico] analisando código atual...", expanded=True) as s3:
                    critica = chamar_gemini_direto(gemini_key, p_sistema_3, codigo_v1)
                    st.write(critica)
                    s3.update(label=f"🗺️ Rodada {rodada}: Análise do Crítico Emitida!", state="complete")
                
                # Turno de Julgamento do Supervisor (IA04)
                with st.status(f"⚖️ Rodada {rodada}: IA04 [Supervisor] julgando qualidade...", expanded=True) as s_super:
                    contexto_supervisao = f"Briefing:\n{briefing}\n\nCódigo:\n{codigo_v1}\n\nCrítica:\n{critica}"
                    veredito = chamar_gemini_direto(gemini_key, p_sistema_4, contexto_supervisao).strip().upper()
                    st.write(f"Veredito do Supervisor: **{veredito}**")
                    
                    if "APROVADO" in veredito:
                        s_super.update(label=f"✅ Rodada {rodada}: Supervisor aprovou a solução!", state="complete")
                        loop_ativo = False
                    else:
                        s_super.update(label=f"⚠️ Rodada {rodada}: Supervisor reprovou! Forçando refatoração.", state="complete")
                        # Turno de Correção do Executor (IA02)
                        with st.status(f"🛠️ Rodada {rodada}: IA02 [Executor] aplicando correções...", expanded=True) as s_exec_fix:
                            prompt_reajuste = f"Briefing:\n{briefing}\n\nCódigo Atual:\n{codigo_v1}\n\nErros para Corrigir:\n{critica}"
                            codigo_v1 = chamar_gemini_direto(gemini_key, p_sistema_2, prompt_reajuste)
                            st.code(codigo_v1, language="python")
                            s_exec_fix.update(label=f"🛠️ Rodada {rodada}: Código Reescrito pelo Executor!", state="complete")
                        rodada += 1

            # --- CASO 4: IA05 AUDITOR ---
            with st.status("⚖️ IA05 [Auditor] está caçando bugs e revisando a segurança do código...", expanded=True) as s4:
                p_sistema_5 = "Você é o IA05 Auditor de Código/Adversário. Analise o código gerado pelo Executor e aponte se ele está seguro e funcional ou se tem algum erro grave."
                auditoria = chamar_gemini_direto(gemini_key, p_sistema_5, codigo_v1)
                st.write(auditoria)
                s4.update(label="⚖️ IA05 [Auditor] finalizou a Auditoria Técnica!", state="complete")

            st.success("🎉 Processo de Orquestração Concluído pela Colmeia!")
            
            # Resultado Final Consolidado
            st.write("### 🏁 Entrega Final Homologada:")
            st.info(f"**Requisitos do Projeto:**\n{briefing}")
            st.markdown("**Código Final Desenvolvido:**")
            st.code(codigo_v1, language="python")
    else:
        st.warning("Por favor,描述 o que você deseja realizar.")

st.markdown("---")
with st.expander("⚙️ Ver Arquitetura da Rede"):
    st.caption("Synapse 12 Engine • Integração de Extensões Concorrentes • Google AI Studio Layer")
