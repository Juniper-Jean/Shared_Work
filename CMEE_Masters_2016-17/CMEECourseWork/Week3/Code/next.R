# Calum Pennington (c.pennington@imperial.ac.uk)
# Oct 2016

# Shows how to skip to the next iteration of a loop, using 'next'.

# Prints odd numbers between 1 and 10.
for (i in 1:10) {
  if ((i %% 2) == 0)
    next # pass to next iteration of loop
  print(i)
}
# Iterate over each number 1-10.
# If i/2 = 0, i.e. i is even, skip to the next number.
# Otherwise, print the number.