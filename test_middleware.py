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
    
    # Envia um comando de projeto para o Executor e valida se ele responde com o código pronto
    envelope_falso = {"header": {}, "body": {"especificacao": "app"}}
    resposta = bus.enviar("IA03", "IA02", "[CMD:EXECUTAR_PROJETO]", envelope_falso)
    
    # O barramento encapsula a resposta final em um dict de resposta do handle_logic do IA03 alvo
    assert "status" in str(resposta)

def test_ia03_itera_com_executor():
    bus = MessageBus()
    critico = AgenteCritico("IA03", "Critico", bus, user_tier="BASIC") # Permite até 3 tentativas
    executor = AgenteExecutor("IA02", "Executor", bus)
    
    bus.registrar(critico)
    bus.registrar(executor)
    
    # Se o IA05 envia uma reprovação, o IA03 deve processar e acionar o Executor para corrigir
    envelope_reprovado = {"header": {}, "body": "Falta tratamento de erro"}
    resposta = bus.enviar("IA05", "IA03", "[FEEDBACK_IA05_REPROVADO]", envelope_reprovado)
    
    # Verifica se a mensagem bateu no executor e gerou o código de retorno esperado
    assert "SUCESSO" in str(resposta)
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
