import os
import json
import sys

# Alinha caminhos modulares para execução limpa
PATH_ATUAL = os.path.dirname(os.path.abspath(__file__))
PATH_SRC = os.path.dirname(PATH_ATUAL)
if PATH_SRC not in sys.path:
    sys.path.append(PATH_SRC)
if PATH_ATUAL not in sys.path:
    sys.path.append(PATH_ATUAL)

from ia02_smart_validator import SmartValidator
from ia05_auditor_feedback import AuditorFeedbackSystem
from ia01_mediador_optimizer import MediadorOptimizer

def executar_teste_estresse_controlado():
    """
    Simula uma sequencia de falhas estruturais para testar o threshold do Optimizer.
    """
    print("🎬 Iniciando Teste de Estresse Controlado do Synapse 24...")
    
    # Inicializa os componentes apontando para a pasta raiz temporaria do teste
    auditor = AuditorFeedbackSystem(pasta_destino=PATH_ATUAL)
    optimizer = MediadorOptimizer(pasta_src=PATH_ATUAL)
    
    # 💥 BRIEFING PROPOSITADAMENTE RUIM (Sem métricas %, sem prazos, sem metas SMART)
    briefing_corrompido = "Preciso de um app simples de vendas para melhorar meus resultados logo."
    
    print("\n[Fase 1] Forçando 3 falhas consecutivas de validação SMART...")
    for i in range(1, 4):
        # Simula a validação e força a gravação da lacuna identificada
        validador = SmartValidator()
        is_smart, lacunas = validador.avaliar_briefing_smart(briefing_corrompido)
        
        # Injeta a falha proposital para acumular no contador do arquivo .json
        auditor.processar_e_salvar_feedback(
            tarefa_solicitada="Simulação de Estresse",
            sucesso_bool=False,
            rodadas_consumidas=1,
            lacunas_lista=lacunas if lacunas else ["Ausencia total de Metricas e Prazos"]
        )
        print(f"   -> Rodada de Falha {i}/3 registrada no JSON.")

    print("\n[Fase 2] Verificando logs adaptativos persistidos em disco...")
    with open(os.path.join(PATH_ATUAL, "config_adaptativa.json"), "r", encoding="utf-8") as f:
        dados_log = json.load(f)
    print(f"   📊 Dados do JSON: {json.dumps(dados_log, indent=2)}")

    print("\n[Fase 3] Acionando o Optimizer para validar a reconfiguração da diretriz...")
    diretriz_final = optimizer.gerar_diretriz_otimizada(threshold_erros=3)
    
    print("\n📋 DIRETRIZ RESULTANTE GERADA PELO MOTOR:")
    print("-" * 60)
    print(diretriz_final)
    print("-" * 60)
    
    if "🚨 ALERTA DO OPTIMIZER:" in diretriz_final:
        print("\n✅ SUCESSO DE HOMOLOGAÇÃO: O ciclo de retroalimentação foi ativado perfeitamente!")
        return True
    else:
        print("\n❌ FALHA DE HOMOLOGAÇÃO: O Optimizer ignorou o limite de erros.")
        return False

if __name__ == "__main__":
    executar_teste_estresse_controlado()
  
