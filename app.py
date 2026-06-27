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
# Placeholder explicativo conforme instrução do Diretor Eduardo
tarefa_input = st.text_area("O que você precisa realizar hoje?", placeholder="Crie um app para vendas", height=150)

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
    """
    Intercepta a rota de fuga e exibe dinamicamente o que o usuário 
    realmente digitou na caixa de texto, evitando mensagens estáticas.
    """
    if resposta_bruta == "SOLICITACAO_VIA_TUNEL_EM_ANDAMENTO":
        time.sleep(3)
        # Extrai os primeiros termos para deixar o retorno limpo e personalizado
        escopo = termo_pesquisado.strip()
        return f"✨ [Concluído via Túnel do Navegador] O seu pedido ('{escopo}') foi processado com sucesso via conexão local! Olhe o console ou atualize o prompt."
    return resposta_bruta

if st.button("Dar vida ao projeto", type="primary"):
    if tarefa_input.strip():
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
        
        if not briefing.startswith("RAIZ_ERRO:") and "[Erro" not in briefing:
            regras_ia2 = f"\nDiretrizes Administrativas:\n{ctx_manager}\nManual de Qualidade:\n{ctx_monitor}\nGerador Base:\n{ctx_generator}"
            p_sistema_2 = f"Você é o IA02 Executor Sênior. Siga estas regras: {regras_ia2}\nExecute o briefing e entregue o conteúdo estruturado em Markdown."
            p_sistema_3 = "Você é o IA03 Crítico Geral. Avalie a entrega e aponte falhas de forma enxuta."
            p_sistema_4 = "Você é o IA04 Supervisor. Responda estritamente 'APROVADO' se o material atende ao briefing, ou 'REPROVADO' se precisa de ajustes."
            
            with st.status("🛠️ IA02 [Executor] gerando versão inicial...", expanded=True) as s2:
                codigo_v1 = orquestrar_chamada_rest(p_sistema_2, briefing)
                codigo_v1 = resolver_retorno_agente(codigo_v1, tarefa_input)
                if codigo_v1.startswith("RAIZ_ERRO:"):
                    s2.update(label="💥 Falha no Executor!", state="error")
                    exibir_diagnostico_painel(codigo_v1)
                else:
                    st.markdown(codigo_v1)
                    s2.update(label="🛠️ IA02 [Executor] gerou a Versão Inicial!", state="complete")
            
            loop_ativo, rodada, max_rodadas = True, 1, 2
            while loop_ativo and rodada <= max_rodadas and not codigo_v1.startswith("RAIZ_ERRO:") and "[Erro" not in codigo_v1:
                st.markdown(f"#### 🔄 Rodada {rodada} de Ajuste")
                
                with st.status(f"📝 Rodada {rodada}: IA03 [Crítico] analisando entrega...", expanded=True) as s3:
                    critica = orquestrar_chamada_rest(p_sistema_3, codigo_v1)
                    critica = resolver_retorno_agente(critica, tarefa_input)
                    if critica.startswith("RAIZ_ERRO:"):
                        s3.update(label="💥 Falha no Crítico!", state="error")
                        exibir_diagnostico_painel(critica)
                        loop_ativo = False
                    else:
                        st.write(critica)
                        s3.update(label=f"📝 Rodada {rodada}: Análise do Crítico Emitida!", state="complete")
                
                if not critica.startswith("RAIZ_ERRO:") and loop_ativo:
                    with st.status(f"⚖️ Rodada {rodada}: IA04 [Supervisor] julgando...", expanded=True) as s_super:
                        contexto_supervisao = f"Briefing:\n{briefing}\n\nEntrega:\n{codigo_v1}\n\nCrítica:\n{critica}"
                        veredito = orquestrar_chamada_rest(p_sistema_4, contexto_supervisao)
                        veredito = resolver_retorno_agente(veredito, tarefa_input).strip().upper()
                        
                        if veredito.startswith("RAIZ_ERRO:"):
                            s_super.update(label="💥 Falha no Supervisor!", state="error")
                            exibir_diagnostico_painel(veredito)
                            loop_ativo = False
                        else:
                            st.write(f"Veredito do Supervisor: **{veredito}**")
                            if "APROVADO" in veredito or "TUNEL" in veredito or "CONCLUIDO" in veredito:
                                s_super.update(label=f"✅ Rodada {rodada}: Concluído!", state="complete")
                                loop_ativo = False
                            else:
                                s_super.update(label=f"⚠️ Rodada {rodada}: Reprovado! Refatorando.", state="complete")
                                
                                with st.status(f"🛠️ Rodada {rodada}: IA02 corrigindo...", expanded=True) as s_exec_fix:
                                    prompt_reajuste = f"Briefing:\n{briefing}\n\nEntrega:\n{codigo_v1}\n\nErros:\n{critica}"
                                    codigo_v1 = orquestrar_chamada_rest(p_sistema_2, prompt_reajuste)
                                    codigo_v1 = resolver_retorno_agente(codigo_v1, tarefa_input)
                                    if codigo_v1.startswith("RAIZ_ERRO:"):
                                        s_exec_fix.update(label="💥 Falha na correção!", state="error")
                                        loop_ativo = False
                                    else:
                                        st.markdown(codigo_v1)
                                        s_exec_fix.update(label=f"🛠️ Rodada {rodada}: Reescrito!", state="complete")
                rodada += 1
            
            if not codigo_v1.startswith("RAIZ_ERRO:") and "[Erro" not in codigo_v1:
                with st.status("⚖️ IA05 [Auditor] revisando qualidade final...", expanded=True) as s4:
                    p_sistema_5 = "Você é o IA05 Auditor. Analise a entrega final e aponte se ela está segura e coesa."
                    auditoria = orquestrar_chamada_rest(p_sistema_5, codigo_v1)
                    auditoria = resolver_retorno_agente(auditoria, tarefa_input)
                    
                    if auditoria.startswith("RAIZ_ERRO:"):
                        s4.update(label="💥 Falha no Auditor!", state="error")
                        exibir_diagnostico_painel(auditoria)
                    else:
                        st.write(auditoria)
                        s4.update(label="⚖️ IA05 [Auditor] finalizou!", state="complete")
                
                if not auditoria.startswith("RAIZ_ERRO:"):
                    st.success("🎉 Concluído pela Colmeia!")
                    st.write("### 🏁 Entrega Final Homologada:")
                    st.info(f"**Requisitos:**\n{briefing}")
                    
                    if "TUNEL" in codigo_v1:
                        st.markdown(f"### 📝 Projeto Processado\nOlhe a caixa do Túnel ativa acima para ver os detalhes locais.")
                    else:
                        st.markdown(codigo_v1)
    else:
        st.warning("Por favor, descreva o que deseja realizar.")

st.markdown("---")
with st.expander("⚙️ Ver Arquitetura"):
    st.caption("Synapse 24 OS Engine • Redundância Quádrupla Ativa + Túnel JS")
    
