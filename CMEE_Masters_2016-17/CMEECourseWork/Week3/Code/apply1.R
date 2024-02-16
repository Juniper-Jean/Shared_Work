# Calum Pennington (c.pennington@imperial.ac.uk)
# Oct 2016

# Demonstrates the 'apply()' function.
# Shows how to apply a function to an entire matrix without looping.

## apply: applying the same function to rows/colums of a matrix

## Build a random matrix
M <- matrix(rnorm(100), 10, 10)
# Make a matrix, 'M', 10 by 10, with 100 random numbers from the normal distribution.

## Take the mean of each row
RowMeans <- apply(M, 1, mean)
print (RowMeans)
# 'apply()' arguments:
#   array/matrix to which the function is applied
#   subset to which the function is applied, e.g. 1 for matrix rows
#   the function, e.g. mean.
# Print the mean of objects in each row.

## Now the variance
RowVars <- apply(M, 1, var)
print (RowVars)
# Print the variance of objects in each row.

## By column
ColMeans <- apply(M, 2, mean)
print (ColMeans)
# Print the mean of objects in each column.