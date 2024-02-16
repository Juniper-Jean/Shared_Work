# Calum Pennington (c.pennington@imperial.ac.uk)
# Oct 2016

# Maps locations from which there is data in the Global Population Dynamics Database (GPDD).

# install.packages("maps")
library(maps)

load("../Data/GPDDFiltered.RData")
# Load an R data file.

str(gpdd)
head(gpdd)
# Show the structure and top of the data.

pdf('../Results/GPDD_Map.pdf')

map('world', resolution=0)
# ?map
# 'map()' draws lines and polygones as specified by a map database.
# 'world' names the database.
# 'resolution=0' - draw the map to the full resolution of the database.

# To colour the land and ocean differently:
# map('world', regions='.', fill=T, col='white', bg='lightblue')
# 'regions=' - character vector that names the polygons to draw. Here, I did not specify a region, so the world's land is one polygon.
# 'fill=' - whether to draw lines or fill areas.
# 'col='
#   A vector of colours.
#   Specifies the line colour, if 'fill' is FALSE. (Only the first colour is used; the others are ignored.)
#   Otherwise, the colours are matched to polygons.
# 'bg=' - background colour. 'fill=T', to colour just the ocean. Otherwise this colours the whole map.

points(gpdd$long, gpdd$lat, pch=19, col="red", cex=0.35)
# 'points()' adds, to the last plot, a sequence of points at the specified x, y coordinates.
# x is longitude, y latitude. I.e. each point is a location from which there is data in the GPDD.
# 'pch=' - point shape
# 'cex=' - size

title(main = 'Locations from which there is data in the GPDD',
      font.main=1, # Specify font of main title.
      line = 3) # Place title this many lines out from the plot edge.

dev.off()

# The maps shows that most GPDD data is from the UK and west coast of North America. With two exceptions, there are no data from outside Europe and North America. Thus, we could not use this data to draw conclusions about global population dynamics.
# If, for example, we studied the impact of climate or humans on global population dynamics, there would be a bias for temperate, developed regions.
# Given the species in the GPDD, we could draw conclusions about individual populations. There do not seem to be species with big ranges, where this location bias may suggest we do not have a representative population sample.

# There also seems to be a bias for coastal habitats, but on close inspection, this is only in the US.
# map('world', region='UK', resolution=0)
# points(gpdd$long, gpdd$lat, pch=19, col="red", cex=0.35)
# 
# map('world', region='Canada', resolution=0)
# points(gpdd$long, gpdd$lat, pch=19, col="red", cex=0.35)
# 
# map('state', interior=F)
# points(gpdd$long, gpdd$lat, pch=19, col="red", cex=0.35)
# 'interior=F' - do not draw interior segments


# The map is useful to show locations from which there is data.
# colour by species, legend - but 72 species
# length(unique(gpdd$common.name))
# Heat map
# Density