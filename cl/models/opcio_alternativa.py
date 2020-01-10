from .item import Item


class OpcioAlternativa(object):

    def __init__(self, value: int, destino: Item):
        self.value = value
        self.destino = destino

    def get_value(self):
        return self.value

    def get_destino(self):
        return self.destino

    def set_destino(self, destino):
        self.destino = destino


    def __eq__(self, other):
        try:
            return self.value == other.get_value()
        except Exception:
            return False