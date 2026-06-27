from agents.base import BaseAgent
from utils.network_helper import executar_requisicao_ia

class ExecutorAgent(BaseAgent):
    def __init__(self):
        super().__init__("IA02_Executor", "Executor Técnico e Matemático Sênior")

    def executar(self, payload):
        conteudo_projeto = payload.get("projeto_intermedio", "")
        prompt_sistema = f"Você é o {self.role}. Roda lógica, matemática ou estrutura e devolva para o IA03 refinar."
        return executar_requisicao_ia(prompt_sistema, conteudo_projeto)
        
