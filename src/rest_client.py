import streamlit as st
import json
import time

def executar_chamada_rest_v5(prompt_sistema, prompt_usuario):
    """
    Orquestrador Synapse 24 via SDKs Oficiais.
    Leitura pura de tokens e espaçamento de requisições anti-429.
    """
    # Pequena pausa pró-ativa para evitar o estouro de RPM (429) visto no gráfico do Diretor
    time.sleep(2)
    logs_erros = []

    # -------------------------------------------------------------
    # NÍVEL 1: GROQ VIA CLIENTE OFICIAL
    # -------------------------------------------------------------
    try:
        from groq import Groq
        
        key_groq = st.secrets.get("GROQ_API_KEY", "").strip()
        if key_groq:
            client_groq = Groq(api_key=key_groq)
            
            resposta = client_groq.chat.completions.create(
                model="llama-3.3-70b-specdec",
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": prompt_usuario}
                ],
                timeout=12
            )
            return resposta.choices[0].message.content
    except Exception as e:
        logs_erros.append(f"💥 Groq SDK Falhou: {str(e)[:60]}")

    # -------------------------------------------------------------
    # NÍVEL 2: FALLBACK GEMINI VIA CLIENTE OFICIAL GOOGLE
    # -------------------------------------------------------------
    try:
        from google import genai
        from google.genai import types
        
        # Leitura 100% pura e sem filtros para nao quebrar a nova chave AQ.Ab8RN6Im...
        key_gemini = st.secrets.get("GEMINI_API_KEY", "").strip()

        if key_gemini:
            client_gemini = genai.Client(api_key=key_gemini)
            
            resposta = client_gemini.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_usuario,
                config=types.GenerateContentConfig(
                    system_instruction=prompt_sistema,
                    temperature=0.2
                )
            )
            return resposta.text
    except Exception as e:
        logs_erros.append(f"💥 Gemini SDK Falhou: {str(e)[:60]}")

    return f"RAIZ_ERRO:{json.dumps(logs_erros)}"
    
