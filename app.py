import streamlit as st
import sys
import os
import json
import importlib.util
import time

# CONFIGURAÇÃO DA PASTA FONTE NO TOPO
PATH_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
if PATH_SRC not in sys.path:
    sys.path.append(PATH_SRC)

# Carregamento Dinâmico Isolado
caminho_rest = os.path.join(PATH_SRC, "rest_client.py")
if os.path.exists(caminho_rest):
    especificacao = importlib.util.spec_from_file_location("rest_client", caminho_rest)
    rest_client = importlib.util.module_from_spec(especificacao)
    especificacao.loader.exec_module(rest_client)
    orquestrar_chamada_rest = rest_client.orquestrar_chamada_rest
else:
    st.error(f"🚨 Arquivo crítico não encontrado em: {caminho_rest}")
    st.stop()

st.set_page_config(page_title="Synapse 24 OS", page_icon="🧠", layout="centered")
st.title("🧠 Synapse 24 OS")
st.subheader("Sua ideia, executada por uma rede de agentes.")
st.write("_Sistema operando com Rota de Fuga Híbrida Ativa (Servidor + Browser)._")
st.markdown("---")

st.write("### 🎬 Iniciar Nova Orquestração")
tarefa_input = st.text_area("O que você precisa realizar hoje?", placeholder="Crie um app para vendas", height=150)

# INTERCEPTADOR DE RESGATE PARA EXIBIR O TEXTO REAL DO GEMINI
html_gatilho_leitura = """
<script>
    const checarEEnviar = () => {
        const texto = sessionStorage.getItem("synapse_resultado_bruto");
        if (texto) {
            const inputArea = window.parent.document.querySelector("textarea");
            // Cria um alerta visual discreto no console do celular
            console.log("Synapse Cache Pronto.");
        }
    };
    setInterval(checarEEnviar, 2000);
</script>
"""
st.components.v1.html(html_gatilho_leitura, height=0)

def carregar_contexto_extensao(nome_arquivo):
    caminho = os.path.join(PATH_SRC, "agents", nome_arquivo)
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return "".join([l for l in f.readlines() if not l.startswith("import")][:20])
        except Exception:
            return ""
    return ""

def exibir_diagnostico_painel(resultado_erro):
    st.error("🚨 [Falha Crítica]: A colmeia falhou no processamento de dados.")
    with st.expander("🛠️ Ver Relatório de Diagnóstico Técnico", expanded=True):
        st.code(resultado_erro, language="text")

def resolver_retorno_agente(resposta_bruta, termo_pesquisado):
    if resposta_bruta == "SOLICITACAO_VIA_TUNEL_EM_ANDAMENTO":
        st.session_state["usando_tunel"] = True
        return f"TUNEL_ATIVO: Processando '{termo_pesquisado.strip()}' via Browser."
    return resposta_bruta

# BOTÃO DE RESGATE AUTOMÁTICO CASO O BACKEND TENHA CAÍDO
if st.session_state.get("usando_tunel"):
    st.markdown("### 📥 Captura do Navegador")
    if st.button("Visualizar Texto Gerado pelo Google", type="secondary"):
        # Pequeno script JS que injeta o valor guardado de volta na interface
        js_get = """
        <script>
        const txt = sessionStorage.getItem("synapse_resultado_bruto");
        if(txt) {
            const div = document.createElement("div");
            div.innerHTML = "<h4>📝 Resultado do Gemini Extraído com Sucesso:</h4><pre style='white-space: pre-wrap; background: #262730; padding: 15px; border-radius: 5px; color: white;'>" + txt + "</pre>";
            document.body.appendChild(div);
        } else {
            alert("O navegador ainda está processando a resposta da IA. Aguarde 3 segundos e clique novamente.");
        }
        </script>
        """
        st.components.v1.html(js_get, height=400, scrolling=True)

if st.button("Dar vida ao projeto", type="primary"):
    if tarefa_input.strip():
        st.session_state["usando_tunel"] = False
        st.write("### ⚙️ Debate e Orquestração em Tempo Real:")
        
        ctx_manager = carregar_contexto_extensao("ia02_executor_manager.py")
        ctx_monitor = carregar_contexto_extensao("ia02_executor_monitor.py")
        ctx_generator = carregar_contexto_extensao("ia02_executor_content_generator.py")
        
        with st.status("🧠 IA01 [Mediador] analisando e montando briefing técnico...", expanded=True) as s1:
            p_sistema_1 = "Você é o IA01 Mediador. Escreva um briefing enxuto com 3 requisitos baseados no objetivo final do usuário."
            briefing = orquestrar_chamada_rest(p_sistema_1, tarefa_input)
            briefing = resolver_retorno_agente(briefing, tarefa_input)
            
            if briefing.startswith("RAIZ_ERRO:"):
                s1.update(label="💥 Falha na comunicação do Mediador!", state="error")
                exibir_diagnostico_painel(briefing)
            else:
                st.write(briefing)
                s1.update(label="🧠 IA01 [Mediador] concluiu o Briefing!", state="complete")
        
        if not briefing.startswith("RAIZ_ERRO:") and "TUNEL_ATIVO" not in briefing:
            regras_ia2 = f"\nDiretrizes Administrativas:\n{ctx_manager}\nManual de Qualidade:\n{ctx_monitor}\nGerador Base:\n{ctx_generator}"
            p_sistema_2 = f"Você é o IA02 Executor Sênior. Siga estas regras: {regras_ia2}\nExecute o briefing e entregue o conteúdo estruturado em Markdown."
            p_sistema_3 = "Você é o IA03 Crítico Geral. Avalie a entrega e aponte falhas de forma enxuta."
            p_sistema_4 = "Você é o IA04 Supervisor. Responda estritamente 'APROVADO' se o material atende ao briefing, ou 'REPROVADO' se precisa de ajustes."
            
            with st.status("🛠️ IA02 [Executor] gerando versão inicial...", expanded=True) as s2:
                codigo_v1 = orquestrar_chamada_rest(p_sistema_2, briefing)
                codigo_v1 = resolver_retorno_agente(codigo_v1, tarefa_input)
                st.markdown(codigo_v1)
                s2.update(label="🛠️ IA02 [Executor] Processado!", state="complete")
                
            # Finaliza fluxo limpo exibindo instrução para o painel de resgate
            st.success("🎉 Processo de colmeia concluído via rota de segurança!")
            
