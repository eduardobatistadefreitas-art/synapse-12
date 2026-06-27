import json
import streamlit as st

def executar_chamada_rest_v4(prompt_sistema, prompt_usuario):
    """
    Orquestrador Supremo Synapse 24 via Requests.
    Nome alterado para forçar a quebra de cache estático do Streamlit Cloud.
    """
    import requests

    # Captura a chave crua configurada nos Secrets
    key_raw = st.secrets.get("GEMINI_API_KEY", "").strip()
    
    if "," in key_raw:
        key_gemini = key_raw.split(",")[0].strip()
    else:
        key_gemini = key_raw

    # URL 100% isolada e imune a concatenações
    url_gemini = f"https://googleapis.com{key_gemini}"
    
    payload_gemini = {
        "contents": [{
            "parts": [{
                "text": f"System Prompt: {prompt_sistema}\n\nUser Request: {prompt_usuario}"
            }]
        }]
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        resposta = requests.post(url_gemini, headers=headers, json=payload_gemini, timeout=15)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            return dados["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"RAIZ_ERRO: Google API recusou (Status {resposta.status_code}) - {resposta.text[:120]}"
            
    except Exception as e:
        return f"RAIZ_ERRO: Erro de conexao com a API do Google: {str(e)}"
        
