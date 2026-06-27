import http.client
import json
import urllib.parse
import streamlit as st

def requisitar_api(url_completa, headers, payload, timeout=15):
    """
    Executa a requisição HTTP tratando strings de URL de forma robusta.
    Adiciona o header Host para corrigir falhas de DNS no Streamlit Cloud.
    """
    try:
        if not url_completa.startswith(('http://', 'https://')):
            url_completa = 'https://' + url_completa
            
        parsed_url = urllib.parse.urlparse(url_completa)
        host = parsed_url.netloc
        path = parsed_url.path if parsed_url.path else "/"
        if parsed_url.query:
            path += "?" + parsed_url.query

        if ":" in host:
            hostname, port = host.split(":", 1)
            if not port.isdigit():
                host = hostname

        # Injeta o Host explicitamente nos headers para resolver o DNS
        headers["Host"] = host

        conexao = http.client.HTTPSConnection(host, timeout=timeout)
        conexao.request("POST", path, body=json.dumps(payload), headers=headers)
        
        resposta = conexao.getresponse()
        status_code = resposta.status
        corpo = resposta.read().decode('utf-8')
        conexao.close()
        
        return status_code, corpo

    except Exception as e:
        return 500, json.dumps({"error": {"message": str(e), "code": 500}})

def orquestrar_chamada_rest(prompt_sistema, prompt_usuario):
    """
    Orquestrador com Malha de Redundância Quádrupla Automática.
    Corrigido contra falhas de DNS corporativo.
    """
    logs_erros = []

    # 1. NVIDIA Build
    payload_nv = {
        "model": "nvidia/llama-3.3-nemotron-super-49b-v1.5",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ],
        "temperature": 0.2,
        "max_tokens": 1024
    }
    key_nv = st.secrets.get("NVIDIA_API_KEY", "")
    headers_nv = {
        "Authorization": f"Bearer {key_nv}",
        "Content-Type": "application/json"
    }
    status, res = requisitar_api("://nvidia.com", headers_nv, payload_nv)
    if status == 200:
        try:
            return json.loads(res)["choices"]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"💥 NVIDIA Parse Erro: {str(e)}")
    else:
        logs_erros.append(f"💥 NVIDIA Erro (Status {status}): {res[:120]}")

    # 2. OpenRouter
    payload_or = {
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]
    }
    key_or = st.secrets.get("OPENROUTER_API_KEY", "")
    headers_or = {
        "Authorization": f"Bearer {key_or}",
        "Content-Type": "application/json"
    }
    status, res = requisitar_api("openrouter.ai/api/v1/chat/completions", headers_or, payload_or)
    if status == 200:
        try:
            return json.loads(res)["choices"]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"⚠️ OpenRouter Parse Erro: {str(e)}")
    else:
        logs_erros.append(f"⚠️ OpenRouter Erro (Status {status}): {res[:120]}")

    # 3. Groq Cloud
    payload_groq = {
        "model": "llama-3.3-70b-specdec",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]
    }
    key_groq = st.secrets.get("GROQ_API_KEY", "")
    headers_groq = {
        "Authorization": f"Bearer {key_groq}",
        "Content-Type": "application/json"
    }
    status, res = requisitar_api("api.groq.com/openai/v1/chat/completions", headers_groq, payload_groq)
    if status == 200:
        try:
            return json.loads(res)["choices"]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"💥 Groq Parse Erro: {str(e)}")
    else:
        logs_erros.append(f"💥 Groq Erro (Status {status}): {res[:120]}")

    # 4. Gemini (OpenAI Compatibility Gateway)
    payload_gemini = {
        "model": "gemini-2.5-flash",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]
    }
    key_gemini = st.secrets.get("GEMINI_API_KEY", "")
    headers_gemini = {
        "Authorization": f"Bearer {key_gemini}",
        "Content-Type": "application/json"
    }
    status, res = requisitar_api("://googleapis.com", headers_gemini, payload_gemini)
    if status == 200:
        try:
            return json.loads(res)["choices"]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"💥 Gemini Parse Erro: {str(e)}")
    else:
        logs_erros.append(f"💥 Gemini Erro (Status {status}): {res[:120]}")

    return f"RAIZ_ERRO:{json.dumps(logs_erros)}"
    
