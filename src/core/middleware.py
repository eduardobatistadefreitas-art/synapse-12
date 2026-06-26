# src/core/middleware.py
import time

class MiddlewareResiliencia:
    """
    Middleware de Segurança para Agentes Autônomos.
    Filtra latência e ajusta a carga de trabalho.
    """
    def __init__(self, tau_validade_max=0.05, limite_supressao_critico=0.4):
        self.tau_max = tau_validade_max
        self.limite_critico = limite_supressao_critico
        self.supressoes = 0
        self.total_comandos = 0

    def filtrar_comando(self, comando, t_origem):
        latencia = time.perf_counter() - t_origem
        self.total_comandos += 1
        
        if latencia >= self.tau_max:
            self.supressoes += 1
            return None 
        return comando 

    def obter_comando_de_throttle(self):
        taxa = self.supressoes / max(1, self.total_comandos)
        if taxa > self.limite_critico:
            return 0.05 
        return 1.0 - taxa
      
