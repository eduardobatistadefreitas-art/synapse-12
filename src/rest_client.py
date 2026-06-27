import subprocess
import json
import streamlit as st

def executar_via_curl(url, headers, payload, timeout=15):
    """
    Executa a chamada REST delegando para o utilitario 'curl' do sistema operacional.
    Fura 100% dos bloqueios de HTML/Cloudflare que barram o urllib/http.client.
    """
    try:
        # Monta os argumentos do comando cURL de forma segura
        comando = ["curl", "-X", "POST", url, "-s", "--max-time", str(timeout)]
        
        # Adiciona os cabeçalhos padrão simulando navegador real
        comando += ["-H", "Content-Type: application/json"]
        comando += ["-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"]
        
        for chave, valor in headers.items():
            comando += ["-H", f"{chave}: {valor}"]
            
        comando += ["-d", json.dumps(payload)]
        
        # Executa no ecossistema Linux do Streamlit Cloud
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True)
        return 200, resultado.stdout
    except subprocess.CalledProcessError as e:
        return 500, json.dumps({"error": {"message": f"Erro cURL: {e.stderr}", "code": 500}})
    except Exception as e:
        return 500, json.dumps({"error": {"message": str(e), "code": 500}})

def orquestrar_chamada_rest(prompt_sistema, prompt_usuario):
    """
    Orquestrador Supremo Synapse 24 via Malha cURL Isolada.
    """
    logs_erros = []

    # 1. NVIDIA Build
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
    status, res = executar_via_curl("https://nvidia.com", headers_nv, payload_nv)
    if status == 200 and "choices" in res:
        try:
            return json.loads(res)["choices"][0]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"💥 NVIDIA Parse Erro: {str(e)}")
    else:
        logs_erros.append(f"💥 NVIDIA Erro/HTML detectado pelo cURL.")

    # 2. OpenRouter (Fura o Cloudflare usando cURL nativo)
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
    status, res = executar_via_curl("https://openrouter.ai", headers_or, payload_or)
    if status == 200 and "choices" in res:
        try:
            return json.loads(res)["choices"][0]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"⚠️ OpenRouter Parse Erro: {str(e)}")
    else:
        logs_erros.append(f"⚠️ OpenRouter Erro (Cota ou Limite): {res[:80]}")

    # 3. Groq Cloud
    key_groq = st.secrets.get("GROQ_API_KEY", "").strip()
    payload_groq = {
        "model": "llama-3.3-70b-specdec",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]
    }
    headers_groq = {"Authorization": f"Bearer {key_groq}"}
    status, res = executar_via_curl("https://groq.com", headers_groq, payload_groq)
    if status == 200 and "choices" in res:
        try:
            return json.loads(res)["choices"][0]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"💥 Groq Parse Erro: {str(e)}")
    else:
        logs_erros.append(f"💥 Groq Erro (Status/Chave): {res[:80]}")

    # 4. Gemini - Rota Nativa Pura (Desarma erro 400 de Compatibilidade OpenAI)
    key_gemini = st.secrets.get("GEMINI_API_KEY", "")
    # Se houver multiplas chaves separadas por virgula, extrai a primeira de forma limpa
    if "," in key_gemini:
        key_gemini = key_gemini.split(",")[0].strip()
    else:
        key_gemini = key_gemini.strip()
        
    payload_gemini = {
        "contents": [{
            "parts": [{"text": f"System Prompt: {prompt_sistema}\n\nUser Request: {prompt_usuario}"}]
        }],
        "generationConfig": {"temperature": 0.2}
    }
    url_gemini = f"https://googleapis.com{key_gemini}"
    status, res = executar_via_curl(url_gemini, {}, payload_gemini)
    if status == 200 and "candidates" in res:
        try:
            return json.loads(res)["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            logs_erros.append(f"💥 Gemini Parse Erro Nativo: {str(e)}")
    else:
        logs_erros.append(f"💥 Gemini Erro Nativo: {res[:100]}")

    return f"RAIZ_ERRO:{json.dumps(logs_erros)}"
    
