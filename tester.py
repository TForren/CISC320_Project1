import networkx as nx
import sys

f = open(sys.argv[1])
routesFile = f.read()
f.close()

print routesFile[0]
