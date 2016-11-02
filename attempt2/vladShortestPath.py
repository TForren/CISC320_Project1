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

	if hour2 == float('inf'):
		return True 
	if hour1 >= 18 and hour1 <= 24:
		if hour2 <= 6:
			result = True
		elif hour1 < hour2:
			result = True
	elif hour1 <= 6 and hour2 <= 6:
		if hour1 < hour2:
			result = True	
	return result

#minDist
#takes in a dictionary of blood distances and the current Q of nodes
#returns the node with the smallest value in distances
def minDist(stationData,Q):
	smallest = float("inf")
	result = None
	for curNode in Q:
		nodeEnd = stationData[curNode][0]
		if isEarlier(nodeEnd,smallest):
			#print "newEarliest",curNode,"with end time of", nodeEnd
			result = curNode
			smallest = nodeEnd
	return result	

#calcBloodUsage
#takes the start time, and duration of trip
#returns how many litres of blood will be needed and the ending hour
def calcBloodUsage(startHour,duration,curClock):
	cost = 0
	if curClock <= 6 and startHour >= 18: #we must wait at the train station for next ride
		cost += 1
	elif curClock > startHour:
		cost += 1	
	return cost

def earliestEnd(graph, start, end, curBestTime, curBloodUsed):
	result = float('inf')
	edges = graph[start][end]
	earliestEnd = float('inf')
	bloodUsage = curBloodUsed
	
	for edge in edges:
		startTime = edges[edge]["weight"]
		duration = edges[edge]["length"]
		endTime = startTime + duration
		if endTime > 24:
			endTime -= 24
		if isEarlier(endTime, earliestEnd):
			earliestEnd = endTime
			bloodUsage += calcBloodUsage(startTime,duration,curBestTime)
	return (earliestEnd,bloodUsage)

#vladkstras
#takes in a directed weighted graph, start, and end node
#returns needed blood bags in system out
def vladkstras(graph,start,end):
	result = "There are no paths that Vlad can take."
	stations = graph.nodes()
	if not len(stations) == 0:
		stationData = dict()
		prev = dict()
		for station in stations:
			#bestTimes[station] = float("inf")
			stationData[station] = (float('inf'),float('inf'))
			prev[station] = None
		#bestTimes[start] = 18
		stationData[start] = (18, 0)
		Q = set(stations)
		while len(Q) > 0:
			u = minDist(stationData,Q) #pick next station ends the soonest
			Q.remove(u)
			if stationData[u][0] == float('inf'):
				break
			neighbors = graph.neighbors(u)
			for station in neighbors:
				curBestTime = stationData[u][0]
				curBloodUsed = stationData[u][1]
				earliestEndPath = earliestEnd(graph, u, station,curBestTime,curBloodUsed)
				if earliestEndPath[0] < stationData[station][0]:
					if earliestEndPath[1] <= stationData[station][1]:
						stationData[station] = earliestEndPath
						prev[station] = u
					
				elif earliestEndPath[0] == stationData[station][0]:
					if earliestEndPath[1] < stationData[station][1]:
						stationData[station] = earliestEndPath
						prev[station] = u
		result = "Vlad will need " + str(stationData[end][1])+ " litre(s) of blood."
		#result = stationData
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
