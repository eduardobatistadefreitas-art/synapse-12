# test_middleware.py
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from bus.message_bus import MessageBus
from agents.base_agent import BaseAgent
from agents.ia01_mediador import AgenteMediador
from agents.ia03_critico import AgenteCritico
from agents.ia02_executor import AgenteExecutor
from agents.ia05_auditor import AgenteAuditor

class AgenteMockIsolado(BaseAgent):
    def handle_logic(self, tag, payload):
        return f"MOCK_RECEBEU:{tag}"

def test_infraestrutura_e_mediador():
    bus = MessageBus()
    mediador = AgenteMediador("IA01", "Mediador", bus)
    bus.registrar(mediador)
    resposta = bus.enviar("USER", "IA01", "[CMD:PROCESSAR]", {"tarefa": "banco de dados complexo"})
    assert "[ERR:ESCOPO_NAO_PERMITIDO]" in resposta

def test_executor_e_critico():
    bus = MessageBus()
    executor = AgenteExecutor("IA02", "Executor", bus)
    critico = AgenteCritico("IA03", "Critico", bus, user_tier="BASIC")
    bus.registrar(executor)
    bus.registrar(critico)
    
    # Registra mocks para as pontas soltas
    bus.registrar(AgenteMockIsolado("IA04", "Orquestrador", bus))
    
    envelope_reprovado = {"header": {}, "body": "Falta tratamento de erro"}
    resposta = bus.enviar("IA05", "IA03", "[FEEDBACK_IA05_REPROVADO]", envelope_reprovado)
    assert resposta is not None

def test_auditor_fluxos():
    bus = MessageBus()
    auditor = AgenteAuditor("IA05", "Auditor", bus)
    bus.registrar(auditor)
    bus.registrar(AgenteMockIsolado("IA03", "Critico", bus))
    bus.registrar(AgenteMockIsolado("IA04", "Orquestrador", bus))
    
    envelope_v1 = {"header": {}, "body": {"versao": "1.0", "codigo": "print(1)"}}
    resposta_v1 = bus.enviar("IA02", "IA05", "[CMD:VALIDAR_ENTREGA]", envelope_v1)
    assert resposta_v1 == "MOCK_RECEBEU:[FEEDBACK_IA05_ANALISE_INICIAL]"
    
    ia03_mock = AgenteMockIsolado("IA03", "Critico", bus)
    bus.registrar(ia03_mock)
    
    envelope_falso = {"header": {}, "body": {"especificacao": "app"}}
    resposta = bus.enviar("IA03", "IA02", "[CMD:EXECUTAR_PROJETO]", envelope_falso)
    
    assert resposta == "MOCK_RECEBEU:[DATA:CODIGO_PRONTO]"

def test_ia03_isolado_reprovacao():
    bus = MessageBus()
    critico = AgenteCritico("IA03", "Critico", bus, user_tier="BASIC")
    bus.registrar(critico)
    
    ia02_mock = AgenteMockIsolado("IA02", "Executor", bus)
    bus.registrar(ia02_mock)
    
    envelope_reprovado = {"header": {}, "body": "Falta tratamento de erro"}
    resposta = bus.enviar("IA05", "IA03", "[FEEDBACK_IA05_REPROVADO]", envelope_reprovado)
    
    assert resposta == "MOCK_RECEBEU:[CMD:CORRIGIR_PROJETO]"

def test_auditor_analise_inicial_e_aprovacao():
    bus = MessageBus()
    auditor = AgenteAuditor("IA05", "Auditor", bus)
    bus.registrar(auditor)
    
    ia03_mock = AgenteMockIsolado("IA03", "Critico", bus)
    ia04_mock = AgenteMockIsolado("IA04", "Orquestrador", bus)
    bus.registrar(ia03_mock)
    bus.registrar(ia04_mock)
    
    # 1. Primeira entrega (Historico vazio): Deve ir para o IA03
    envelope_v1 = {"header": {}, "body": {"versao": "1.0", "codigo": "print(1)"}}
    resposta_v1 = bus.enviar("IA02", "IA05", "[CMD:VALIDAR_ENTREGA]", envelope_v1)
    assert resposta_v1 == "MOCK_RECEBEU:[FEEDBACK_IA05_ANALISE_INICIAL]"
    
    # 2. Segunda entrega (Historico preenchido): Deve ir para o IA04
    envelope_v2 = {"header": {}, "body": {"versao": "1.1", "codigo": "print(1)"}}
    resposta_v2 = bus.enviar("IA02", "IA05", "[CMD:VALIDAR_ENTREGA]", envelope_v2)
    assert resposta_v2 == "MOCK_RECEBEU:[FEEDBACK_IA05_APROVADO]"
    
    ia03_mock = AgenteMockIsolado("IA03", "Critico", bus)
    bus.registrar(ia03_mock)
    
    envelope_falso = {"header": {}, "body": {"especificacao": "app"}}
    resposta = bus.enviar("IA03", "IA02", "[CMD:EXECUTAR_PROJETO]", envelope_falso)
    
    assert resposta == "MOCK_RECEBEU:[DATA:CODIGO_PRONTO]"

def test_ia03_isolado_reprovacao():
    bus = MessageBus()
    critico = AgenteCritico("IA03", "Critico", bus, user_tier="BASIC")
    bus.registrar(critico)
    
    ia02_mock = AgenteMockIsolado("IA02", "Executor", bus)
    bus.registrar(ia02_mock)
    
    envelope_reprovado = {"header": {}, "body": "Falta tratamento de erro"}
    resposta = bus.enviar("IA05", "IA03", "[FEEDBACK_IA05_REPROVADO]", envelope_reprovado)
    
    assert resposta == "MOCK_RECEBEU:[CMD:CORRIGIR_PROJETO]"

def test_auditor_analise_inicial_e_aprovacao():
    bus = MessageBus()
    auditor = AgenteAuditor("IA05", "Auditor", bus)
    bus.registrar(auditor)
    
    ia03_mock = AgenteMockIsolado("IA03", "Critico", bus)
    ia04_mock = AgenteMockIsolado("IA04", "Orquestrador", bus)
    bus.registrar(ia03_mock)
    bus.registrar(ia04_mock)
    
    # 1. Primeira entrega: Deve ir para o IA03
    envelope_v1 = {"header": {}, "body": {"versao": "1.0", "codigo": "print(1)"}}
    resposta_v1 = bus.enviar("IA02", "IA05", "[CMD:VALIDAR_ENTREGA]", envelope_v1)
    assert resposta_v1 == "MOCK_RECEBEU:[FEEDBACK_IA05_ANALISE_INICIAL]"
    
    # 2. Segunda entrega: Deve ir para o IA04
    envelope_v2 = {"header": {}, "body": {"versao": "1.1", "codigo": "print(1)"}}
    resposta_v2 = bus.enviar("IA02", "IA05", "[CMD:VALIDAR_ENTREGA]", envelope_v2)
    assert resposta_v2 == "MOCK_RECEBEU:[FEEDBACK_IA05_APROVADO]"
    
    ia03_mock = AgenteMockIsolado("IA03", "Critico", bus)
    bus.registrar(ia03_mock)
    
    envelope_falso = {"header": {}, "body": {"especificacao": "app"}}
    resposta = bus.enviar("IA03", "IA02", "[CMD:EXECUTAR_PROJETO]", envelope_falso)
    
    assert resposta == "MOCK_RECEBEU:[DATA:CODIGO_PRONTO]"

def test_ia03_isolado_reprovacao():
    bus = MessageBus()
    critico = AgenteCritico("IA03", "Critico", bus, user_tier="BASIC")
    bus.registrar(critico)
    
    ia02_mock = AgenteMockIsolado("IA02", "Executor", bus)
    bus.registrar(ia02_mock)
    
    envelope_reprovado = {"header": {}, "body": "Falta tratamento de erro"}
    resposta = bus.enviar("IA05", "IA03", "[FEEDBACK_IA05_REPROVADO]", envelope_reprovado)
    
    assert resposta == "MOCK_RECEBEU:[CMD:CORRIGIR_PROJETO]"

def test_auditor_analise_inicial_e_aprovacao():
    bus = MessageBus()
    auditor = AgenteAuditor("IA05", "Auditor", bus)
    bus.registrar(auditor)
    
    # Mocks para as saídas do Auditor
    ia03_mock = AgenteMockIsolado("IA03", "Critico", bus)
    ia04_mock = AgenteMockIsolado("IA04", "Orquestrador", bus)
    bus.registrar(ia03_mock)
    bus.registrar(ia04_mock)
    
    # 1. Primeira entrega (Histórico vazio): Deve disparar análise inicial para o IA03
    envelope_v1 = {"header": {}, "body": {"versao": "1.0", "codigo": "print(1)"}}
    resposta_v1 = bus.enviar("IA02", "IA05", "[CMD:VALIDAR_ENTREGA]", envelope_v1)
    assert resposta_v1 == "MOCK_RECEBEU:[FEEDBACK_IA05_ANALISE_INICIAL]"
    
    # 2. Segunda entrega (Sem falhas simuladas): Deve disparar aprovação para o IA04
    envelope_v2 = {"header": {}, "body": {"versao": "1.1", "codigo": "print(1)"}}
    resposta_v2 = bus.enviar("IA02", "IA05", "[CMD:VALIDAR_ENTREGA]", envelope_v2)
    assert resposta_v2 == "MOCK_RECEBEU:[FEEDBACK_IA05_APROVADO]"
    
    ia03_mock = AgenteMockIsolado("IA03", "Critico", bus)
    bus.registrar(ia03_mock)
    
    envelope_falso = {"header": {}, "body": {"especificacao": "app"}}
    resposta = bus.enviar("IA03", "IA02", "[CMD:EXECUTAR_PROJETO]", envelope_falso)
    
    assert resposta == "MOCK_RECEBEU:[DATA:CODIGO_PRONTO]"

def test_ia03_isolado_reprovacao():
    bus = MessageBus()
    critico = AgenteCritico("IA03", "Critico", bus, user_tier="BASIC")
    bus.registrar(critico)
    
    ia02_mock = AgenteMockIsolado("IA02", "Executor", bus)
    bus.registrar(ia02_mock)
    
    envelope_reprovado = {"header": {}, "body": "Falta tratamento de erro"}
    resposta = bus.enviar("IA05", "IA03", "[FEEDBACK_IA05_REPROVADO]", envelope_reprovado)
    
    assert resposta == "MOCK_RECEBEU:[CMD:CORRIGIR_PROJETO]"
