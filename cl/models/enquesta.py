import networkx as nx

from .item import Item


class Enquesta(object):
    id = None
    items = []

    def __init__(self, id, items=None, enquesta=None):
        self.id = id
        items = items if items else []
        if enquesta:
            enqs = enquesta.get_items()
            self.items = enqs if len(enqs) > 0 else items
        else:
            self.items = items

    def get_id(self):
        return self.id

    def get_items(self):
        return self.items

    def set_items(self, items):
        self.items = items

    def add_item(self, item: Item):
        if item not in self.items:
            self.items.append(item)

    def get_graph(self):
        G = nx.DiGraph()
        G.add_node(self.id)
        ids = []
        for i in self.items:
            ids.append(i.get_pregunta().get_id())
            G = nx.compose(G, i.get_graph())
        ant = self.id
        for i in ids:
            G.add_edge(ant, i)
            ant = i
        G.add_node('END')
        G.add_edge(ids[-1], 'END')
        return G
