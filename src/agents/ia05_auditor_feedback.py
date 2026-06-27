import json
import os

class AuditorFeedbackSystem:
    """
    Agente IA05 de Aprendizado Continuo. Transforma feedback do usuario
    e logs de processamento em configuracoes persistentes em disco (.json).
    """
    def __init__(self, pasta_destino=None):
        # Define a pasta de configuracoes dinâmicas do ecossistema
        if pasta_destino is None:
            self.caminho_config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config_adaptativa.json")
        else:
            self.caminho_config = os.path.join(pasta_destino, "config_adaptativa.json")

    def processar_e_salvar_feedback(self, tarefa_solicitada, sucesso_bool, rodadas_consumidas, logs_erro=""):
        """
        Gera ou atualiza o arquivo de aprendizado com base na execucao da colmeia.
        """
        dados_aprendizado = {
            "ultima_tarefa": tarefa_solicitada,
            "status_sucesso": sucesso_bool,
            "rodadas_no_loop": rodadas_consumidas,
            "erros_de_infraestrutura": logs_erro if logs_erro else "Nenhum",
            "diretriz_ajustada": "MANTER_CADENCIA"
        }

        # Engenharia adaptativa: se gastou muitas rodadas, força o sistema a ser mais rígido no proximo boot
        if rodadas_consumidas >= 2 or not sucesso_bool:
            dados_aprendizado["diretriz_ajustada"] = "FORCAR_METRICAS_ESTRITAS_SMART"

        try:
            with open(self.caminho_config, "w", encoding="utf-8") as f:
                json.dump(dados_aprendizado, f, indent=4, ensure_ascii=False)
            return True, f"Configuracao adaptativa salva com sucesso em: {self.caminho_config}"
        except Exception as e:
            return False, f"Falha ao persistir aprendizado em disco: {str(e)}"

    def carregar_aprendizado_atual(self):
        """
        Le a configuracao salva para reinjetar o aprendizado passado no prompt do IA01.
        """
        if os.path.exists(self.caminho_config):
            try:
                with open(self.caminho_config, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
      
