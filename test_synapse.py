# test_synapse.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from bus.message_bus import MessageBus
from agents.base_agent import BaseAgent
from agents.ia01_mediador import AgenteMediador
from agents.ia04_supervisor import AgenteSupervisor

class AgenteMockIsolado(BaseAgent):
    def handle_logic(self, tag, payload):
        return f"MOCK_RECEBEU:{tag}"

def test_mediador_e_infra():
    bus = MessageBus()
    mediador = AgenteMediador("IA01", "Mediador", bus)
    bus.registrar(mediador)
    resposta = bus.enviar("USER", "IA01", "[CMD:PROCESSAR]", {"tarefa": "banco de dados"})
    assert "[ERR:ESCOPO_NAO_PERMITIDO]" in resposta

def test_supervisor_maestro_fluxos():
    bus = MessageBus()
    supervisor = AgenteSupervisor("IA04", "Supervisor", bus)
    bus.registrar(supervisor)
    
    # Registra o IA03 mockado para capturar o comando de intervenção do Maestro
    bus.registrar(AgenteMockIsolado("IA03", "Critico", bus))
    
    # 1. Testando finalização com sucesso
    res_sucesso = bus.enviar("IA03", "IA04", "[STATUS:PRONTO]", {"codigo": "ok"})
    assert res_sucesso == "PROJETO_CONCLUIDO_COM_SUCESSO"
    
    # 2. Testando intervenção em tag de erro
    res_falha = bus.enviar("IA02", "IA04", "[ERR:FALHA_CODIFICACAO]", {"motivo": "timeout"})
    assert res_falha == "MOCK_RECEBEU:[CMD:RESET_ESTRATEGIA_FORCADO]"
