import json
import streamlit as st

def orquestrar_chamada_rest(prompt_sistema, prompt_usuario):
    """
    Orquestrador Supremo Synapse 24 via Requests.
    Expoe o erro real para o Diretor Eduardo eliminar o bug de rede.
    """
    import requests

    key_gemini = st.secrets.get("GEMINI_API_KEY", "").strip()
    if "," in key_gemini:
        key_gemini = key_gemini.split(",")[0].strip()

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
        resposta = requests.post(url_gemini, headers=headers, json=payload_gemini, timeout=12)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            return dados["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"RAIZ_ERRO: Google API retornou status {resposta.status_code} - {resposta.text[:150]}"
            
    except Exception as e:
        # EXPÕE O ERRO REAL EM VEZ DO TEXTO DE MOCK
        import traceback
        erro_detalhado = traceback.format_exc()
        return f"RAIZ_ERRO: Falha fisica no requests: {str(e)} | Trace: {erro_detalhado[:150]}"
        
