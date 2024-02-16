# Shows how vectorization is faster than looping in R.

M <- matrix(runif(1000000),1000,1000)
# Make a matrix, called 'M', 1000 by 1000, with 1 000 000 random numbers from the uniform distribution.

# Sums all elements of a matrix
SumAllElements <- function(M){
  Dimensions <- dim(M)
  Tot <- 0
  for (i in 1:Dimensions[1]){
    for (j in 1:Dimensions[2]){
      Tot <- Tot + M[i,j]
    }
  }
  return (Tot)
}
# Make and name a function, which takes an argument 'M', the matrix.
# Assign M's dimensions to an object, 'Dimensions'.
# Give 'Tot' value 0.
# 'Dimensions[1]' is the number of rows in M, [2] the number of columns.
# 'M[i,j]' specifies that i and j are objects in M - i, a row; j, a column.
# R iterates over every column in every row.
# For each column in each row
# add to 'Tot' the value in row i, column j of 'M'. This is 'Tot''s new value.
# At the end of the loop, return 'Tot''s final value.

## This on my computer takes about 1 sec
print(system.time(SumAllElements(M)))
# Print this function's run time.

## While this takes about 0.01 sec
print(system.time(sum(M)))
# The inbuilt function, 'sum()', does the same as the last function.
# It's faster because it uses vectorization, not loops. I.e. operations are applied to the whole data structure at once, not to individuals elements.
# ('sum()' sums all values in its arguments - here, the matrix.)