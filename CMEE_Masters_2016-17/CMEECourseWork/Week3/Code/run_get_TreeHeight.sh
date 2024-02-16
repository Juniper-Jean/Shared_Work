#!/bin/bash

# Calum Pennington (c.pennington@imperial.ac.uk)
# Oct 2016

# Runs the R script, 'get_TreeHeight.R'. Checks there is a correctly-named output file.
# 'get_TreeHeight.R' calculates tree heights.

# Arguments:
#		a .csv file, containing the angle of elevation and distance from the base, for each tree.
#		Only specify the file's name, not its extension or path.

echo -e "\nRunning the R script, 'get_TreeHeight.R'\n"
# Print a string to the terminal.

Rscript get_TreeHeight.R ../Data/$1.csv
# Run the R script with a file argument - the input file.

echo -e "\nChecking if output file exists...\n"
if [ -f ../Results/$1_treeheights.csv ]
	then
		echo -e "\nOutput file exists.\n"
	else
		echo -e "Cannot find output file. Check R script for errors.\n"
fi # End of 'if' statement
# Print one message if the output file exists, otherwise print another.

#exit

# Ask user y/n
# 'Have you specified a file argument?'
# n > 'The R script needs an input file. Specify this as a command line argument.'
