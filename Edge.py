class Edge:

	def __init__(self,name,v1,v2):
		self.name = name
		self.adjacent_edges = list()
		self.color = None
		self.degree = 0 
		self.v1 = v1
		self.v2 = v2


	def add_adjacent(self, edge):
		self.adjacent_edges.append(edge)
		self.degree += 1

	def set_color(self,color):
		self.color = color

	def __eq__(self,other):
		return self.name == other.name

	def __str__(self):
		return "Grana {} je boje {}".format(self.name, self.color)