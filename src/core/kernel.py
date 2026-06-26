# src/core/kernel.py
from utils.logger import SynapseLogger

class SynapseKernel:
    """
    O Orquestrador Central. 
    Ele é a única porta de entrada para o sistema Synapse 12.
    """
    def __init__(self, bus):
        self.bus = bus
        self.log = SynapseLogger()
        self.log.info("Kernel do Synapse 12 inicializado com sucesso.")

    def start_pipeline(self, user_input):
        """
        Inicia a jornada da informação no sistema.
        Garante que a resposta final dos agentes retorne até o usuário.
        """
        self.log.info("SISTEMA ATIVADO: Recebendo entrada do usuário.")
        
        envelope = {
            "header": {
                "from": "KERNEL", 
                "to": "IA01", 
                "tag": "[CMD:INICIAR]",
                "timestamp": None
            },
            "body": user_input
        }
        
        # O 'return' garante que o resultado final gerado pelo Executor (IA02) 
        # seja devolvido para o Kernel, que por sua vez devolve para a tela do app.py
        resposta_final = self.bus.enviar("KERNEL", "IA01", "[CMD:INICIAR]", envelope)
        self.log.info("Orquestração concluída com sucesso.")
        return resposta_final

    def signal_shutdown(self):
        self.log.info("SISTEMA DESLIGANDO: Finalizando processos de agentes.")
        
