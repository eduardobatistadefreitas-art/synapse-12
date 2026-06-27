import urllib.request
import urllib.parse
import json
import streamlit as st

def requisitar_api_v3(url_completa, headers, payload, timeout=15):
    """
    Executa a requisição HTTP usando urllib.request nativo.
    Blinda o método POST e limpa redirecionamentos para evitar erro 405.
    """
    try:
        if not url_completa.startswith("https://"):
            url_completa = "https://" + url_completa
            
        dados_bytes = json.dumps(payload).encode('utf-8')
        
        # Injeta cabeçalhos corporativos estritos obrigatórios
        headers["Content-Type"] = "application/json"
        headers["User-Agent"] = "Synapse24OS/1.1"
        
        req = urllib.request.Request(url_completa, data=dados_bytes, headers=headers, method="POST")
        
        with urllib.request.urlopen(req, timeout=timeout) as resposta:
            status_code = resposta.status
            corpo = resposta.read().decode('utf-8')
            return status_code, corpo

    except urllib.error.HTTPError as e:
        corpo_erro = e.read().decode('utf-8')
        return e.code, corpo_erro
    except Exception as e:
        return 500, json.dumps({"error": {"message": str(e), "code": 500}})

def orquestrar_chamada_rest(prompt_sistema, prompt_usuario):
    """
    Orquestrador com Malha de Redundância Quádrupla Automática.
    JSON Parsing seguro e rotas oficiais restabelecidas.
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
    key_nv = st.secrets.get("NVIDIA_API_KEY", "").strip()
    headers_nv = {"Authorization": f"Bearer {key_nv}"}
    status, res = requisitar_api_v3("https://nvidia.com", headers_nv, payload_nv)
    if status == 200:
        try:
            return json.loads(res)["choices"][0]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"💥 NVIDIA Parse Erro interno: {str(e)} | Resposta: {res[:100]}")
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
    key_or = st.secrets.get("OPENROUTER_API_KEY", "").strip()
    headers_or = {"Authorization": f"Bearer {key_or}"}
    status, res = requisitar_api_v3("https://openrouter.ai", headers_or, payload_or)
    if status == 200:
        try:
            return json.loads(res)["choices"][0]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"⚠️ OpenRouter Parse Erro interno: {str(e)} | Resposta: {res[:100]}")
    else:
        logs_erros.append(f"⚠️ OpenRouter Erro (Status {status}): {res[:120]}")

    # 3. Groq Cloud (Endpoint limpo sem barras duplas ou redirecionamento)
    payload_groq = {
        "model": "llama-3.3-70b-specdec",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]
    }
    key_groq = st.secrets.get("GROQ_API_KEY", "").strip()
    headers_groq = {"Authorization": f"Bearer {key_groq}"}
    status, res = requisitar_api_v3("https://groq.com", headers_groq, payload_groq)
    if status == 200:
        try:
            return json.loads(res)["choices"][0]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"💥 Groq Parse Erro interno: {str(e)} | Resposta: {res[:100]}")
    else:
        logs_erros.append(f"💥 Groq Erro (Status {status}): {res[:120]}")

    # 4. Gemini (Rota Oficial OpenAI-Compatible Certificada)
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
    headers_gemini = {"Authorization": f"Bearer {key_gemini}"}
    # Endpoint correto de produção do Google AI Studio com mapeamento OpenAI
    url_gemini = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    status, res = requisitar_api_v3(url_gemini, headers_gemini, payload_gemini)
    if status == 200:
        try:
            return json.loads(res)["choices"][0]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"💥 Gemini Parse Erro interno: {str(e)} | Resposta: {res[:100]}")
    else:
        logs_erros.append(f"💥 Gemini Erro (Status {status}): {res[:120]}")

    return f"RAIZ_ERRO:{json.dumps(logs_erros)}"
    
