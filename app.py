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
st.write("_Sistema operando em Malha de Redundância Quádrupla Automática._")

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

def orquestrar_chamada_rest(prompt_sistema, prompt_usuario):
    """Orquestrador resiliente com Failover Real e correção estrita de sintaxe"""
    palavras_bloqueadas = ["act as", "atue como", "ignore as regras", "system prompt"]
    if any(palavra in prompt_usuario.lower() for palavra in palavras_bloqueadas):
        return "[Erro de Segurança]: Comando inválido."

    # Mapeamento dinâmico sem funções lambda complexas que quebram o interpretador
    provedores = [
        {
            "nome": "NVIDIA",
            "key": st.secrets.get("NVIDIA_API_KEY"),
            "host": "integrate.api.nvidia.com",
            "url": "/v1/chat/completions",
            "payload": {"model": "meta/llama-3.3-70b-instruct", "messages": [{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt_usuario}], "temperature": 0.3, "max_tokens": 1024},
            "is_openai_format": True
        },
        {
            "nome": "OpenRouter",
            "key": st.secrets.get("OPENROUTER_API_KEY"),
            "host": "openrouter.ai",
            "url": "/api/v1/chat/completions",
            "payload": {"model": "meta-llama/llama-3.3-70b-instruct:free", "messages": [{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt_usuario}], "temperature": 0.3},
            "is_openai_format": True
        },
        {
            "nome": "Groq",
            "key": st.secrets.get("GROQ_API_KEY"),
            "host": "://groq.com",
            "url": "/openai/v1/chat/completions",
            "payload": {"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt_usuario}], "temperature": 0.3},
            "is_openai_format": True
        },
        {
            "nome": "Gemini",
            "key": st.secrets.get("GEMINI_API_KEY"),
            "host": "generativelanguage.googleapis.com",
            "url": "/v1/models/gemini-2.0-flash:generateContent",
            "payload": {"contents": [{"parts": [{"text": f"INSTRUÇÃO: {prompt_sistema}\n\nENTRADA: {prompt_usuario}"}]}], "generationConfig": {"temperature": 0.3}},
            "is_openai_format": False
        }
    ]

    for prov in provedores:
        # Tratamento seguro de strings das chaves
        chave_bruta = str(prov["key"]).strip()
        if not prov["key"] or "não localizada" in chave_bruta.lower() or chave_bruta == "None" or not chave_bruta:
            continue
            
        # Pega a primeira chave se for o formato de lista do Gemini
        if prov["nome"] == "Gemini" and "," in chave_bruta:
            chave_bruta = [k.strip() for k in chave_bruta.split(",") if k.strip()][0]
            
        try:
            conn = http.client.HTTPSConnection(prov["host"], timeout=45)
            
            # Cabeçalhos montados nativamente com correção do token AQ.
            if prov["is_openai_format"]:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {chave_bruta}",
                    "Connection": "keep-alive"
                }
            else:
                headers = {
                    "Content-Type": "application/json",
                    "x-goog-api-key": chave_bruta.replace("https://", "").replace("http://", "").replace("//", ""),
                    "Connection": "keep-alive"
                }
            
            time.sleep(1) # Respiro preventivo
            conn.request("POST", prov["url"], json.dumps(prov["payload"]), headers)
            res = conn.getcall = conn.getresponse() if hasattr(conn, 'getcall') else conn.getresponse()
            data = res.read().decode("utf-8")
            conn.close()
            
            if res.status == 200:
                json_data = json.loads(data)
                if prov["is_openai_format"]:
                    return json_data["choices"][0]["message"]["content"]
                return json_data["candidates"][0]["content"]["parts"][0]["text"]
                
            # Se a API atual falhar (Cota/429/503), pula silenciosamente para a próxima da malha
            continue
                
        except Exception:
            continue
            
    return "[Erro Crítico Total]: Todas as malhas de IA (NVIDIA, OpenRouter, Groq e Gemini) falharam ou estão sem chaves válidas configuradas."

if st.button("Dar vida ao projeto", type="primary"):
    if tarefa_input.strip():
        st.write("### ⚙️ Debate e Orquestração da Synapse em Tempo Real:")
        
        ctx_manager = carregar_contexto_extensao("ia02_executor_manager.py")
        ctx_monitor = carregar_contexto_extensao("ia02_executor_monitor.py")
        ctx_generator = carregar_contexto_extensao("ia02_executor_content_generator.py")
        
        # --- CASO 1: IA01 MEDIADOR ---
        with st.status("🧠 IA01 [Mediador] analisando e montando briefing técnico...", expanded=True) as s1:
            p_sistema_1 = "Você é o IA01 Mediador. Escreva um briefing enxuto com 3 requisitos baseados no objetivo final do usuário (seja texto, literatura, tese ou código)."
            briefing = orquestrar_chamada_rest(p_sistema_1, tarefa_input)
            st.write(briefing)
            s1.update(label="🧠 IA01 [Mediador] concluiu o Briefing!", state="complete")
        
        if "[Erro" not in briefing:
            regras_ia2 = f"\nDiretrizes Administrativas:\n{ctx_manager}\nManual de Qualidade:\n{ctx_monitor}\nGerador Base:\n{ctx_generator}"
            
            p_sistema_2 = f"Você é o IA02 Executor Sênior. Siga estas regras internas: {regras_ia2}\nExecute e redija o conteúdo final solicitado no briefing. Se o usuário pediu código, fornecer código Python puro dentro de blocos markdown. Se ele pediu uma tese, livro ou história, entregue em formato de texto limpo, rico e estruturado em Markdown."
            p_sistema_3 = "Você é o IA03 Crítico Geral. Avalie a entrega enviada pelo Executor e aponte erros estruturais, conceituais ou de qualidade de conteúdo de forma enxuta."
            p_sistema_4 = "Você é o IA04 Supervisor. Analise a entrega e a crítica do IA03. Responda estritamente 'APROVADO' se o material atende perfeitamente ao briefing, ou 'REPROVADO' se ele ainda precisa passar por refinamento."
            
            # Geração da versão inicial
            with st.status("🛠️ IA02 [Executor] gerando versão inicial da entrega...", expanded=True) as s2:
                codigo_v1 = orquestrar_chamada_rest(p_sistema_2, briefing)
                st.markdown(codigo_v1)
                s2.update(label="🛠️ IA02 [Executor] gerou a Versão Inicial!", state="complete")

            # --- O LOOPING REAL SUPERVISIONADO ---
            loop_ativo = True
            rodada = 1
            max_rodadas = 2
            
            while loop_ativo and rodada <= max_rodadas and "[Erro" not in codigo_v1:
                st.markdown(f"#### 🔄 Rodada {rodada} de Ajuste")
                
                with st.status(f"🗺️ Rodada {rodada}: IA03 [Crítico] analisando entrega atual...", expanded=True) as s3:
                    critica = orquestrar_chamada_rest(p_sistema_3, codigo_v1)
                    st.write(critica)
                    s3.update(label=f"🗺️ Rodada {rodada}: Análise do Crítico Emitida!", state="complete")
                
                with st.status(f"⚖️ Rodada {rodada}: IA04 [Supervisor] julgando qualidade...", expanded=True) as s_super:
                    contexto_supervisao = f"Briefing:\n{briefing}\n\nEntrega:\n{codigo_v1}\n\nCrítica:\n{critica}"
                    veredito = orquestrar_chamada_rest(p_sistema_4, contexto_supervisao).strip().upper()
                    st.write(f"Veredito do Supervisor: **{veredito}**")
                    
                    if "APROVADO" in veredito:
                        s_super.update(label=f"✅ Rodada {rodada}: Supervisor aprovou a solução!", state="complete")
                        loop_ativo = False
                    else:
                        s_super.update(label=f"⚠️ Rodada {rodada}: Supervisor reprovou! Forçando refatoração.", state="complete")
                        with st.status(f"🛠️ Rodada {rodada}: IA02 [Executor] aplicando correções...", expanded=True) as s_exec_fix:
                            prompt_reajuste = f"Briefing:\n{briefing}\n\nEntrega Atual:\n{codigo_v1}\n\nErros para Corrigir:\n{critica}"
                            codigo_v1 = orquestrar_chamada_rest(p_sistema_2, prompt_reajuste)
                            st.markdown(codigo_v1)
                            s_exec_fix.update(label=f"🛠️ Rodada {rodada}: Material Reescrito pelo Executor!", state="complete")
                            rodada += 1

            if "[Erro" not in codigo_v1:
                # --- CASO 4: IA05 AUDITOR ---
                with st.status("⚖️ IA05 [Auditor] revisando a qualidade final da entrega...", expanded=True) as s4:
                    p_sistema_5 = "Você é o IA05 Auditor. Analise a entrega final gerada pelo Executor e aponte se ela está segura, coesa e funcional."
                    auditoria = orquestrar_chamada_rest(p_sistema_5, codigo_v1)
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
    st.caption("Synapse 24 OS Engine • Malha Crítica de Redundância Quádrupla Ativa • Custo Zero")
