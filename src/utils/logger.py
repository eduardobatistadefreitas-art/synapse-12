# src/utils/logger.py
import datetime

class SynapseLogger:
    """
    Sistema de diagnóstico e rastreamento de logs do Synapse 12.
    Garante visibilidade das operações e decisões dos agentes.
    """
    def __init__(self):
        pass

    def info(self, mensagem):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"ℹ️ [{timestamp}] [INFO] {mensagem}")

    def erro(self, mensagem):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🚨 [{timestamp}] [ERROR] {mensagem}")

    def alerta(self, mensagem):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"⚠️ [{timestamp}] [WARN] {mensagem}")
      
