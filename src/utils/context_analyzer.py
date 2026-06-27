class ContextAnalyzer:
    def __init__(self):
        self.mapeamento = {
            "venda": "SISTEMA_COMERCIAL", "poema": "CREATIVO_TEXTO",
            "tese": "ACADEMICO_TECNICO", "melhoria": "REFATORACAO"
        }

    def extrair_intencao(self, texto):
        texto_limpo = texto.lower()
        for palavra, tag in self.mapeamento.items():
            if palavra in texto_limpo:
                return [tag]
        return ["GERAL_CUSTOM"]
        
