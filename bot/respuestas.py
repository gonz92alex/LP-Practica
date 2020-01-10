

class Respuestas(object):


    def __init__(self, id):
        self.id = id
        self.resultados = {}



    def add_resultados(self, encuesta):
        for item in encuesta.get_respuestas():
            id = item[0]
            value = item[1]
            if id in self.resultados:
                if value in self.resultados[id]:
                    self.resultados[id][value] += 1
                else:
                    self.resultados[id][value] = 1
            else:
                self.resultados[id] = {
                        value: 1
                }

