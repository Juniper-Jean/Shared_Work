# Calum Pennington (c.pennington@imperial.ac.uk)
# Oct 2016
# This script calculates heights of trees in the data file, 'trees.csv'.

TreeData <- read.csv("../Data/trees.csv") # Import data from a file to a dataframe.
ls() # Check the dataframe was made.
head(TreeData) # Print the top of the dataframe.
dim(TreeData)

# This function calculates tree height from the angle of elevation and distance from the base.
TreeHeight <- function(degrees, distance){
# 'TreeHeight' is a function with 2 arguments.
  
  radians <- degrees * pi / 180
  height <- distance * tan(radians)
  # Each argument is used to calculate a value, 'radians' or 'height'.
  
  print(paste("Tree height is:", height)) # Print a string and the tree height.
  
  return (height) # This allows 'height' to be passed to other functions.
} # End of function.

TreeHeight(37, 40) # Test the function.

TreeData[,"TreeHeight.m"] <- TreeHeight(TreeData[3], TreeData[2])
dim(TreeData)
TreeData$TreeHeight.m
# Pass, to 'TreeHeight' function as arguments, data in dataframe column 2 and 3.
# Data in the same row are passed as a pair of arguments. Each row is passed separately (R iterates over each row).
# Store outputs as a new column, 'TreeHeight.m', in 'TreeData'.
#   This can be broken down into 2 steps:
#   names(TreeData[4] <- c(TreeHeight.m)) # Make and name a new column.
#   ?names
#   TreeData[4] <- TreeHeight(TreeData[3], TreeData[2]) # Add function outputs to the new column.
# Check new column.

write.csv(TreeData, "../Results/TreeHts.csv", row.names = FALSE)
# Export the updated dataframe to a new file. Do not include row names (these are generic). Column names are included by default.