# src/agents/ia01_mediador.py
from agents.base_agent import BaseAgent
from utils.logger import SynapseLogger

class AgenteMediador(BaseAgent):
    """
    IA01 - MEDIADOR: O co-piloto de triagem.
    Garante que a ideia do usuário seja compreendida e estruturada.
    """
    def __init__(self, agent_id, role, bus, user_plan="BASIC"):
        super().__init__(agent_id, role, bus)
        self.user_plan = user_plan
        self.log = SynapseLogger()
        self.model = "gemma2-9b-it" # Define o modelo da Groq

    def handle_logic(self, tag, payload):
        # Desembrulha o envelope síncrono do barramento
        corpo = payload.get("body") if isinstance(payload, dict) else payload
        if isinstance(corpo, dict):
            tarefa_usuario = corpo.get("tarefa", "")
        else:
            tarefa_usuario = str(corpo)

        self.log.info(f"Mediador analisando projeto: {tarefa_usuario[:30]}...")

        # 🎭 CHAMADA REAL DE IA: O Mediador usa o modelo Gemma2 para criar o briefing estruturado
        prompt_sistema = (
            "Você é o IA01 - Mediador do ecossistema Synapse 12. "
            "Sua tarefa é ler a ideia de automação do usuário e criar um briefing técnico super enxuto "
            "com 3 requisitos claros para o engenheiro de software executar. Seja direto e prático."
        )
        
        prompt_usuario = f"Ideia do cliente: {tarefa_usuario}"
        
        # Faz a chamada real e gratuita via API REST da Groq
        briefing_estruturado = self.chamar_ia(prompt_sistema, prompt_usuario)
        
        # Envia o briefing real direto para o Executor (IA02) continuar a cadeia
        self.log.info("Briefing estruturado com sucesso. Acionando Executor...")
        return self.send_to("IA02", "[CMD:EXECUTAR_PROJETO]", briefing_estruturado)
        
