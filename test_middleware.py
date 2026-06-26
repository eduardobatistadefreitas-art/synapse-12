# test_middleware.py
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from core.middleware import MiddlewareResiliencia
from bus.message_bus import MessageBus
from agents.ia01_mediador import AgenteMediador
from agents.ia03_critico import AgenteCritico

# Mocks para simular os agentes que ainda não subimos para o GitHub
class AgenteMockGenerico:
    def __init__(self, agent_id): self.agent_id = agent_id
    def handle_logic(self, tag, payload): return f"{self.agent_id}_RECEBEU:{tag}"

def test_interacao_ia01_bloqueios():
    bus = MessageBus()
    mediador = AgenteMediador("IA01", "Mediador", bus)
    bus.registrar(mediador)
    
    resposta = bus.enviar("USER", "IA01", "[CMD:PROCESSAR]", {"tarefa": "banco de dados complexo"})
    assert "[ERR:ESCOPO_NAO_PERMITIDO]" in resposta

def test_ia03_controle_de_cotas_free():
    bus = MessageBus()
    critico = AgenteCritico("IA03", "Critico", bus, user_tier="FREE")
    ia04 = AgenteMockGenerico("IA04")
    
    bus.registrar(critico)
    bus.registrar(ia04)
    
    # 1. Primeira reprovação: Como o tier é FREE (limite=1), deve esgotar imediatamente
    # Simulamos o envelope que o barramento enviaria
    envelope_falso = {"header": {}, "body": "Código com bug"}
    resposta = bus.enviar("IA05", "IA03", "[FEEDBACK_IA05_REPROVADO]", envelope_falso)
    
    # Garante que o IA03 barrou e encaminhou para o IA04 com a tag correta
    assert resposta == "IA04_RECEBEU:[STATUS:ESGOTADO]"

def test_ia03_fluxo_aprovado():
    bus = MessageBus()
    critico = AgenteCritico("IA03", "Critico", bus, user_tier="FREE")
    ia04 = AgenteMockGenerico("IA04")
    
    bus.registrar(critico)
    bus.registrar(ia04)
    
    envelope_falso = {"header": {}, "body": "Código Perfeito"}
    resposta = bus.enviar("IA05", "IA03", "[FEEDBACK_IA05_APROVADO]", envelope_falso)
    
    assert resposta == "IA04_RECEBEU:[STATUS:PRONTO]"
    resposta = bus.enviar("USER", "IA01", "[CMD:PROCESSAR]", payload_incompleto)
    assert "[IA01] Por favor" in resposta

def test_mediador_fluxo_sucesso_envio_executor():
    bus = MessageBus()
    mediador = AgenteMediador("IA01", "Mediador", bus, user_plan="BASIC")
    executor = AgenteExecutorMock("IA02")
    
    bus.registrar(mediador)
    bus.registrar(executor)
    
    # Payload válido com a palavra chave que ativa o checklist
    payload_valido = {"tarefa": "Script simples de automacao", "status": "conclusao definida"}
    resposta = bus.enviar("USER", "IA01", "[CMD:PROCESSAR]", payload_valido)
    
    # Garante que a mensagem passou pelo barramento e bateu no Executor fictício
    assert resposta == "EXECUTOR_RECEBEU:[CMD:INICIAR_ESQUELETO]"
