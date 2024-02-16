# Calum Pennington (c.pennington@imperial.ac.uk)
# Nov 2016

# Uses 'igraph' package to visualise the QMEE CDT collaboration network.

library(igraph) # Load the igraph package

rm(list = ls())

# 	ICL	UoR	CEH	ZSL	CEFAS	Nonacademic/CASE
# ICL	0	0	10	9	5	70
# UoR		0	12	0	2	76
# CEH		0	0	0	6
# ZSL		0 	0	28
# CEFAS	0	0
# Nonacademic/CASE	0

## Import edges and nodes data
links <- read.csv("../Data/QMEE_Net_Mat_edges.csv", header=T, as.is=T)
nodes <- read.csv("../Data/QMEE_Net_Mat_nodes.csv", header=T, row.names = 1)
# 'header=T' - the file's first row contains names of variables.
# 'read.csv()' converts character variables to factors, by default. 'as.is=T' stops this. Seems unneeded here, as variables in 'links' are numeric.
# 'row.names = 1' - the column that contains row names.

## Create graph object
net <- graph.adjacency(as.matrix(links), mode = "directed", weighted=TRUE, diag=F)
# 'links' is a dataframe. 'as.matrix()' makes a matrix from the values.
# 'graph.adjacency()' makes graphs from adjacency matrices.
# Options:
#   'mode = "directed"' - show direction of links.
#   'weighted=TRUE' - make links weighted.
#   'diag=F' - do not include the diagonal of the matrix. **Explain

## Test plot
# plot(net, edge.arrow.size=1, edge.curved=.1,
#      vertex.color="orange", vertex.frame.color="#555555",
#      vertex.label=V(net)$Type, vertex.label.color="black",
#      vertex.label.cex=.7) 

## Generate colors based on partner type:
colrs <- c("green", "red", "blue") # Make a vector of strings.
# V(net)$color <- colrs[V(net)$Type]
# 'V()' makes a sequence of a graph's vertices (nodes). Type/view 'V(net)'.
# Seems this code does nothing, as 'V(net)$Type' is NULL. To fix:

LookUp <- setNames(c("green", "red", "blue"), unique(nodes$Type))
LookUp # See object.
V(net)$color <- LookUp[as.character(nodes$Type)]
V(net)$color
# Make a look-up table to match types to colours.
# Note 'unique()' to skip duplicates.
# Per item in 'nodes$Type', return the corresponding match from 'LookUp'.
# Make a vector of colours, corresponding to the occurrence of partner types in 'nodes'. Note 'as.character()' ensures 'nodes' dataframe is correctly read. Not using it makes an erroneous result - I do not exactly understand why.

# Alternatively:
# V(net)$color <- as.character(nodes$Type)
# V(net)$color <- gsub('University','green',V(net)$color)
# V(net)$color <- gsub('Non-Hosting Partners','blue',V(net)$color)
# V(net)$color <- gsub('Hosting Partner','red',V(net)$color)
# 'gsub()' replace matches.
# But, replacing 'Hosting Partner' before 'Non-Hosting Partners' makes an error. I felt this code was not robust.

## Set node size based on Number of PIs:
# V(net)$size <- V(net)$Pis*0.9
V(net)$size <- 50

## Set edge width based on weight (PhD Students):
E(net)$width <- E(net)$weight
# 'E()' makes a sequence of edge IDs.

## Change arrow size and edge color:
E(net)$arrow.size <- 1
E(net)$edge.color <- "gray80"

E(net)$width <- 1+E(net)$weight/10

graphics.off()

## Plot the graph, saving to a svg file.
svg("../Results/QMEENet.svg",width=7,height=7)

plot(net, edge.curved=0, vertex.label.color="black", main='QMEE CDT Collaboration Network') 
# 'edge.curved=' specifies edge curvature. 0 means straight lines. Curve edges so ones pointing in the same direction do not overlap.
# 'vertex.label.color=' - node label colour.
# See '?plot.igraph'.

legend(x=-1.5, y=-1.1, c("University","Hosting Partner", "Non-hosting Partner"), pch=21,
       col="#777777", pt.bg=colrs, pt.cex=2, cex=.8, bty="n", ncol=1)
# Add legend.
# 'x=/y=' - legend's position.
# 'pt.bg=colrs' - colour of points (labels).
# 'pt.cex=2/cex=.8' - size of points/text.
# 'bty=' - type of box drawn around legend. Here, no box.

dev.off()