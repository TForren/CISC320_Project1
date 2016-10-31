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

#populateGraph
#given the 2D array of routes, populate the networkx graph
#def populateGraph(routes):
#	for route in routes:
#		trainGraph.add_edge(route[0],route[1],weight=route[2]+route[3])

def getNeighborsDict(routes):
	neighbors = {} # ('station' : [n,e,i,g,h,b,o,r,s], 'station2' : [r,t,g])
	for route in routes:
		curStation = route[0]
		curNeighbor = route[1]
		if not curStation in neighbors:
			neighbors[curStation] = [curNeighbor]
		else:
			if not (curNeighbor in neighbors[curStation]):
				neighbors[curStation] = neighbors[curStation] + [curNeighbor]
	print neighbors
	return neighbors

def getRouteLength(start, end, routes):
        result = None
        for route in routes:
                if route[0] == start:
                        if route[1] == end:
                                result = route[3]
        return result


def Dks(start,end,stations,neighbors,routes):
        distances = {} #{'a': 5, 'b': 6 }
        visited = [] # all nodes we have visited

        #init all distances from start to all other stations to large value
        for station in stations:
                distances[station] = 99999
        distances[start] = 0
        while not stations is None:
                minDist = 99999
                curStation = start
                for station in stations:
                        if distances[station] < minDist:
                                minDist = distances[station]
                                curStation = station
                stations.remove(curStation)
                visited.append(curStation)
			
                for neighbor in neighbors[curStation]:
                        dist = getRouteLength(curStation,neighbor,routes)
                        if (dist + distances[curStation] < distances[neighbor]):
                                distances[neighbor] = dist
        print visited

#parseFileLines
#takes in the contents of a route file and stores all needed information
#in global variables
def parseFileLines(fileLines):
	splitLine = []
	testCaseCount = 0
	routeCount = 0
	routes = []
	stations = []
	endPath = []
	for counter, line in enumerate(fileLines):
		#print line
		if (counter == 0):
		    testCaseCount = line
		    print "Loading", line, "test cases..."
		else:
		    splitLine = line.split()
		if (len(splitLine) == 1): #must be route count line.
		    routeCount = int(splitLine[0]) #record how many routes need to be recorded
		    routes = []
		    stations = []
		else:
		    if (routeCount > 0):
			#print splitLine 
			routes.append([splitLine[0],splitLine[1],int(splitLine[2]),int(splitLine[3])])
			if not splitLine[0] in stations: 
				stations.append(splitLine[0])
			if not splitLine[1] in stations:
				stations.append(splitLine[1])
			routeCount -= 1
		    elif (len(splitLine) == 2): #end of the test case. should be start and destination ["s","d"]
			print "routes:",routes
			#print "stations:",stations
			neighbors = getNeighborsDict(routes)
			print "neighborsDict:", neighbors
			Dks(splitLine[0],splitLine[1],stations,neighbors,routes)

parseFileLines(routesFile)
