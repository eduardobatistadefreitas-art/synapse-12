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
        Todo input entra aqui e é encapsulado para os agentes.
        """
        self.log.info("SISTEMA ATIVADO: Recebendo entrada do usuário.")
        
        # O kernel cria o 'envelope' inicial (título e endereço)
        # O Mediador (IA01) é sempre o primeiro a processar
        envelope = {
            "header": {
                "from": "KERNEL", 
                "to": "IA01", 
                "tag": "[CMD:INICIAR]",
                "timestamp": None
            },
            "body": user_input
        }
        
        # Entrega o envelope ao barramento (Bus) usando o método correto 'enviar'
        resposta = self.bus.enviar("KERNEL", "IA01", "[CMD:INICIAR]", envelope)
        self.log.info("Comando entregue ao Mediador (IA01).")
        return resposta

    def signal_shutdown(self):
        self.log.info("SISTEMA DESLIGANDO: Finalizando processos de agentes.")
      
