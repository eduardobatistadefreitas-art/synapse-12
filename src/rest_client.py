# src/rest_client.py
import http.client
import json
import time
import traceback
import streamlit as st

def orquestrar_chamada_rest(prompt_sistema, prompt_usuario):
    """Orquestrador com Failover Real e captura detalhada de tracebacks para diagnóstico."""
    provedores = [
        {
            "nome": "NVIDIA",
            "key": st.secrets.get("NVIDIA_API_KEY"),
            "host": "://nvidia.com",
            "url": "/v1/chat/completions",
            "payload": {"model": "meta/llama-3.3-70b-instruct", "messages": [{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt_usuario}], "temperature": 0.3, "max_tokens": 1024},
            "is_openai_format": True
        },
        {
            "nome": "OpenRouter",
            "key": st.secrets.get("OPENROUTER_API_KEY"),
            "host": "openrouter.ai",
            "url": "/api/v1/chat/completions",
            "payload": {"model": "meta-llama/llama-3.3-70b-instruct:free", "messages": [{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt_usuario}], "temperature": 0.3},
            "is_openai_format": True
        },
        {
            "nome": "Groq",
            "key": st.secrets.get("GROQ_API_KEY"),
            "host": "://groq.com",
            "url": "/openai/v1/chat/completions",
            "payload": {"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt_usuario}], "temperature": 0.3},
            "is_openai_format": True
        },
        {
            "nome": "Gemini",
            "key": st.secrets.get("GEMINI_API_KEY"),
            "host": "://googleapis.com",
            "url": "/v1/models/gemini-2.0-flash:generateContent",
            "payload": {"contents": [{"parts": [{"text": f"INSTRUÇÃO: {prompt_sistema}\n\nENTRADA: {prompt_usuario}"}]}], "generationConfig": {"temperature": 0.3}},
            "is_openai_format": False
        }
    ]

    historico_erros = []

    for prov in provedores:
        chave_bruta = str(prov["key"]).strip() if prov["key"] else ""
        if not chave_bruta or "não localizada" in chave_bruta.lower() or chave_bruta == "None":
            historico_erros.append(f"❌ {prov['nome']}: Chave não configurada ou vazia nos Secrets.")
            continue
            
        if prov["nome"] == "Gemini" and "," in chave_bruta:
            chave_bruta = [k.strip() for k in chave_bruta.split(",") if k.strip()][0]
            
        try:
            conn = http.client.HTTPSConnection(prov["host"], timeout=20)
            
            if prov["is_openai_format"]:
                headers = {
                    "Content-Type": "application/json", 
                    "Authorization": f"Bearer {chave_bruta}", 
                    "Connection": "keep-alive"
                }
            else:
                token_gemini = chave_bruta.replace("https://", "").replace("http://", "").replace("//", "")
                headers = {
                    "Content-Type": "application/json", 
                    "x-goog-api-key": token_gemini, 
                    "Connection": "keep-alive"
                }
            
            time.sleep(0.5)
            conn.request("POST", prov["url"], json.dumps(prov["payload"]), headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            conn.close()
            
            if res.status == 200:
                json_data = json.loads(data)
                if prov["is_openai_format"]:
                    return json_data["choices"]["message"]["content"]
                return json_data["candidates"]["content"]["parts"]["text"]
            
            historico_erros.append(f"⚠️ {prov['nome']} (Status {res.status}): {data[:120]}")
            
        except Exception as e:
            tb = traceback.format_exc()
            historico_erros.append(f"💥 {prov['nome']} Falha Interna: {str(e)}\n{tb[:150]}")
            continue
            
    # Retorna o relatório completo estruturado em JSON para o app decodificar na tela
    return "RAIZ_ERRO:" + json.dumps(historico_erros)
    
