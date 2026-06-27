# src/rest_client.py
import http.client
import json
import time
import traceback
import streamlit as st

def orquestrar_chamada_rest(prompt_sistema, prompt_usuario):
    """Orquestrador resiliente definitivo com correção de variáveis."""
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
        if not prov["key"]:
            historico_erros.append(f"❌ {prov['nome']}: Chave ausente nos Secrets.")
            continue
            
        token_limpo = str(prov["key"]).strip()
        if "não localizada" in token_limpo.lower() or token_limpo == "None" or not token_limpo:
            historico_erros.append(f"❌ {prov['nome']}: Chave inválida ou vazia.")
            continue
            
        # Tratamento seguro caso a string do Gemini possua rotação por vírgula
        if prov["nome"] == "Gemini" and "," in token_limpo:
            token_limpo = [k.strip() for k in token_limpo.split(",") if k.strip()][0]
            
        try:
            conn = http.client.HTTPSConnection(prov["host"], timeout=30)
            
            if prov["is_openai_format"]:
                headers = {
                    "Content-Type": "application/json", 
                    "Authorization": f"Bearer {token_limpo}", 
                    "Connection": "keep-alive"
                }
            else:
                # 🚀 CORREÇÃO CRÍTICA: Variável corrigida para token_limpo eliminando o NameError
                token_gemini_puro = token_limpo.replace("https://", "").replace("http://", "").replace("//", "")
                headers = {
                    "Content-Type": "application/json", 
                    "x-goog-api-key": token_gemini_puro, 
                    "Connection": "keep-alive"
                }
            
            time.sleep(0.5)
            conn.request("POST", prov["url"], json.dumps(prov["payload"]), headers)
            res = conn.getcall = conn.getresponse() if hasattr(conn, 'getcall') else conn.getcall if False else conn.getresponse()
            data = res.read().decode("utf-8")
            conn.close()
            
            if res.status == 200:
                json_data = json.loads(data)
                if prov["is_openai_format"]:
                    return json_data["choices"]["message"]["content"]
                return json_data["candidates"]["content"]["parts"]["text"]
            
            historico_erros.append(f"⚠️ {prov['nome']} (Status {res.status}): {data[:80]}")
            
        except Exception as e:
            historico_erros.append(f"💥 {prov['nome']} Erro: {str(e)}")
            continue
            
    return "RAIZ_ERRO:" + json.dumps(historico_erros)
    
