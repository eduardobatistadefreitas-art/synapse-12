```python
import ast
import os

class ExecutorManagerConfig:
    """
    Simula o conteúdo do arquivo `ia02_executor_manager.py`.
    Em um cenário real, este conteúdo seria lido de um arquivo físico.
    Define as diretrizes SMART e palavras-chave para análise.
    """
    _CONFIG_CONTENT = """
# Configuração para IA02 Executor Manager
# Este arquivo define as diretrizes para alinhamento SMART de briefings.

SMART_CRITERIA = {
    "Specific": {
        "description": "O briefing declara claramente QUEM, O QUÊ, ONDE, QUANDO, POR QUÊ? É inequívoco?",
        "keywords": ["quem", "o quê", "onde", "quando", "por quê", "objetivo", "meta", "detalhes", "escopo"]
    },
    "Measurable": {
        "description": "Como o sucesso será medido? Existem métricas quantificáveis ou indicadores?",
        "keywords": ["métricas", "quantificar", "medir", "indicador", "progresso", "contagem", "porcentagem", "KPI"]
    },
    "Achievable": {
        "description": "O objetivo é realista e atingível dados os recursos e restrições disponíveis?",
        "keywords": ["recursos", "viável", "realista", "capacidade", "orçamento", "possível", "atingível"]
    },
    "Relevant": {
        "description": "O objetivo se alinha com os objetivos mais amplos e a visão do Diretor? É valioso?",
        "keywords": ["alinhar", "estratégico", "visão", "impacto", "prioridade", "relevante", "importante"]
    },
    "Time-bound": {
        "description": "Existe um prazo claro ou período para conclusão?",
        "keywords": ["prazo", "data", "até", "antes", "duração", "cronograma", "finalização", "período"]
    }
}

# Outras configurações podem ser adicionadas aqui no futuro.
"""

    @staticmethod
    def get_config_content():
        """Retorna o conteúdo simulado do arquivo de configuração."""
        return ExecutorManagerConfig._CONFIG_CONTENT

class ConfigInterpreter:
    """
    Responsável por ler e interpretar o conteúdo de um arquivo de configuração
    (neste caso, simulado como `ia02_executor_manager.py`).
    """
    def __init__(self, config_source_content: str):
        self.config_source_content = config_source_content
        self._parsed_config = {}
        self._interpret_content()

    def _interpret_content(self):
        """
        Interpreta o conteúdo da string como um script Python para extrair variáveis.
        Usa ast.literal_eval para segurança ao avaliar literais Python.
        """
        tree = ast.parse(self.config_source_content)
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        # Avalia o valor atribuído se for um literal (dict, list, str, num, etc.)
                        try:
                            self._parsed_config[target.id] = ast.literal_eval(node.value)
                        except (ValueError, TypeError):
                            # Se não for um literal simples, tenta obter o valor bruto
                            # ou ignora se não for relevante para a interpretação atual.
                            # Para este caso, esperamos apenas literais.
                            pass
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                # Ignora docstrings ou comentários que são interpretados como expressões constantes
                pass

    def get_smart_criteria(self) -> dict:
        """Retorna os critérios SMART interpretados."""
        return self._parsed_config.get("SMART_CRITERIA", {})

class SMARTAnalyzer:
    """
    Analisa um briefing com base nos critérios SMART fornecidos.
    """
    def __init__(self, smart_criteria: dict):
        self.smart_criteria = smart_criteria

    def analyze_briefing(self, briefing_text: str) -> dict:
        """
        Analisa o texto do briefing e gera um relatório de alinhamento SMART.
        Retorna um dicionário com sugestões para cada critério SMART.
        """
        analysis_report = {}
        briefing_lower = briefing_text.lower()

        for criterion, details in self.smart_criteria.items():
            description = details.get("description", "")
            keywords = details.get("keywords", [])
            found_keywords = [kw for kw in keywords if kw in briefing_lower]

            if found_keywords:
                analysis_report[criterion] = {
                    "status": "Potencialmente Alinhado",
                    "sugestao": f"O briefing contém palavras-chave relacionadas a '{criterion}': {', '.join(found_keywords)}. Revise para garantir que atende à descrição: '{description}'",
                    "keywords_encontradas": found_keywords
                }
            else:
                analysis_report[criterion] = {
                    "status": "Requer Atenção",
                    "sugestao": f"O briefing parece não abordar explicitamente o critério '{criterion}'. Considere adicionar detalhes que respondam a: '{description}'. Palavras-chave sugeridas: {', '.join(keywords)}",
                    "keywords_encontradas": []
                }
        return analysis_report

class BriefingOptimizer:
    """
    Interface principal para o IA01 Mediador.
    Capacita o IA01 para auto-otimização de briefings,
    utilizando as diretrizes do ia02_executor_manager.py.
    """
    def __init__(self, manager_config_path: str = None):
        """
        Inicializa o otimizador.
        manager_config_path: Caminho para o arquivo ia02_executor_manager.py.
                             Se None, usa o conteúdo simulado.
        """
        config_content = self._load_manager_config(manager_config_path)
        self.config_interpreter = ConfigInterpreter(config_content)
        self.smart_analyzer = SMARTAnalyzer(self.config_interpreter.get_smart_criteria())

    def _load_manager_config(self, path: str) -> str:
        """
        Carrega o conteúdo do arquivo de configuração do IA02 Executor Manager.
        Se o caminho não for fornecido ou o arquivo não existir, usa o conteúdo simulado.
        """
        if path and os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
            except IOError as e:
                print(f"IA02 Executor: Erro ao ler '{path}': {e}. Usando configuração simulada.")
                return ExecutorManagerConfig.get_config_content()
        else:
            print("IA02 Executor: Caminho para ia02_executor_manager.py não fornecido ou arquivo não encontrado. Usando configuração simulada.")
            return ExecutorManagerConfig.get_config_content()

    def optimize_briefing(self, briefing_text: str) -> dict:
        """
        Recebe um briefing e retorna um relatório de otimização SMART.
        Este relatório pode ser usado pelo IA01 Mediador para refinar seus briefings.
        """
        print("\nIA02 Executor: Iniciando análise de otimização de briefing...")
        analysis_results = self.smart_analyzer.analyze_briefing(briefing_text)
        print("IA02 Executor: Análise concluída. Gerando recomendações.")
        return analysis_results

    def generate_optimization_summary(self, analysis_results: dict) -> str:
        """
        Formata os resultados da análise em um resumo legível para o IA01 Mediador.
        """
        summary = ["\n--- Relatório de Otimização de Briefing (IA02 Executor) ---"]
        summary.append("Este relatório visa auxiliar o IA01 Mediador na auto-otimização de briefings.")
        summary.append("\nCritérios SMART:")

        for criterion, details in analysis_results.items():
            summary.append(f"\n  - {criterion}: {details['status']}")
            summary.append(f"    Sugestão: {details['sugestao']}")
            if details['keywords_encontradas']:
                summary.append(f"    Palavras-chave encontradas: {', '.join(details['keywords_encontradas'])}")
            else:
                summary.append(f"    Nenhuma palavra-chave SMART para '{criterion}' encontrada.")

        summary.append("\n--- Fim do Relatório ---")
        return "\n".join(summary)

# --- Exemplo de Uso (Simulação do IA01 Mediador interagindo com IA02 Executor) ---
if __name__ == "__main__":
    # 1. Simular a criação do arquivo ia02_executor_manager.py (opcional, para testar leitura de arquivo)
    # Em um ambiente real, este arquivo já existiria.
    manager_file_path = "ia02_executor_manager.py"
    with open(manager_file_path, "w", encoding="utf-8") as f:
        f.write(ExecutorManagerConfig.get_config_content())
    print(f"IA02 Executor: Arquivo '{manager_file_path}' simulado criado para teste.")

    # 2. IA01 Mediador inicializa o BriefingOptimizer do IA02 Executor
    # O IA01 passa o caminho para o arquivo de configuração do Executor.
    ia01_mediador_optimizer = BriefingOptimizer(manager_config_path=manager_file_path)

    # 3. IA01 Mediador prepara um briefing para otimização
    sample_briefing_1 = """
    Precisamos expandir a funcionalidade de acesso móvel para o Diretor.
    O objetivo é permitir que ele opere o ecossistema diretamente do celular.
    """

    sample_briefing_2 = """
    **Objetivo:** Implementar o Módulo de Operação Móvel Direta para o Diretor.

    **O Quê:** Desenvolver uma interface de usuário otimizada para dispositivos móveis
    que permita ao Diretor acessar e controlar as principais funções do ecossistema.
    **Quem:** Equipe de Desenvolvimento Sênior (IA02 Executor e IA03 Integrador).
    **Quando:** Conclusão da Fase 1 (acesso a relatórios e aprovações) até 30 de Setembro de 2024.
    Conclusão da Fase 2 (controle de módulos) até 30 de Novembro de 2024.
    **Por Quê:** Para aumentar a agilidade operacional e a capacidade de decisão do Diretor,
    alinhando-se à visão de mobilidade total.

    **Métricas de Sucesso:**
    - 95% de uptime da interface móvel.
    - Tempo médio de resposta da interface inferior a 2 segundos.
    - Feedback positivo do Diretor em 80% dos testes de usabilidade.

    **Recursos:**
    - Equipe de 3 desenvolvedores dedicados.
    - Orçamento de 50.000 créditos para ferramentas e licenças.
    - Acesso total aos repositórios de código existentes.

    **Relevância:** Este projeto é crucial para a estratégia de expansão do ecossistema
    e para a modernização das operações do Diretor, garantindo sua capacidade de gestão
    em qualquer local e momento.
    """

    print("\n--- Briefing Original 1 ---")
    print(sample_briefing_1)

    # 4. IA01 Mediador solicita a otimização do briefing ao IA02 Executor
    optimization_results_1 = ia01_mediador_optimizer.optimize_briefing(sample_briefing_1)

    # 5. IA01 Mediador recebe e interpreta o relatório de otimização
    optimization_summary_1 = ia01_mediador_optimizer.generate_optimization_summary(optimization_results_1)
    print(optimization_summary_1)

    print("\n--- Briefing Original 2 ---")
    print(sample_briefing_2)

    optimization_results_2 = ia01_mediador_optimizer.optimize_briefing(sample_briefing_2)
    optimization_summary_2 = ia01_mediador_optimizer.generate_optimization_summary(optimization_results_2)
    print(optimization_summary_2)

    # Limpeza do arquivo simulado
    if os.path.exists(manager_file_path):
        os.remove(manager_file_path)
        print(f"\nIA02 Executor: Arquivo '{manager_file_path}' simulado removido.")
```
