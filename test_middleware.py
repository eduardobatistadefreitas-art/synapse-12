# test_middleware.py
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from core.middleware import MiddlewareResiliencia
from bus.message_bus import MessageBus
from utils.logger import SynapseLogger
from agents.ia01_mediador import AgenteMediador

# Criamos um IA02 Simulado (Mock) para interceptar o envio do IA01
class AgenteExecutorMock:
    def __init__(self, agent_id):
        self.agent_id = agent_id
    def handle_logic(self, tag, payload):
        return f"EXECUTOR_RECEBEU:{tag}"

def test_mediador_bloqueio_plano_basic():
    bus = MessageBus()
    mediador = AgenteMediador("IA01", "Mediador", bus, user_plan="BASIC")
    bus.registrar(mediador)
    
    # Testa se o mediador barra termos complexos no plano BASIC
    payload_complexo = {"tarefa": "Configurar um banco de dados relacional"}
    resposta = bus.enviar("USER", "IA01", "[CMD:PROCESSAR]", payload_complexo)
    assert "[ERR:ESCOPO_NAO_PERMITIDO]" in resposta

def test_mediador_checklist_incompleto():
    bus = MessageBus()
    mediador = AgenteMediador("IA01", "Mediador", bus, user_plan="BASIC")
    bus.registrar(mediador)
    
    # Payload sem a palavra 'conclusao' deve pedir mais dados
    payload_incompleto = {"tarefa": "Criar um script simples"}
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
