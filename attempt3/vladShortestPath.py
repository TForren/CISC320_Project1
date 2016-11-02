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
	
	end = start + duration
	if end > 24:
		end -= 24	
	if start >= 18 and end >= 18: #starts in pm and ends in pm
		result = True
	if start <= 6 and end <= 6: #starts and ends in pm
		result = True
	if start >= 18 and end <= 6: #starts in pm and ends in am
		result = True
	#else all others are invalid
		 
	return result

#isEarlier
#returns true if hour1 comes before hour 2
def isEarlier(hour1,hour2):
	result = False	
	#print "comparing hours", hour1, hour2
	if hour1 >= 18 and hour1 <= 24:
		if hour2 <= 6:
			result = True
		elif hour1 < hour2:
			result = True
	elif hour1 <= 6 and hour2 <= 6:
		if hour1 < hour2:
			result = True	
	return result

#calcBloodUsage
#determines if we have to wait for the next day to leave
def calcBloodUsage(startTime, departureTime):
	result = 0
	#print "calculating blood usage with", startTime, departureTime
	if startTime == departureTime:
		result = 0
	elif isEarlier(departureTime, startTime):
		result = 1
	#print "bloodusage:", result
	return result
#bestLocalEdge
#determines the better edge to pick between two stations
def bestLocalEdge(graph, stationData, u, neighbor):
	startTime = stationData[u][0]
	startBlood = stationData[u][1]
	edges = graph[u][neighbor]
	result = None
	bestBloodUsage = float('inf')
	bestEndTime = 6
	for edge in edges:
		departureTime = edges[edge]["weight"]
		duration = edges[edge]["length"]
		endTime = departureTime + duration
		bloodUsage = calcBloodUsage(startTime, departureTime) + stationData[u][1]
		if endTime > 24:
			endTime -= 24
		if bloodUsage < bestBloodUsage:
			result = (endTime, bloodUsage)
			bestBloodUsage = bloodUsage
		elif bloodUsage >= bestBloodUsage:
			if isEarlier(endTime, bestEndTime):
				result = (endTime, bloodUsage)
				bestEndTime = endTime
	return result
 
def getBestStation(stationData,Q):	
	bestStationData = (float('inf'),float('inf'))
	bestStation = None
	for station in Q:
		stationEndTime = stationData[station][0]
		stationBloodUsage = stationData[station][1]
		if stationBloodUsage < bestStationData[1]:
			bestStation = station
			bestStationData = stationData[station]
		elif stationBloodUsage >= bestStationData[1]:
			if isEarlier(stationEndTime,bestStationData[0]):
				bestStation = station
				bestStationData = stationData[station]
	return bestStation

#isBetterResult
#takes in a new found edge result end time and blood cost
#determines if this is better than what we already know 
def isBetterResult(bestLocalEdgeResult, knownEdgeResult):
	newFoundEnd = bestLocalEdgeResult[0]
	newFoundBloodCost = bestLocalEdgeResult[1]
	knownEnd = knownEdgeResult[0]
	knownBloodCost = knownEdgeResult[1]
	result = False
	if newFoundBloodCost < knownBloodCost:
		result = True
	elif newFoundBloodCost >= knownBloodCost:
		if isEarlier(newFoundEnd,knownEnd):
			result = True
	return result
#vladkstras
#takes in a directed weighted graph, start, and end node
#returns needed blood bags in system out
def vladkstras(graph,start,end):
	result = "There are no paths that Vlad can take."
	stations = graph.nodes()
	stationData = dict() #{ L: [12,0], R: [24, 0]  }
	prev = dict()
	for station in stations:
		stationData[station] = (float('inf'),float('inf'))
		prev[station] = None
	stationData[start] = (18,0)
	Q = set(stations)
	while len(Q) > 0:
		u = getBestStation(stationData,Q) #get the best station that's still in Q
		#mark u as known??
		Q.remove(u)
		neighbors = graph.neighbors(u)
		
		for neighbor in neighbors:
			bestLocalEdgeResult = bestLocalEdge(graph, stationData, u, neighbor)
			#print "bestLocalEdge to", neighbor,bestLocalEdgeResult
			if isBetterResult(bestLocalEdgeResult, stationData[neighbor]):
				#print "bestLocalResult", bestLocalEdgeResult, "from", u,"to", neighbor
				stationData[neighbor] = bestLocalEdgeResult
				prev[neighbor] = u

		result = "Vlad will need "+ str(stationData[end][1])+ " litre(s) of blood"
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
		    trainGraph = nx.MultiDiGraph()
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
