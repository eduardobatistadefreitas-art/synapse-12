import urllib.request
import urllib.error
import json
import streamlit as st

def requisitar_via_urllib_limpo(url, headers, payload, timeout=15):
    """
    Requisiçao HTTP tradicional limpa via urllib padrao do Python.
    """
    try:
        dados_bytes = json.dumps(payload).encode('utf-8')
        headers_finais = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }
        for k, v in headers.items():
            headers_finais[k] = v
            
        req = urllib.request.Request(url, data=dados_bytes, headers=headers_finais, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as resposta:
            return resposta.status, resposta.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 500, json.dumps({"error": {"message": str(e), "code": 500}})

def orquestrar_chamada_rest(prompt_sistema, prompt_usuario):
    """
    Orquestrador Synapse 24 com injeçao dinamica de Rota de Fuga.
    """
    logs_erros = []

    # 1 & 2. Pulando provedores em blackout temporario de rede Cloudflare
    logs_erros.append("💥 NVIDIA: Modo de segurança ativo")
    logs_erros.append("⚠️ OpenRouter: Modo de segurança ativo")

    # 3. Tenta Groq via Backend Tradicional
    key_groq = st.secrets.get("GROQ_API_KEY", "").strip()
    payload_groq = {
        "model": "llama-3.3-70b-specdec",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]
    }
    headers_groq = {"Authorization": f"Bearer {key_groq}"}
    status, res = requisitar_via_urllib_limpo("https://groq.com", headers_groq, payload_groq)
    if status == 200:
        try:
            return json.loads(res)["choices"][0]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"💥 Groq Parse Erro: {str(e)}")
    else:
        logs_erros.append(f"💥 Groq Erro (Status {status}): {res[:50]}")

    # 4. Tenta Gemini via Backend Tradicional
    key_gemini = st.secrets.get("GEMINI_API_KEY", "").strip()
    payload_gemini = {
        "contents": [{"parts": [{"text": f"System Prompt: {prompt_sistema}\n\nUser: {prompt_usuario}"}]}]
    }
    url_gemini = f"https://googleapis.com{key_gemini}"
    status, res = requisitar_via_urllib_limpo(url_gemini, {}, payload_gemini)
    if status == 200:
        try:
            dados = json.loads(res)
            return dados["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            logs_erros.append(f"💥 Gemini Parse Erro: {str(e)}")
    else:
        logs_erros.append(f"💥 Gemini Erro Backend (Status {status})")

    # 🚀 ROTA DE FUGA SUPREMA: Se a rede do servidor quebrou geral, joga o fluxo no proxy_bridge
    try:
        from proxy_bridge import injetar_ponte_frontend
        injetar_ponte_frontend(prompt_sistema, prompt_usuario, key_gemini, provedor="gemini")
        
        # Como o javascript roda assincrono na tela, instruimos o app.py a colher o resultado visual
        return "SOLICITACAO_VIA_TUNEL_EM_ANDAMENTO"
    except Exception as e:
        logs_erros.append(f"🚨 Falha ao acionar a ponte de frontend: {str(e)}")

    return f"RAIZ_ERRO:{json.dumps(logs_erros)}"
    
