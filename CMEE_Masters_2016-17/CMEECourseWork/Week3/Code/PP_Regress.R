# Calum Pennington (c.pennington@imperial.ac.uk)
# Oct 2016

# Plots prey versus predator mass, by feeding interaction type and predator lifestage. Output file: 'PP_Regress_Plot.pdf'.
# Writes accompanying regression results to 'PP_Regress_Results.csv'.
# Uses data from the Ecological Archives of the ESA.

# Demonstrates
#   various 'ggplot2' customisations
#   'ddply()'.

library(plyr)
library(ggplot2)
# Load packages.

EcolArchives <- read.csv("../Data/EcolArchives-E089-51-D1.csv")
# Import data from a csv, store as a dataframe 'EcolArchives'.

p <- ggplot(EcolArchives, aes(x = Prey.mass,
                              y = Predator.mass,
                              colour = Predator.lifestage
                              )
            )
# Initialise a ggplot object.
# Specifies which variables to plot. Map x-position to Prey.mass, y-position to Predator.mass,
# and colour to Predator.lifestage. I.e. colour each level of lifestage factor differently.

q <- p + geom_point(size = I(1), shape = I(3)) +
  geom_smooth(method = "lm", fullrange = TRUE, size = 0.5) +
  scale_x_log10("Prey mass in grams") + scale_y_log10("Predator mass in grams") +
  facet_grid(Type.of.feeding.interaction ~.)
# Make a scatterplot. Specify size and shape of points.
# Fit a linear smoother. Specify the line's thickness.
# 'fullrange' - fit the line across the whole plot width.
# Log transform the axes scale.
# Lay out panels by feeding interaction type.

r <- q + theme_bw() +
  theme(legend.position = "bottom",
        aspect.ratio = 0.5, 
        text = element_text(size = 10),
        legend.title = element_text(face = "bold", size = 8),
        legend.key.size = unit(0.5, "cm"),
        panel.margin = unit(0.1, "cm") # Space between panels.
        )
# 'theme_bw()' - a theme with a white background.
# Move legend.
# Specify plot's aspect ratio (width:height).
# Specify font size of all text. (Can be more specific, e.g. 'axis.text'.)
# Font face and size of legend title.

s <- r + guides(colour = guide_legend(nrow = 1))
# Present the legend on one row.

# Useful website: docs.ggplot2.org/0.9.2.1/theme.html
# Edit facet labels with e.g. 'strip.text'.

pdf("../Results/PP_Regress_Plot.pdf", 11.7, 8.3)
print(s)
dev.off()
# Save to a pdf file.


####################
# Subsets the data by feeding interaction type, then predator lifestage.
# For each feeding type x lifestage combination, calculates a linear regression for the relationship between prey and predator mass.
# Writes the results to a csv.

LinearModel <- function(d) {
  LM <- lm(Predator.mass~Prey.mass, data = d)
  data.frame(Intercept = LM$coefficients[1],
             Slope = LM$coefficients[2],
             R.squared = summary(LM)$r.squared,
             F.statistic = anova(LM)[1,4],
             p.value = anova(LM)[1,5]
             )
  }
# Make a function, 'LinearModel', with one argument.
# For 'd', fit a linear model of prey vs predator mass.
# Return a dataframe with the model's results in one row.
# Specify columns names, e.g. 'Intercept'.
# 'lm()' only outputs the model's coefficients - intercept and slope.
# 'summary()' produces a more verbose output, which includes R^2.
# 'anova()' computes ANOVA tables for fitted models. Get the F statistic and p value here.
# Note the use of indices to extract values from stats outputs.

# Note:
#   We will run several regressions, and want to append each set of results to one dataframe. Outputs of 'lm()' and 'summary(lm())' are not conducive to this, which is why we must extract the results as above.
#   This function could be contained within the following code. But this would complicate the code; it is good practice to make a new function.

SubsettedStats <- ddply(EcolArchives, .(Type.of.feeding.interaction, Predator.lifestage), LinearModel)
# 'ddply()' - for each subset of a dataframe, apply a function then combine the results into a dataframe.
# Usage: ddply(data, .variables, function)
# .variables - variables by which to split the dataframe.
# To each feeding interaction x predator lifestage combination in 'EcolArchives', apply 'LinearModel' function.

# You should report statistics to the same precision as the original measurements.
# The following rounds our results:
# Rounded <- format(SubsettedStats, digits = 2)

write.csv(SubsettedStats, "../Results/PP_Regress_Results.csv", row.names = FALSE)
# Export the results dataframe to a new file. Do not include row names (these are generic). Column names are included by default.