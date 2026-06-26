import os
os.system("pip install openai")
# src/agents/base_agent.py
import time
import os
from openai import OpenAI

class BaseAgent:
    """
    Classe base poliglota para todos os agentes do Synapse 12.
    Gerencia comunicação via Barramento e chamadas gratuitas de IA.
    """
    def __init__(self, agent_id, role, bus, model=None):
        self.agent_id = agent_id
        self.role = role
        self.bus = bus
        self.memory = []
        
        # Define a IA padrão de cada agente baseada no planejamento gratuito
        self.model = model
        
        # Inicializa os clientes de API apenas se as chaves existirem no ambiente
        self.groq_client = None
        self.gemini_client = None
        
        groq_key = os.getenv("GROQ_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")
        
        if groq_key:
            # Groq usa o SDK da OpenAI apontando para a URL deles
            self.groq_client = OpenAI(base_url="https://groq.com", api_key=groq_key)
        if gemini_key:
            # Para o Gemini, usaremos requisição direta ou biblioteca oficial
            # Deixamos o cliente preparado
            self.gemini_client = gemini_key

    def chamar_ia(self, prompt_sistema, prompt_usuario):
        """
        Método unificado e gratuito para os agentes processarem inteligência real.
        """
        # Se for um modelo da Groq (Llama ou DeepSeek)
        if self.groq_client and ("llama" in str(self.model).lower() or "deepseek" in str(self.model).lower()):
            try:
                response = self.groq_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": prompt_usuario}
                    ],
                    temperature=0.2
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"[ERR_API_GROQ]: {e}"
                
        # Fallback caso as chaves não estejam configuradas (modo simulação inteligente)
        return f"[MOCK_INTELLIGENCE] Agente {self.agent_id} processou com modelo {self.model}"

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
        
