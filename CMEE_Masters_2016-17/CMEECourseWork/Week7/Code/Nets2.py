import csv
import networkx as nx
import scipy as sc
import matplotlib.pyplot as plt


## Adjacency list
f = open('../Data/QMEE_Net_Mat_edges.csv','rb')
csvread = csv.reader(f)

temp = []
csvread.next()
for row in csvread:
	temp.append(tuple(row))

f.close()

Edges = sc.array(temp)

## Node data
g = open('../Data/QMEE_Net_Mat_nodes.csv','rb')
csvread2 = csv.reader(g)

temp2 = []
csvread2.next()
for row in csvread2:
	temp2.append(row[0])

g.close()

Nodes = sc.array(temp2)
