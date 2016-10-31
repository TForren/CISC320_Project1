import networkx as nx
import sys
###########################################################################
# vladShortestPath
# takes in proprietary train graph *_in.txt file
# prints out to system how many bags of blood vlad will need for each graph
###########################################################################

#globals
trainGraph = nx.DiGraph() #create networkx graph

#python vladShortestPath.py sample_in.txt
f = open(sys.argv[1])
routesFile = f.readlines()
f.close()


#validateTime
#takes in start and duration hours and returns boolean if vlad can travel during it
def validateTime(start,duration):
	result = False
	hourRange = range(18,25) + range(1,7)
	if start in hourRange:
		try:
			end = hourRange[hourRange.index(start)+duration]
			result = True
		except IndexError: #end time is out of our hourRange and thus, daytime
			result = False
	return result

#minDist
#takes in a dictionary of distances and the current Q of nodes
#returns the node with the smallest value in distances
def minDist(dists,Q):
	smallest = float("inf")
	result = None
	for curNode in Q:
		if dists[curNode] < smallest:
			result = curNode
	return result	

#calcBloodUsage
#takes the current time, start time, and duration of trip
#returns how many litres of blood will be needed
def calcBloodUsage(curClock,startTime,duration):
	totalHours = 0
	bloodBags = 0
	#for i in enumerate(path):
		#nx.shortest_path_length(graph,i,i+1
	return bloodBags

#vladkstras
#takes in a directed weighted graph, start, and end node
#returns needed blood bags in system print
def vladkstras(graph,start,end):
	result = "There are no paths that Vlad can take!"
	stations = trainGraph.nodes()
	path = None
	curClock = 18
	if not len(stations) == 0:
		dist = dict()
		prev = dict()
		for station in stations:
			dist[station] = float("inf")
			prev[station] = None
		dist[start] = 0
		Q = set(stations)
		while len(Q) > 0:
			u = minDist(dist,Q)
			Q.remove(u)

			if dist[u] == float('inf'):
				break
			n = graph.neighbors(u)
			for station in n:
				alt = dist[u] + nx.shortest_path_length(graph, u, station,weight='weight')
				if alt < dist[station]:
					dist[station] = alt
					prev[station] = u
		#result = dist
		path = nx.shortest_path(graph,start,end, weight='weight')
		result = calcBloodUsage(graph,path)
	print path

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
			#neighbors = getNeighborsDict(routes)
			#print "neighborsDict:", neighbors
			print "start:",splitLine[0],"end:",splitLine[1]
			for route in routes:
				routeStart = route[2]
				routeDuration = route[3]
				if validateTime(routeStart,routeDuration): #route start is O.K.
					trainGraph.add_edge(route[0],route[1], weight=routeStart, length=routeDuration)
			vladkstras(trainGraph,splitLine[0],splitLine[1])	


parseFileLines(routesFile)
