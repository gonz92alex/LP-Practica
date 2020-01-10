import networkx as nx

from .pregunta import Pregunta
from .resposta import Resposta


class Item(object):
    def __init__(self, id: str, pregunta: Pregunta = None,
                 resposta: Resposta = None, item=None):
        self.id = id
        if item:
            self.pregunta = item.get_pregunta() or pregunta
            self.resposta = item.get_resposta() or resposta
        else:
            self.pregunta = pregunta
            self.resposta = resposta

    def get_id(self):
        return self.id

    def get_pregunta(self):
        return self.pregunta

    def set_pregunta(self, pregunta: Pregunta):
        self.pregunta = pregunta

    def get_resposta(self):
        return self.resposta

    def set_resposta(self, resposta: Resposta):
        self.resposta = resposta

    def get_graph(self):
        G = nx.compose(self.pregunta.get_graph(),
                       self.resposta.get_graph())
        G.add_edge(self.pregunta.get_id(), self.resposta.get_id())
        return G

    def __eq__(self, other):
        return type(other) == self and self.id == other.get_id()
