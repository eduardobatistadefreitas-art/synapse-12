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

# Carregamento Dinâmico com Quebra de Cache Total
caminho_rest = os.path.join(PATH_SRC, "rest_client.py")
if os.path.exists(caminho_rest):
    especificacao = importlib.util.spec_from_file_location("rest_client", caminho_rest)
    rest_client = importlib.util.module_from_spec(especificacao)
    especificacao.loader.exec_module(rest_client)
    orquestrar_chamada_rest = rest_client.executar_chamada_rest_v5
else:
    st.error(f"🚨 Arquivo critico nao encontrado em: {caminho_rest}")
    st.stop()

# Importacoes dos Modulos .py de Inteligencia e Adaptacao Estruturada
try:
    from src.agents.ia02_smart_validator import SmartValidator
    from src.agents.ia02_executor_manager import executar_analise_gerencial
    from src.utils.context_analyzer import ContextAnalyzer
    from src.agents.ia05_auditor_feedback import AuditorFeedbackSystem
except ModuleNotFoundError:
    sys.path.append(os.path.join(PATH_SRC, "agents"))
    sys.path.append(os.path.join(PATH_SRC, "utils"))
    from ia02_smart_validator import SmartValidator
    from ia02_executor_manager import executar_analise_gerencial
    from context_analyzer import ContextAnalyzer
    from ia05_auditor_feedback import AuditorFeedbackSystem

st.set_page_config(page_title="Synapse 24 OS", page_icon="🧠", layout="centered")
st.title("🧠 Synapse 24 OS")
st.subheader("Sua ideia, executada por uma rede de agentes.")
st.write("_Ecossistema Expandido com Analisador de Contexto e Aprendizado Continuo .py_")
st.markdown("---")

st.write("### 🎬 Iniciar Nova Orquestração")
tarefa_input = st.text_area("O que voce precisa realizar hoje?", placeholder="Crie um app para vendas", height=150)

if st.button("Dar vida ao projeto", type="primary"):
    if tarefa_input.strip():
        st.write("### ⚙️ Debate e Orquestracao em Tempo Real:")
        
        # Inicializacao dos utilitarios de back-end criados
        validador_smart = SmartValidator()
        analisador_contexto = ContextAnalyzer()
        sistema_feedback = AuditorFeedbackSystem(pasta_destino=PATH_SRC)
        
        # 1. Fase de Contexto Pro-ativa: Extracao de tags via Python nativo
        tags_contexto = analisador_contexto.extrair_tags_intencao(tarefa_input)
        historico_aprendido = sistema_feedback.carregar_aprendizado_atual()
        
        st.info(f"🔍 **Analise de Contexto de Nuvem**: Intent identificada -> `{tags_contexto}`")
        if historico_aprendido.get("diretriz_ajustada") == "FORCAR_METRICAS_ESTRITAS_SMART":
            st.caption("📈 *Ajuste Adaptativo*: Rodadas anteriores foram instaveis. Forcando rigor SMART maximo.*")

        loop_mediador = True
        rodada_mediador = 1
        max_rodadas_mediador = 2
        briefing = ""
        
        # 🔄 LOOP DE VALIDAÇÃO PROGRAMÁTICA DO MEDIADOR (IA01)
        while loop_mediador and rodada_mediador <= max_rodadas_mediador:
            time.sleep(3) # Pausa obrigatoria anti-spam de chaves
            
            with st.status(f"🧠 [Rodada {rodada_mediador}] IA01 [Mediador] estruturando briefing...", expanded=True) as s1:
                diretriz_historica = historico_aprendido.get("diretriz_ajustada", "NORMAL")
                p_sistema_1 = f"Voce e o IA01 Mediador. Contexto: {tags_contexto}. Diretriz: {diretriz_historica}. Escreva um briefing tecnico contendo Objetivo, Requisitos com metricas (%) e Cronograma."
                
                prompt_envio = tarefa_input if rodada_mediador == 1 else f"{tarefa_input} \n\n⚠️ REPROVADO: O briefing anterior falhou nos criterios SMART do validador. Refatore inserindo metricas quantificaveis claras."
                
                briefing = orquestrar_chamada_rest(p_sistema_1, prompt_envio)
                
                if briefing.startswith("RAIZ_ERRO:"):
                    s1.update(label="💥 Falha fisica de comunicacao na rede!", state="error")
                    st.error(briefing)
                    sistema_feedback.processar_e_salvar_feedback(tarefa_input, False, rodada_mediador, logs_erro=briefing)
                    loop_mediador = False
                    break
                
                is_smart, lacunas = validador_smart.avaliar_briefing_smart(briefing)
                
                if is_smart:
                    st.write(briefing)
                    s1.update(label="✅ IA01 [Mediador] entregou um Briefing SMART Aprovado!", state="complete")
                    loop_mediador = False
                else:
                    st.warning(f"⚠️ Briefing Reprovado pelo Validador .py (Rodada {rodada_mediador}). Lacunas: {', '.join(lacunas)}")
                    s1.update(label="⚠️ Briefing incompleto. Solicitando refatoracao...", state="error")
                    
            rodada_mediador += 1

        # EXECUÇÃO TÉCNICA E SALVAMENTO DE APRENDIZADO CONTÍNUO
        if briefing and not briefing.startswith("RAIZ_ERRO:"):
            time.sleep(3)
            with st.status("🛠️ IA02 [Executor Sênior] gerando plano tecnico...", expanded=True) as s2:
                p_sistema_2 = "Voce e o IA02 Executor Senior. Siga o briefing validado e estruture o plano de acao tecnico final em Markdown."
                codigo_v1 = orquestrar_chamada_rest(p_sistema_2, briefing)
                
                if codigo_v1.startswith("RAIZ_ERRO:"):
                    s2.update(label="💥 Falha no Executor!", state="error")
                    st.error(codigo_v1)
                    sistema_feedback.processar_e_salvar_feedback(tarefa_input, False, rodada_mediador, logs_erro=codigo_v1)
                else:
                    st.markdown(codigo_v1)
                    s2.update(label="🛠️ IA02 [Executor Sênior] concluiu a entrega final!", state="complete")
                    
                    # 📈 CONSOLIDAR APRENDIZADO
                    sistema_feedback.processar_e_salvar_feedback(tarefa_input, True, rodada_mediador)
                    st.success("🎉 Processo homologado sob validacao SMART e persistido no Aprendizado Continuo!")
    else:
        st.warning("Por favor, descreva o que deseja realizar.")

st.markdown("---")
with st.expander("⚙️ Ver Arquitetura"):
    st.caption("Synapse 24 OS Engine • ContextAnalyzer & Feedback System Ativos • Anti-429")
    
