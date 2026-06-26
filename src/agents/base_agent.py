# src/agents/base_agent.py
import time

class BaseAgent:
    """
    Classe base para todos os agentes do Synapse 12.
    Garante o padrão de envelopamento e comunicação via Barramento.
    """
    def __init__(self, agent_id, role, bus):
        self.agent_id = agent_id
        self.role = role
        self.bus = bus
        self.memory = []

    def format_envelope(self, receiver_id, tag, payload):
        """
        Cria o 'cabeçalho' padrão para garantir que a IA receptora
        saiba exatamente quem enviou e qual o objetivo.
        """
        return {
            "header": {
                "from": self.agent_id,
                "role": self.role,
                "to": receiver_id,
                "tag": tag,
                "timestamp": time.time()
            },
            "body": payload
        }

    def process(self, tag, payload):
        """
        Ponto de entrada único. Todo agente recebe o envelope já processado.
        """
        print(f"[{self.agent_id} | {self.role}] Recebi tag: {tag}")
        return self.handle_logic(tag, payload)

    def handle_logic(self, tag, payload):
        raise NotImplementedError("Cada agente deve definir sua própria lógica.")

    def send_to(self, receiver_id, tag, payload):
        """
        Envia a mensagem já formatada como um envelope.
        Ajustado para o método 'enviar' do Barramento 2.1.
        """
        envelope = self.format_envelope(receiver_id, tag, payload)
        return self.bus.enviar(self.agent_id, receiver_id, tag, envelope)
      
