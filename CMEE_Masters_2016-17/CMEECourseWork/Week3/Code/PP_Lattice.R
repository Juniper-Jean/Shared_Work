# Calum Pennington (c.pennington@imperial.ac.uk)
# Oct 2016

# Using data from the Ecological Archives of the ESA:
# Draws lattice plots by feeding interaction type, of prey mass, predator mass, and prey-predator size ratio. (Output files: Prey_Lattice.pdf, Pred_Lattice.pdf, SizeRatio_Lattice.pdf.)
# Calculates means and medians - saves to PP_Results.csv.


# A multi-panel plot allows us to compare groups.
# Like histograms, kernel density plots estimate the probability density function. Area under the curve is 1. A value's probability of being between x1 and x2 is the area between these points. Histrograms, however, plot discrete variables and are sensitive to bin size.


library(lattice)
library(plyr)
# Load a package that is not included by default when you run R.
# 'lattice' graphics automatically make groups within plots, or separate panels for each group.
# It is very customisable. The vocab to do this is hard but there is a book and responsive team on the R help forum.
# To read about it: help(package = lattice).

EcolArchives <- read.csv("../Data/EcolArchives-E089-51-D1.csv")
# Import data from a csv, store as a dataframe 'EcolArchives'.

dim(EcolArchives)
str(EcolArchives)
head(EcolArchives)
# See size, structure, first part of dataframe.

EcolArchives$PreyPredRatio <- EcolArchives$Prey.mass / EcolArchives$Predator.mass
dim(EcolArchives)
head(EcolArchives$PreyPredRatio)
# Make a column of prey-predator size ratio.
# Check new column.

pdf("../Results/Pred_Lattice.pdf", 11.7, 8.3)
print(densityplot(~log(Predator.mass) | Type.of.feeding.interaction, data=EcolArchives,
            xlab="log Body mass(Kg)",
            main="Distribution of Predator Masses by Feeding Interaction Type"))
dev.off()
# Open and name a new pdf.
# To save a plot, specify the 'device'. We want to save to a pdf (the default is the computer screen).
# Specify height and width in inches.
# Plot kernel density as a function of body mass, given feeding interaction type.
# Take the log of body mass.
# Label x axis and title the plot.
# Close the pdf device.
# Got an error > 'print' ensures the whole command is kept together and you can use the command in a script.

pdf("../Results/Prey_Lattice.pdf", 11.7, 8.3)
print(densityplot(~log(Prey.mass) | Type.of.feeding.interaction, data=EcolArchives,
            xlab="log Body mass(Kg)",
            main="Distribution of Prey Masses by Feeding Interaction Type"))
dev.off()
# Plot kernel density as a function of prey body mass, given feeding interaction type.
# Save to a pdf.

pdf("../Results/SizeRatio_Lattice.pdf", 11.7, 8.3)
print(densityplot(~log(PreyPredRatio) | Type.of.feeding.interaction, data=EcolArchives,
            xlab="log Size ratio",
            main="Distribution of Prey-Predator Size Ratios by Feeding Interaction Type"))
dev.off()
# Plot kernel density as a function of prey-predator size ratio, given feeding interaction type.
# Save to a pdf.

Stats <- ddply(EcolArchives, .(Type.of.feeding.interaction), summarise,
               Mean.log.predator.mass = mean(log(Predator.mass)),
               Median.log.predator.mass = median(log(Predator.mass)),
               Mean.log.prey.mass = mean(log(Prey.mass)),
               Median.log.prey.mass = median(log(Prey.mass)),
               Mean.size.ratio = mean(log(PreyPredRatio)),
               Median.size.ratio = median(log(PreyPredRatio))
               )
# For each feeding interaction type, calculate mean and median:
# - prey and predator mass
# - size ratio.
# 'summarise', in conjunction with ddply, makes a dataframe. Each calculation is added as a column, with a specified name.
# To round the results to a number of decimal places: round(mean(log(Predator.mass)), 2). I did not use this, as mass was measured to a high precision.

write.csv(Stats, "../Results/PP_Results.csv", row.names = FALSE)
# Export the dataframe to a new file. Do not include row names (these are generic). Column names are included by default.