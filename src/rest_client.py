import json
import streamlit as st

def orquestrar_chamada_rest(prompt_sistema, prompt_usuario):
    """
    Orquestrador Supremo Synapse 24 via Requests.
    Tratamento estrito da URL do Gemini contra erros de Secrets.
    """
    import requests

    # 1. Captura e higieniza a chave do Gemini
    key_raw = st.secrets.get("GEMINI_API_KEY", "").strip()
    
    # Se houver múltiplas chaves ou strings complexas, limpa de forma robusta
    if "," in key_raw:
        key_gemini = key_raw.split(",")[0].strip()
    else:
        key_gemini = key_raw

    # Remove resíduos caso a chave contenha pedaços de URL por erro de digitação
    key_gemini = key_gemini.replace("https://", "").replace("://googleapis.com", "")
    key_gemini = key_gemini.replace("v1beta", "").replace("?key=", "").strip("/")

    # 2. URL Fixa e Intocável de Produção do Google
    url_gemini = f"https://://googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key_gemini}"
    
    # 3. Payload oficial exigido pela API do Google
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
        # Dispara com motor robusto isolado
        resposta = requests.post(url_gemini, headers=headers, json=payload_gemini, timeout=15)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            # Navega na estrutura correta do dicionário JSON da Google
            return dados["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"RAIZ_ERRO: Google API recusou (Status {resposta.status_code}) - {resposta.text[:120]}"
            
    except Exception as e:
        return f"RAIZ_ERRO: Erro de conexao com a API do Google: {str(e)}"
        
