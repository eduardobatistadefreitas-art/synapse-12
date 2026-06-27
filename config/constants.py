import streamlit as st

# Configurações de Fluxo e Segurança contra estouro de cotas
MAX_RODADAS = 2
DELAY_REQUISICAO = 2  # Segundos (Anti-429)

# Recuperação limpa de Segredos Oficiais
def obter_chave_groq():
    return st.secrets.get("GROQ_API_KEY", "").strip()

def obter_chave_gemini():
    return st.secrets.get("GEMINI_API_KEY", "").strip()
  
