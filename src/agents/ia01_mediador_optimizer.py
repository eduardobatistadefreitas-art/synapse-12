import json
import os

class MediadorOptimizer:
    """
    Agente tradutor que analisa o historico adaptativo e reescreve
    as diretrizes do IA01 Mediador de forma automatica.
    """
    def __init__(self, pasta_src):
        self.pasta_src = pasta_src
        self.caminho_config = os.path.join(pasta_src, "config_adaptativa.json")

    def gerar_diretriz_otimizada(self, threshold_erros=3):
        """
        Le os erros acumulados e monta um prompt cirurgico de correcao para o IA01.
        """
        diretriz_base = "Voce e o IA01 Mediador. Escreva um briefing tecnico contendo Objetivo, Requisitos e Cronograma."
        
        if not os.path.exists(self.caminho_config):
            return diretriz_base

        try:
            with open(self.caminho_config, "r", encoding="utf-8") as f:
                dados = json.load(f)
            
            # Recupere o contador acumulado do historico
            erros_seguidos = dados.get("erros_acumulados_requisito", 0)
            ultima_lacuna = dados.get("ultima_lacuna_identificada", "")

            # Se atingir o limite (Threshold) de 3 erros seguidos, endurece a regra
            if erros_seguidos >= threshold_erros:
                diretriz_reforcada = (
                    f"{diretriz_base}\n"
                    f"🚨 ALERTA DO OPTIMIZER: O validador rejeitou as ultimas {erros_seguidos} tentativas "
                    f"por falhas em: '{ultima_lacuna}'. "
                    f"ESTA PROIBIDO entregar o texto sem especificar metricas quantificaveis com '%' "
                    f"e prazos em meses para todas as fases descritas!"
                )
                return diretriz_reforcada
                
        except Exception:
            return diretriz_base
            
        return diretriz_base
