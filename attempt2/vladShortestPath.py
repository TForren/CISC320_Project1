###########################################################################
# vladShortestPath by Teague Forren
# takes in proprietary train graph *_in.txt file
# prints out to system how many bags of blood vlad will need for each graph
# example: python vladShortestPath.py examples/sample_in.txt
###########################################################################
import networkx as nx
import sys

#globals
trainGraph = nx.MultiDiGraph() #create networkx graph
hourRange = range(18,25) + range(1,7)
f = open(sys.argv[1])
routesFile = f.readlines()
f.close()

#validateTime
#takes in start and duration hours and returns boolean if vlad can travel during it
def validateTime(start,duration):
	result = False
	if start in hourRange:
		try:
			end = hourRange[hourRange.index(start)+duration]
			result = True
		except IndexError: #end time is out of our hourRange and thus, daytime
			result = False
	return result

#minDist
#takes in a dictionary of blood distances and the current Q of nodes
#returns the node with the smallest value in distances
def minDist(bloodDists,Q):
	smallest = float("inf")
	result = None
	for curNode in Q:
		if bloodDists[curNode] < smallest:
			result = curNode
	return result	

#calcBloodUsage
#takes the start time, and duration of trip
#returns how many litres of blood will be needed and the ending hour
def calcBloodUsage(startHour,duration,curBlood,curClock):
	cost = curBlood
	endHour = hourRange[hourRange.index(startHour)+duration]
	startIndex = hourRange.index(startHour)
	
	if (startIndex < hourRange.index(curClock)):
		cost += 1	
	#if (endHour < startHour):
	#	endHour += 24
	#if (startHour < 12 and endHour > 12):
	#	cost += 1
	return (cost,endHour)

#leastBloodPathCost
#determines the path that needs the least amount of blood 
#returns a tuple (bloodCount, newClockHour)
def leastBloodPathCost(graph, start, end, curBlood, curClock):
	result = (float('inf'),float('inf'))
	edges = graph[start][end]
	for edge in edges:
		startTime = edges[edge]["weight"]
		duration = edges[edge]["length"]
		bloodEval = calcBloodUsage(startTime, duration, curBlood, curClock)
		if (bloodEval[0] <= result):
			result = bloodEval
	return result

#vladkstras
#takes in a directed weighted graph, start, and end node
#returns needed blood bags in system out
def vladkstras(graph,start,end):
	result = "There are no paths that Vlad can take."
	stations = graph.nodes()
	if not len(stations) == 0:
		bloodDists = dict()
		clockTimes = dict()
		prev = dict()
		for station in stations:
			bloodDists[station] = float("inf")
			clockTimes[station] = None
			prev[station] = None
		bloodDists[start] = 0
		clockTimes[start] = 18
		Q = set(stations)
		while len(Q) > 0:
			u = minDist(bloodDists,Q) #pick next station that needs the least blood
			Q.remove(u)

			if bloodDists[u] == float('inf'):
				break
			neighbors = graph.neighbors(u)
			for station in neighbors:
				curBlood = bloodDists[u]
				curClock = clockTimes[u]
				possiblePathCost = leastBloodPathCost(graph,u,station,curBlood,curClock)
				if possiblePathCost[0] <= bloodDists[station]:
					bloodDists[station] = possiblePathCost[0]
					clockTimes[station] = possiblePathCost[1]
					prev[station] = u
		result = "Vlad will need " + str(bloodDists[end])+ " litres of blood."
	print result

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
		if (counter == 0):
		    print line.split()[0],"test cases."
		    testCaseCount = line
		else:
		    splitLine = line.split()
		if (len(splitLine) == 1): #must be route count line.
		    routeCount = int(splitLine[0]) #record how many routes need to be recorded
		    routes = []
		    stations = []
		else:
		    if (routeCount > 0):
			routes.append([splitLine[0],splitLine[1],int(splitLine[2]),int(splitLine[3])])
			if not splitLine[0] in stations: 
				stations.append(splitLine[0])
			if not splitLine[1] in stations:
				stations.append(splitLine[1])
			routeCount -= 1
		    elif (len(splitLine) == 2): #end of the test case. should be start and destination ["s","d"]
			print "start at",splitLine[0],"and going to",splitLine[1]
			for route in routes:
				routeStart = route[2]
				routeDuration = route[3]
				if validateTime(routeStart,routeDuration): #route start is O.K.
					trainGraph.add_edge(route[0],route[1], weight=routeStart, length=routeDuration)
			vladkstras(trainGraph,splitLine[0],splitLine[1])	


parseFileLines(routesFile)
