import networkx as nx
import sys
import trainGraph

#f = open(sys.argv[1])
#routesFile = f.read()
#f.close()

#print routesFile[0]

trainGraph = trainGraph.trainGraph()
trainGraph.add_node('a')
trainGraph.add_node('b')
trainGraph.add_node('c')

trainGraph.add_edge('a','b',18,6)
trainGraph.add_edge('a','b',12,6)
trainGraph.add_edge('a','b',24,5)


print "nodes",trainGraph.nodes
print "edges",trainGraph.edges
print "startTimes",trainGraph.startTimes
print "duratiions",trainGraph.durations
