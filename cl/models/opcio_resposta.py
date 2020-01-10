class OpcioResposta(object):
    def __init__(self, value: int, resposta: str):
        self.value = value
        self.resposta = resposta

    def get_resposta(self):
        return self.pregunta

    def get_value(self):
        return self.value

    def __eq__(self, other):
        return type(other) == self and self.value == other.get_value()
