# src/bus/message_bus.py
import time
from core.middleware import MiddlewareResiliencia

class MessageBus:
    """
    O Sistema Nervoso Central do Synapse 12.
    Gerencia o roteamento de mensagens com proteção contra latência.
    """
    def __init__(self):
        self.agentes = {}
        # Inicializa o filtro do middleware com 50ms de tolerância
        self.middleware = MiddlewareResiliencia(tau_validade_max=0.05)

    def registrar(self, agente):
        self.agentes[agente.agent_id] = agente
        print(f"[⚙️ BUS] Agente {agente.agent_id} conectado ao ecossistema.")

    def enviar(self, de_quem, para_quem, tag, payload):
        # 1. Registra o tempo em que o sinal foi disparado
        t_origem = time.perf_counter()
        
        # 2. Valida a resiliência por meio do middleware integrado
        if self.middleware.filtrar_comando(tag, t_origem) is None:
            print(f"⚠️ [BUS] ALERTA: Comando {tag} descartado por latência excessiva.")
            return "[ERR:LATENCIA_ALTA]"

        # 3. Faz o roteamento para o agente de destino se ele existir
        if para_quem in self.agentes:
            print(f"📡 [BUS] {de_quem} ➡️ {para_quem} | Tag: {tag}")
            return self.agentes[para_quem].handle_logic(tag, payload)
        
        print(f"❌ [BUS] ERRO: Destinatário {para_quem} não encontrado.")
        return "[ERR:DESTINO_NAO_ENCONTRADO]"
