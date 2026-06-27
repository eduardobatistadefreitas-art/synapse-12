import json

class SmartValidator:
    """
    Validador programático baseado na metodologia SMART para barrar briefings vagos.
    """
    def __init__(self):
        # Gatilhos obrigatórios que indicam mensurabilidade e prazo
        self.indicadores_mensuraveis = ["%", "kpi", "taxa", "tempo", "pontos", "acuracia", "sucesso"]
        self.indicadores_tempo = ["meses", "quinzenal", "prazo", "cronograma", "fase", "data", "ate"]

    def avaliar_briefing_smart(self, texto_briefing):
        """
        Analisa o texto do briefing e retorna se ele cumpre os requisitos mínimos.
        """
        if not texto_briefing or "RAIZ_ERRO" in texto_briefing:
            return False, ["Briefing inexistente ou corrompido."]
            
        texto_minusculo = texto_briefing.lower()
        lacunas = []

        # 1. Validação de Especificidade (Specific)
        if "requisitos" not in texto_minusculo and "objetivo" not in texto_minusculo:
            lacunas.append("Falta clareza no objetivo geral ou escopo de requisitos.")

        # 2. Validação de Mensurabilidade (Measurable)
        has_measurable = any(ind in texto_minusculo for ind in self.indicadores_mensuraveis)
        if not has_measurable:
            lacunas.append("Falta de Metricas Quantificaveis ou KPIs de sucesso.")

        # 3. Validação de Prazos (Time-bound)
        has_time = any(ind in texto_minusculo for ind in self.indicadores_tempo)
        if not has_time:
            lacunas.append("Ausencia de Cronograma ou Prazos definidos para as fases.")

        # Se não houver lacunas, o briefing é considerado SMART
        is_smart = len(lacunas) == 0
        return is_smart, lacunas
    
