# Calum Pennington (c.pennington@imperial.ac.uk)
# Oct 2016

# This script shows how to run functions with 'try()', to "catch" errors (useful for debugging).

x <- rnorm(50) #Generate your population
doit <- function(x){
  x <- sample(x, replace = TRUE)
  if(length(unique(x)) > 30) { #only take mean if sample was sufficient
    print(paste("Mean of this sample was:", as.character(mean(x))))
    }
  else {
    stop("Couldn't calculate mean: too few unique points!")
    }
  }
# 'x' is a vector of 50 normal random numbers.
# Make and name a function, which has an argument 'x'.
# Take a sample, size x, with replacement. **How big is the sample?
# If the number of unique elements in x is > 30 (i.e. the sample is representative), print the sample's mean.
# Otherwise, stop the function and print a string.
# ('unique()' returns a vector with duplicates removed - extracts unique elements.)

## Try using "try" with vectorization:
result <- lapply(1:100, function(i) try(doit(x), FALSE))
# Apply a function to each object in a vector of numbers 1-100. The function is 'doit', with an argument 'x' (previously defined).
# 'try()' runs an expression that may fail - it catches errors and keeps going.
# Error messages are printed, but there is an option to suppress them. 'FALSE' ensures them are not suppressed.
# Makes a list of 100 objects - either sample means of x, or, if the sample wasn't sufficient, the function's error message.

## Or using a for loop:
result <- vector("list", 100) #Preallocate/Initialize
for(i in 1:100) {
  result[[i]] <- try(doit(x), FALSE)
  }
# Make a list with 100 empty objects.
# Iterate over each list index.
# For each index, evaluate 'doit', with argument 'x' (defined previously). Trap any errors that occur.
# Add the output to index i of 'result'.
# Makes a list of 100 objects - either sample means of x, or, if the sample wasn't sufficient, the function's error message.