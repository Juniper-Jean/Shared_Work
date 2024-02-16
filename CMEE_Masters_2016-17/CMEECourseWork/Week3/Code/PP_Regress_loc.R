# Calum Pennington (c.pennington@imperial.ac.uk)
# Oct 2016

# For each location, calculates a linear regression for the relationship between prey and predator mass.
# Writes the results to a csv.
# Uses data from the Ecological Archives of the ESA.

library(plyr)
# Load packages.

EcolArchives <- read.csv("../Data/EcolArchives-E089-51-D1.csv")
# Import data from a csv, store as a dataframe 'EcolArchives'.

LinearModel <- function(d) {
  LM <- lm(Predator.mass~Prey.mass, data = d)
  data.frame(Intercept = LM$coefficients[1],
             Slope = LM$coefficients[2],
             R.squared = summary(LM)$r.squared,
             F.statistic = anova(LM)[1,4],
             p.value = anova(LM)[1,5])
  }
# Make a function, 'LinearModel', with one argument.
# For 'd', fit a linear model of prey vs predator mass.
# Return a dataframe with the model's results in one row.
# Specify columns names, e.g. 'Intercept'.
# 'lm()' only outputs the model's coefficients - intercept and slope.
# 'summary()' produces a more verbose output, which includes R^2.
# 'anova()' computes ANOVA tables for fitted models. Get the F statistic and p value here.
# Note the use of indices to extract values from stats outputs.

StatsLocation <- ddply(EcolArchives, .(Type.of.feeding.interaction, Predator.lifestage, Location), LinearModel)
# 'ddply()' - for each subset of a dataframe, apply a function then combine the results into a dataframe.
# Usage: ddply(data, .variables, function)
# .variables - variables by which to split the dataframe.
# To each combination of feeding interaction, predator lifestage, and location, apply 'LinearModel' function.

# You should report statistics to the same precision as the original measurements.
# The following rounds our results:
# Rounded <- format(SubsettedStats, digits = 2)

write.csv(StatsLocation, "../Results/PP_Regress_loc_Results.csv", row.names = FALSE)
# Export the results dataframe to a new file. Do not include row names (these are generic). Column names are included by default.