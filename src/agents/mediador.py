from agents.base import BaseAgent
from utils.network_helper import executar_requisicao_ia

class MediadorAgent(BaseAgent):
    def __init__(self):
        super().__init__("IA01_Mediador", "Mediador de Briefings Técnicos")

    def executar(self, payload):
        diretriz_optimizer = payload.get("diretriz_optimizer", "")
        tarefa_usuario = payload.get("tarefa_usuario", "")
        rodada = payload.get("rodada", 1)
        
        prompt_sistema = f"Você é o {self.role}. {diretriz_optimizer}. Monte um briefing com Objetivo, Requisitos quantificáveis (%) e Cronograma com prazos."
        prompt_user = tarefa_usuario if rodada == 1 else f"{tarefa_usuario}\n\n⚠️ REPROVADO: Adicione métricas (%) e prazos obrigatórios."
        
        return executar_requisicao_ia(prompt_sistema, prompt_user)
      
