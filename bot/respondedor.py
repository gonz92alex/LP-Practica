from cl.models.enquesta import Enquesta


class EnquestaResposta(Enquesta):
    enquesta = None
    respostes = []

    def __init__(self, enquesta: Enquesta):
        self.enquesta = enquesta
        self.respostes = []
        self.pos_item = 0
        self.last_resposta = None
        super().__init__(id=enquesta.get_id(), enquesta=enquesta)

    def responde(self, value):
        item = self.get_item()
        if item:
            alters = item.get_pregunta().get_alternativa()
            if len(alters) > 0:
                for a in alters:
                    if a.get_value() == value:
                        destino = a.get_destino()
                        inicio = self.items[:self.pos_item + 1]
                        final = self.items[self.pos_item + 1:]
                        self.items = inicio
                        self.items.append(destino)
                        self.items += final
            pregunta = item.get_pregunta().get_id()
            respuesta = (pregunta, value)
            self.respostes.append(respuesta)
            self.pos_item += 1
            self.last_resposta = respuesta
            return self.get_item()
        else:
            return None

    def get_respuestas(self):
        return self.respostes

    def get_item(self):
        if len(self.items) > self.pos_item:
            return self.items[self.pos_item]
        else:
            return None

    def get_last_respuesta(self):
        return self.last_resposta

    def restart(self):
        self.pos_item = 0
        self.last_resposta = None
