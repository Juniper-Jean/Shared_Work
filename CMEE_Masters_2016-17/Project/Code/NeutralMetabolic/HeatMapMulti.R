rm(list = ls())
graphics.off()

library(RcppCNPy)
library(reshape2)
library(ggplot2)
library(RColorBrewer)


LoadMap <- function(file_ID){
  # browser()
  
  ## Load dispersal map. To prepare it for plotting, convert it to a data frame and log-transform the probabilities.
  dispersal_map <- npyLoad(paste('AreaNoTemp_', file_ID, '.npy', sep = ''))#; tail(dispersal_map)
  reversed_map <- apply(dispersal_map, 2, rev)#; head(reversed_map)
  DF <- melt(reversed_map)
  
  #head(DF); head(reversed_map)
  colnames(DF)[1:2] <- c('Row', 'Column')
  # Which data-frame column contains the map's row indices, and which contains the map's column indices?
  
  DF$log_Probability <- log(DF$value)#; head(DF)
  # max(DF$log_Probability); min(DF$log_Probability)
  
  DF <- cbind(DF, mass = rep(file_ID, 900))
  # Add a column of factor levels. To make a multi-panel plot (aka facet grid) with `ggplot`, you must associate the different data sets with a factor level.
  
  return(DF)
}

DF1000 <- LoadMap('1000')
DF100 <- LoadMap('100')
DF10 <- LoadMap('10')
head(DF10)

DF <- rbind(DF1000, DF100, DF10) # Combine the data frames by row.
head(DF)

# DF_Temp <- LoadMap('Temp')
# DF_NoTemp <- LoadMap('NoTemp')
# DF <- rbind(DF_Temp, DF_NoTemp) # Combine the data frames by row.
# head(DF)


## Make plot
palette_fn <- colorRampPalette(rev(brewer.pal(11, 'RdYlBu')))
# Make a colour palette.

p <- ggplot(DF, aes(x = Column, y = Row, fill = log_Probability)) + geom_tile() +
  scale_fill_gradientn(colors = palette_fn(900),
                       limit = c(-14, 0)) # Don't fill tiles with a log probability < -14 (~= 8*10**-7 ~= 1 in a million chance).

p <- p + facet_wrap(~mass)

p <- p + scale_x_continuous(breaks = seq(1, 30, 5), labels = seq(0, 29, 5), expand = c(0, 0)) +
  scale_y_continuous(breaks = seq(5, 30, 5), labels = seq(25, 0, -5), expand = c(0, 0))
# Align axis labels so they point to the correct [row, column] index (tile) in the plotted map.

p <- p + geom_point(aes(x = 15, y = 30, color = 'black', fill = max(DF$log_Probability))) + scale_color_manual(values = 'black', name = '', labels = 'destination cell')
# Highlight the destination cell with a black dot.
# Example destination cell is [row, column] [14, 14]:
  # Indices start at 0 in Python, but 1 in R. So, a destination column 14 in Python, becomes 15 in R.
  # Row index (y value) 0 is the mountain top, but 0 is usually at the bottom of a plot. So, I flip the y axis - row indices are reversed - destination row 14 has y coordinate 16 on the plot.

p <- p + labs(fill = 'log Probability\n') + ylab('Row (Altitude)') +
  theme(legend.text = element_text(size = 15),
        legend.title = element_text(size = 15, face ='bold'),
        axis.text = element_text(size = 15),
        axis.title = element_text(size = 15),
        # Title the legend and y-axis.
        # Enlarge their text.
        
        aspect.ratio = 1, # Make the plot panels square.
        strip.text = element_text(size = 15),
        
        legend.key.size = unit(2, 'line'),
        legend.position = 'bottom',
        legend.justification = c(0.5, 0)
        # Enlarge and move the legend.
        )

# pdf('TempVsNoTemp_Top.pdf')
p
# dev.off()

max(DF$log_Probability); min(DF$log_Probability)