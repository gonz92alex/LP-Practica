import networkx as nx
class Pregunta(object):

    id = None
    pregunta = None

    def __init__(self, id: str, pregunta: str=None, preguntada=None):
        self.id = id

        if preguntada:
            self.pregunta = preguntada.get_pregunta() or pregunta
            alt = preguntada.get_alternativa()
            self.alternativa = alt if len(alt) > 0 else []
        else:
            self.pregunta = pregunta
            self.alternativa = []

    def get_pregunta(self):
        return self.pregunta


    def get_id(self):
        return self.id

    def add_alternativas(self, alternativa):
        self.alternativa = alternativa.get_alternativas()

    def get_alternativa(self):
        return self.alternativa


    def get_graph(self):
        G = nx.DiGraph()
        G.add_node(self.id)
        for a in self.alternativa:
            item = a.get_destino()
            I = item.get_graph()
            G = nx.compose(G, I)
            G.add_edge(self.id, item.get_pregunta().get_id())
        return G


