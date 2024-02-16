#!/usr/bin/python

"""
		Plot a snapshot of a food web graph/network.
		
		Needs: Adjacency list of who eats whom (consumer name/id in 1st
		column, resource name/id in 2nd column), and list of species
		names/ids and properties such as biomass (node abundance), or average
		body mass.
		
"""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import networkx as nx
import scipy as sc
import matplotlib.pyplot as plt
# import matplotlib.animation as ani #for animation
#		- allows assembling networks in real time
#		Here, output is a static network.
# Output is a static network

def GenRdmAdjList(N = 2, C = 0.5):
	"""
	Generate random adjacency list given N nodes with connectance
	probability C
	"""
	Ids = range(N)
	ALst = []
	for i in Ids:
		if sc.random.uniform(0,1,1) < C:
			Lnk = sc.random.choice(Ids,2).tolist()
			if Lnk[0] != Lnk[1]: #avoid self loops
				ALst.append(Lnk)
	return ALst
# Give every node an ID.
# For each node
#		Draw a random number between 0 and 1 from a uniform distribution.
# 	If it is < C (0.5) - 50% chance of generating a link
#		'sc.random.choice()' generates a random sample from an array.
#		Pick 2 random IDs. Store them as a list.
#		Ensure the same ID was not picked twice. Add the IDs to 'ALst'.
# Randomly generates connectance among nodes.

## Assign body mass range
SizRan = ([-10,10]) #use log scale

## Assign number of species (MaxN) and connectance (C)
MaxN = 30
C = 0.75

## Generate adjacency list:
AdjL = sc.array(GenRdmAdjList(MaxN, C))

## Generate species (node) data:
Sps = sc.unique(AdjL) # get species ids
Sizs = sc.random.uniform(SizRan[0],SizRan[1],MaxN) # Generate body sizes (log10 scale)
# 'sc.unique()' returns the unique elements of an array. Return each unique ID in 'AdjL' (exclude repeats).
# 

###### The Plotting #####
plt.close('all')

## Plot using networkx:

# Calculate coordinates for circular configuration:
# (See networkx.layout for inbuilt functions to compute other types of node
# coords)
pos = nx.circular_layout(Sps)

G = nx.Graph() # A graph stores nodes and edges.
G.add_nodes_from(Sps)
G.add_edges_from(tuple(AdjL)) # An edge is a link.

NodSizs= 10**-32 + (Sizs-min(Sizs))/(max(Sizs)-min(Sizs))
# Node sizes in proportion to body sizes
# 'Sizs' is an array. Note 'min()'/'max()' functions.

nx.draw(G, pos, node_size = NodSizs*1000)
# ?nx.draw
# (Node size is body size in log space.
# Body sizes tend to be log-normally distributed - skewed to lots of small values.
# Here, you cannot plot in normal scale, as big nodes would blot out small ones.)

plt.show()
