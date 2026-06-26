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
from agents.ia02_executor import AgenteExecutor

# Mock genérico para isolar as saídas sem causar chamadas em cascata
class AgenteMockIsolado(BaseAgent):
    def handle_logic(self, tag, payload):
        return f"MOCK_RECEBEU:{tag}"

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

def test_executor_isolado():
    bus = MessageBus()
    executor = AgenteExecutor("IA02", "Executor", bus)
    bus.registrar(executor)
    
    # Registramos um mock para o IA03 para interceptar a saída do Executor sem loop
    ia03_mock = AgenteMockIsolado("IA03", "Critico", bus)
    bus.registrar(ia03_mock)
    
    envelope_falso = {"header": {}, "body": {"especificacao": "app"}}
    resposta = bus.enviar("IA03", "IA02", "[CMD:EXECUTAR_PROJETO]", envelope_falso)
    
    assert resposta == "MOCK_RECEBEU:[DATA:CODIGO_PRONTO]"

def test_ia03_isolado_reprovacao():
    bus = MessageBus()
    critico = AgenteCritico("IA03", "Critico", bus, user_tier="BASIC")
    bus.registrar(critico)
    
    # Registramos um mock para o IA02 para interceptar o reenvio do Critico de forma limpa
    ia02_mock = AgenteMockIsolado("IA02", "Executor", bus)
    bus.registrar(ia02_mock)
    
    envelope_reprovado = {"header": {}, "body": "Falta tratamento de erro"}
    resposta = bus.enviar("IA05", "IA03", "[FEEDBACK_IA05_REPROVADO]", envelope_reprovado)
    
    assert resposta == "MOCK_RECEBEU:[CMD:CORRIGIR_PROJETO]"
    # O executor processa e responde enviando para o IA03_Mock através do barramento
    assert resposta == "IA03_RECEBEU:[DATA:CODIGO_PRONTO]"

def test_ia03_itera_com_executor():
    bus = MessageBus()
    critico = AgenteCritico("IA03", "Critico", bus, user_tier="BASIC")
    executor = AgenteExecutor("IA02", "Executor", bus)
    
    bus.registrar(critico)
    bus.registrar(executor)
    
    # Registra o mock do IA04 para interceptar caso o fluxo saia do circuito
    ia04_mock = AgenteMockGenerico("IA04", "Orquestrador", bus)
    bus.registrar(ia04_mock)
    
    # IA05 envia uma reprovação em formato de envelope válido
    envelope_reprovado = {"header": {}, "body": "Falta tratamento de erro"}
    resposta = bus.enviar("IA05", "IA03", "[FEEDBACK_IA05_REPROVADO]", envelope_reprovado)
    
    # O IA03 pega a reprovação, refina e manda para o IA02. 
    # O IA02 processa a correção e tenta devolver para o IA03. 
    # Como o IA03 não repassa mais adiante na tag DATA:CODIGO_PRONTO (retorna None por padrão),
    # o barramento entrega com sucesso o fim da cadeia de chamadas síncronas.
    assert resposta is not None
