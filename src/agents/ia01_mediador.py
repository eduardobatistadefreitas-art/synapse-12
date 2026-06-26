# src/agents/ia01_mediador.py
from agents.base_agent import BaseAgent
from utils.logger import SynapseLogger

class AgenteMediador(BaseAgent):
    """
    IA01 - MEDIADOR: O porteiro do Synapse 12.
    Responsável pela triagem, validação de escopo e entrevista estruturada.
    """
    def __init__(self, agent_id, role, bus, user_plan="BASIC"):
        super().__init__(agent_id, role, bus)
        self.user_plan = user_plan
        self.log = SynapseLogger()
        self.log.info(f"Mediador {agent_id} iniciado no plano {user_plan}")

    def handle_logic(self, tag, payload):
        # Garante que o payload não seja None para não quebrar as strings
        payload_seguro = payload if payload is not None else {}

        # 1. Validação de Escopo (Gatekeeper)
        if not self._validar_escopo(payload_seguro):
            return "[ERR:ESCOPO_NAO_PERMITIDO] Tarefa excede o limite do seu plano."

        # 2. Entrevista Estruturada (Máquina de Estados)
        if self._checklist_completo(payload_seguro):
            self.log.info("Checklist completo. Enviando para Executor (IA02).")
            return self.send_to("IA02", "[CMD:INICIAR_ESQUELETO]", payload_seguro)
        
        return "[IA01] Por favor, forneça os dados conforme o checklist de 5 passos."

    def _validar_escopo(self, payload):
        """Bloqueia projetos fora do escopo do plano gratuito (Isca)."""
        if self.user_plan == "BASIC":
            complexidade_palavras = ["banco de dados", "servidor", "agente autônomo", "api complexa"]
            payload_str = str(payload).lower()
            if any(p in payload_str for p in complexidade_palavras):
                return False
        return True

    def _checklist_completo(self, payload):
        """Verifica se as 5 perguntas de ouro foram respondidas."""
        return "conclusao" in str(payload).lower()
      
