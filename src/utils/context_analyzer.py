import json

class ContextAnalyzer:
    """
    Modulo utilitario para processamento estruturado do historico de conversas.
    Evita amnesia de contexto e reduz o consumo desnecessario de tokens.
    """
    def __init__(self, limite_mensagens=5):
        self.limite_mensagens = limite_mensagens
        # Dicionario simples de mapeamento de palavras-chave para intencoes
        self.dicionario_intencoes = {
            "venda": "SISTEMA_COMERCIAL",
            "poema": "CONTEUDO_CREATIVO",
            "tese": "ACADEMICO_TECNICO",
            "melhoria": "REFATORACAO_PROCESSO",
            "ajuste": "REFATORACAO_PROCESSO",
            "erro": "CORRECAO_DE_BUG"
        }

    def otimizar_historico(self, historico_lista):
        """
        Garante que a janela deslizante de contexto nao estoure o limite de tokens.
        """
        if len(historico_lista) > self.limite_mensagens:
            return historico_lista[-self.limite_mensagens:]
        return historico_lista

    def extrair_tags_intencao(self, texto_usuario):
        """
        Analisa programaticamente o input cru antes de enviar para a IA principal.
        Retorna tags que fixam o foco do IA01.
        """
        texto_limpo = texto_usuario.lower()
        tags_encontradas = []
        
        for palavra, tag in self.dicionario_intencoes.items():
            if palavra in texto_limpo:
                tags_encontradas.append(tag)
                
        if not tags_encontradas:
            tags_encontradas.append("GERAL_CUSTOM")
            
        return tags_encontradas
