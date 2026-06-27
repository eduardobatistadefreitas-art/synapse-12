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

# Importações Modulares de Inteligência e Otimização
try:
    from src.agents.ia02_smart_validator import SmartValidator
    from src.utils.context_analyzer import ContextAnalyzer
    from src.agents.ia05_auditor_feedback import AuditorFeedbackSystem
    from src.agents.ia01_mediador_optimizer import MediadorOptimizer
except ModuleNotFoundError:
    sys.path.append(os.path.join(PATH_SRC, "agents"))
    sys.path.append(os.path.join(PATH_SRC, "utils"))
    from ia02_smart_validator import SmartValidator
    from context_analyzer import ContextAnalyzer
    from ia05_auditor_feedback import AuditorFeedbackSystem
    from ia01_mediador_optimizer import MediadorOptimizer

st.set_page_config(page_title="Synapse 24 OS", page_icon="🧠", layout="centered")
st.title("🧠 Synapse 24 OS")
st.subheader("Sua ideia, executada por uma rede de agentes.")
st.write("_Motor de Ajuste Adaptativo Automático Ativo._")
st.markdown("---")

# 🛠️ PAINEL DE TESTES EXPOSTO E PROTEGIDO POR ESTADO (IMUNE A TRAVAMENTOS DE UI)
st.write("### 🛠️ Sandbox de Testes e Homologacao (Passo 3)")
st.write("Clique abaixo para simular o estouro do limite de 3 falhas SMART e forçar a auto-otimização:")

if st.button("🔥 Disparar Teste de Estresse Controlado", type="secondary"):
    try:
        auditor_teste = AuditorFeedbackSystem(pasta_destino=PATH_SRC)
        optimizer_teste = MediadorOptimizer(pasta_src=PATH_SRC)
        
        # Força o acúmulo consecutivo de 3 falhas direto no JSON oficial
        for i in range(1, 4):
            auditor_teste.processar_e_salvar_feedback(
                tarefa_solicitada="Simulacao Controle de Estresse",
                sucesso_bool=False,
                rodadas_consumidas=1,
                lacunas_lista=["Ausencia de metricas quantificaveis (%) e cronogramas em meses."]
            )
        
        # Salva o resultado no estado para garantir renderização contínua no celular
        st.session_state["resultado_diretriz"] = optimizer_teste.generar_diretriz_otimizada(threshold_erros=3) if hasattr(optimizer_teste, 'generar_diretriz_otimizada') else "FALHA_METODO_DIRETRIZ"
        st.session_state["resultado_json"] = auditor_teste.carregar_aprendizado_atual()
        st.session_state["teste_estresse_rodado"] = True
    except Exception as e:
        st.error(f"Erro ao processar sandbox em tela: {str(e)}")

# Exibe os resultados fixados fora do botão se o teste já tiver sido acionado
if st.session_state.get("teste_estresse_rodado"):
    st.success("🎉 Teste de Estresse Executado com Sucesso!")
    st.write("📋 **Nova Diretriz Injetada no Mediador (IA01):**")
    st.code(st.session_state["resultado_diretriz"], language="text")
    st.write("📊 **Estado Atual do Arquivo de Logs Persistidos (`config_adaptativa.json`):**")
    st.json(st.session_state["resultado_json"])
    st.markdown("---")

st.write("### 🎬 Iniciar Nova Orquestração")
tarefa_input = st.text_area("O que voce precisa realizar hoje?", placeholder="Crie um app para vendas", height=150)

if st.button("Dar vida ao projeto", type="primary"):
    if tarefa_input.strip():
        st.write("### ⚙️ Debate e Orquestracao em Tempo Real:")
        
        # Inicialização dos utilitários
        validador_smart = SmartValidator()
        analisador_contexto = ContextAnalyzer()
        sistema_feedback = AuditorFeedbackSystem(pasta_destino=PATH_SRC)
        otimizador_mediador = MediadorOptimizer(pasta_src=PATH_SRC)
        
        # 1. Análise de Contexto Pró-ativa
        tags_contexto = analisador_contexto.extrair_tags_intencao(tarefa_input)
        st.info(f"🔍 **Analise de Contexto de Nuvem**: Intent identificada -> `{tags_contexto}`")
        
        # GATILHO DO OPTIMIZER: Avalia os logs e reescreve se estourar o limite de 3 erros
        historico = sistema_feedback.carregar_aprendizado_atual()
        erros_contados = historico.get("erros_acumulados_requisito", 0)
        
        p_sistema_1 = otimizador_mediador.gerar_diretriz_otimizada(threshold_erros=3)
        
        if erros_contados >= 3:
            st.warning(f"🚨 **Auto-Otimização Acionada**: {erros_contados} falhas seguidas detectadas. Diretriz do Mediador reconfigurada à força.")

        loop_mediador = True
        rodada_mediador = 1
        max_rodadas_mediador = 2
        briefing = ""
        lacunas = []
        
        # 🔄 LOOP DE VALIDAÇÃO PROGRAMÁTICA
        while loop_mediador and rodada_mediador <= max_rodadas_mediador:
            time.sleep(3) # Anti-429
            
            with st.status(f"🧠 [Rodada {rodada_mediador}] IA01 [Mediador] estruturando briefing...", expanded=True) as s1:
                prompt_envio = tarefa_input if rodada_mediador == 1 else f"{tarefa_input} \n\n⚠️ REPROVADO: Falhou nos criterios SMART. Insira metricas (%) e cronogramas obrigatoriamente."
                
                briefing = orquestrar_chamada_rest(p_sistema_1, prompt_envio)
                
                if briefing.startswith("RAIZ_ERRO:"):
                    s1.update(label="💥 Falha de comunicacao na rede!", state="error")
                    st.error(briefing)
                    sistema_feedback.processar_e_salvar_feedback(tarefa_input, False, rodada_mediador, ["Falha de Rede"])
                    loop_mediador = False
                    break
                
                is_smart, lacunas = validador_smart.avaliar_briefing_smart(briefing)
                
                if is_smart:
                    st.write(briefing)
                    s1.update(label="✅ IA01 [Mediador] Briefing SMART Aprovado!", state="complete")
                    loop_mediador = False
                else:
                    st.warning(f"⚠️ Briefing Reprovado (Rodada {rodada_mediador}). Lacunas: {', '.join(lacunas)}")
                    s1.update(label="⚠️ Briefing incompleto. Refatorando...", state="error")
                    
            rodada_mediador += 1

        # EXECUÇÃO E GRAVAÇÃO DE FEEDBACK ADAPTATIVO
        if briefing and not briefing.startswith("RAIZ_ERRO:"):
            time.sleep(3)
            with st.status("🛠️ IA02 [Executor Sênior] gerando plano tecnico...", expanded=True) as s2:
                p_sistema_2 = "Voce e o IA02 Executor Senior. Siga o briefing validado e estruture o plano final em Markdown."
                codigo_v1 = orquestrar_chamada_rest(p_sistema_2, briefing)
                
                if codigo_v1.startswith("RAIZ_ERRO:"):
                    s2.update(label="💥 Falha no Executor!", state="error")
                    st.error(codigo_v1)
                    sistema_feedback.processar_e_salvar_feedback(tarefa_input, False, rodada_mediador, ["Falha no Executor"])
                else:
                    st.markdown(codigo_v1)
                    s2.update(label="🛠️ IA02 [Executor Sênior] concluido!", state="complete")
                    
                    # Salva o resultado e atualiza/reseta o contador de Threshold
                    sistema_feedback.processar_e_salvar_feedback(tarefa_input, is_smart, rodada_mediador, lacunas)
                    st.success("🎉 Processo homologado e registrado no Ciclo de Retroalimentação!")
    else:
        st.warning("Por favor, descreva o que deseja realizar.")

st.markdown("---")
with st.expander("⚙️ Ver Arquitetura"):
    st.caption("Synapse 24 OS Engine • MediadorOptimizer Ativo • Threshold: 3 • Anti-429")
                    
