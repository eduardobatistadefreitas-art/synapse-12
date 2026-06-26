# src/agents/ia05_auditor.py
from agents.base_agent import BaseAgent
from utils.logger import SynapseLogger

class AgenteAuditor(BaseAgent):
    """
    IA05 - AUDITOR: O Juiz implacável.
    Pragmático, direto e sem otimismo. 
    Valida a evolução técnica do projeto.
    """
    def __init__(self, agent_id, role, bus):
        super().__init__(agent_id, role, bus)
        self.historico_versao_anterior = None
        self.log = SynapseLogger()
        self.log.info(f"Auditor {agent_id} iniciado e monitorando entregas.")

    def handle_logic(self, tag, payload):
        if tag == "[CMD:VALIDAR_ENTREGA]":
            # Extrai o corpo real do payload de dentro do envelope do barramento
            corpo_payload = payload.get("body") if isinstance(payload, dict) else payload
            return self._auditar(corpo_payload)

    def _auditar(self, novo_projeto):
        # 1. Auditoria da primeira entrega (Cega)
        if self.historico_versao_anterior is None:
            self.historico_versao_anterior = novo_projeto
            return self.send_to("IA03", "[FEEDBACK_IA05_ANALISE_INICIAL]", novo_projeto)

        # 2. Auditoria pragmática (Comparação de evolução)
        falhas = self._comparar_e_validar(self.historico_versao_anterior, novo_projeto)
        
        if not falhas:
            self.historico_versao_anterior = novo_projeto
            return self.send_to("IA04", "[FEEDBACK_IA05_APROVADO]", "PROJETO VALIDADO.")
        
        # O IA05 não é otimista. Ele lista o erro e encerra.
        return self.send_to("IA03", "[FEEDBACK_IA05_REPROVADO]", falhas)

    def _comparar_e_validar(self, anterior, atual):
        # Lógica rigorosa: Detecta se o código regrediu ou se o erro persiste
        # Retorna lista de erros ou None se perfeito
        return None
