import json
import os

class AuditorFeedbackSystem:
    """
    Agente IA05 de Aprendizado Continuo. 
    Contabiliza erros acumulados para o gatilho do Optimizer.
    """
    def __init__(self, pasta_destino):
        self.caminho_config = os.path.join(pasta_destino, "config_adaptativa.json")

    def processar_e_salvar_feedback(self, tarefa_solicitada, sucesso_bool, rodadas_consumidas, lacunas_lista=None):
        """
        Atualiza o contador de erros seguidos no JSON.
        """
        erros_acumulados = 0
        ultima_lacuna = ""
        
        # Se houver lacunas SMART pendentes, extrai a primeira para o log
        if lacunas_lista and len(lacunas_lista) > 0:
            ultima_lacuna = lacunas_lista[0]

        # Tenta ler o historico existente para nao zerar o contador anterior
        if os.path.exists(self.caminho_config):
            try:
                with open(self.caminho_config, "r", encoding="utf-8") as f:
                    antigo = json.load(f)
                    erros_acumulados = antigo.get("erros_acumulados_requisito", 0)
            except Exception:
                pass

        # Logica do contador de Threshold
        if not sucesso_bool or (lacunas_lista and len(lacunas_lista) > 0):
            erros_acumulados += 1
        else:
            erros_acumulados = 0 # Reseta se houve sucesso absoluto

        dados_aprendizado = {
            "ultima_tarefa": tarefa_solicitada,
            "status_sucesso": sucesso_bool and (erros_acumulados == 0),
            "rodadas_no_loop": rodadas_consumidas,
            "erros_acumulados_requisito": erros_acumulados,
            "ultima_lacuna_identificada": ultima_lacuna,
            "diretriz_ajustada": "FORCAR_METRICAS_ESTRITAS_SMART" if erros_acumulados > 0 else "MANTER_CADENCIA"
        }

        try:
            with open(self.caminho_config, "w", encoding="utf-8") as f:
                json.dump(dados_aprendizado, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def carregar_aprendizado_atual(self):
        if os.path.exists(self.caminho_config):
            try:
                with open(self.caminho_config, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
        
