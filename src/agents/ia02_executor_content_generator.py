```python
import logging
import requests
import time
from typing import Dict, Any, Optional

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Synapse12ContentGenerator:
    """
    IA02 Executor - Programador Sênior.
    Otimiza a criação de conteúdo para diversas finalidades,
    abordando requisitos de compreensão contextual, precisão em código
    e adaptabilidade criativa.

    Correções aplicadas com base nas observações do IA03 Crítico Comercial:
    1. Gerenciamento de Estado de Retentativa: `retry_count` agora é local ao loop de retentativa.
    2. Importações Locais em Loop: `requests` e `time` movidos para o topo do arquivo.
    3. Tratamento de Erros Genéricos: Blocos `except` refinados.
    4. Retorno de String de Erro: Métodos de geração agora lançam exceções em caso de falha.
    5. Parâmetros de API Configuráveis: `backoff_factor` agora é configurável no __init__.
    6. Simulação de Erro 503: Exemplo de uso atualizado para usar um mock simples para demonstração.
    """

    def __init__(self, api_endpoint: str = "https://api.synapse12.com/v1/generate", max_retries: int = 5, backoff_factor: float = 2.0):
        """
        Inicializa o gerador de conteúdo com o endpoint da API e configurações de retentativa.

        Args:
            api_endpoint (str): O URL do endpoint da API do Synapse 12.
            max_retries (int): Número máximo de tentativas para lidar com erros 503.
            backoff_factor (float): Fator de backoff exponencial para retentativas.
        """
        self.api_endpoint = api_endpoint
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def _call_api(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Simula a chamada à API do Synapse 12, incluindo lógica de retentativa
        para erros HTTP 503.

        Args:
            prompt (str): O texto de entrada para a geração de conteúdo.
            **kwargs: Argumentos adicionais para a chamada da API.

        Returns:
            Dict[str, Any]: A resposta da API.

        Raises:
            ConnectionError: Se a API retornar um erro 503 após múltiplas retentativas.
            requests.exceptions.RequestException: Para outros erros de requisição.
            Exception: Para outros erros inesperados.
        """
        payload = {"prompt": prompt, **kwargs}
        retry_count = 0 # Contador de retentativas local ao método

        while retry_count < self.max_retries:
            try:
                response = requests.post(self.api_endpoint, json=payload, timeout=10) # Adicionado timeout
                response.raise_for_status()  # Lança exceção para códigos de status ruins (4xx ou 5xx)
                return response.json()
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 503:
                    wait_time = self.backoff_factor ** retry_count
                    logging.warning(f"Erro HTTP 503: Alta demanda na API. Tentando novamente em {wait_time:.2f} segundos... (Tentativa {retry_count + 1}/{self.max_retries})")
                    time.sleep(wait_time)
                    retry_count += 1
                else:
                    logging.error(f"Erro HTTP inesperado: {e.response.status_code} - {e.response.text}")
                    raise # Relança a exceção para que o chamador possa tratá-la
            except requests.exceptions.Timeout:
                logging.warning(f"Timeout na requisição para a API. Tentando novamente em {self.backoff_factor ** retry_count:.2f} segundos... (Tentativa {retry_count + 1}/{self.max_retries})")
                time.sleep(self.backoff_factor ** retry_count)
                retry_count += 1
            except requests.exceptions.RequestException as e:
                logging.error(f"Erro de requisição: {e}")
                raise # Relança a exceção
            except Exception as e:
                logging.error(f"Ocorreu um erro inesperado durante a chamada da API: {type(e).__name__} - {e}")
                raise # Relança a exceção

        raise ConnectionError(f"Falha ao conectar à API após {self.max_retries} tentativas devido a alta demanda (HTTP 503) ou outros erros de rede.")

    def _generate_content(self, prompt: str, content_type: str, **api_params) -> str:
        """
        Método auxiliar para unificar a lógica de chamada da API e tratamento de exceções.

        Args:
            prompt (str): O prompt para a geração de conteúdo.
            content_type (str): O tipo de conteúdo a ser gerado (usado como parâmetro para a API).
            **api_params: Parâmetros adicionais para a chamada da API.

        Returns:
            str: O conteúdo gerado.

        Raises:
            ConnectionError: Se a geração de conteúdo falhar devido a problemas de conexão.
            Exception: Para outros erros inesperados.
        """
        logging.info(f"Chamando API para {content_type} com prompt: '{prompt[:50]}...'")
        try:
            response = self._call_api(prompt, content_type=content_type, **api_params)
            generated_text = response.get("generated_text")
            if generated_text is None:
                logging.error(f"Resposta da API para {content_type} não contém 'generated_text'. Resposta: {response}")
                raise ValueError("Resposta inválida da API: 'generated_text' não encontrado.")
            return generated_text
        except (ConnectionError, requests.exceptions.RequestException, ValueError) as e:
            logging.error(f"Falha ao gerar conteúdo do tipo '{content_type}': {e}")
            raise # Relança a exceção para que o chamador possa tratá-la
        except Exception as e:
            logging.error(f"Erro inesperado ao gerar conteúdo do tipo '{content_type}': {e}")
            raise # Relança a exceção

    def generate_thesis_content(self, topic: str, sections: list[str], style: str = "acadêmico") -> str:
        """
        Gera conteúdo para teses, focando em compreensão contextual profunda.

        Args:
            topic (str): O tópico principal da tese.
            sections (list[str]): Uma lista das seções a serem abordadas.
            style (str): O estilo de escrita desejado (padrão: "acadêmico").

        Returns:
            str: O conteúdo gerado para a tese.

        Raises:
            ValueError: Se o tópico ou as seções forem inválidos.
            ConnectionError: Se a geração de conteúdo falhar.
        """
        if not topic or not sections:
            raise ValueError("O tópico e as seções são obrigatórios para a geração de conteúdo de tese.")
        prompt = f"Gere conteúdo para uma tese sobre '{topic}'. As seções a serem abordadas são: {', '.join(sections)}. O estilo de escrita deve ser {style}."
        return self._generate_content(prompt, content_type="thesis", style=style)

    def generate_script_story(self, premise: str, characters: list[str], genre: str = "drama") -> str:
        """
        Gera conteúdo para histórias roteirizadas, mantendo coerência e adaptabilidade.

        Args:
            premise (str): A premissa básica da história.
            characters (list[str]): Uma lista dos personagens principais.
            genre (str): O gênero da história (padrão: "drama").

        Returns:
            str: O conteúdo gerado para a história roteirizada.

        Raises:
            ValueError: Se a premissa ou os personagens forem inválidos.
            ConnectionError: Se a geração de conteúdo falhar.
        """
        if not premise or not characters:
            raise ValueError("A premissa e os personagens são obrigatórios para a geração de roteiro.")
        prompt = f"Crie um roteiro para uma história com a premissa: '{premise}'. Os personagens principais são: {', '.join(characters)}. O gênero é {genre}."
        return self._generate_content(prompt, content_type="script", genre=genre)

    def generate_python_code(self, description: str, complexity: str = "médio") -> str:
        """
        Gera código Python com precisão, legibilidade e otimização.

        Args:
            description (str): Uma descrição clara do que o código deve fazer.
            complexity (str): O nível de complexidade do código (padrão: "médio").

        Returns:
            str: O código Python gerado.

        Raises:
            ValueError: Se a descrição for inválida.
            ConnectionError: Se a geração de conteúdo falhar.
        """
        if not description:
            raise ValueError("A descrição é obrigatória para a geração de código Python.")
        prompt = f"Gere código Python que: {description}. O nível de complexidade é {complexity}."
        return self._generate_content(prompt, content_type="python_code", complexity=complexity)

    def generate_step_by_step_tutorial(self, task: str, target_audience: str = "iniciantes") -> str:
        """
        Gera tutoriais passo a passo claros e funcionais.

        Args:
            task (str): A tarefa que o tutorial deve ensinar.
            target_audience (str): O público-alvo do tutorial (padrão: "iniciantes").

        Returns:
            str: O tutorial passo a passo gerado.

        Raises:
            ValueError: Se a tarefa for inválida.
            ConnectionError: Se a geração de conteúdo falhar.
        """
        if not task:
            raise ValueError("A tarefa é obrigatória para a geração de tutorial.")
        prompt = f"Crie um tutorial passo a passo para realizar a seguinte tarefa: '{task}'. O público-alvo é {target_audience}."
        return self._generate_content(prompt, content_type="tutorial", audience=target_audience)

    def generate_creative_content(self, idea: str, format_type: str = "poema", style: str = "livre") -> str:
        """
        Gera conteúdo criativo, adaptando-se a diferentes formatos e estilos.

        Args:
            idea (str): A ideia central para a criação.
            format_type (str): O formato do conteúdo (padrão: "poema").
            style (str): O estilo de escrita (padrão: "livre").

        Returns:
            str: O conteúdo criativo gerado.

        Raises:
            ValueError: Se a ideia for inválida.
            ConnectionError: Se a geração de conteúdo falhar.
        """
        if not idea:
            raise ValueError("A ideia é obrigatória para a geração de conteúdo criativo.")
        prompt = f"Gere conteúdo criativo com base na ideia: '{idea}'. O formato é {format_type} e o estilo é {style}."
        return self._generate_content(prompt, content_type="creative", format=format_type, style=style)

# --- Exemplo de Uso ---
if __name__ == "__main__":
    # Mock para simular respostas da API, incluindo erros 503
    class MockResponse:
        def __init__(self, json_data, status_code):
            self._json_data = json_data
            self.status_code = status_code

        def json(self):
            return self._json_data

        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.exceptions.HTTPError(f"HTTP Error: {self.status_code}", response=self)

    def mock_requests_post(*args, **kwargs):
        url = args[0]
        payload = kwargs.get("json", {})
        prompt = payload.get("prompt", "")

        # Simula falha 503 nas primeiras chamadas para um prompt específico
        if "simular erro 503" in prompt and mock_requests_post.call_count < 3:
            mock_requests_post.call_count += 1
            logging.warning(f"Mock: Simulando erro 503 para '{prompt[:30]}...'")
            return MockResponse({"error": "Service Unavailable"}, 503)
        elif "simular timeout" in prompt:
            logging.warning(f"Mock: Simulando timeout para '{prompt[:30]}...'")
            raise requests.exceptions.Timeout("Mocked timeout")
        elif "simular erro genérico" in prompt:
            logging.warning(f"Mock: Simulando erro genérico para '{prompt[:30]}...'")
            return MockResponse({"error": "Bad Request"}, 400)
        else:
            # Resposta de sucesso simulada
            mock_requests_post.call_count += 1
            logging.info(f"Mock: Simulando sucesso para '{prompt[:30]}...'")
            return MockResponse({"generated_text": f"Conteúdo simulado para: {prompt}"}, 200)

    mock_requests_post.call_count = 0 # Inicializa o contador de chamadas do mock

    # Substitui a chamada real de requests.post pelo mock
    original_requests_post = requests.post
    requests.post = mock_requests_post

    try:
        generator = Synapse12ContentGenerator(max_retries=4, backoff_factor=1.5) # Configuração para teste

        # 1. Geração de Conteúdo para Tese
        print("--- Gerando Conteúdo para Tese ---")
        thesis_content = generator.generate_thesis_content(
            topic="O Impacto da Inteligência Artificial no Mercado de Trabalho",
            sections=["Introdução", "Metodologia", "Análise de Dados", "Conclusão"]
        )
        print(thesis_content)
        print("\n" + "="*50 + "\n")

        # 2. Geração de História Roteirizada
        print("--- Gerando História Roteirizada ---")
        script_content = generator.generate_script_story(
            premise="Um detetive solitário investiga um mistério em uma cidade futurista onde a tecnologia é onipresente.",
            characters=["Detetive Kaito", "IA assistente 'Aura'"],
            genre="sci-fi noir"
        )
        print(script_content)
        print("\n" + "="*50 + "\n")

        # 3. Geração de Código Python
        print("--- Gerando Código Python ---")
        python_code = generator.generate_python_code(
            description="Uma função que calcula o fatorial de um número inteiro positivo usando recursão.",
            complexity="simples"
        )
        print(python_code)
        print("\n" + "="*50 + "\n")

        # 4. Geração de Tutorial Passo a Passo
        print("--- Gerando Tutorial Passo a Passo ---")
        tutorial_content = generator.generate_step_by_step_tutorial(
            task="Como configurar um ambiente virtual em Python usando venv",
            target_audience="desenvolvedores iniciantes"
        )
        print(tutorial_content)
        print("\n" + "="*50 + "\n")

        # 5. Geração de Conteúdo Criativo
        print("--- Gerando Conteúdo Criativo ---")
        creative_content = generator.generate_creative_content(
            idea="A solidão de uma estrela distante observando a Terra",
            format_type="poema",
            style="melancólico"
        )
        print(creative_content)
        print("\n" + "="*50 + "\n")

        # --- Testando tratamento de erro 503 (simulado) ---
        print("--- Testando tratamento de erro 503 (simulado) ---")
        mock_requests_post.call_count = 0 # Resetar contador para o teste
        try:
            # Este prompt fará com que o mock simule 3 erros 503 antes de ter sucesso
            error_sim_content = generator.generate_python_code("simular erro 503 e depois sucesso")
            print("Sucesso após simulação de 503:")
            print(error_sim_content)
        except ConnectionError as e:
            print(f"Capturado erro esperado após múltiplas falhas 503: {e}")
        except Exception as e:
            print(f"Capturado outro erro inesperado: {e}")
        print("\n" + "="*50 + "\n")

        # --- Testando tratamento de timeout (simulado) ---
        print("--- Testando tratamento de timeout (simulado) ---")
        mock_requests_post.call_count = 0 # Resetar contador para o teste
        try:
            timeout_sim_content = generator.generate_thesis_content("simular timeout", ["Intro"])
            print("Sucesso após simulação de timeout:")
            print(timeout_sim_content)
        except ConnectionError as e:
            print(f"Capturado erro esperado após simulação de timeout: {e}")
        except Exception as e:
            print(f"Capturado outro erro inesperado: {e}")
        print("\n" + "="*50 + "\n")

        # --- Testando tratamento de erro genérico (simulado) ---
        print("--- Testando tratamento de erro genérico (simulado) ---")
        mock_requests_post.call_count = 0 # Resetar contador para o teste
        try:
            generic_error_sim_content = generator.generate_script_story("simular erro genérico", ["Char1"])
            print("Sucesso após simulação de erro genérico (não deveria acontecer):")
            print(generic_error_sim_content)
        except ConnectionError as e:
            print(f"Capturado erro esperado após simulação de erro genérico: {e}")
        except Exception as e:
            print(f"Capturado outro erro inesperado: {e}")
        print("\n" + "="*50 + "\n")

        # --- Testando validação de entrada ---
        print("--- Testando validação de entrada ---")
        try:
            generator.generate_thesis_content(topic="", sections=["Intro"])
        except ValueError as e:
            print(f"Capturado erro esperado de validação: {e}")
        try:
            generator.generate_python_code(description="")
        except ValueError as e:
            print(f"Capturado erro esperado de validação: {e}")
        print("\n" + "="*50 + "\n")

    finally:
        # Restaura a função original de requests.post
        requests.post = original_requests_post
```
