from cl.models.enquesta import Enquesta


class EnquestaResposta(Enquesta):
    enquesta = None
    respostes = []

    def __init__(self, enquesta: Enquesta, id):
        self.enquesta = enquesta
        self.respostes = []
        super().__init__(id, enquesta)

    def responde(self, pos_item, value):
        item = self.items[pos_item]
        alters = item.get_pregunta().get_alternativas()
        if len(alters) > 0:
            for a in alters:
                if a.get_value() == value:
                    destino = a.get_destino()
                    inicio = self.items[:pos_item]
                    final = self.items[pos_item:]
                    self.items = inicio
                    self.items.append(destino)
                    self.items += final
        self.respostes.append((item.get_pregunta().get_id(), value))

    def get_respuestas(self):
        return self.respostes
