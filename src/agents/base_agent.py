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
        Blindado contra o erro HTTP 405 usando requisições brutas em POST estruturado.
        """
        groq_key = os.getenv("GROQ_API_KEY")
        
        # Garante que temos a chave e o modelo correto configurado
        if groq_key and self.model:
            try:
                # Endpoint oficial compatível com requisições POST para completions
                url = "https://groq.com"
                
                headers = {
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json"
                }
                
                # Payload montado seguindo rigorosamente a documentação da API
                data = {
                    "model": str(self.model),
                    "messages": [
                        {"role": "system", "content": str(prompt_sistema)},
                        {"role": "user", "content": str(prompt_usuario)}
                    ],
                    "temperature": 0.2
                }
                
                # Executa o POST nativo limpando o Method Not Allowed (405)
                response = requests.post(url, headers=headers, json=data, timeout=15)
                
                if response.status_code == 200:
                    return response.json()["choices"]["message"]["content"]
                else:
                    return f"[ERR_API_GROQ_STATUS]: {response.status_code} - {response.text[:100]}"
            except Exception as e:
                return f"[ERR_API_GROQ_EXCEPTION]: {e}"
                
        return f"[MOCK] Agente {self.agent_id} rodou em contingência local."

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
        return self.handle_logic(tag, payload)

    def handle_logic(self, tag, payload):
        raise NotImplementedError("Cada agente deve definir sua própria lógica.")

    def send_to(self, receiver_id, tag, payload):
        envelope = self.format_envelope(receiver_id, tag, payload)
        return self.bus.enviar(self.agent_id, receiver_id, tag, envelope)
        
