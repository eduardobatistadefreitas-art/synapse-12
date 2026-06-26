# test_middleware.py
import time
import sys
import os

# Ajusta o caminho para o Python encontrar a pasta src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from core.middleware import MiddlewareResiliencia
from bus.message_bus import MessageBus
from utils.logger import SynapseLogger
from agents.base_agent import BaseAgent

# Agente de testes real herdando da classe BaseAgent oficial
class AgenteTesteReal(BaseAgent):
    def handle_logic(self, tag, payload):
        if tag == "[CMD:TESTAR_ENVELOPE]":
            return "ENVELOPE_OK"
        return "READY"

def test_middleware_latencia():
    middleware = MiddlewareResiliencia(tau_validade_max=0.05)
    t_origem = time.perf_counter()
    assert middleware.filtrar_comando("[TESTE]", t_origem) == "[TESTE]"

def test_barramento_roteamento_sucesso():
    bus = MessageBus()
    agente = AgenteTesteReal("IA01", "Mediador", bus)
    bus.registrar(agente)
    resposta = bus.enviar("USER", "IA01", "[CMD:TESTAR_ENVELOPE]", {"data": 123})
    assert resposta == "ENVELOPE_OK"

def test_barramento_agente_inexistente():
    bus = MessageBus()
    resposta = bus.enviar("USER", "IA_FANTASMA", "[CMD:AÇÃO]", {})
    assert resposta == "[ERR:DESTINO_NAO_ENCONTRADO]"

def test_logger_funcionamento(capsys):
    logger = SynapseLogger()
    logger.info("Teste de log do sistema")
    captured = capsys.readouterr()
    assert "[INFO] Teste de log do sistema" in captured.out

def test_base_agent_e_envelopamento():
    bus = MessageBus()
    agente = AgenteTesteReal("IA05", "Contestador", bus)
    envelope = agente.format_envelope("IA01", "[TAG:TESTE]", {"data": 1})
    assert envelope["header"]["from"] == "IA05"
    assert envelope["header"]["role"] == "Contestador"
    assert envelope["body"]["data"] == 1
    assert envelope["body"]["data"] == 1

def test_logger_funcionamento(capsys):
    logger = SynapseLogger()
    logger.info("Teste de log do sistema")
    
    # Captura o print na tela para checar se o Logger funcionou
    captured = capsys.readouterr()
    assert "[INFO] Teste de log do sistema" in captured.out
