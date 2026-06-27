import http.client
import json
import urllib.parse

def requisitar_api(url_completa, headers, payload, timeout=15):
    """
    Executa a requisição HTTP tratando strings de URL de forma robusta.
    Imune ao erro 'nonnumeric port'.
    """
    try:
        # Força o parse correto da URL indepedente do formato de entrada
        if not url_completa.startswith(('http://', 'https://')):
            url_completa = 'https://' + url_completa
            
        parsed_url = urllib.parse.urlparse(url_completa)
        host = parsed_url.netloc
        path = parsed_url.path if parsed_url.path else "/"
        if parsed_url.query:
            path += "?" + parsed_url.query

        # Remove portas fantasmas causadas por barras residuais
        if ":" in host:
            hostname, port = host.split(":", 1)
            if not port.isdigit():
                host = hostname  # Limpa se a porta for não numérica

        # Executa a conexão limpa
        conexao = http.client.HTTPSConnection(host, timeout=timeout)
        conexao.request("POST", path, body=json.dumps(payload), headers=headers)
        
        resposta = conexao.getresponse()
        status = resposta.read().decode('utf-8')
        conexao.close()
        
        return resposta.status, status

    except Exception as e:
        # Captura a falha e formata para o painel de diagnóstico visual
        return 500, json.dumps({"error": {"message": str(e), "code": 500}})
        
