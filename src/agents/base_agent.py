# src/agents/base_agent.py
import time
import os
import requests

class BaseAgent:
    """
    Classe base poliglota para todos os agentes do Synapse 12.
    Gerencia comunicação via Barramento e chamadas gratuitas de IA via HTTP nativo.
    """
    def __init__(self, agent_id, role, bus, model=None):
        self.agent_id = agent_id
        self.role = role
        self.bus = bus
        self.memory = []
        self.model = model

    def chamar_ia(self, prompt_sistema, prompt_usuario):
        """
        Método unificado, gratuito e nativo para processar inteligência via Groq.
        Removeu a dependência do pacote 'openai' para evitar quebras de servidor.
        """
        groq_key = os.getenv("GROQ_API_KEY")
        
        if groq_key and ("llama" in str(self.model).lower() or "deepseek" in str(self.model).lower() or "gemma" in str(self.model).lower()):
            try:
                # Chamada direta via API REST da Groq usando a biblioteca padrão requests
                url = "https://groq.com"
                headers = {
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": prompt_usuario}
                    ],
                    "temperature": 0.2
                }
                response = requests.post(url, headers=headers, json=data, timeout=10)
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
                else:
                    return f"[ERR_API_GROQ_STATUS]: {response.status_code} - {response.text}"
            except Exception as e:
                return f"[ERR_API_GROQ_EXCEPTION]: {e}"
                
        return f"[MOCK] Agente {self.agent_id} rodou localmente com o modelo {self.model}"

    def format_envelope(self, receiver_id, tag, payload):
        return {
            "header": {
                "from": self.agent_id,
                "role": self.role,
                "to": receiver_id,
                "tag": tag,
                "timestamp": time.time()
            },
            "body": payload
        }

    def process(self, tag, payload):
        print(f"[{self.agent_id} | {self.role}] Recebi tag: {tag}")
        return self.handle_logic(tag, payload)

    def handle_logic(self, tag, payload):
        raise NotImplementedError("Cada agente deve definir sua própria lógica.")

    def send_to(self, receiver_id, tag, payload):
        envelope = self.format_envelope(receiver_id, tag, payload)
        return self.bus.enviar(self.agent_id, receiver_id, tag, envelope)
        
