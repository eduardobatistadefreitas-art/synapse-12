import streamlit as st
import sys
import os

# INJEÇÃO DINÂMICA DE CAMINHOS CORPORATIVOS NO PYTHON PATH
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

# Importação limpa pós-bootstrap
try:
    from visual_engine import renderizar_ui_principal
except ModuleNotFoundError:
    from src.ui.visual_engine import renderizar_ui_principal

st.set_page_config(page_title="Synapse 24 OS", page_icon="🧠", layout="centered")
st.title("🧠 Synapse 24 OS")

if __name__ == "__main__":
    renderizar_ui_principal()
    
