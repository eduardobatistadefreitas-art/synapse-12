# src/agents/ia02_executor.py
from agents.base_agent import BaseAgent
from utils.logger import SynapseLogger

class AgenteExecutor(BaseAgent):
    """
    IA02 - EXECUTOR: O Arquiteto de Software.
    Escreve código funcional baseado no briefing gerado pelo Mediador.
    """
    def __init__(self, agent_id, role, bus):
        super().__init__(agent_id, role, bus)
        self.log = SynapseLogger()
        self.model = "deepseek-r1-distill-llama-70b" # Cérebro avançado de código

    def handle_logic(self, tag, payload):
        if tag in ["[CMD:EXECUTAR_PROJETO]", "[CMD:CORRIGIR_PROJETO]", "[CMD:INICIAR_ESQUELETO]"]:
            # Desembrulha o envelope de dados
            corpo = payload.get("body") if isinstance(payload, dict) else payload
            
            self.log.info("Iniciando codificação inteligente via DeepSeek Engine...")
            
            prompt_sistema = (
                "Você é o IA02 - EXECUTOR. Um programador sênior focado em resultados. "
                "Escreva um código em Python completo, funcional e bem estruturado que resolva o pedido. "
                "Não mande explicações de texto, coloque apenas o código dentro de blocos markdown de programação."
            )
            
            prompt_usuario = f"Escreva o software baseado neste briefing técnico: {corpo}"
            
            # Chama a inteligência profunda do DeepSeek na Groq de graça
            codigo_gerado = self.chamar_ia(prompt_sistema, prompt_usuario)
            
            # Como o fluxo é síncrono e estamos exibindo o fim da linha, 
            # retornamos o código direto para o painel do app
            return codigo_gerado
            
