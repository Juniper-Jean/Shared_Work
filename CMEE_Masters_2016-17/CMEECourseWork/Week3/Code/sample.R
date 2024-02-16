# Calum Pennington (c.pennington@imperial.ac.uk)
# Oct 2016

# Run a simulation that involves sampling from a population

x <- rnorm(50) #Generate your population
doit <- function(x){
  x <- sample(x, replace = TRUE)
  if(length(unique(x)) > 30) { #only take mean if sample was sufficient
    print(paste("Mean of this sample was:", as.character(mean(x))))
    }
  }
# 'x' is a vector of 50 normal random numbers.
# Make and name a function, which has an argument 'x'.
# Take a sample, size x, with replacement.
# If the number of unique elements in x is > 30 - i.e. the sample is representative
# print the sample's mean.
# ('unique()' returns a vector with duplicates removed - extracts unique elements.)

## Run 100 iterations using vectorization:
result <- lapply(1:100, function(i) doit(x))
# Apply a function to each object in a vector of numbers 1-100. The function is 'doit', with an argument 'x' (previously defined).
# Makes a list of 100 sample means of x.
# ('lappy()' requires 2 arguments: a vector, X, and the function to be applied to each element of X. lapply returns a list, the same length as X. Each element is the result of applying the function to the corresponding X element.)

## Or using a for loop:
result <- vector("list", 100) #Preallocate/Initialize
for(i in 1:100) {
  result[[i]] <- doit(x)
}
# Make a list with 100 empty objects.
# Iterate over each list index.
# For each index, run 'doit', with argument 'x' (defined previously).
# Add the output to index i of 'result'.
# Makes a list of 100 sample means of x.