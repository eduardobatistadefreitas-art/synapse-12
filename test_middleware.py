# test_middleware.py
import time
import sys
import os

# Ajusta o caminho para o Python encontrar a pasta src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from core.middleware import MiddlewareResiliencia

def test_middleware_sucesso():
    middleware = MiddlewareResiliencia(tau_validade_max=0.05)
    # Simula um comando instantâneo (sem latência)
    t_origem = time.perf_counter()
    resultado = middleware.filtrar_comando("[CMD:TESTE]", t_origem)
    assert resultado == "[CMD:TESTE]"

def test_middleware_descarte_por_latencia():
    middleware = MiddlewareResiliencia(tau_validade_max=0.05)
    # Simula um comando enviado há 1 segundo atrás (alta latência)
    t_origem = time.perf_counter() - 1.0
    resultado = middleware.filtrar_comando("[CMD:TESTE]", t_origem)
    assert resultado is None
  
