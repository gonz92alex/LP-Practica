from .opcio_alternativa import OpcioAlternativa

class Alternativa(object):

    def __init__(self, id: str, origen=None, alternativas:list=None, alternativa=None):
        self.id = id
        alternativas = alternativas if alternativas else []
        if alternativa:
            self.origen = alternativa.get_origen or origen
            alts = alternativa.get_alternativas()
            self.alternativas = alts if len(alts) > 0 else alternativas
        else:
            self.origen = origen
            self.alternativas = alternativas


    def get_id(self):
        return self.id

    def get_origen(self):
        return self.origen

    def set_origen(self, origen):
        self.origen = origen

    def get_alternativas(self):
        return self.alternativas

    def set_alternativas(self, alternativas):
        self.alternativas = alternativas

    def add_alternativa(self, alternativa: OpcioAlternativa):
        if alternativa not in self.alternativas:
            self.alternativas.append(alternativa)

    def __eq__(self, other):
        return type(other) == self and self.id == other.get_id()