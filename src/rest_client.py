import urllib.request
import urllib.error
import json
import streamlit as st

def requisitar_via_net_limpa(url, headers, payload, timeout=15):
    """
    Mecanismo puro via urllib com injeção segura de dados.
    Imune a bloqueios de sandbox do Streamlit Cloud.
    """
    try:
        dados_bytes = json.dumps(payload).encode('utf-8')
        
        # Define cabeçalhos limpos de mercado para evitar assinaturas de bots
        headers_finais = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }
        # Mescla os cabeçalhos específicos de autenticação das chaves
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
    Orquestrador Synapse 24 recalibrado para as rotas de contingência estáveis.
    """
    logs_erros = []

    # --- PULAR PROVEDORES BLOQUEADOS EM FLASH PELO CLOUDFLARE ---
    logs_erros.append("💥 NVIDIA: Bypass preventivo (Cloudflare ativo)")
    logs_erros.append("⚠️ OpenRouter: Bypass preventivo (Cota/Cloudflare ativo)")

    # 3. Groq Cloud (Endpoint limpo com a payload padrão OpenAI)
    key_groq = st.secrets.get("GROQ_API_KEY", "").strip()
    payload_groq = {
        "model": "llama-3.3-70b-specdec",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ]
    }
    headers_groq = {"Authorization": f"Bearer {key_groq}"}
    status, res = requisitar_via_net_limpa("https://groq.com", headers_groq, payload_groq)
    if status == 200:
        try:
            return json.loads(res)["choices"][0]["message"]["content"]
        except Exception as e:
            logs_erros.append(f"💥 Groq Parse Erro: {str(e)}")
    else:
        logs_erros.append(f"💥 Groq Erro (Status {status}): {res[:100]}")

    # 4. Gemini - Rota Nativa Pura (Ajustada contra o Erro 400)
    key_gemini = st.secrets.get("GEMINI_API_KEY", "").strip()
    if "," in key_gemini:
        key_gemini = key_gemini.split(",")[0].strip()

    # Formatação exata do dicionário que a API estruturada do Google exige
    payload_gemini = {
        "contents": [{
            "parts": [{
                "text": f"System Prompt: {prompt_sistema}\n\nUser Prompt: {prompt_usuario}"
            }]
        }]
    }
    
    url_gemini = f"https://googleapis.com{key_gemini}"
    status, res = requisitar_via_net_limpa(url_gemini, {}, payload_gemini)
    if status == 200:
        try:
            # Captura a árvore de nós correta da resposta nativa da Google
            dados = json.loads(res)
            return dados["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            logs_erros.append(f"💥 Gemini Parse Erro: {str(e)} | Res: {res[:50]}")
    else:
        logs_erros.append(f"💥 Gemini Erro Nativo (Status {status}): {res[:100]}")

    return f"RAIZ_ERRO:{json.dumps(logs_erros)}"
    
