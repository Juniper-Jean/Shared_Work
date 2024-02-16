'Week3' Contents

R (statistical software with programming capabilities)
October 17-21

As this is a coursework repository, to help revision, some files are listed by topic, not alphabetically. Use 'ctrl F' to quickly look up a file.

####################
## 'Code' Directory
####################
*AutoCorr_Latex.tex - 

basic_io.R - Shows how R imports/exports data from/to files.

boilerplate.R - A simple R function - prints the type of two variables.

*DataWrang.R - 

get_TreeHeight.R - A copy of 'TreeHeight.R' with additions:
	- using 'commandArgs()', loads data from a csv file specified in the bash commandline
	- includes the input file name in the output file name (as 'InputFileName_treeheights.csv').

TreeHeight.R - Calculates the heights of trees in 'trees.csv'. Makes a new file, 'TreeHts.csv' - a copy of 'trees.csv', with a new column of heights.

*run_get_TreeHeight.sh - 

sample.R - Runs a simulation that involves sampling a population. Uses the 'sample()' function.

TAutoCorr.R - Test for correlation among temperatures in successive years of the 20th Century, for Key West, Florida.

### Control Flow ###
break.R - Shows how to break out of a loop when a condition is met, using 'break'.

control.R - Functions illustrating control statements and loops.

next.R - Shows how to skip to the next iteration of a loop, using 'next'.

### Debugging ###
browse.R - A script to practice using the 'browser()' function - allows you to single step through code.

try.R - Shows how to run functions with 'try()', to "catch" errors.

### Vectorisation ###
apply1.R - Demonstrates 'apply()' - applies a function to an entire matrix without looping.

apply2.R - Shows how to use 'apply()' with your own function, instead of inbuilt ones.

Vectorize1.R - Shows how vectorisation is faster than looping in R.

Vectorize2.R - Using 'system.time()', shows that R is slow at running loops. It is quicker to apply a function to a whole matrix with vectorisation.

### 'ggplot2' and 'plyr' Packages ###
PP_Lattice.R - For the EcolArchives data, draws lattice plots by feeding interaction type, of prey mass, predator mass, and prey-predator size ratio. Calculates means and medians.

PP_Regress_loc.R - Like 'PP_Regress.R', but subsets by location, as well as feeding interaction type and predator lifestage.

PP_Regress.R - For the EcolArchives data, plots prey versus predator mass, by feeding interaction type and predator lifestage. Writes accompanying regression results.

### 'maps' Package ###
GPDD_Map.R - Uses the 'maps' package to map locations from which there is data in the Global Population Dynamics Database (GPDD).


####################
## 'Data' Directory
####################
EcolArchives-E089-51-D1.csv - Predator-prey body mass ratios taken from the Ecological Archives of the ESA. Input for 'PP_Lattice.R' and 'PP_Regress.R'.

GPDDFiltered.RData - Locations from which there is data in the Global Population Dynamics Database. Input for 'GPDD_Map'.

KeyWestAnnualMeanTemperature.RData - Temperature in Key West, Florida, for each year of the 20th Century. Input for 'TAutoCorr.R'.

PoundHillData.csv - 

PoundHillMetaData.csv - Describes Pound Hill dataset.

trees.csv - Angle of elevation and distance from the base of tree species. Input for 'basic_io.R' and 'TreeHeight.R'.


####################
## 'Results' Directory
####################
AutoCorr_Hist.pdf - Histogram to check the Key West temperature data is normally distributed.

AutoCorr_Interpretation.pdf - Results of a test for correlation among temperatures in successive years of the 20th Century, for Key West, Florida.

AutoCorr_Scatter.pdf - Plot of temperature in a year against the previous year, for the Key West data.

GPDD_Map.pdf - Map of locations from which there is data in the Global Population Dynamics Database. Output of 'GPDD_Map.R'.

MyData.csv - 'basic_io.R' output. Used to show how R writes data to csv files.

MyFirst-ggplot2-Figure.pdf - Plot of prey versus predator mass, for the EcolArchives data.

PP_Regress_loc_Results.csv - Like 'PP_Regress_Results.csv', but for each combination of feeding interaction, predator lifestage, and location. 'PP_Regress_loc.R' output.

PP_Regress_Plot - Plot of prey and predator mass, by feeding interaction type and predator lifestage. 'PP_Regress.R' output.

PP_Regress_Results.csv - A linear regression for prey and predator mass, for each combination of feeding interaction type and predator lifestage. 'PP_Regress.R' output.

PP_Results.csv - Mean and median prey mass, predator mass, and prey-predator size ratio, by feeding interaction type. Output of 'PP_Lattice.R'.

Pred_Lattice.pdf - Kernel density plot of predator mass by feeding interaction type. Output of 'PP_Lattice.R'.

Prey_Lattice.pdf - Kernel density plot of prey mass by feeding interaction type. Output of 'PP_Lattice.R'.

SizeRatio_Lattice.pdf - Distribution of prey-predator size ratio by feeding interaction type. Output of 'PP_Lattice.R'.

TreeHts.csv - A copy of 'trees.csv', with an added column, containing heights of tree species. 'TreeHeight.R' output.

trees_treeheights.csv - Heights of tree species. Output of 'get_TreeHeight.R' run on 'trees.csv'.

### 'ggplot2' Examples ###
Girko.pdf - plotting two dataframes

MyBars.pdf - annotating plots

MyLinReg.pdf - mathematical annotation
