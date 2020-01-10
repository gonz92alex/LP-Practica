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

    def add_respuesta(self, respuesta):
        id = respuesta[0]
        value = respuesta[1]
        if id in self.resultados:
            if value in self.resultados[id]:
                self.resultados[id][value] += 1
            else:
                self.resultados[id][value] = 1
        else:
            self.resultados[id] = {
                value: 1
            }

    def get_data_plot(self, pregunta_id):
        print(pregunta_id)
        if pregunta_id in self.resultados:
            labels = []
            data = []
            for valor, count in self.resultados[pregunta_id].items():
                labels.append(valor)
                data.append(count)
            return {
                'labels': labels,
                'data': data
            }
        else:
            return None

    def get_pie(self, pregunta_id):
        raw = self.get_data_plot(pregunta_id)
        if raw:
            labels = raw['labels']
            data = raw['data']
            plt.pie(data,
                    labels=labels,
                    explode=tuple(len(labels) * [0.05]),
                    shadow=True,
                    autopct='%1.1f%%')
            path = '../img/{id}_{pregunta}_pie.png'.format(
                id=self.id,
                pregunta=pregunta_id
            )
            plt.savefig(path)
            plt.clf()
            return path
        else:
            return None

    def get_bar(self, pregunta_id):
        raw = self.get_data_plot(pregunta_id)
        if raw:
            labels = tuple(raw['labels'])
            data = raw['data']
            print(raw)
            index = list(range(len(data)))
            plt.bar(index, data)
            plt.xticks(index, labels)
            path = '../img/{id}_{pregunta}_bar.png'.format(
                id=self.id,
                pregunta=pregunta_id
            )
            plt.savefig(path)
            plt.clf()
            return path
        else:
            return None

    def report(self):
        template = '{pregunta} {resposta} {count}\n'
        salida = template.format(
            pregunta='*PREGUNTA*'.rjust(10, ' '),
            resposta='*VALOR*'.rjust(10, ' '),
            count='*RESPOSTES*'.rjust(10, ' ')
        )
        for preg, resp in self.resultados.items():
            for valor, count in resp.items():
                salida += template.format(
                    pregunta=preg.rjust(10, ' '),
                    resposta=str(valor).rjust(10, ' '),
                    count=str(count).rjust(10, ' ')
                )
        return salida
