# A simple R script to illustrate R input-output.

# Run line by line and check inputs outputs to understand what is happening.

MyData <- read.csv("../Data/trees.csv", header = TRUE)
# Import data from a file and store as a dataframe, 'MyData'.
# Import with headers (column names). Setting to false gives the dataframe generic column names (V1, V2, V3).

write.csv(MyData, "../Results/MyData.csv")
# Write out MyData as a new file, 'MyData.csv' in '../Results'.
# Uses the dataframe's column names.
# Puts row numbers in the first column.

write.table(MyData[1,], file = "../Results/MyData.csv",append=TRUE) # Append to it (you will get a warning!)
# Append the top row (plus column names) to the bottom of this file - does not separate with commas.

write.csv(MyData, "../Results/MyData.csv", row.names=FALSE) # write row names
# Currently, row names are stored as an unamed column. To fix this, the code exports 'MyData', without row names, overwriting the existing file.
# Shows how 'row.names=TRUE' is the default option.

write.table(MyData, "../Results/MyData.csv", col.names=FALSE) # ignore column names
# Remove column names.
# (Export dataframe without column names, overwriting existing file.)

# Cannot discern a difference between 'write.csv' and 'write.table' - using help on both directs to the same page.