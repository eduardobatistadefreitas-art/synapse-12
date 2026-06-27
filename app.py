# app.py
import streamlit as st
import sys
import os
import json
import http.client
import time

# Garante que o Streamlit encontre a pasta 'src' no servidor em nuvem
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

st.set_page_config(page_title="Synapse 12 OS", page_icon="🧠", layout="centered")

st.title("🧠 Synapse 12 OS")
st.subheader("Sua ideia, refinada em looping autônomo supervisionado.")
st.write("_Abaixo, duas IAs principais debatem continuamente. O loop é governado pelas regras de controle do Supervisor._")

st.markdown("---")

st.write("### 🎬 Iniciar Nova Criação")
tarefa_input = st.text_area(
    "Descreva o sistema ou projeto que deseja criar:", 
    placeholder="Ex: Crie um sistema de automação para leads imobiliários que separe compradores de inquilinos...",
    height=150
)

def chamar_gemini_direto(api_key, prompt_sistema, prompt_usuario):
    """Executa a chamada REST nativa com Backoff Exponencial agressivo contra Erro 429"""
    # 🚀 BLINDAGEM CONTRA BLOQUEIOS: Aumentamos para 4 tentativas com pausas maiores de descompressão
    tentativas = 4
    atraso = 5  # Tempo inicial de espera em segundos para o recuo
    
    api_key_limpa = str(api_key).strip().replace("https://", "").replace("http://", "").replace("//", "")
    
    for tentativa in range(tentativas):
        try:
            palavras_bloqueadas = ["act as", "atue como", "ignore as regras", "system prompt"]
            if any(palavra in prompt_usuario.lower() for palavra in palavras_bloqueadas):
                return "[Erro de Segurança]: Comando inválido."

            host_limpo = "://googleapis.com"
            conn = http.client.HTTPSConnection(host_limpo, timeout=60)
            headers = {"Content-Type": "application/json", "Connection": "keep-alive"}
            
            payload = json.dumps({
                "contents": [{
                    "parts": [{"text": f"INSTRUÇÃO: {prompt_sistema}\n\nENTRADA: {prompt_usuario}"}]
                }],
                "generationConfig": {"temperature": 0.3}
            })
            
            # 🕒 CADÊNCIA DE RESPIRO: Pausa estratégica obrigatória de 3 segundos para evitar disparos em rajada
            time.sleep(3)
            
            url = f"/v1/models/gemini-2.5-flash:generateContent?key={api_key_limpa}"
            conn.request("POST", url, payload, headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            conn.close()
            
            # Interceptação e tratamento em tempo real do limite excedido
            if res.status == 429:
                if tentativa < tentativas - 1:
                    # Avisa discretamente no console/log e aguarda o tempo de recuo dobrado
                    time.sleep(atraso)
                    atraso *= 2  # O tempo dobra a cada nova falha (5s -> 10s -> 20s)
                    continue
                return "[Erro HTTP 429]: O limite gratuito do Google AI Studio está congestionado. Aguarde 60 segundos antes de reenviar."
                
            if res.status == 200:
                return json.loads(data)["candidates"]["content"]["parts"]["text"]
            return f"[Erro HTTP {res.status}]: {data[:50]}"
            
        except Exception as e:
            if tentativa < tentativas - 1:
                time.sleep(3)
                continue
            return f"[Falha de Conexão]: {e}"

if st.button("Disparar Colmeia Supervisionada", type="primary"):
    if tarefa_input.strip():
        gemini_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")
        
        if not gemini_key:
            st.error("Chave GEMINI_API_KEY não localizada nos Secrets.")
        else:
            st.write("### ⚙️ Execução da Colmeia Concorrente:")
            
            # --- 1. TRIAGEM DO MEDIADOR ---
            with st.status("🧠 IA01 [Mediador] gerando briefing inicial...", expanded=False) as s1:
                p_mediador = "Você é o IA01 Mediador. Escreva um briefing técnico com 3 requisitos objetivos baseado no desejo do usuário."
                briefing = chamar_gemini_direto(gemini_key, p_mediador, tarefa_input)
                st.write(briefing)
                s1.update(label="🧠 Briefing Inicial Estruturado!", state="complete")
            
            # --- 2. O LOOPING DINÂMICO GOVERNADO PELA IA04 ---
            st.write("#### 🔄 Ciclos de Refinamento Ativos (Supervisionados por IA04)")
            
            p_executor = "Você é o IA02 Executor, programador sênior. Escreva um código Python estruturado para resolver o briefing ou corrigir rigorosamente os erros e críticas apontados. Mande APENAS o código puro."
            p_critico = "Você é o IA03 Crítico Comercial e de Código. Analise o código enviado pelo Executor e aponte os erros e melhorias que precisam ser feitos. Se o código estiver imperfeito, exija correções."
            p_supervisor = (
                "Você é o IA04 Supervisor. Analise a última versão do código e a crítica feita pela IA03. "
                "Responda estritamente com uma palavra: 'APROVADO' se o código resolve o briefing perfeitamente, "
                "ou 'REPROVADO' se ele ainda precisa passar por mais um ciclo de refatoração."
            )
            
            # Inicialização do loop de debate
            codigo_atual = chamar_gemini_direto(gemini_key, p_executor, briefing)
            loop_ativo = True
            rodada = 1
            # 🛡️ TRAVA ANTIFRAUDE E CUSTO: Fixado em 2 rodadas para blindar o ambiente gratuito contra quedas
            max_rodadas = 2
            
            while loop_ativo and rodada <= max_rodadas:
                with st.expander(f"🔄 Rodada {rodada}: Debate Ativo & Decisão do Supervisor", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.caption(f"🛠️ Código Atual (Executor)")
                        st.code(codigo_atual, language="python")
                    
                    with col2:
                        st.caption(f"🗺️ Avaliação de Erros / Melhorias (Crítico)")
                        critica = chamar_gemini_direto(gemini_key, p_critico, codigo_atual)
                        st.write(critica)
                    
                    st.markdown("---")
                    with st.spinner("⚖️ IA04 [Supervisor] avaliando qualidade do ciclo..."):
                        contexto_supervisao = f"Briefing:\n{briefing}\n\nCódigo:\n{codigo_atual}\n\nCrítica:\n{critica}"
                        veredito = chamar_gemini_direto(gemini_key, p_supervisor, contexto_supervisao).strip().upper()
                    
                    if "APROVADO" in veredito:
                        st.success(f"✅ Rodada {rodada}: IA04 [Supervisor] emitiu veredito: **APROVADO**. Encerrando looping!")
                        loop_ativo = False
                    else:
                        st.warning(f"⚠️ Rodada {rodada}: IA04 [Supervisor] emitiu veredito: **REPROVADO**. Forçando refatoração!")
                        prompt_reajuste = f"Briefing Original:\n{briefing}\n\nCódigo Atual:\n{codigo_atual}\n\nErros para Corrigir:\n{critica}"
                        codigo_atual = chamar_gemini_direto(gemini_key, p_executor, prompt_reajuste)
                        rodada += 1
            
            # --- 3. AUDITORIA FINAL DE SEGURANÇA ---
            with st.status("🛡️ IA05 [Auditor] validando entrega final...", expanded=False) as s4:
                p_auditor = "Você é o IA05 Auditor. Faça uma varredura final de segurança no código homologado pelo supervisor e dê seu aval."
                auditoria = chamar_gemini_direto(gemini_key, p_auditor, codigo_atual)
                st.write(auditoria)
                s4.update(label="🛡️ Auditoria Final de Segurança Concluída!", state="complete")

            st.success("🎉 Processo de Orquestração Concluído pela Colmeia!")
            
            # Entrega Final
            st.write("### 🏁 Código Homologado Pós-Debate:")
            st.code(codigo_atual, language="python")
    else:
        st.warning("Por favor, descreva o que você deseja realizar.")
                        
