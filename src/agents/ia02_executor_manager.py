import sys
import os

# Alinha os caminhos modulares
PATH_ATUAL = os.path.dirname(os.path.abspath(__file__))
if PATH_ATUAL not in sys.path:
    sys.path.append(PATH_ATUAL)

from ia02_smart_validator import SmartValidator

def executar_analise_gerencial(briefing_ia01):
    """
    Interface do Executor Sênior que valida e processa o briefing do Mediador.
    """
    validador = SmartValidator()
    is_smart, lacunas = validador.avaliar_briefing_smart(briefing_ia01)
    
    resposta_gerencial = {
        "aprovado_pelo_validador": is_smart,
        "lacunas_identificadas": lacunas,
        "plano_de_acao": "Pronto para avancar para o plano tecnico." if is_smart else "Exigir reajuste ao Mediador."
    }
    
    return resposta_gerencial
    
