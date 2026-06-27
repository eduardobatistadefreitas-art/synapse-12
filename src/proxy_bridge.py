import streamlit as st
import streamlit.components.v1 as components
import json

def injetar_ponte_frontend(prompt_sistema, prompt_usuario, api_key, provedor="gemini"):
    """
    Injeta um script javascript oculto em tela que executa a chamada HTTP
    direto pelo navegador do cliente, salvando o texto gerado na sessao local.
    """
    id_componente = f"bridge_{provedor}"
    
    # Payload oficial estruturado do Gemini Nativo
    url = f"https://googleapis.com{api_key}"
    payload_js = {
        "contents": [{
            "parts": [{"text": f"System Prompt: {prompt_sistema}\n\nUser Prompt: {prompt_usuario}"}]
        }]
    }

    html_javascript = f"""
    <div id="{id_componente}" style="color: #4CAF50; font-size: 14px; font-weight: bold; margin-bottom: 10px;">
        🔄 Processando sua requisiçao direto via Google AI Gateway...
    </div>
    <script>
    (async function() {{
        const el = document.getElementById("{id_componente}");
        try {{
            const resposta = await fetch("{url}", {{
                method: "POST",
                headers: {{ "Content-Type": "application/json" }},
                body: JSON.stringify({json.dumps(payload_js)})
            }});
            
            if (!resposta.ok) throw new Error("Erro HTTP: " + resposta.status);
            
            const dados = await resposta.json();
            const textoFinal = dados.candidates[0].content.parts[0].text;
            
            // Grava o texto gerado de forma segura no navegador do celular
            window.parent.sessionStorage.setItem("synapse_resultado_bruto", textoFinal);
            el.innerText = "✅ Conteúdo gerado com sucesso pelo Google! Clique abaixo para extrair.";
        }} catch (erro) {{
            window.parent.sessionStorage.setItem("synapse_resultado_bruto", "ERRO:" + erro.message);
            el.innerText = "💥 Erro no Tunel: " + erro.message;
            el.style.color = "red";
        }}
    }})();
    </script>
    """
    components.html(html_javascript, height=50)
