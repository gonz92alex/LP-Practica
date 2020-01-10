import pickle
import sys

import matplotlib.pyplot as plt
import networkx as nx
from antlr4 import *
from antlr4.InputStream import InputStream
from compilador import EnquestesLexer, EnquestesParser, EnquestesVisitor

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
    plt.clf()
