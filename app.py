# app.py
import streamlit as st
import sys
import os
import json
import http.client
import time

# Garante que o Streamlit encontre a pasta 'src' no servidor em nuvem
PATH_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(PATH_SRC)

st.set_page_config(page_title="Synapse 12 OS", page_icon="🧠", layout="centered")

st.title("🧠 Synapse 12 OS")
st.subheader("Sua ideia, executada por uma rede de agentes.")
st.write("_Descreva seu objetivo. Nossa colmeia poliglota cria códigos, teses ou histórias em tempo real com tolerância a falhas._")

st.markdown("---")

# Painel de Entrada do Usuário (Cliente 01)
st.write("### 🎬 Iniciar Nova Orquestração")
tarefa_input = st.text_area(
    "O que você precisa realizar hoje?", 
    placeholder="Ex: Escreva uma tese sobre física quântica... OU Crie um sistema de automação em Python...",
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

def chamar_gemini_direto(api_keys_str, prompt_sistema, prompt_usuario):
    """Executa a chamada REST nativa com Rotação Automática de Chaves de Backup se houver Erro 429"""
    # Isola cada chave separada por vírgula nos Secrets
    lista_chaves = [k.strip() for k in str(api_keys_str).split(",") if k.strip()]
    
    palavras_bloqueadas = ["act as", "atue como", "ignore as regras", "system prompt"]
    if any(palavra in prompt_usuario.lower() for palavra in palavras_bloqueadas):
        return "[Erro de Segurança]: Comando inválido."

    host_limpo = "://googleapis.com"
    payload = json.dumps({
        "contents": [{
            "parts": [{"text": f"INSTRUÇÃO: {prompt_sistema}\n\nENTRADA: {prompt_usuario}"}]
        }],
        "generationConfig": {"temperature": 0.3}
    })

    # Varre a lista de chaves. Se uma falhar por cota, assume a próxima na hora
    for api_key in lista_chaves:
        api_key_limpa = api_key.replace("https://", "").replace("http://", "").replace("//", "")
        tentativas = 2
        
        for tentativa in range(tentativas):
            try:
                conn = http.client.HTTPSConnection(host_limpo, timeout=60)
                headers = {"Content-Type": "application/json", "Connection": "keep-alive"}
                
                # Respiro regulatório sutil para evitar concorrência destrutiva
                time.sleep(2)
                
                # 🚀 OPERAÇÃO SEGURA: gemini-2.0-flash aguenta maior volume de texto sem engasgar
                url = f"/v1/models/gemini-2.0-flash:generateContent?key={api_key_limpa}"
                conn.request("POST", url, payload, headers)
                res = conn.getresponse()
                data = res.read().decode("utf-8")
                conn.close()
                
                # 🛡️ CAPTURA SELETIVA DE QUEDA DE COTA DIÁRIA (429)
                if res.status == 429:
                    if "quota" in data.lower() or "limit" in data.lower() or "exceeded" in data.lower():
                        break # Abandona esta chave esgotada e pula para a próxima da lista
                    time.sleep(4)
                    continue
                    
                if res.status == 200:
                    return json.loads(data)["candidates"]["content"]["parts"]["text"]
                return f"[Erro HTTP {res.status}]: {data[:50]}"
                
            except Exception:
                if tentativa < tentativas - 1:
                    time.sleep(2)
                    continue
                    
    return "[Erro Crítico]: Todas as suas chaves gratuitas do Google AI Studio atingiram o limite diário de cota. Insira uma nova chave de backup nos Secrets para destravar."

if st.button("Dar vida ao projeto", type="primary"):
    if tarefa_input.strip():
        gemini_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")
        
        if not gemini_key:
            st.error("Chave GEMINI_API_KEY não localizada nos Secrets do Streamlit.")
        else:
            st.write("### ⚙️ Debate e Orquestração da Synapse em Tempo Real:")
            
            ctx_manager = carregar_contexto_extensao("ia02_executor_manager.py")
            ctx_monitor = carregar_contexto_extensao("ia02_executor_monitor.py")
            ctx_generator = carregar_contexto_extensao("ia02_executor_content_generator.py")
            
            # --- CASO 1: IA01 MEDIADOR ---
            with st.status("🧠 IA01 [Mediador] está fazendo a triagem e estruturando o briefing...", expanded=True) as s1:
                p_sistema_1 = "Você é o IA01 Mediador. Escreva um briefing enxuto com 3 requisitos baseados no objetivo final do usuário (seja texto, literatura, tese ou código)."
                briefing = chamar_gemini_direto(gemini_key, p_sistema_1, tarefa_input)
                st.write(briefing)
                s1.update(label="🧠 IA01 [Mediador] concluiu o Briefing!", state="complete")
            
            if "[Erro" not in briefing:
                regras_ia2 = f"\nDiretrizes Administrativas:\n{ctx_manager}\nManual de Qualidade:\n{ctx_monitor}\nGerador Base:\n{ctx_generator}"
                
                p_sistema_2 = f"Você é o IA02 Executor Sênior. Siga estas regras internas: {regras_ia2}\nExecute e redija o conteúdo final solicitado no briefing. Se o usuário pediu código, forneça código. Se ele pediu uma tese, livro ou história, entregue em formato de texto limpo, rico e estruturado em Markdown."
                p_sistema_3 = "Você é o IA03 Crítico Geral. Avalie a entrega enviada pelo Executor e aponte erros estruturais, conceituais ou de qualidade de conteúdo de forma enxuta."
                p_sistema_4 = "Você é o IA04 Supervisor. Analise a entrega e a crítica do IA03. Responda estritamente 'APROVADO' se o material atende perfeitamente ao briefing, ou 'REPROVADO' se ele ainda precisa passar por refinamento."
                
                # Geração da versão inicial
                with st.status("🛠️ IA02 [Executor] gerando versão inicial da entrega...", expanded=True) as s2:
                    codigo_v1 = chamar_gemini_direto(gemini_key, p_sistema_2, briefing)
                    st.markdown(codigo_v1)
                    s2.update(label="🛠️ IA02 [Executor] gerou a Versão Inicial!", state="complete")

                # --- O LOOPING REAL SUPERVISIONADO ---
                loop_ativo = True
                rodada = 1
                max_rodadas = 2
                
                while loop_ativo and rodada <= max_rodadas and "[Erro" not in codigo_v1:
                    st.markdown(f"#### 🔄 Rodada {rodada} de Ajuste")
                    
                    with st.status(f"🗺️ Rodada {rodada}: IA03 [Crítico] analisando entrega atual...", expanded=True) as s3:
                        critica = chamar_gemini_direto(gemini_key, p_sistema_3, codigo_v1)
                        st.write(critica)
                        s3.update(label=f"🗺️ Rodada {rodada}: Análise do Crítico Emitida!", state="complete")
                    
                    with st.status(f"⚖️ Rodada {rodada}: IA04 [Supervisor] julgando qualidade...", expanded=True) as s_super:
                        contexto_supervisao = f"Briefing:\n{briefing}\n\nEntrega:\n{codigo_v1}\n\nCrítica:\n{critica}"
                        veredito = chamar_gemini_direto(gemini_key, p_sistema_4, contexto_supervisao).strip().upper()
                        st.write(f"Veredito do Supervisor: **{veredito}**")
                        
                        if "APROVADO" in veredito:
                            s_super.update(label=f"✅ Rodada {rodada}: Supervisor aprovou a solução!", state="complete")
                            loop_ativo = False
                        else:
                            s_super.update(label=f"⚠️ Rodada {rodada}: Supervisor reprovou! Forçando refatoração.", state="complete")
                            with st.status(f"🛠️ Rodada {rodada}: IA02 [Executor] aplicando correções...", expanded=True) as s_exec_fix:
                                prompt_reajuste = f"Briefing:\n{briefing}\n\nEntrega Atual:\n{codigo_v1}\n\nErros para Corrigir:\n{critica}"
                                codigo_v1 = chamar_gemini_direto(gemini_key, p_sistema_2, prompt_reajuste)
                                st.markdown(codigo_v1)
                                s_exec_fix.update(label=f"🛠️ Rodada {rodada}: Material Reescrito pelo Executor!", state="complete")
                            rodada += 1

                if "[Erro" not in codigo_v1:
                    # --- CASO 4: IA05 AUDITOR ---
                    with st.status("⚖️ IA05 [Auditor] revisando a qualidade final da entrega...", expanded=True) as s4:
                        p_sistema_5 = "Você é o IA05 Auditor. Analise a entrega final gerada pelo Executor e aponte se ela está segura, coesa e funcional."
                        auditoria = chamar_gemini_direto(gemini_key, p_sistema_5, codigo_v1)
                        st.write(auditoria)
                        s4.update(label="⚖️ IA05 [Auditor] finalizou a Auditoria!", state="complete")

                    st.success("🎉 Processo de Orquestração Concluído pela Colmeia!")
                    
                    # Resultado Final Consolidado Dinâmico
                    st.write("### 🏁 Entrega Final Homologada:")
                    st.info(f"**Requisitos do Projeto:**\n{briefing}")
                    st.markdown("**Conteúdo Final Desenvolvido:**")
                    st.markdown(codigo_v1)
                else:
                    st.error(codigo_v1)
            else:
                st.error(briefing)
    else:
        st.warning("Por favor, descreva o que você deseja realizar.")

st.markdown("---")
with st.expander("⚙️ Ver Arquitetura da Rede"):
    st.caption("Synapse 24 Engine • Malha Multi-Chave Poliglota • Google AI Studio Layer")
