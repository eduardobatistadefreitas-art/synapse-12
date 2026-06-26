# src/agents/ia04_supervisor.py
from agents.base_agent import BaseAgent
from utils.logger import SynapseLogger

class AgenteSupervisor(BaseAgent):
    """
    IA04 - MAESTRO: O Gerente de Fluxo.
    Não executa código, apenas gerencia o estado do sistema.
    """
    def __init__(self, agent_id, role, bus):
        super().__init__(agent_id, role, bus)
        self.log = SynapseLogger()
        self.log.info(f"Supervisor/Maestro {agent_id} ativado na malha.")

    def handle_logic(self, tag, payload):
        # O Maestro "escuta" tudo. Se encontrar erros, ele age.
        
        # Caso 1: Erro de Escopo ou Fatal
        if "ERR" in tag or "FATAL" in tag:
            return self._tratar_falha_critica(tag, payload)
        
        # Caso 2: Projeto validado e pronto
        if tag == "[STATUS:PRONTO]":
            return self._finalizar_projeto(payload)

    def _tratar_falha_critica(self, tag, payload):
        self.log.alerta(f"Maestro detectou anomalia crítica: {tag}")
        # Intervenção: Se houver falha, o IA04 força um reset no IA03
        return self.send_to("IA03", "[CMD:RESET_ESTRATEGIA_FORCADO]", payload)

    def _finalizar_projeto(self, payload):
        self.log.info("Maestro confirmou conclusão do projeto. Liberando entrega.")
        return "PROJETO_CONCLUIDO_COM_SUCESSO"
      
