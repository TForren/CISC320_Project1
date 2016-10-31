import collections
class trainGraph:
	def __init__(self):
		self.nodes = set()
		self.edges = collections.defaultdict(list)
		self.startTimes = {}
		self.durations = {}
	
	def add_node(self,value):
		self.nodes.add(value)
	
	def add_edge(self,source,destination,startTime,duration):
		self.edges[source].append(destination)
		self.startTimes[(source,destination)] = startTime
		self.durations[(source,destination)] = duration

