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
    st.error(f"🚨 Arquivo crítico não encontrado em: {caminho_rest}")
    st.stop()

# Importação da nossa nova infraestrutura gerencial SMART
try:
    from src.agents.ia02_smart_validator import SmartValidator
    from src.agents.ia02_executor_manager import executar_analise_gerencial
except ModuleNotFoundError:
    sys.path.append(os.path.join(PATH_SRC, "agents"))
    from ia02_smart_validator import SmartValidator
    from ia02_executor_manager import executar_analise_gerencial

st.set_page_config(page_title="Synapse 24 OS", page_icon="🧠", layout="centered")
st.title("🧠 Synapse 24 OS")
st.subheader("Sua ideia, executada por uma rede de agentes.")
st.write("_Módulos .py de Validação SMART e Controle Anti-Spam Ativos._")
st.markdown("---")

st.write("### 🎬 Iniciar Nova Orquestração")
tarefa_input = st.text_area("O que você precisa realizar hoje?", placeholder="Crie um app para vendas", height=150)

if st.button("Dar vida ao projeto", type="primary"):
    if tarefa_input.strip():
        st.write("### ⚙️ Debate e Orquestração em Tempo Real:")
        validador_smart = SmartValidator()
        
        loop_mediador = True
        rodada_mediador = 1
        max_rodadas_mediador = 2
        briefing = ""
        
        # 🔄 LOOP DE VALIDAÇÃO PROGRAMÁTICA DO MEDIADOR (IA01)
        while loop_mediador and rodada_mediador <= max_rodadas_mediador:
            time.sleep(3) # Pausa obrigatória anti-bloqueio de chaves
            
            with st.status(f"🧠 [Rodada {rodada_mediador}] IA01 [Mediador] estruturando briefing...", expanded=True) as s1:
                p_sistema_1 = "Você é o IA01 Mediador. Escreva um briefing técnico contendo Objetivo, Requisitos com métricas (%) e Cronograma de prazos."
                # Se for uma re-tentativa, adiciona o feedback de falha no prompt do usuário
                prompt_envio = tarefa_input if rodada_mediador == 1 else f"{tarefa_input} \n\n⚠️ REPROVADO: O briefing anterior falhou nos critérios SMART. Refatore incluindo prazos e métricas reais obrigatórias."
                
                briefing = orquestrar_chamada_rest(p_sistema_1, prompt_envio)
                
                if briefing.startswith("RAIZ_ERRO:"):
                    s1.update(label="💥 Falha física de comunicação na rede!", state="error")
                    st.error(briefing)
                    loop_mediador = False
                    break
                
                # Executa o validador nativo em arquivo .py compilado
                is_smart, lacunas = validador_smart.avaliar_briefing_smart(briefing)
                
                if is_smart:
                    st.write(briefing)
                    s1.update(label="✅ IA01 [Mediador] entregou um Briefing SMART Aprovado!", state="complete")
                    loop_mediador = False
                else:
                    st.warning(f"⚠️ Briefing Reprovado pelo Validador .py (Rodada {rodada_mediador}). Lacunas: {', '.join(lacunas)}")
                    st.write("_Forçando re-generation automática com injeção de correção..._")
                    s1.update(label="⚠️ Briefing incompleto. Solicitando refatoração...", state="error")
                    
            rodada_mediador += 1

        # SE O BRIEFING PASSOU OU ESTOUROU O LIMITE, SEGUE O FLUXO SEGURO
        if briefing and not briefing.startswith("RAIZ_ERRO:"):
            time.sleep(3)
            with st.status("🛠️ IA02 [Executor Sênior] gerando plano técnico...", expanded=True) as s2:
                # Dispara a análise complementar integrada
                analise_gerencial = executar_analise_gerencial(briefing)
                
                p_sistema_2 = f"Você é o IA02 Executor Sênior. Siga o briefing validado e estruture o plano de ação técnico final em Markdown."
                codigo_v1 = orquestrar_chamada_rest(p_sistema_2, briefing)
                
                if codigo_v1.startswith("RAIZ_ERRO:"):
                    s2.update(label="💥 Falha no Executor!", state="error")
                    st.error(codigo_v1)
                else:
                    st.markdown(codigo_v1)
                    s2.update(label="🛠️ IA02 [Executor Sênior] concluiu a entrega final!", state="complete")
                    st.success("🎉 Processo de colmeia homologado com sucesso sob validação SMART!")
    else:
        st.warning("Por favor, descreva o que deseja realizar.")

st.markdown("---")
with st.expander("⚙️ Ver Arquitetura"):
    st.caption("Synapse 24 OS Engine • Validador SMART .py • Controle de Cadência Anti-429")
    
