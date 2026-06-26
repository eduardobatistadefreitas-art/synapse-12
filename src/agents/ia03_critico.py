# src/agents/ia03_critico.py
from agents.base_agent import BaseAgent

class AgenteCritico(BaseAgent):
    """
    IA03 - CRÍTICO: O avaliador técnico e controlador de iterações.
    Ajusta e refina projetos baseado nos feedbacks ou encerra por limite de cota.
    """
    def __init__(self, agent_id, role, bus, user_tier="FREE"):
        super().__init__(agent_id, role, bus)
        self.limites = {"FREE": 1, "BASIC": 3, "PREMIUM": 99}
        self.max_tentativas = self.limites.get(user_tier, 1)
        self.tentativas_atuais = 0

    def handle_logic(self, tag, payload):
        # Como o ecossistema trafega envelopes, extraímos o corpo real da mensagem
        corpo_payload = payload.get("body") if isinstance(payload, dict) else payload

        if tag == "[FEEDBACK_IA05_REPROVADO]":
            self.tentativas_atuais += 1
            
            if self.tentativas_atuais >= self.max_tentativas:
                return self.send_to("IA04", "[STATUS:ESGOTADO]", "Limite de tentativas atingido.")
            
            # Se ainda houver tentativas, processa e manda corrigir no IA02
            projeto_refinado = self._refinar_projeto(corpo_payload)
            return self.send_to("IA02", "[CMD:CORRIGIR_PROJETO]", projeto_refinado)
            
        elif tag == "[FEEDBACK_IA05_APROVADO]":
            return self.send_to("IA04", "[STATUS:PRONTO]", corpo_payload)

    def _refinar_projeto(self, falhas):
        """Simulação interna de refinamento baseado nas falhas pontuadas."""
        return {"status": "refinado", "detalhes_correcao": falhas}
      
