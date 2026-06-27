import urllib.request
import urllib.parse
import json
import streamlit as st

def requisitar_api_final(url_completa, headers, payload, timeout=15):
    """
    Mecanismo definitivo de tráfego. Simula requisição legítima de navegador,
    forçando o cálculo de Content-Length e desarmando o bloqueio Cloudflare.
    """
    try:
        dados_bytes = json.dumps(payload).encode('utf-8')
        
        # Cabeçalhos cruciais contra desafios de segurança Cloudflare / WAF
        headers["Content-Type"] = "application/json"
        headers["Content-Length"] = str(len(dados_bytes))
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        headers["Accept"] = "application/json"
        
        req = urllib.request.Request(url_completa, data=dados_bytes, headers=headers, method="POST")
        
        with urllib.request.urlopen(req, timeout=timeout) as resposta:
            return resposta.status, resposta.read().decode('utf-8')

    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 500, json.dumps({"error": {"message": str(e), "code": 500}})

def orquestrar_chamada_rest(prompt_sistema, prompt_usuario):
    """
    Orquestrador Supremo da Malha Quádrupla Synapse 24.
    Rotas calibradas individualmente por provedor com proteção de JSON Parsing.
    """
    logs_erros = []

    # 1. NVIDIA Build (Protegido por Content-Length explícito)
    key_nv = st.secrets.get("NVIDIA_API_KEY", "").strip()
    payload_nv = {
        "model": "nvidia/llama-3.3-nemotron-super-49b-v1.5",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ],
        "temperature": 0.2,
        "max_tokens": 1024
    }
    headers_nv = {"Authorization": f"Bearer {key_nv}"}
    status, res = requisitar_api_final("https://nvidia.com", headers_nv, payload_nv)
    if status == 200:
        try:
            return json.loads(res)["choices"][0]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"💥 NVIDIA Parse Erro interno: {str(e)} | Res: {res[:50]}")
    else:
        logs_erros.append(f"💥 NVIDIA Erro (Status {status}): {res[:100]}")

    # 2. OpenRouter (Mapeamento indexado choices[0])
    key_or = st.secrets.get("OPENROUTER_API_KEY", "").strip()
    payload_or = {
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]
    }
    headers_or = {
        "Authorization": f"Bearer {key_or}",
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Synapse 24 OS"
    }
    status, res = requisitar_api_final("https://openrouter.ai", headers_or, payload_or)
    if status == 200:
        try:
            return json.loads(res)["choices"][0]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"⚠️ OpenRouter Parse Erro interno: {str(e)} | Res: {res[:50]}")
    else:
        logs_erros.append(f"⚠️ OpenRouter Erro (Status {status}): {res[:100]}")

    # 3. Groq Cloud (Endpoint limpo sem barras duplas ou redirecionamento)
    key_groq = st.secrets.get("GROQ_API_KEY", "").strip()
    payload_groq = {
        "model": "llama-3.3-70b-specdec",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]
    }
    headers_groq = {"Authorization": f"Bearer {key_groq}"}
    status, res = requisitar_api_final("https://groq.com", headers_groq, payload_groq)
    if status == 200:
        try:
            return json.loads(res)["choices"][0]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"💥 Groq Parse Erro interno: {str(e)} | Res: {res[:50]}")
    else:
        logs_erros.append(f"💥 Groq Erro (Status {status}): {res[:100]}")

    # 4. Gemini (Dupla autenticação: Bearer + x-goog-api-key)
    key_gemini = st.secrets.get("GEMINI_API_KEY", "")
    if "," in key_gemini:
        key_gemini = key_gemini.split(",")[0].strip()
    else:
        key_gemini = key_gemini.strip()
        
    payload_gemini = {
        "model": "gemini-2.5-flash",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]
    }
    # Força a injeção dupla para sanar o erro de autorização ausente da Google
    headers_gemini = {
        "Authorization": f"Bearer {key_gemini}",
        "x-goog-api-key": key_gemini
    }
    url_gemini = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    status, res = requisitar_api_final(url_gemini, headers_gemini, payload_gemini)
    if status == 200:
        try:
            return json.loads(res)["choices"][0]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"💥 Gemini Parse Erro interno: {str(e)} | Res: {res[:50]}")
    else:
        logs_erros.append(f"💥 Gemini Erro (Status {status}): {res[:100]}")

    return f"RAIZ_ERRO:{json.dumps(logs_erros)}"
    
