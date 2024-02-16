# Calum Pennington (c.pennington@imperial.ac.uk)
# Oct 2016

# This script calculates tree heights.
# Takes a data file from the commandline.
# Data file should contain, the angle of elevation and distance from the base, for each tree.

library(tools)
# Load a package.
# Utilities in this package allow us to extract a file's name from its path and extension.

args = commandArgs(trailingOnly = TRUE)
# ?commandArgs
# 'commandArgs()' gives R access to command line arguments.
# 'trailingOnly = TRUE' - only return arguments after the first argument.
# (In the commandline, you enter a command followed by arguments, which can be files or variables. When running a script, the first argument is the script's file name. We only want to return arguments after this - i.e. inputs for the script.)
# Make a character vector, 'args', of those arguments.

# Tests if there is an argument (input file). If not, prints an error.
if (length(args)==0) {
  stop("Script needs an input file. Please specify this as a commandline argument.")
} else if (length(args)>=1) {
    TreeData <- read.csv(args[1], header=TRUE)
}
# If there is no argument after the script's file name, stop execution, and print an error message. This even prints to the bash terminal!
# Otherwise, if there's at least 1 argument, import data from a file, whose path is the first argument.
# Store data as 'TreeData'.
# (Note syntax of 'if/else' statement. 'else' is optional and evaluated if 'if(x)' is false. 'else' must be on the same line as if's closing brace.)

ls() # Check dataframe was made.
head(TreeData) # Print top of dataframe.

# This function calculates tree height from the angle of elevation and distance from the base.
TreeHeight <- function(degrees, distance){
  # 'TreeHeight' is a function with 2 arguments.
  
  radians <- degrees * pi / 180
  height <- distance * tan(radians)
  # Each argument is used to calculate a value, 'radians' or 'height'.
  
  print(paste("Tree height is:", height))
  # 'paste()' - concatenate vectors after converting to character.
  # Then print.
  # Note: later, we pass rows of arguments to the function, thus printing lots of outputs.
  # If the input file is big, this floods the console with text and slows the script.
  # So you may prefer to suppress this line.
  # I left it in, as it helped me check if the script worked, and if it didn't, where the error came from.
  
  return (height) # This allows 'height' to be passed to other functions.
} # End of function.

TreeHeight(37, 40)
# Test the function

TreeData["TreeHeight.m"] <- TreeHeight(TreeData[3], TreeData[2])
# Pass, to 'TreeHeight' function as arguments, data in dataframe column 2 and 3.
# Data in the same row are passed as a pair of arguments. Each row is passed separately (R iterates over each row).
# Store outputs as a new column, 'TreeHeight.m', in 'TreeData'.
# Note how you can name and add to a new column in one code line.

name <- basename(file_path_sans_ext(args[1]))
# Get a file's name excluding its extension and path.
# The file is the input file (from the command line).

write.csv(TreeData, file = paste("../Results/",name,"_treeheights.csv", sep = ""), row.names = FALSE)
# Save the updated dataframe to a new file. Do not include row names (these are generic). Column names are included by default.
# Name the file: 'InputFileName_treeheights.csv'. Save in the Results directory.
# 'file =' - name a file.
# 'sep = ""' - do not separate the strings (separate with nothing).
