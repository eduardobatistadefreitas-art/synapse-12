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

class AgenteMockGenerico(BaseAgent):
    def handle_logic(self, tag, payload):
        return f"{self.agent_id}_RECEBEU:{tag}"

def test_middleware_latencia():
    middleware = MiddlewareResiliencia(tau_validade_max=0.05)
    t_origem = time.perf_counter()
    assert middleware.filtrar_comando("[TESTE]", t_origem) == "[TESTE]"

def test_executor_fluxo_codificacao():
    bus = MessageBus()
    executor = AgenteExecutor("IA02", "Executor", bus)
    bus.registrar(executor)
    
    # Criamos um mock de IA03 para registrar no barramento e receber o retorno
    critico_mock = AgenteMockGenerico("IA03", "Critico", bus)
    bus.registrar(critico_mock)
    
    # Envia o comando simulando o envelope padrão
    envelope_falso = {"header": {}, "body": {"especificacao": "app"}}
    resposta = bus.enviar("IA03", "IA02", "[CMD:EXECUTAR_PROJETO]", envelope_falso)
    
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
