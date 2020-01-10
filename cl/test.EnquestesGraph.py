import networkx as nx
import matplotlib.pyplot as plt


def id_dict(lista: list):
    salida = {}
    for l in lista:
        salida[l['id']] = l['contenido']
    return salida



def genera_graph(root: dict):
    enquestes = id_dict(root['ENQUESTA'])
    preguntes = id_dict(root['PREGUNTA'])
    alternatives = id_dict(root['ALTERNATIVA'])
    respostes = id_dict(root['RESPOSTA'])
    items = id_dict(root['ITEM'])
    edges_color = []
    labels = {}
    for id, enq in enquestes.items():
        G = nx.DiGraph()
        ant = id
        usados = [ant]
        G.add_node(ant)
        for pos, item in enq.items():
            preg = None
            for id_item, itm in items.items():
                if item == id_item:
                    preg = itm['PREGUNTA']
                    G.add_node(preg)
                    G.add_node(itm['RESPOSTA'])
                    G.add_edge(preg, itm['RESPOSTA'])
                    edges_color.append('black')
                    labels[(preg, itm['RESPOSTA'])] = id_item
                    break
            for id_alt, alt in alternatives.items():
                preg_alt = alt['item']
                for id_item, itm in items.items():
                    if preg_alt == id_item:
                        preg_alt = itm['PREGUNTA']
                        break
                for a in alt['alternativas']:
                    destino = a[1]
                    preg_i = None
                    for id_item, itm in items.items():
                        if destino == id_item:
                            preg_i = itm['PREGUNTA']
                            G.add_node(preg_i)
                            G.add_node(itm['RESPOSTA'])
                            G.add_edge(preg_i, itm['RESPOSTA'])
                            labels[(preg_i, itm['RESPOSTA'])] = id_item
                            edges_color.append('b')
                            G.add_edge(preg_alt, preg_i)
                            labels[(preg_alt, preg_i)] = a[0]
                            edges_color.append('g')
                            break


            G.add_edge(ant, preg)
            ant = preg
        G.add_node('END')
        G.add_edge(ant, 'END')




        '''G = nx.DiGraph()
        ant = e['id']
        usados = [ant]
        G.add_node(ant)
        for i, item in e['contenido'].items():
            G.add_node(item)
            if ant:
                G.add_edge(ant, item)
            ant = item
            if ant not in usados:
                usados.append(ant)
        for item in items:
            id = item['id']
            contenido = item['contenido']
            preg = contenido['PREGUNTA']
            resp = contenido['RESPOSTA']
            if id in usados:
                G.add_node(resp)
                G.add_node(preg)
                G.add_edge(preg, resp, label=id)
                usados.append(resp) if resp not in usados else None
                usados.append(id)if id not in usados else None'''
        pos = nx.spring_layout(G)
        nx.draw_circular(G, with_labels=True,
                         edge_color=edges_color)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.axis('off')
        plt.show()
        #nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G))

