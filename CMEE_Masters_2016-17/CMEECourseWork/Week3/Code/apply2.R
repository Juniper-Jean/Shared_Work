# Calum Pennington (c.pennington@imperial.ac.uk)
# Oct 2016

# Shows how to use 'apply()' with your own function, instead of inbuilt functions

SomeOperation <- function(v){
  if (sum(v) > 0){
    return (v * 100)
  }
  return (v)
}
# If the sum of 'v' is > 0, return v * 100.
# Otherwise, return v.

M <- matrix(rnorm(100), 10, 10)
# Make a matrix, 'M', 10 by 10 with 100 random deviates from the normal distribution (100 normally distributed random variables).

print (apply(M, 1, SomeOperation))
# Apply the function, 'SomeOperation', to each row in M.
# 
# Return the matrix with the value of objects *100, if the sum of their row is > 0.
# Will be sum of whole column - as 1, go by row

# ** How is the function applied across the matrix? Not output I expected
# What is 'v' read as?