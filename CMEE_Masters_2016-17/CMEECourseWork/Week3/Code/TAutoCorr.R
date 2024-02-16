# Calum Pennington (c.pennington@imperial.ac.uk)
# Oct 2016

# This script tests for a correlation among temperatures in successive years.
# Uses temperature in Key West, Florida, for the 20th Century.

library(ggplot2)

load("../Data/KeyWestAnnualMeanTemperature.RData")
str(ats)
head(ats)
# Load an R data file.
# Show the structure and top of the data.

p <- ggplot(ats, aes(x = Year,
                     y = Temp)
            ) +
  labs(y = "Temperature in a year (degrees C)") +
  geom_point() +
  theme_bw()
p
# Plot data.

# Each dataframe row is a year and the year's temperature.
# I want to plot a year's temperature against the previous year's temperature. So, in each row, I need a year's temperature in one column, and the previous year's temperature in the next column.

TempN <- ats[2:100,2]
# Make a vector of all but the first row in the second column. I.e. a vector of all temperatures but that in year 1.
# is.vector(TempN) # Check it's a vector.

TempNminus1 <- ats[1:99,2]
# Make a vector of all but the last row in the second column. I.e. a vector of all temperatures but that in the last year.

# YearVsPrev <- cbind(TempN, TempNminus1)
# Make a matrix, where each of the above vectors is a column.
# Unneeded for this script but left in as it is useful revision.

p2 <- ggplot(data = NULL, aes(x = TempNminus1,
                              y = TempN)
             ) +
  labs(x = "\nPrevious year's temperature (degrees C)",
       y = "Temperature in a year (degrees C)\n") +
  geom_point() +
  theme_bw() +
  theme(axis.text = element_text(size = 20),
        axis.title = element_text(size = 25),
        axis.line = element_line(colour = 'black'),
        panel.border = element_blank())

p2
# Plot the temperature in a year against the previous year.

pdf("../Results/AutoCorr_Scatter.pdf", 11.7, 8.3)
print(p2)
dev.off()
# Save plot to a pdf.

CheckNorm <- ggplot(data = ats, aes(x = Temp)) + 
  geom_histogram(bins = 15,
                 colour = "white") +
  labs(x = "\nTemperature in a year (degrees C)",
       y = "") +
  theme_bw() +
  theme(axis.text = element_text(size = 20),
        axis.title = element_text(size = 25),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.line = element_line(colour = 'black'),
        panel.border = element_blank())

CheckNorm
# Pearson's product-moment correlation assumes both variables are normally distributed.
# Check by eye.
# 'TempN' and 'TempNminus1' are subsets of one variable. So, just check this variable's distribution.

pdf("../Results/AutoCorr_Hist.pdf", 11.7, 8.3)
print(CheckNorm)
dev.off()
# Save to pdf.

CorCoef <- cor(TempN, TempNminus1, method = "spearman")
# Correlation among paired temperatures - temperature in a year and the previous year.
# Correlation coefficient
# Store as 'CorCoef'.
# cor.test(TempN, TempNminus1)

# CorCoef2 <- ats[2:100,2] %>% cor.test(ats[1:99,2])
# Do not need to make vectors of temperatures. Can pipe specific indices of the original dataframe to directly calculate correlation.
# But in this script, vectors make permuting/sampling easier (see below).


## Calculates the correlation between temperature in randomly permuted pairs of years.
Permute <- function(x) {
  PermTemp <- sample(TempNminus1, replace = TRUE)
  print(cor(TempN, PermTemp, method = "spearman"))
}
# Make a function, 'Permute', which takes an argument 'x'.
# Functions do not need arguments. But, this function does, so we can use it later in 'lapply()'.
# The function is:
# Take a sample, with replacement, from the elements of the vector, 'TempNminus1'. Store as 'PermTemp'.
# The sample size is not stated explicitly. The default is the number of items in the vector.
# Calculate the correlation between 'TempN' and 'PermTemp' - i.e. between 'TempN' and a permutation of 'TempNminus1'.
# ?sample

CorPer <- lapply(1:10000, function(y) Permute(x))
# Or: 'CorPer <- lapply(1:10000, Permute)'?
# Apply the 'Permute' function to each item in a list of integers, 1-10000.
# Repeats 'Permute' 10 000 times. Output is a list of 10 000 correlation coefficients.
# I.e. calculates and stores the correlation for 10 000 randomly permuted sets of year pairs.
# ?lapply

ListCoef <- CorPer[CorPer > CorCoef]
# From 'CorPer', list items greater than 'CorCoef'.
# Lists the coefficients that are greater than the original one.
# This can be broken down into 2 steps:
# a <- CorPer > CorCoef # Return a vector of booleans.
# b <- CorPer[a] # From 'CorPer', list items that returned TRUE in 'a'.

FractCoef <- length(ListCoef)/10000
# Calculate the fraction of coefficients that are greater than the original one.

print(paste("p-value for whether there is a significant correlation:", FractCoef))