# test_synapse.py
import time
import sys
import os

# Ajusta o caminho para que o Python localize a pasta src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from core.middleware import MiddlewareResiliencia
from bus.message_bus import MessageBus

# Criamos um agente falso (Mock) apenas para validar o funcionamento do barramento
class AgenteMock:
    def __init__(self, agent_id):
        self.agent_id = agent_id
    def handle_logic(self, tag, payload):
        return f"Sucesso:{tag}"

def test_middleware_latencia():
    middleware = MiddlewareResiliencia(tau_validade_max=0.05)
    t_origem = time.perf_counter()
    assert middleware.filtrar_comando("[TESTE]", t_origem) == "[TESTE]"

def test_barramento_roteamento_sucesso():
    bus = MessageBus()
    agente = AgenteMock("IA01")
    
    # Testa se o registro e o envio ocorrem perfeitamente
    bus.registrar(agente)
    resposta = bus.enviar("USER", "IA01", "[CMD:INICIAR]", {"data": 123})
    assert resposta == "Sucesso:[CMD:INICIAR]"

def test_barramento_agente_inexistente():
    bus = MessageBus()
    resposta = bus.enviar("USER", "IA_FANTASMA", "[CMD:AÇÃO]", {})
    assert resposta == "[ERR:DESTINO_NAO_ENCONTRADO]"
