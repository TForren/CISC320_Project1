
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


