from agents.base import BaseAgent
from utils.network_helper import executar_requisicao_ia

class ExecutorAgent(BaseAgent):
    def __init__(self):
        super().__init__("IA02_Executor", "Executor Técnico Sênior")

    def executar(self, payload):
        briefing = payload.get("briefing", "")
        prompt_sistema = f"Você é o {self.role}. Siga o briefing e estruture o plano técnico em Markdown."
        return executar_requisicao_ia(prompt_sistema, briefing)
      
