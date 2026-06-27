# src/agents/ia02_executor.py
import json
import http.client
from agents.base_agent import BaseAgent

# 🚀 IMPORTAÇÃO DO MANUAL DE QUALIDADE (CÉREBRO INTERNO)
try:
    from agents.ia02_executor_monitor import IA02ExecutorImprovementSystem
except ImportError:
    # Fallback caso o arquivo ainda não tenha sido criado no repositório
    IA02ExecutorImprovementSystem = None

class AgenteExecutor(BaseAgent):
    def __init__(self, agent_id, role, bus):
        super().__init__(agent_id, role, bus)
        # O agente guarda o sistema de autoavaliação na "mochila"
        if IA02ExecutorImprovementSystem:
            self.monitor = IA02ExecutorImprovementSystem(system_id=agent_id)
        else:
            self.monitor = None

    def executar_com_auto_reflexao(self, api_key, briefing):
        """Gera o código e usa o monitor interno para revisar a entrega"""
        prompt_sistema = (
            "Você é o IA02 Executor, programador sênior. Escreva um código Python estruturado "
            "para resolver o briefing enviado. Mande apenas o código dentro de blocos markdown."
        )
        
        # 1. O Operário gera a primeira versão do código
        codigo_v1 = self._chamar_gemini_api(api_key, prompt_sistema, briefing)
        
        # 2. Se o Revisor (Monitor) existir, ele entra em ação antes da entrega final
        if self.monitor:
            # Executa o diagnóstico interno de qualidade
            diagnostico = self.monitor.perform_diagnosis()
            
            # Se o diagnóstico apontar falhas, pede um refinamento ao Gemini
            prompt_correcao = f"Revise e corrija o seguinte código baseado neste diagnóstico: {diagnostico}"
            codigo_refinado = self._chamar_gemini_api(api_key, prompt_correcao, codigo_v1)
            return codigo_refinado
            
        return codigo_v1

    def _chamar_gemini_api(self, api_key, prompt_sistema, prompt_usuario):
        """Chamada REST estável interna do agente (Gemini 2.5 Flash)"""
        try:
            host = "://googleapis.com"
            conn = http.client.HTTPSConnection(host, timeout=60)
            headers = {"Content-Type": "application/json", "Connection": "keep-alive"}
            
            payload = json.dumps({
                "contents": [{
                    "parts": [{"text": f"{prompt_sistema}\n\nEntrada: {prompt_usuario}"}]
                }],
                "generationConfig": {"temperature": 0.2}
            })
            
            url = f"/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
            conn.request("POST", url, payload, headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            conn.close()
            
            if res.status == 200:
                return json.loads(data)["candidates"]["content"]["parts"]["text"]
            return f"[Erro Agent {res.status}]: {data[:100]}"
        except Exception as e:
            return f"[Falha de Conexão Agente]: {e}"
