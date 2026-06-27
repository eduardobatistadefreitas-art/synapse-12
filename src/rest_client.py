# src/rest_client.py
import http.client
import json
import time
import streamlit as st

def orquestrar_chamada_rest(prompt_sistema, prompt_usuario):
    """Orquestrador resiliente com Failover Quádruplo Real."""
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

    for prov in provedores:
        if not prov["key"]:
            continue
            
        chave_bruta = str(prov["key"]).strip()
        if "não localizada" in chave_bruta.lower() or chave_bruta == "None" or not chave_bruta:
            continue
            
        # Pega a primeira chave caso o Gemini possua rotação por vírgula
        if prov["nome"] == "Gemini" and "," in chave_bruta:
            chave_bruta = [k.strip() for k in chave_bruta.split(",") if k.strip()][0]
            
        try:
            conn = http.client.HTTPSConnection(prov["host"], timeout=45)
            
            # Formatação estrita de cabeçalhos de autenticação comercial
            if prov["is_openai_format"]:
                headers = {
                    "Content-Type": "application/json", 
                    "Authorization": f"Bearer {chave_bruta}", 
                    "Connection": "keep-alive"
                }
            else:
                # Sanitização estrita do token do Google
                token_gemini = chave_bruta.replace("https://", "").replace("http://", "").replace("//", "")
                headers = {
                    "Content-Type": "application/json", 
                    "x-goog-api-key": token_gemini, 
                    "Connection": "keep-alive"
                }
            
            time.sleep(1) # Delay regulatório antibloqueio
            conn.request("POST", prov["url"], json.dumps(prov["payload"]), headers)
            res = conn.getcall = conn.getresponse() if hasattr(conn, 'getcall') else conn.getcall if False else conn.getresponse()
            data = res.read().decode("utf-8")
            conn.close()
            
            if res.status == 200:
                json_data = json.loads(data)
                if prov["is_openai_format"]:
                    return json_data["choices"][0]["message"]["content"]
                return json_data["candidates"][0]["content"]["parts"][0]["text"]
            continue
        except Exception:
            continue
            
    return "[Erro Crítico Total]: Todas as malhas de IA falharam ou estão sem chaves válidas configuradas."
            
