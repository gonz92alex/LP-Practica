import sys
from antlr4 import *
import pickle
from EnquestesLexer import EnquestesLexer
from EnquestesParser import EnquestesParser
from antlr4.InputStream import InputStream
from EnquestesVisitor import EnquestesVisitor
import networkx as nx
import matplotlib.pyplot as plt
import importlib
enquesta_graph = importlib.machinery.SourceFileLoader('EnquestesGraph',
                                          'test.EnquestesGraph.py')
genera_graph = enquesta_graph.load_module()

if len(sys.argv) > 1:
    input_stream = FileStream(sys.argv[1], encoding='UTF-8')
else:
    input_stream = InputStream(input('? '))
lexer = EnquestesLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = EnquestesParser(token_stream)
tree = parser.root()

visitor = EnquestesVisitor()
root = visitor.visit(tree)
objests = root['objetos']
pickle.dump(objests, open('../data/modelado.p', 'wb'))
for enq in root['tipos']['ENQUESTA']:
    G = objests[enq].get_graph()
    nx.draw_circular(G, with_labels=True)
    plt.savefig('../img/{id}.png'.format(id=enq))
    plt.show()
#genera_graph.genera_graph(root)
