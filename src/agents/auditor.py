import os
import json
from agents.base import BaseAgent

class AuditorAgent(BaseAgent):
    def __init__(self):
        super().__init__("IA05_Auditor", "Auditor de Qualidade SMART")
        self.caminho_config = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config_adaptativa.json")

    def executar(self, payload):
        briefing = payload.get("briefing", "")
        sucesso = payload.get("sucesso", True)
        
        texto_limpo = briefing.lower()
        lacunas = []
        
        if "%" not in texto_limpo and "taxa" not in texto_limpo:
            lacunas.append("Falta de Métricas quantificáveis (%)")
        if "meses" not in texto_limpo and "fase" not in texto_limpo:
            lacunas.append("Ausência de Cronograma ou Prazos")
            
        is_smart = len(lacunas) == 0 or "CONTINGÊNCIA" in briefing
        
        # Persistência adaptativa do histórico
        erros_acumulados = 0
        if os.path.exists(self.caminho_config):
            try:
                with open(self.caminho_config, "r", encoding="utf-8") as f:
                    erros_acumulados = json.load(f).get("erros_acumulados", 0)
            except Exception: pass
            
        erros_acumulados = (erros_acumulados + 1) if not is_smart else 0
        
        dados_log = {
            "erros_acumulados": erros_acumulados,
            "ultima_lacuna": lacunas[0] if lacunas else "Nenhuma",
            "diretriz_ajustada": "FORCAR_METRICAS_ESTRITAS_SMART" if erros_acumulados > 0 else "NORMAL"
        }
        
        try:
            with open(self.caminho_config, "w", encoding="utf-8") as f:
                json.dump(dados_log, f, indent=4)
        except Exception: pass

        return {"is_smart": is_smart, "lacunas": lacunas, "erros_acumulados": erros_acumulados, "dados_log": dados_log}
      
