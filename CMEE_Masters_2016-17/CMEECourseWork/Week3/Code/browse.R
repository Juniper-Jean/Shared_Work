# Calum Pennington (c.pennington@imperial.ac.uk)
# Oct 2016

# A script to practice using 'browser()'.
# 'browser()' allows you to "single-step" through code (useful for debugging).

# ?browser

Exponential <- function(N0 = 1, r = 1, generations = 10){
  # Runs a simulation of exponential growth
  # Returns a vector of length generations
  
  N <- rep(NA, generations) # Creates a vector of NA
  
  N[1] <- N0
  for (t in 2:generations){
    N[t] <- N[t-1] * exp(r)
         browser()
  }
  return (N)
}
# rep(x, times) - replicate the values in x.
# Give index 1 of N a new value, 'N0'.
# Iterate over indices 2-generations in N.
# Give the current index a new value - e times the previous index's value.
# Return the updated N.
# Returns y values of the natural exponential function, for x values from 0 to 'generations' - an exponential series.

plot(Exponential(), type="l", main="Exponential growth")
# Plots the natural exponential function.
