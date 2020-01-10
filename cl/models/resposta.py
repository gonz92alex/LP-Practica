import networkx as nx

from .opcio_resposta import OpcioResposta


class Resposta(object):
    id = None
    respostes = None

    def __init__(self, id: str, respostes: list = None, resposta=None):
        self.id = id
        self.respostes = respostes if respostes else []
        if resposta:
            resp = resposta.get_respostes()
            self.respostes = resp if len(resp) > 0 else respostes

    def get_respostes(self):
        return self.respostes

    def get_id(self):
        return self.id

    def get_graph(self):
        G = nx.DiGraph()
        G.add_node(self.id)
        return G

    def get_respostes_str(self):
        sortida = ''
        template = '{value}: {resposta}\n'
        for resp in self.respostes:
            sortida += template.format(
                value=resp.get_value(),
                resposta=resp.get_resposta())
        return sortida

    def add_resposta(self, resposta: OpcioResposta):
        if resposta not in self.respostes:
            self.respostes.append(resposta)
