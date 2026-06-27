class MessageBus:
    """
    Barramento Central que desacopla a comunicação dos agentes de IA.
    """
    def __init__(self):
        self.historico_eventos = []

    def publicar_evento(self, de_agente, para_agente, tipo_conteudo, dados):
        evento = {
            "origem": de_agente,
            "destino": para_agente,
            "tipo": tipo_conteudo,
            "payload": dados
        }
        self.historico_eventos.append(evento)
        return evento

    def obter_ultimo_evento(self, do_agente=None):
        if not self.historico_eventos:
            return None
        if do_agente:
            for ev in reversed(self.historico_eventos):
                if ev["origem"] == do_agente:
                    return ev
        return self.historico_eventos[-1]
      
