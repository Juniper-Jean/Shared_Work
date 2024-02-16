# Plots log(field metabolic rate) against log(body mass) for the Nagy et al
# 1999 dataset to a file fmr.pdf.
# Writes the sorted list of species names to species.csv

cat("Reading CSV\n")
# Outputs a character vector to the console.

#~setwd("~/Documents/Teaching/2013_Imperial_BIG+QB/Python/Code") #set working directory
nagy <- read.csv('../Data/NagyEtAl1999.csv', stringsAsFactors = FALSE)

cat("Creating graph\n")

pdf('../Results/fmr_plot.pdf', 11, 8.5)

col <- c(Aves='purple3', Mammalia='red3', Reptilia='green3')
# Assign colours to factor levels.

plot(log10(nagy$M.g), log10(nagy$FMR.kJ.day.1),
     pch=19, # Shape of points.
     col=col[nagy$Class], # Per item in 'nagy$Class', return the corresponding colour.
     xlab=~log[10](M), # '~log[10]' - '10' will be subscript.
     ylab=~log[10](FMR))

for(class in unique(nagy$Class)){
    model <- lm(log10(FMR.kJ.day.1) ~ log10(M.g), data=nagy[nagy$Class==class,])
    abline(model, col=col[class])
}
# Fit a linear model of metabolic rate vs body mass, per class.
# 'nagy[nagy$Class==class,]', combined with the 'for' loop, subsets the data by class.
# Plot each model.

dev.off()

nagy_sorted <- arrange(nagy, nagy$Class, nagy$Order, nagy$Species)
# Order the dataframe alphabetically by class, then order and species.

write.csv(nagy_sorted, '../Results/species.csv', row.names = FALSE)

cat("Finished in R!\n")