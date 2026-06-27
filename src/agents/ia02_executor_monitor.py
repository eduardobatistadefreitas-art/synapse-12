```python
import datetime

class IA02ExecutorImprovementSystem:
    """
    Sistema de Melhoramento Contínuo para IA02 Executor.
    Implementa diagnóstico, plano de ação e métricas de sucesso conforme briefing.
    """

    def __init__(self, system_id: str = "IA02 Executor"):
        """
        Inicializa o sistema de melhoramento.
        Args:
            system_id (str): Identificador do sistema (e.g., "IA02 Executor").
        """
        self.system_id = system_id
        self.current_performance = {}
        self.action_plan = []
        self.success_metrics = {}
        self.performance_history = [] # Para acompanhar o histórico de desempenho
        self._log_event("INICIALIZAÇÃO", f"Sistema de Melhoramento para {self.system_id} inicializado.")

    def _log_event(self, event_type: str, message: str):
        """
        Método interno para logar eventos de forma padronizada.
        Args:
            event_type (str): Tipo do evento (e.g., "DIAGNOSIS", "ACTION_PLAN").
            message (str): Mensagem do log.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}][{self.system_id}][{event_type}] {message}")

    def perform_diagnosis(self):
        """
        1. Diagnóstico de Desempenho: Autoavaliação objetiva do estado atual.
        Simula a coleta e análise de dados de desempenho do IA02 Executor,
        identificando áreas que necessitam de melhoria.
        """
        self._log_event("DIAGNOSIS", "Iniciando autoavaliação objetiva do desempenho atual...")

        # Simulação de métricas de desempenho atuais com valores hipotéticos.
        # Inclui limites (thresholds) para identificar automaticamente áreas de atenção.
        self.current_performance = {
            "response_accuracy": {"value": 0.88, "unit": "%", "threshold_low": 0.90, "description": "Precisão das respostas geradas."},
            "processing_speed_ms": {"value": 280, "unit": "ms", "threshold_high": 250, "description": "Tempo médio de processamento de requisições."},
            "instruction_adherence": {"value": 0.92, "unit": "%", "threshold_low": 0.95, "description": "Percentual de aderência às instruções fornecidas."},
            "resource_utilization_cpu": {"value": 0.65, "unit": "%", "threshold_high": 0.60, "description": "Utilização média de CPU."},
            "user_satisfaction_score": {"value": 4.1, "unit": "/5.0", "threshold_low": 4.3, "description": "Pontuação média de satisfação do usuário."},
            "code_quality_score": {"value": 0.80, "unit": "/1.0", "threshold_low": 0.85, "description": "Pontuação da qualidade do código base do Executor."}
        }

        self._log_event("DIAGNOSIS", "Diagnóstico concluído. Resultados atuais e status:")
        for metric, data in self.current_performance.items():
            status = "OK"
            if "threshold_low" in data and data["value"] < data["threshold_low"]:
                status = "ATENÇÃO (Abaixo do Limite)"
            elif "threshold_high" in data and data["value"] > data["threshold_high"]:
                status = "ATENÇÃO (Acima do Limite)"
            self._log_event("DIAGNOSIS", f"  - {metric} ({data['description']}): {data['value']}{data['unit']} ({status})")

        # Registra o estado atual no histórico
        self.performance_history.append({
            "timestamp": datetime.datetime.now(),
            "metrics": {k: v['value'] for k, v in self.current_performance.items()}
        })
        return self.current_performance

    def generate_action_plan(self):
        """
        2. Plano de Ação Estruturado: Definição de etapas e metas claras para melhoria.
        Gera um plano de ação detalhado com base nos resultados do diagnóstico.
        """
        self._log_event("ACTION_PLAN", "Gerando plano de ação estruturado com base no diagnóstico...")
        self.action_plan = [] # Limpa o plano anterior para gerar um novo

        if not self.current_performance:
            self._log_event("ACTION_PLAN", "Nenhum diagnóstico disponível. Não é possível gerar plano de ação.")
            return

        # Lógica para adicionar ações ao plano com base nas métricas que estão fora dos limites
        if self.current_performance["response_accuracy"]["value"] < self.current_performance["response_accuracy"]["threshold_low"]:
            self.action_plan.append({
                "id": "PA-001",
                "description": "Refinar modelos de Processamento de Linguagem Natural (NLP) para aumentar a precisão das respostas.",
                "target": f"Atingir precisão de resposta de {self.current_performance['response_accuracy']['threshold_low'] * 100:.0f}%",
                "status": "Pendente",
                "priority": "Alta",
                "responsible": self.system_id,
                "due_date": (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
            })

        if self.current_performance["processing_speed_ms"]["value"] > self.current_performance["processing_speed_ms"]["threshold_high"]:
            self.action_plan.append({
                "id": "PA-002",
                "description": "Otimizar algoritmos e infraestrutura subjacente para reduzir o tempo de processamento.",
                "target": f"Reduzir tempo de processamento para {self.current_performance['processing_speed_ms']['threshold_high']}ms",
                "status": "Pendente",
                "priority": "Média",
                "responsible": self.system_id,
                "due_date": (datetime.date.today() + datetime.timedelta(days=45)).isoformat()
            })

        if self.current_performance["instruction_adherence"]["value"] < self.current_performance["instruction_adherence"]["threshold_low"]:
            self.action_plan.append({
                "id": "PA-003",
                "description": "Revisar e aprimorar o módulo de interpretação de instruções para melhor compreensão dos comandos.",
                "target": f"Atingir aderência de instruções de {self.current_performance['instruction_adherence']['threshold_low'] * 100:.0f}%",
                "status": "Pendente",
                "priority": "Alta",
                "responsible": self.system_id,
                "due_date": (datetime.date.today() + datetime.timedelta(days=20)).isoformat()
            })
        
        if self.current_performance["code_quality_score"]["value"] < self.current_performance["code_quality_score"]["threshold_low"]:
            self.action_plan.append({
                "id": "PA-004",
                "description": "Realizar refatoração de código, implementar testes unitários e aderir a melhores práticas de desenvolvimento.",
                "target": f"Atingir score de qualidade de código de {self.current_performance['code_quality_score']['threshold_low'] * 100:.0f}%",
                "status": "Pendente",
                "priority": "Média",
                "responsible": self.system_id,
                "due_date": (datetime.date.today() + datetime.timedelta(days=60)).isoformat()
            })

        if not self.action_plan:
            self._log_event("ACTION_PLAN", "Nenhuma ação crítica identificada. O desempenho atual está dentro dos limites aceitáveis.")
        else:
            self._log_event("ACTION_PLAN", f"Plano de ação gerado com {len(self.action_plan)} itens:")
            for item in self.action_plan:
                self._log_event("ACTION_PLAN", f"  - [{item['id']}] {item['description']} (Meta: {item['target']})")
        return self.action_plan

    def define_success_metrics(self):
        """
        3. Métricas de Sucesso e Acompanhamento: Critérios para medir o progresso e o impacto.
        Define as métricas chave que serão usadas para acompanhar o progresso do plano de ação
        e o impacto geral das melhorias.
        """
        self._log_event("METRICS", "Definindo métricas de sucesso e acompanhamento para o projeto...")
        self.success_metrics = {} # Limpa métricas anteriores

        if not self.current_performance:
            self._log_event("METRICS", "Nenhum diagnóstico disponível. Não é possível definir métricas de sucesso.")
            return

        # As métricas de sucesso são diretamente ligadas aos alvos de melhoria identificados no diagnóstico
        self.success_metrics["Overall Response Accuracy Target"] = {
            "target_value": self.current_performance["response_accuracy"]["threshold_low"],
            "current_value": self.current_performance["response_accuracy"]["value"],
            "unit": "%",
            "description": self.current_performance["response_accuracy"]["description"]
        }
        self.success_metrics["Processing Speed Target"] = {
            "target_value": self.current_performance["processing_speed_ms"]["threshold_high"],
            "current_value": self.current_performance["processing_speed_ms"]["value"],
            "unit": "ms",
            "description": self.current_performance["processing_speed_ms"]["description"]
        }
        self.success_metrics["Instruction Adherence Target"] = {
            "target_value": self.current_performance["instruction_adherence"]["threshold_low"],
            "current_value": self.current_performance["instruction_adherence"]["value"],
            "unit": "%",
            "description": self.current_performance["instruction_adherence"]["description"]
        }
        self.success_metrics["Code Quality Score Target"] = {
            "target_value": self.current_performance["code_quality_score"]["threshold_low"],
            "current_value": self.current_performance["code_quality_score"]["value"],
            "unit": "/1.0",
            "description": self.current_performance["code_quality_score"]["description"]
        }
        
        self._log_event("METRICS", f"Métricas de sucesso definidas com {len(self.success_metrics)} itens:")
        for metric_name, data in self.success_metrics.items():
            self._log_event("METRICS", f"  - {metric_name}: Meta {data['target_value']}{data['unit']}, Atual {data['current_value']}{data['unit']} ({data['description']})")
        return self.success_metrics

    def simulate_progress(self, action_id: str, new_value: float):
        """
        Simula o progresso de uma ação ou a atualização de uma métrica.
        Em um sistema real, isso seria alimentado por dados de monitoramento contínuo.
        Args:
            action_id (str): ID da ação ou nome da métrica a ser atualizada.
            new_value (float): Novo valor para a métrica ou impacto da ação.
        """
        self._log_event("SIMULATION", f"Simulando progresso para a ação/métrica: '{action_id}' com novo valor {new_value}")
        
        # Atualiza o status de uma ação no plano, se o ID corresponder
        for action in self.action_plan:
            if action["id"] == action_id:
                action["status"] = "Em Progresso"
                self._log_event("SIMULATION", f"Status da ação {action_id} atualizado para 'Em Progresso'.")
                break
        
        # Atualiza as métricas de sucesso e desempenho atuais
        if "PA-001" in action_id or "Response Accuracy" in action_id:
            if "Overall Response Accuracy Target" in self.success_metrics:
                self.success_metrics["Overall Response Accuracy Target"]["current_value"] = new_value
            self.current_performance["response_accuracy"]["value"] = new_value
        elif "PA-002" in action_id or "Processing Speed" in action_id:
            if "Processing Speed Target" in self.success_metrics:
                self.success_metrics["Processing Speed Target"]["current_value"] = new_value
            self.current_performance["processing_speed_ms"]["value"] = new_value
        elif "PA-003" in action_id or "Instruction Adherence" in action_id:
            if "Instruction Adherence Target" in self.success_metrics:
                self.success_metrics["Instruction Adherence Target"]["current_value"] = new_value
            self.current_performance["instruction_adherence"]["value"] = new_value
        elif "PA-004" in action_id or "Code Quality" in action_id:
            if "Code Quality Score Target" in self.success_metrics:
                self.success_metrics["Code Quality Score Target"]["current_value"] = new_value
            self.current_performance["code_quality_score"]["value"] = new_value

        self._log_event("SIMULATION", "Métricas de sucesso e desempenho atualizados após simulação.")
        # Registra o novo estado no histórico
        self.performance_history.append({
            "timestamp": datetime.datetime.now(),
            "metrics": {k: v['value'] for k, v in self.current_performance.items()}
        })

    def monitor_progress(self):
        """
        Acompanhamento: Verifica o progresso em relação às métricas de sucesso definidas.
        Reporta o status de cada métrica e o status geral do projeto de melhoramento.
        """
        self._log_event("MONITORING", "Monitorando progresso das métricas de sucesso...")
        overall_status = "Em Andamento"
        all_targets_met = True

        for metric_name, data in self.success_metrics.items():
            current = data["current_value"]
            target = data["target_value"]
            unit = data["unit"]
            
            status = "Não Avaliado"
            # Lógica para métricas onde menor é melhor (e.g., tempo de processamento)
            if "Speed" in metric_name: 
                if current <= target:
                    status = "Meta Atingida!"
                elif current > target:
                    status = "Ainda Acima da Meta"
                    all_targets_met = False
            # Lógica para métricas onde maior é melhor (e.g., precisão, aderência)
            else: 
                if current >= target:
                    status = "Meta Atingida!"
                elif current < target:
                    status = "Ainda Abaixo da Meta"
                    all_targets_met = False
            
            self._log_event("MONITORING", f"  - {metric_name}: Atual {current}{unit} / Meta {target}{unit} -> {status}")
        
        # Verifica se todas as ações do plano foram concluídas
        all_actions_completed = True
        if self.action_plan:
            for action in self.action_plan:
                if action["status"] != "Concluído":
                    all_actions_completed = False
                    break
        else: # Se não há plano de ação, considera-se que não há ações a serem concluídas
            all_actions_completed = True

        if all_targets_met and all_actions_completed:
            overall_status = "Projeto Concluído com Sucesso!"
        elif all_targets_met:
            overall_status = "Metas Atingidas, aguardando conclusão das ações pendentes."
        else:
            overall_status = "Ainda em Progresso"

        self._log_event("MONITORING", f"Status Geral do Projeto: {overall_status}")
        return overall_status

    def report_status(self):
        """
        Gera um relatório completo do estado atual do sistema de melhoramento,
        abrangendo diagnóstico, plano de ação e métricas de sucesso.
        """
        self._log_event("REPORT", "Gerando Relatório de Status Completo do Projeto de Melhoramento:")
        self._log_event("REPORT", "\n--- 1. Diagnóstico de Desempenho Atual ---")
        if not self.current_performance:
            self._log_event("REPORT", "Nenhum diagnóstico realizado ainda.")
        else:
            for metric, data in self.current_performance.items():
                status = "OK"
                limit_info = ""
                if "threshold_low" in data:
                    limit_info = f" (Limite: >={data['threshold_low']}{data['unit']})"
                    if data["value"] < data["threshold_low"]:
                        status = "CRÍTICO (Abaixo do Limite)"
                elif "threshold_high" in data:
                    limit_info = f" (Limite: <={data['threshold_high']}{data['unit']})"
                    if data["value"] > data["threshold_high"]:
                        status = "CRÍTICO (Acima do Limite)"
                self._log_event("REPORT", f"  - {metric}: {data['value']}{data['unit']}{limit_info} -> {status}")

        self._log_event("REPORT", "\n--- 2. Plano de Ação Estruturado ---")
        if not self.action_plan:
            self._log_event("REPORT", "Nenhum plano de ação gerado.")
        else:
            for item in self.action_plan:
                self._log_event("REPORT", f"  - [{item['id']}] {item['description']}")
                self._log_event("REPORT", f"    Meta: {item['target']}")
                self._log_event("REPORT", f"    Status: {item['status']} | Prioridade: {item['priority']} | Prazo: {item['due_date']}")

        self._log_event("REPORT", "\n--- 3. Métricas de Sucesso e Acompanhamento ---")
        if not self.success_metrics:
            self._log_event("REPORT", "Nenhuma métrica de sucesso definida.")
        else:
            for metric_name, data in self.success_metrics.items():
                status = "Não Avaliado"
                if "Speed" in metric_name: # Para métricas onde menor é melhor
                    if data["current_value"] <= data["target_value"]:
                        status = "Meta Atingida"
                    else:
                        status = "Ainda Acima da Meta"
                else: # Para métricas onde maior é melhor
                    if data["current_value"] >= data["target_value"]:
                        status = "Meta Atingida"
                    else:
                        status = "Ainda Abaixo da Meta"
                self._log_event("REPORT", f"  - {metric_name}: Atual {data['current_value']}{data['unit']} / Meta {data['target_value']}{data['unit']} -> {status}")
        
        self._log_event("REPORT", "\n--- Histórico de Desempenho ---")
        if not self.performance_history:
            self._log_event("REPORT", "Nenhum histórico de desempenho registrado.")
        else:
            for entry in self.performance_history:
                self._log_event("REPORT", f"  - {entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}: {entry['metrics']}")

        self._log_event("REPORT", "\n--- Fim do Relatório ---")

# Exemplo de uso do sistema de melhoramento para IA02 Executor
if __name__ == "__main__":
    executor_system = IA02ExecutorImprovementSystem()

    # --- FASE 1: DIAGNÓSTICO ---
    print("\n" + "="*80 + "\n")
    executor_system.perform_diagnosis()
    print("\n" + "="*80 + "\n")

    # --- FASE 2: PLANO DE AÇÃO ---
    executor_system.generate_action_plan()
    print("\n" + "="*80 + "\n")

    # --- FASE 3: MÉTRICAS DE SUCESSO E ACOMPANHAMENTO ---
    executor_system.define_success_metrics()
    print("\n" + "="*80 + "\n")

    # Gerar um relatório inicial para visualizar o estado antes das melhorias
    executor_system.report_status()
    print("\n" + "="*80 + "\n")

    # --- SIMULAÇÃO DE PROGRESSO E ACOMPANHAMENTO ---
    print("--- SIMULANDO PROGRESSO DAS AÇÕES DE MELHORIA ---")
    
    # Simular melhoria na precisão das respostas (PA-001)
    executor_system.simulate_progress("PA-001", 0.91) 
    # Simular melhoria no tempo de processamento (PA-002)
    executor_system.simulate_progress("PA-002", 240) 
    # Simular melhoria na qualidade do código (PA-004)
    executor_system.simulate_progress("PA-004", 0.86) 
    print("\n" + "="*80 + "\n")

    # Monitorar o progresso após a primeira rodada de simulações
    executor_system.monitor_progress()
    print("\n" + "="*80 + "\n")

    # Gerar um relatório atualizado para ver o impacto das simulações
    executor_system.report_status()
    print("\n" + "="*80 + "\n")

    # Simular mais progresso para atingir as metas restantes e concluir as ações
    print("--- SIMULANDO MAIS PROGRESSO PARA ATINGIR TODAS AS METAS ---")
    executor_system.simulate_progress("PA-003", 0.96) # Aumenta a aderência às instruções
    
    # Marcar as 
