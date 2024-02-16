# Calum Pennington (c.pennington@imperial.ac.uk)
# Oct 2016

# Shows how to break out of a loop when a condition is met

i <- 0 #Initialize i
while(i < Inf) {
  if (i == 20) {
    break } # Break out of the while loop!
  else {
    cat("i equals " , i , " \n")
    i <- i + 1 # Update i
  }
}
# Give 'i' value 0.
# While i is less than infinity
# if i = 20, stop the loop.
# Otherwise, print a string: 'i equals', i's value and a new line character
# give i a new value, plus 1.

# R iterates through values for i, starting with 0.
# The loop stops when i = 20.