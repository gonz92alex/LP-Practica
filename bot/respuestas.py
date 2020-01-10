import matplotlib.pyplot as plt

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


    def _get_data_plot(self, pregunta_id):
        if pregunta_id in self.resultados:
            labels = []
            data = []
            for valor, count in self.resultados[pregunta_id].items():
                labels.append(valor)
                data.append(labels)
                return {
                    'labels': labels,
                    'data': data
                }
        else:
            return None



    def get_pie(self, pregunta_id):
        raw = self._get_data_plot(pregunta_id)
        if raw:
            labels = raw['labels']
            data = raw['data']
            plt.pie(data,
                    labels=labels,
                    explode=(0.05, 0.05, 0.05),
                    shadow=True,
                    autopct='%1.1f%%')
            path = '../img/{id}_{pregunta}_pie.png'.format(
                    id=self.id,
                    pregunta=pregunta_id
            )
            plt.savefig(path)
            return path
        else:
            return None



    def get_bar(self, pregunta_id):
        raw = self._get_data_plot(pregunta_id)
        if raw:
            labels = tuple(raw['labels'])
            data = raw['data']
            index = list(range(len(data)))
            x = [5, 3, 2]
            plt.bar(index, data)
            plt.xticks(index, labels)
            path = '../img/{id}_{pregunta}_bar.png'.format(
                id=self.id,
                pregunta=pregunta_id
            )
            plt.savefig(path)
            return path
        else:
            return None


    def repost(self):
        template ='{pregunta} {resposta} {count}'
        salida = template.format(
            pregunta='*PREGUNTA*'.rjust(10, ' '),
            resposta='*VALOR*'.rjust(10, ' '),
            count='*RESPOSTES*'.rjust(10, ' ')
        )
        for preg, resp in self.resultados.items():
            for valor, count in resp.items():
                salida += template.format(
                    pregunta=preg.rjust(10, ' '),
                    resposta=valor.rjust(10, ' '),
                    count=count.rjust(10, ' ')
                )
        return salida
