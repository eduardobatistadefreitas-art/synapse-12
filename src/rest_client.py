import json
import streamlit as st

def executar_chamada_rest_v4(prompt_sistema, prompt_usuario):
    """
    Orquestrador Supremo Synapse 24 via Requests.
    Cura cirurgicamente chaves corrompidas no st.secrets.
    """
    import requests

    # 1. Resgata o segredo (que sabemos que está misturado com a URL no painel)
    key_suja = st.secrets.get("GEMINI_API_KEY", "").strip()
    
    # 2. ENGENHARIA DE CURA: Isola estritamente a chave real
    # Se a chave contiver a palavra 'com', quebra ali e pega o que vem depois
    if "com" in key_suja:
        key_gemini = key_suja.split("com")[-1].strip()
    elif "," in key_suja:
        key_gemini = key_suja.split(",")[0].strip()
    else:
        key_gemini = key_suja

    # Remove qualquer resíduo restante de caracteres inválidos ou pontuação
    key_gemini = key_gemini.replace("'", "").replace('"', "").strip()

    # 3. URL Absoluta, Limpa e Intocável do Google AI Studio
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
        # Dispara usando o requests puro com a chave curada
        resposta = requests.post(url_gemini, headers=headers, json=payload_gemini, timeout=15)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            return dados["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"RAIZ_ERRO: Google API recusou (Status {resposta.status_code}) - Chave Usada: {key_gemini[:8]}... - Erro: {resposta.text[:100]}"
            
    except Exception as e:
        return f"RAIZ_ERRO: Erro de conexao com a API do Google: {str(e)} | Chave Tentada: {key_gemini[:15]}"
        
