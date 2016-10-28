import networkx as nx
import sys

###########################################################################
# vladShortestPath
# takes in proprietary train graph *_in.txt file
# prints out to system how many bags of blood vlad will need for each graph
###########################################################################

#globals
trainGraph = nx.Graph() #create networkx graph


#python vladShortestPath.py sample_in.txt
f = open(sys.argv[1])
routesFile = f.readlines()
f.close()

#clearVars
#empties the variables for the next test
def clearVars():
	splitLine = []
	routeCount = 0
	routes = []
	goal = []

#populateGraph
#given the 2D array of routes, populate the networkx graph
def populateGraph(routes):
	for route in routes:
		trainGraph.add_edge(route[0],route[1],weight=route[2]+route[3])

#parseFileLines
#takes in the contents of a route file and stores all needed information
#in global variables
def parseFileLines(fileLines):
	splitLine = []
	testCaseCount = 0
	routeCount = 0
	routes = []
	goal = []
	for counter, line in enumerate(fileLines):
		#print line
		if (counter == 0):
		    testCaseCount = line
		    print "Loading", line, "test cases..."
		    clearVars()
		else:
		    splitLine = line.split()
		if (len(splitLine) == 1): #must be route count line.
		    routeCount = int(splitLine[0]) #record how many routes need to be recorded
		else:
		    if (routeCount > 0):
			print splitLine 
			routes.append([splitLine[0],splitLine[1],splitLine[2],splitLine[3]])
			routeCount -= 1
		    else: #end of the test case. should be start and destination ["s","d"]
			goal = splitLine	
	print routes
	


parseFileLines(routesFile)
