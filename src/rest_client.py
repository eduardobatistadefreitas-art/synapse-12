import json
import streamlit as st

def orquestrar_chamada_rest(prompt_sistema, prompt_usuario):
    """
    Orquestrador Supremo Synapse 24 via Requests.
    URL travada e blindada contra falhas de formatacao.
    """
    import requests

    # 1. Captura e isola estritamente a primeira chave da lista
    key_raw = st.secrets.get("GEMINI_API_KEY", "").strip()
    
    if "," in key_raw:
        # Pega a primeira chave antes da virgula e limpa espaços
        key_gemini = key_raw.split(",")[0].strip()
    else:
        key_gemini = key_raw

    # 2. URL Fixa e Absoluta de Produçao (Sem concatenaçao dinâmica de hosts)
    url_gemini = f"https://googleapis.com{key_gemini}"
    
    # 3. Payload oficial exigido pela API do Google AI Studio
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
        # Dispara com o motor robusto do requests
        resposta = requests.post(url_gemini, headers=headers, json=payload_gemini, timeout=15)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            # Navega com segurança na árvore estruturada do Google
            return dados["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"RAIZ_ERRO: Google API recusou (Status {resposta.status_code}) - {resposta.text[:120]}"
            
    except Exception as e:
        return f"RAIZ_ERRO: Erro de conexao com a API do Google: {str(e)}"
        
