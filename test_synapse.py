# test_synapse.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from bus.message_bus import MessageBus
from agents.ia01_mediador import AgenteMediador

def test_mediador_e_infra():
    bus = MessageBus()
    mediador = AgenteMediador("IA01", "Mediador", bus)
    bus.registrar(mediador)
    resposta = bus.enviar("USER", "IA01", "[CMD:PROCESSAR]", {"tarefa": "banco de dados"})
    assert "[ERR:ESCOPO_NAO_PERMITIDO]" in resposta
  
