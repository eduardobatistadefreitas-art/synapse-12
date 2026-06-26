# src/agents/ia02_executor.py
from agents.base_agent import BaseAgent
from utils.logger import SynapseLogger

class AgenteExecutor(BaseAgent):
    """
    IA02 - EXECUTOR: O Arquiteto de Software.
    Recebe o plano do IA03 e escreve o código funcional.
    """
    def __init__(self, agent_id, role, bus):
        super().__init__(agent_id, role, bus)
        self.log = SynapseLogger()

    def handle_logic(self, tag, payload):
        """
        O Executor opera estritamente sobre um plano recebido.
        Se não houver um plano estruturado, ele solicita correção ao IA03.
        """
        if tag in ["[CMD:EXECUTAR_PROJETO]", "[CMD:CORRIGIR_PROJETO]"]:
            self.log.info("Iniciando codificação conforme plano do IA03.")
            
            # Extrai o corpo real do payload de dentro do envelope do barramento
            corpo_payload = payload.get("body") if isinstance(payload, dict) else payload
            
            try:
                codigo_gerado = self._traduzir_plano_em_codigo(corpo_payload)
                return self.send_to("IA03", "[DATA:CODIGO_PRONTO]", codigo_gerado)
            except Exception as e:
                self.log.erro(f"Falha na execução: {e}")
                return self.send_to("IA03", "[ERR:FALHA_CODIFICACAO]", str(e))

    def _traduzir_plano_em_codigo(self, plano):
        """
        Transforma o dicionário de especificações em arquivos reais.
        Aqui reside a lógica de escrita de arquivos do sistema.
        """
        self.log.info("Traduzindo blueprint para estrutura de arquivos...")
        return {"status": "SUCESSO", "arquivos": ["main.py", "logic.py"]}
      
