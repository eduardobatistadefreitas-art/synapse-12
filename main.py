# main.py
import sys
import os

# Garante que o interpretador do Python localize a pasta 'src' no celular/nuvem
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from bus.message_bus import MessageBus
from core.kernel import SynapseKernel
from agents.ia01_mediador import AgenteMediador
from agents.ia02_executor import AgenteExecutor
from agents.ia03_critico import AgenteCritico
from agents.ia04_supervisor import AgenteSupervisor
from agents.ia05_auditor import AgenteAuditor

print("🚀 [SYNAPSE 12] INICIANDO SISTEMA DE ORQUESTRAÇÃO MÁGICA")
print("="*60)

# 1. Cria a Infraestrutura do Sistema Nervoso Central
bus = MessageBus()

# 2. Inicializa o Kernel Central passando o Barramento
kernel = SynapseKernel(bus)

print("\n🤖 INSTANCIANDO CLONES DE IA...")
# 3. Instancia todos os 5 agentes operacionais da colmeia
ia01 = AgenteMediador("IA01", "Mediador", bus, user_plan="BASIC")
ia02 = AgenteExecutor("IA02", "Executor", bus)
ia03 = AgenteCritico("IA03", "Critico", bus, user_tier="BASIC")
ia04 = AgenteSupervisor("IA04", "Supervisor", bus)
ia05 = AgenteAuditor("IA05", "Auditor", bus)

print("\n⚙️ CONECTANDO ROBÔS AO BARRAMENTO DE REDE...")
# 4. Registra todos no MessageBus para mapear as rotas
bus.registrar(ia01)
bus.registrar(ia02)
bus.registrar(ia03)
bus.registrar(ia04)
bus.registrar(ia05)

print("\n🎬 ENVIANDO COMANDO ATRAVÉS DO KERNEL...")
print("-"*60)

# 5. O Usuário envia a tarefa inicial atendendo ao checklist
payload_usuario = {
    "tarefa": "Criar script simples de qualificacao de leads imobiliarios.",
    "status": "conclusao e escopo bem definidos para corretores."
}

# O Kernel recebe o input e dispara o pipeline de agentes
resultado_fluxo = kernel.start_pipeline(payload_usuario)

print("-"*60)
print(f"🏁 EXECUÇÃO CONCLUÍDA. RETORNO DO ECOSSISTEMA: {resultado_fluxo}")
print("="*60)
