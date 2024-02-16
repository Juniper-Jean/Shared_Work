import networkx as nx
import scipy as sc
import matplotlib.pyplot as plt
import csv

../Data/QMEE_Net_Mat_edges.csv
../Data/QMEE_Net_Mat_nodes.csv

raw_links = sc.genfromtxt('../Data/QMEE_Net_Mat_edges.csv', dtype = None, delimiter = ',') #, skip_header = 1)
nodes = list(raw_links[0,:])
raw_links = sc.delete(raw_links, 0, 0)

f = open('../Data/QMEE_Net_Mat_edges.csv', 'rb')
raw_links = csv.reader(f)
nodes = raw_links.next()
type(nodes)

links = {}

for i in raw_links:
	links[] = list(i)
	for node in nodes:
	
read_nodes = sc.genfromtxt('../Data/QMEE_Net_Mat_nodes.csv', dtype = None, delimiter = ',')
nodes = {}

## Make a dictionary, to assign each node to a number
# Plotting with networkx requires nodes to be numbers.
f = open('../Data/QMEE_Net_Mat_edges.csv', 'rb')
csvread = csv.reader(f)
header = csvread.next()

nodes = {}
for number, name in enumerate(header):
	nodes[number] = name

f.close()

## Store each link as a tuple
raw_links = sc.genfromtxt('../Data/QMEE_Net_Mat_edges.csv', dtype = None, delimiter = ',', skip_header = 1)

dimensions = raw_links.shape
iterable = range(dimensions[0]) # rows?

ICL_links = raw_links[0]
for 

