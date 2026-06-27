import json
import streamlit as st

def executar_chamada_rest_v5(prompt_sistema, prompt_usuario):
    """
    Orquestrador Synapse 24 Enxuto.
    Focado estritamente em Groq e Gemini (Custo Zero e Sem Poluicao).
    """
    import requests
    logs_erros = []

    # -------------------------------------------------------------
    # NÍVEL 1: GROQ CLOUD (Modelo Llama 3.3 ultra rápido custo zero)
    # -------------------------------------------------------------
    key_groq = st.secrets.get("GROQ_API_KEY", "").strip()
    if key_groq.startswith("gsk_"):
        payload_groq = {
            "model": "llama-3.3-70b-specdec",
            "messages": [
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ]
        }
        headers_groq = {"Authorization": f"Bearer {key_groq}"}
        
        try:
            resposta = requests.post(
                "https://groq.com", 
                headers=headers_groq, 
                json=payload_groq, 
                timeout=10
            )
            if resposta.status_code == 200:
                return resposta.json()["choices"][0]["message"]["content"]
            else:
                logs_erros.append(f"💥 Groq Recusou (Status {resposta.status_code})")
        except Exception as e:
            logs_erros.append(f"💥 Groq Falha de Rede: {str(e)[:50]}")

    # -------------------------------------------------------------
    # NÍVEL 2: FALLBACK SUPREMO - GEMINI NATIVA (Google AI Studio)
    # -------------------------------------------------------------
    key_suja = st.secrets.get("GEMINI_API_KEY", "").strip()
    
    # Cura automática contra o texto grudado do painel do Streamlit
    if "com" in key_suja:
        key_gemini = key_suja.split("com")[-1].strip()
    elif "," in key_suja:
        key_gemini = key_suja.split(",")[0].strip()
    else:
        key_gemini = key_suja
        
    key_gemini = key_gemini.replace("'", "").replace('"', "").strip()

    if key_gemini:
        url_gemini = f"https://googleapis.com{key_gemini}"
        payload_gemini = {
            "contents": [{
                "parts": [{"text": f"System Prompt: {prompt_sistema}\n\nUser Request: {prompt_usuario}"}]
            }]
        }
        
        try:
            resposta = requests.post(url_gemini, json=payload_gemini, timeout=12)
            if resposta.status_code == 200:
                return resposta.json()["candidates"][0]["content"]["parts"][0]["text"]
            else:
                logs_erros.append(f"💥 Gemini Recusou (Status {resposta.status_code})")
        except Exception as e:
            logs_erros.append(f"💥 Gemini Falha de Rede: {str(e)[:50]}")

    # Se ambas as rotas gratuitas falharem
    return f"RAIZ_ERRO:{json.dumps(logs_erros)}"
    
