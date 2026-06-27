import urllib.request
import urllib.parse
import json
import streamlit as st

def requisitar_api_v2(url_completa, headers, payload, timeout=15):
    """
    Executa a requisição HTTP usando urllib.request nativo.
    Automatiza headers de Host, tamanho de conteúdo e resolve falhas de DNS.
    """
    try:
        if not url_completa.startswith(('http://', 'https://')):
            url_completa = 'https://' + url_completa
            
        dados_bytes = json.dumps(payload).encode('utf-8')
        
        # Garante cabeçalhos mínimos exigidos pelas APIs de produção
        headers["Content-Type"] = "application/json"
        headers["Content-Length"] = str(len(dados_bytes))
        
        req = urllib.request.Request(url_completa, data=dados_bytes, headers=headers, method="POST")
        
        with urllib.request.urlopen(req, timeout=timeout) as resposta:
            status_code = resposta.status
            corpo = resposta.read().decode('utf-8')
            return status_code, corpo

    except urllib.error.HTTPError as e:
        # Captura erros retornados pelo servidor (ex: 401, 429, 500)
        corpo_erro = e.read().decode('utf-8')
        return e.code, corpo_erro
    except Exception as e:
        # Captura falhas de conexão local ou rede
        return 500, json.dumps({"error": {"message": str(e), "code": 500}})

def orquestrar_chamada_rest(prompt_sistema, prompt_usuario):
    """
    Orquestrador com Malha de Redundância Quádrupla Automática via urllib.
    Rotas calibradas e blindadas contra erros de infraestrutura do Streamlit Cloud.
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
    headers_nv = {"Authorization": f"Bearer {key_nv}"}
    status, res = requisitar_api_v2("://nvidia.com", headers_nv, payload_nv)
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
    headers_or = {"Authorization": f"Bearer {key_or}"}
    status, res = requisitar_api_v2("openrouter.ai/api/v1/chat/completions", headers_or, payload_or)
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
    headers_groq = {"Authorization": f"Bearer {key_groq}"}
    status, res = requisitar_api_v2("://groq.com", headers_groq, payload_groq)
    if status == 200:
        try:
            return json.loads(res)["choices"]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"💥 Groq Parse Erro: {str(e)}")
    else:
        logs_erros.append(f"💥 Groq Erro (Status {status}): {res[:120]}")

    # 4. Gemini (Endpoint Oficial do Google AI Studio para Chat Completions)
    key_gemini = st.secrets.get("GEMINI_API_KEY", "")
    # Tratamento caso a string contenha multiplas chaves separadas por virgula
    if "," in key_gemini:
        key_gemini = key_gemini.split(",")[0].strip()
        
    payload_gemini = {
        "model": "gemini-2.5-flash",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]
    }
    # O Gemini exige a chave passada diretamente via query param na URL pública
    url_gemini = f"://googleapis.com{key_gemini}"
    status, res = requisitar_api_v2(url_gemini, {}, payload_gemini)
    if status == 200:
        try:
            return json.loads(res)["choices"]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"💥 Gemini Parse Erro: {str(e)}")
    else:
        logs_erros.append(f"💥 Gemini Erro (Status {status}): {res[:120]}")

    return f"RAIZ_ERRO:{json.dumps(logs_erros)}"
    
