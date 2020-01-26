from Edge import Edge
import random
#import pydot
import os
from graphviz import Graph

#os.environ["PATH"] += os.pathsep + '/usr/local/lib/python3.6/dist-packages/graphviz/'


filename = "graf1.txt"
graph = list() #lista ciji je element grana i njena dva cvora
edges = list()
visited = list()
solution = list()
colors = list()
#colors.append(1) #Na pocetku imam barem 1 boju

def read_input(): #ucitavamo podatke
	data = open(filename, "r")
	for line in data:
		edge, v1, v2 = line.split(",")
		v1 = int(v1)
		v2 = int(v2)
		graph.append([edge,v1,v2])

	return graph

def add_adjacent_edges():
	for edge in edges:
		for edge2 in edges:
			if (edge2.name != edge.name) and (edge2.v1 == edge.v1 or edge2.v2 == edge.v2 or edge2.v2 == edge.v1 or edge2.v1 == edge.v2):
				edge.add_adjacent(edge2) #ubacujemo u listu susednih grana
                
def add_if_not_in(edge_to_add):
	if edge_to_add not in visited:
		visited.append(edge_to_add)

def get_index(edge_to_find):
	for i in range(len(visited)):
		if visited[i].name == edge_to_find.name:
			return i

def try_to_color(color_to_set, edge_to_color):

	for adjacent_edge in edge_to_color.adjacent_edges:
		if adjacent_edge.color == color_to_set:
			return False
	edge_to_color.set_color(color_to_set)
	return True

def color():
	#sortiramo posecene grane prema stepenu (broju suseda) 
	visited = edges
	visited.sort(key=lambda edge: edge.degree, reverse=True)
	#not_colored = visited #Na pocetku su sve neobojene
	not_colored = [x for x in visited if x.color is None]
	random.shuffle(colors)
	
	for nc_edge in not_colored:
		
		colored = False

		for i in range(len(colors)):
			if try_to_color(colors[i], nc_edge) == True:
				colored = True
				break
			
		if colored == False:
			colors.append(colors[-1] + 1)
			nc_edge.set_color(colors[-1])
			colored = True
		

		#Druga metoda algoritma, mada ne moze sa SA da se uklopi..

		"""
		visited = edges
		visited.sort(key=lambda edge: edge.degree, reverse=True)
		not_colored = visited #Na pocetku su sve neobojene

		color_counter = 0 #Na pocetku broj boja je 0

		while not_colored:
			color_counter += 1

			first_edge_being_colored = not_colored[0]
			first_edge_being_colored.set_color(color_counter)

			not_adjacent = [x for x in not_colored if x not in not_colored[0].adjacent_edges]

			not_adjacent.remove(first_edge_being_colored)

			for edge_in_list in not_adjacent:
				try_to_color(color_counter, edge_in_list)

			not_colored = [x for x in visited if x.color is None]
		"""
		

def Solution():

	solution.clear() #Brisemo sadrzaj prethodnog resenja

	color(); #Bojimo neobojene grane

	colors.clear()

	for edge in edges: #Cuvamo resenje u listi solution
		#print("Edge " + edge.name + " has color: " + str(edge.color))
		solution.append([edge.name,edge.color])
		if edge.color not in colors: #Azuriramo listu boja (ako smo uspeli da obojimo sa manje boja nego prethodni put) 
			colors.append(edge.color)

	
	num_colors = len(colors);
	return solution, num_colors

#Okolina trenutnog resenja kao invertovanje boje neke grane
def invert():
	
	size = len(edges)//4
	
	indexes = list()
	old_colors = list()
	
	for i in range(size): 
		rand_index = random.randrange(len(edges))
		indexes.append(rand_index)
		c = edges[rand_index].color
		old_colors.append(c) #pamtimo staru boju grane rand_index
		edges[rand_index].set_color(None) #obrisali boju grane rand_index
		
   
	"""
	rand_index1 = random.randrange(len(edges))
	rand_index2 = random.randrange(len(edges))
	rand_index3 = random.randrange(len(edges))
	rand_index4 = random.randrange(len(edges))
	rand_index5 = random.randrange(len(edges))
	rand_index6 = random.randrange(len(edges))

	#Pamtimo stare boje zbog restore funkcije kao i indekse
	c1 = edges[rand_index1].color
	c2 = edges[rand_index2].color
	c3 = edges[rand_index3].color
	c4 = edges[rand_index4].color
	c5 = edges[rand_index5].color
	c6 = edges[rand_index6].color

    #Invertujemo npr 6 grana tako sto postavimo boju na None pa ih opet bojimo
	edges[rand_index1].set_color(None)
	edges[rand_index2].set_color(None)
	edges[rand_index3].set_color(None)
	edges[rand_index4].set_color(None)
	edges[rand_index5].set_color(None)
	edges[rand_index6].set_color(None)
    

	return rand_index1,rand_index2,rand_index3,rand_index4,rand_index5,rand_index6,c1,c2,c3,c4,c5,c6
	"""
	return indexes,old_colors

def restore(indexes,old_colors,colors_array,old_solution):
	for i in range(len(indexes)): 
		edges[indexes[i]].set_color(old_colors[i])
		
    

	#print("Restoring...")
	colors = colors_array #Vracamo na stare boje
	solution = old_solution

def simulatedAnnealing(maxIters):

    currValue = (FirstSolution,numF_colors) 
    #currValue = FirstSolution  

    bestValue = currValue
    i = 1
    while i < maxIters:
        indexes,old_colors = invert()
        newValue = Solution()
        print(newValue[0],newValue[1])
        if newValue[1] < currValue[1]: #ako smo uspeli sa manje boja
            currValue = newValue
        else:
            p = 1.0 / i ** 0.5
            q = random.uniform(0, 1)
            if p > q:
                currValue = newValue
            else:
                restore(indexes,old_colors,currValue[1],currValue[0]) #Nije bolje pa vracamo kako je bilo obojeno
        if newValue[1] < bestValue[1]:
            bestValue = newValue
        i += 1
        
    for edge in edges:
        for item in bestValue[0]:
            if(edge.name == item[0]):
                edge.set_color(item[1])
                
    
    
    return bestValue



graph = read_input()  
#print("Graf [grana,v1,v2] gde grana spaja cvorove v1 i v2:")   
#print(graph)

for item in graph:
	edges.append(Edge(item[0],item[1],item[2])) #Lista grana (klasa)

add_adjacent_edges() #Za svaku granu punimo listu suseda

#----------------
#Pocetno resenje (Uzecu najgore da vidim da li ce se nesto desiti)
FirstSolution = list()
i=1
for edge in edges:
	FirstSolution.append([edge.name,i])
	colors.append(i)
	i+=1
numF_colors = i-1

print("●▬▬▬▬ Pocetno resenje: ▬▬▬▬●")
print(FirstSolution,numF_colors)
print()
#----------------

#Pocetno resenje generisano algoritmom (odmah daje optimalno...)
#print("Pocetno resenje:")
#FirstSolution = Solution()
#print(FirstSolution[0],FirstSolution[1])


maxIters = 100
BestValue = simulatedAnnealing(maxIters)
print("●▬▬▬▬ Resenje simuliranim kaljenjem ▬▬▬▬●")
print(BestValue[0], BestValue[1])


#g. prikaz resenja

g = Graph('G', filename='solution.gv')#, engine='sfdp')

for edge in edges:
	g.edge(str(edge.v1), str(edge.v2),label = str(edge.color))
	print(str(edge.v1), str(edge.v2),str(edge.color))
	
#for item in BestValue


#print(g.source)

print(colors)


g.view() #Ovo nesto ne radi, ali upisuje u fajl sta treba..
