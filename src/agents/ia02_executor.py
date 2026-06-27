```python
import datetime
from typing import List, Dict, Any, Optional

class SMARTObjective:
    """
    Representa um objetivo SMART (Specific, Measurable, Achievable, Relevant, Time-bound).
    """
    def __init__(self,
                 specific: str,
                 measurable: str,
                 achievable: str,
                 relevant: str,
                 time_bound: datetime.date):
        self.specific = specific
        self.measurable = measurable
        self.achievable = achievable
        self.relevant = relevant
        self.time_bound = time_bound

    def __str__(self) -> str:
        return (f"Objetivo SMART:\n"
                f"  Específico: {self.specific}\n"
                f"  Mensurável: {self.measurable}\n"
                f"  Atingível: {self.achievable}\n"
                f"  Relevante: {self.relevant}\n"
                f"  Prazo: {self.time_bound.strftime('%Y-%m-%d')}")

class PerformanceEvaluator:
    """
    Realiza a avaliação de desempenho e extrai lições aprendidas.
    """
    def __init__(self, project_name: str):
        self.project_name = project_name

    def evaluate_performance(self, iteration_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa criticamente a performance atual e lições aprendidas da iteração anterior.

        Args:
            iteration_data (Dict[str, Any]): Dados de desempenho da iteração anterior.
                                             Ex: {'latency_ms': 250, 'error_rate_percent': 1.2,
                                                  'user_satisfaction_score': 3.5, 'features_completed': 80}

        Returns:
            Dict[str, Any]: Um dicionário contendo a análise e as lições aprendidas.
        """
        print(f"\n--- Avaliação de Desempenho para {self.project_name} (Iteração 1) ---")
        analysis = {
            "overview": f"Análise da Iteração 1 para o projeto '{self.project_name}'.",
            "metrics_summary": iteration_data
        }
        lessons_learned = []

        # Exemplo de lógica de análise crítica
        if iteration_data.get('latency_ms', 0) > 200:
            analysis['latency_status'] = "Latência acima do limite aceitável."
            lessons_learned.append("Identificar gargalos de performance e otimizar consultas/algoritmos.")
        else:
            analysis['latency_status'] = "Latência dentro do esperado."

        if iteration_data.get('error_rate_percent', 0) > 1.0:
            analysis['error_rate_status'] = "Taxa de erro elevada."
            lessons_learned.append("Revisar testes de unidade/integração e implementar mais validações de entrada.")
        else:
            analysis['error_rate_status'] = "Taxa de erro aceitável."

        if iteration_data.get('user_satisfaction_score', 0) < 4.0:
            analysis['user_satisfaction_status'] = "Satisfação do usuário abaixo do ideal."
            lessons_learned.append("Coletar feedback detalhado dos usuários e priorizar melhorias de UX.")
        else:
            analysis['user_satisfaction_status'] = "Satisfação do usuário boa."

        if iteration_data.get('features_completed', 0) < 90:
            analysis['features_completion_status'] = "Conclusão de features abaixo do planejado."
            lessons_learned.append("Melhorar estimativas e gerenciar escopo de forma mais eficaz.")
        else:
            analysis['features_completion_status'] = "Conclusão de features satisfatória."

        analysis['critical_points'] = [status for key, status in analysis.items() if 'status' in key and 'aceitável' not in status and 'esperado' not in status and 'boa' not in status and 'satisfatória' not in status]

        print("Análise Concluída.")
        print("Lições Aprendidas:")
        for lesson in lessons_learned:
            print(f"- {lesson}")

        return {
            "analysis": analysis,
            "lessons_learned": lessons_learned
        }

class ActionStep:
    """
    Representa uma etapa individual dentro do plano de ação.
    """
    def __init__(self,
                 description: str,
                 resources_needed: List[str],
                 success_metrics: List[str],
                 status: str = "Pendente"):
        self.description = description
        self.resources_needed = resources_needed
        self.success_metrics = success_metrics
        self.status = status # Ex: "Pendente", "Em Andamento", "Concluído", "Bloqueado"

    def __str__(self) -> str:
        return (f"  - Etapa: {self.description}\n"
                f"    Recursos: {', '.join(self.resources_needed)}\n"
                f"    Métricas de Sucesso: {', '.join(self.success_metrics)}\n"
                f"    Status: {self.status}")

class IterativeActionPlan:
    """
    Desenvolve um roteiro detalhado com etapas, recursos e métricas de sucesso
    para a implementação da melhoria.
    """
    def __init__(self, iteration_number: int, plan_name: str):
        self.iteration_number = iteration_number
        self.plan_name = plan_name
        self.objectives: List[SMARTObjective] = []
        self.steps: List[ActionStep] = []

    def add_objective(self, objective: SMARTObjective):
        """Adiciona um objetivo SMART ao plano."""
        self.objectives.append(objective)
        print(f"Objetivo adicionado ao Plano de Ação {self.plan_name}.")

    def add_step(self, step: ActionStep):
        """Adiciona uma etapa ao plano de ação."""
        self.steps.append(step)
        print(f"Etapa '{step.description}' adicionada ao Plano de Ação {self.plan_name}.")

    def update_step_status(self, step_description: str, new_status: str) -> bool:
        """Atualiza o status de uma etapa específica."""
        for step in self.steps:
            if step.description == step_description:
                step.status = new_status
                print(f"Status da etapa '{step_description}' atualizado para '{new_status}'.")
                return True
        print(f"Erro: Etapa '{step_description}' não encontrada no plano.")
        return False

    def generate_plan_report(self) -> Dict[str, Any]:
        """Gera um relatório detalhado do plano de ação."""
        report = {
            "plan_name": self.plan_name,
            "iteration_number": self.iteration_number,
            "objectives": [obj.__dict__ for obj in self.objectives],
            "steps": [step.__dict__ for step in self.steps],
            "summary": {
                "total_steps": len(self.steps),
                "steps_pending": sum(1 for s in self.steps if s.status == "Pendente"),
                "steps_in_progress": sum(1 for s in self.steps if s.status == "Em Andamento"),
                "steps_completed": sum(1 for s in self.steps if s.status == "Concluído"),
                "steps_blocked": sum(1 for s in self.steps if s.status == "Bloqueado"),
            }
        }
        return report

    def print_plan_details(self):
        """Imprime os detalhes do plano de ação de forma legível."""
        print(f"\n--- Plano de Ação Iterativo (Melhoria {self.iteration_number}): {self.plan_name} ---")
        print("\nObjetivos SMART:")
        if not self.objectives:
            print("  Nenhum objetivo definido.")
        for obj in self.objectives:
            print(obj)

        print("\nEtapas do Plano de Ação:")
        if not self.steps:
            print("  Nenhuma etapa definida.")
        for step in self.steps:
            print(step)

        report = self.generate_plan_report()
        print("\nResumo do Plano:")
        for key, value in report['summary'].items():
            print(f"  {key.replace('_', ' ').title()}: {value}")

class ProjectImprovementManager:
    """
    Gerencia o ciclo completo de melhoria do projeto, integrando avaliação,
    definição de objetivos e plano de ação.
    """
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.evaluator = PerformanceEvaluator(project_name)
        self.current_plan: Optional[IterativeActionPlan] = None

    def run_improvement_cycle(self, iteration_data: Dict[str, Any], improvement_iteration: int):
        """
        Executa um ciclo completo de melhoria.

        Args:
            iteration_data (Dict[str, Any]): Dados de desempenho da iteração anterior.
            improvement_iteration (int): Número da iteração de melhoria (ex: 2 para Melhoria 2).
        """
        print(f"\n--- Iniciando Ciclo de Melhoria {improvement_iteration} para '{self.project_name}' ---")

        # 1. Avaliação de Desempenho (Iteração 1)
        evaluation_results = self.evaluator.evaluate_performance(iteration_data)
        analysis = evaluation_results['analysis']
        lessons_learned = evaluation_results['lessons_learned']

        print("\n--- Análise Detalhada ---")
        for key, value in analysis.items():
            if isinstance(value, dict):
                print(f"  {key.replace('_', ' ').title()}:")
                for sub_key, sub_value in value.items():
                    print(f"    {sub_key.replace('_', ' ').title()}: {sub_value}")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value}")

        # 2. Definição de Objetivos SMART (baseado nas lições aprendidas)
        print(f"\n--- Definindo Objetivos SMART para Melhoria {improvement_iteration} ---")
        self.current_plan = IterativeActionPlan(improvement_iteration, f"Plano de Melhoria {improvement_iteration}")

        # Exemplo de como definir objetivos baseados nas lições
        if "Identificar gargalos de performance e otimizar consultas/algoritmos." in lessons_learned:
            obj_latency = SMARTObjective(
                specific="Reduzir a latência média das requisições da API principal.",
                measurable="Latência média da API principal de 250ms para 100ms.",
                achievable="Com otimização de banco de dados e cache, é atingível em 6 semanas.",
                relevant="Melhorar a experiência do usuário e a capacidade de resposta do sistema.",
                time_bound=datetime.date.today() + datetime.timedelta(weeks=6)
            )
            self.current_plan.add_objective(obj_latency)

        if "Revisar testes de unidade/integração e implementar mais validações de entrada." in lessons_learned:
            obj_errors = SMARTObjective(
                specific="Diminuir a taxa de erro em transações críticas.",
                measurable="Taxa de erro de 1.2% para 0.1% em transações de pagamento.",
                achievable="Com revisão de código e testes de regressão, é atingível em 4 semanas.",
                relevant="Garantir a integridade dos dados e a confiança do usuário.",
                time_bound=datetime.date.today() + datetime.timedelta(weeks=4)
            )
            self.current_plan.add_objective(obj_errors)

        if not self.current_plan.objectives:
            print("Nenhum objetivo SMART específico foi gerado automaticamente com base nas lições. Por favor, defina manualmente.")
            # Adicionar um objetivo genérico se nenhum for gerado
            self.current_plan.add_objective(SMARTObjective(
                specific="Melhorar a performance geral do sistema.",
                measurable="Aumentar o score de satisfação do usuário em 0.5 pontos.",
                achievable="Com foco em UX e performance, é atingível em 8 semanas.",
                relevant="Garantir a competitividade e a retenção de usuários.",
                time_bound=datetime.date.today() + datetime.timedelta(weeks=8)
            ))


        # 3. Plano de Ação Iterativo
        print(f"\n--- Desenvolvendo Plano de Ação para Melhoria {improvement_iteration} ---")

        # Exemplo de etapas baseadas nos objetivos
        if any("latência" in obj.specific.lower() for obj in self.current_plan.objectives):
            step1 = ActionStep(
                description="Auditar e otimizar consultas SQL de alto impacto.",
                resources_needed=["Desenvolvedor Sênior", "DBA"],
                success_metrics=["Tempo de execução de consulta < 50ms", "Redução de I/O do DB"],
                status="Pendente"
            )
            self.current_plan.add_step(step1)

            step2 = ActionStep(
                description="Implementar cache de dados para endpoints de leitura frequente.",
                resources_needed=["Desenvolvedor Sênior", "Arquiteto"],
                success_metrics=["Hit rate do cache > 90%", "Latência da API reduzida em 50%"],
                status="Pendente"
            )
            self.current_plan.add_step(step2)

        if any("erro" in obj.specific.lower() for obj in self.current_plan.objectives):
            step3 = ActionStep(
                description="Revisar e expandir cobertura de testes de integração para módulos críticos.",
                resources_needed=["QA Lead", "Desenvolvedor"],
                success_metrics=["Cobertura de testes > 85%", "Nenhum bug crítico encontrado em testes"],
                status="Pendente"
            )
            self.current_plan.add_step(step3)

            step4 = ActionStep(
                description="Implementar validação de entrada robusta em todas as APIs.",
                resources_needed=["Desenvolvedor"],
                success_metrics=["Nenhum erro de validação de entrada em produção", "Redução de 0.5% na taxa de erro"],
                status="Pendente"
            )
            self.current_plan.add_step(step4)

        # Demonstração de atualização de status
        if self.current_plan.steps:
            self.current_plan.update_step_status(self.current_plan.steps[0].description, "Em Andamento")

        # Gerar e imprimir o relatório final do plano
        self.current_plan.print_plan_details()
        print(f"\n--- Ciclo de Melhoria {improvement_iteration} Concluído para '{self.project_name}' ---")


# --- Execução do Projeto de Melhoramento 2 ---
if __name__ == "__main__":
    project_manager = ProjectImprovementManager("Sistema de E-commerce V1")

    # Dados de desempenho da Iteração 1 (simulados)
    iteration_1_performance_data = {
        'latency_ms': 280,  # Alta latência
        'error_rate_percent': 1.5, # Taxa de erro elevada
        'user_satisfaction_score': 3.2, # Baixa satisfação
        'features_completed': 75, # Conclusão abaixo do esperado
        'tech_debt_score': 7, # Pontuação de dívida técnica (1-10, 10=muito alta)
        'deployment_frequency_per_week': 0.5 # Baixa frequência de deploy
    }

    # Executar o ciclo de melhoria para o "Projeto de Melhoramento 2"
    project_manager.run_improvement_cycle(iteration_1_performance_data, 2)

    print("\n--- Fim da Execução do IA02 Executor ---")
```
