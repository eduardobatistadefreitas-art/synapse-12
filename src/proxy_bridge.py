import streamlit as st
import streamlit.components.v1 as components
import json

def injetar_ponte_frontend(prompt_sistema, prompt_usuario, api_key, provedor="gemini"):
    """
    Injeta um script javascript oculto em tela que executa a chamada HTTP
    direto pelo navegador do cliente (smartphone), ignorando o DNS bloqueado do servidor.
    """
    st.warning(f"🔄 Ativando Tunel de Rota de Fuga via Browser (Provedor: {provedor})...")
    
    id_componente = f"bridge_{provedor}"
    
    # Define as payloads estruturadas oficiais baseadas no provedor selecionado
    if provedor == "gemini":
        url = f"https://googleapis.com{api_key}"
        payload_js = {
            "contents": [{
                "parts": [{"text": f"System Prompt: {prompt_sistema}\n\nUser Prompt: {prompt_usuario}"}]
            }]
        }
    else: # Groq Fallback
        url = "https://groq.com"
        payload_js = {
            "model": "llama-3.3-70b-specdec",
            "messages": [
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ]
        }

    # Bloco JavaScript nativo com fetch assíncrono puro (Bypassa o WAF e o DNS corporativo)
    html_javascript = f"""
    <div id="{id_componente}" style="color: gray; font-size: 11px;">Estabelecendo conexao de tunel...</div>
    <script>
    (async function() {{
        const el = document.getElementById("{id_componente}");
        try {{
            const resposta = await fetch("{url}", {{
                method: "POST",
                headers: {{
                    "Content-Type": "application/json",
                    "Authorization": "{'Bearer ' + api_key if provedor == 'groq' else ''}"
                }},
                body: JSON.stringify({json.dumps(payload_js)})
            }});
            
            if (!resposta.ok) {{
                throw new Error("Erro HTTP: " + resposta.status);
            }}
            
            const dados = await resposta.json();
            let textoFinal = "";
            
            if ("{provedor}" === "gemini") {{
                textoFinal = dados.candidates[0].content.parts[0].text;
            }} else {{
                textoFinal = dados.choices[0].message.content;
            }}
            
            // Injeta o resultado em uma tag oculta legivel para o Streamlit scraping local
            el.innerText = "SUCESSO_TUNEL:" + textoFinal;
            el.style.color = "green";
        }} catch (erro) {{
            el.innerText = "ERRO_TUNEL:" + erro.message;
            el.style.color = "red";
        }}
    }})();
    </script>
    """
    # Renderiza o micro-iframe invisivel na UI
    components.html(html_javascript, height=40)
