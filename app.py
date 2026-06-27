import streamlit as st
import sys
import os
import traceback

# Configuração de Página e Inicialização de Estado Básica
st.set_page_config(page_title="Synapse 24 OS", page_icon="🧠", layout="centered")

# Injeção Dinâmica de Caminhos Corporativos no Python Path
RAIZ_DIR = os.path.dirname(os.path.abspath(__file__))
PASTAS_SISTEMA = [
    os.path.join(RAIZ_DIR, "config"),
    os.path.join(RAIZ_DIR, "src"),
    os.path.join(RAIZ_DIR, "src", "ui"),
    os.path.join(RAIZ_DIR, "src", "core"),
    os.path.join(RAIZ_DIR, "src", "agents"),
    os.path.join(RAIZ_DIR, "src", "utils")
]

for pasta in PASTAS_SISTEMA:
    if pasta not in sys.path:
        sys.path.append(pasta)

st.title("🧠 Synapse 24 OS")

# 🔍 MECANISMO ANTIPÂNICO: Captura qualquer erro de sintaxe ou importação modular
try:
    # Tenta carregar e executar a interface gráfica do projeto
    try:
        from visual_engine import renderizar_ui_principal
    except ModuleNotFoundError:
        from src.ui.visual_engine import renderizar_ui_principal

    # Executa a UI se tudo estiver íntegro
    renderizar_ui_principal()

except Exception as erro_físico:
    # 📋 CAIXA COPIÁVEL DE DIAGNÓSTICO DO DIRETOR EDUARDO
    # Se a máquina quebrar, este bloco é acionado imediatamente em tela limpa
    st.error("🚨 [Falha Crítica de Compilação] O ecossistema travou antes de iniciar!")
    st.write("Copie o relatório abaixo e envie para análise imediata:")
    
    # Monta a árvore de logs detalhada do Python
    log_completo = f"""==================================================
🚨 RELATÓRIO DE DIAGNÓSTICO TÉCNICO DA MALHA (COPIÁVEL)
==================================================
Erro Real: {str(erro_físico)}
--------------------------------------------------
Traceback Detalhado:
{traceback.format_exc()}
=================================================="""
    
    # Renderiza o componente de texto puro copiável em um clique no celular
    st.code(log_completo, language="text")
    
