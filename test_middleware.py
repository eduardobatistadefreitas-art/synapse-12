# test_middleware.py
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from core.middleware import MiddlewareResiliencia
from bus.message_bus import MessageBus
from agents.base_agent import BaseAgent
from agents.ia01_mediador import AgenteMediador
from agents.ia03_critico import AgenteCritico

# Ajustando o Mock para herdar de BaseAgent corretamente
class AgenteMockGenerico(BaseAgent):
    def handle_logic(self, tag, payload):
        return f"{self.agent_id}_RECEBEU:{tag}"

def test_middleware_latencia():
    middleware = MiddlewareResiliencia(tau_validade_max=0.05)
    t_origem = time.perf_counter()
    assert middleware.filtrar_comando("[TESTE]", t_origem) == "[TESTE]"

def test_interacao_ia01_bloqueios():
    bus = MessageBus()
    mediador = AgenteMediador("IA01", "Mediador", bus)
    bus.registrar(mediador)
    
    resposta = bus.enviar("USER", "IA01", "[CMD:PROCESSAR]", {"tarefa": "banco de dados complexo"})
    assert "[ERR:ESCOPO_NAO_PERMITIDO]" in resposta

def test_ia03_controle_de_cotas_free():
    bus = MessageBus()
    critico = AgenteCritico("IA03", "Critico", bus, user_tier="FREE")
    ia04 = AgenteMockGenerico("IA04", "Orquestrador", bus)
    
    bus.registrar(critico)
    bus.registrar(ia04)
    
    # Simulamos o envelope real que o barramento envia
    envelope_falso = {"header": {}, "body": "Codigo com bug"}
    resposta = bus.enviar("IA05", "IA03", "[FEEDBACK_IA05_REPROVADO]", envelope_falso)
    
    assert resposta == "IA04_RECEBEU:[STATUS:ESGOTADO]"

def test_ia03_fluxo_aprovado():
    bus = MessageBus()
    critico = AgenteCritico("IA03", "Critico", bus, user_tier="FREE")
    ia04 = AgenteMockGenerico("IA04", "Orquestrador", bus)
    
    bus.registrar(critico)
    bus.registrar(ia04)
    
    envelope_falso = {"header": {}, "body": "Codigo Perfeito"}
    resposta = bus.enviar("IA05", "IA03", "[FEEDBACK_IA05_APROVADO]", envelope_falso)
    
    assert resposta == "IA04_RECEBEU:[STATUS:PRONTO]"
