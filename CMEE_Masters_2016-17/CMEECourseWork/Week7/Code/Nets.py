import networkx as nx
import scipy as sc
import matplotlib.pyplot as plt

import csv

#~ Links = sc.genfromtxt('../Data/QMEE_Net_Mat_edges.csv', delimiter=',')
#~ G = nx.from_numpy_matrix(Links[1:])
#~ View = G.edges(data = True)
#~ View
#~ list(G.edges_iter(data = 'weight'))

Raw_Links = sc.genfromtxt('../Data/QMEE_Net_Mat_edges.csv', delimiter=',')
Links = nx.from_numpy_matrix(Raw_Links[1:])
Links
Links = list(Links.edges_iter(data='weight'))
Links

f = open('../Data/QMEE_Net_Mat_edges.csv','rb')
csvread = csv.reader(f)
Names = csvread.next()

Node_names = {}
for num, name in enumerate(Names):
	Node_names[num] = name

f.close()

Links = [list(i) for i in Links] # Convert to list of lists from list of tuples.
for i in Links:
	i[0] = Node_names[i[0]]
	i[1] = Node_names[i[1]]
Links

for i in Links:
	del i[2]

Links = sc.array(Links)
Partners = sc.unique(Links)

# Size of nodes
g = open('../Data/QMEE_Net_Mat_nodes.csv','rb')
csvread = csv.reader(g)
csvread.next()

Node_Data = []
for ID, Type, PIs in csvread:
	#~ Node_Data.append([ID, PIs])
	Node_Data.append(float(PIs))

g.close()

Node_Data = sc.array(Node_Data)

plt.close('all')
pos = nx.circular_layout(Partners)
G = nx.Graph()
G.add_nodes_from(Partners)
G.add_edges_from(tuple(Links))
nx.draw(G, pos)
#~ nx.draw(G, pos, node_size = Node_Data*100)
plt.show
