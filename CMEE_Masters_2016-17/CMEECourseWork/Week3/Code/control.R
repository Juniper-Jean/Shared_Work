# Some functions illustrating control statements and loops.

## If statement
a <- TRUE
if (a == TRUE){
  print ("a is TRUE")
} else {
  print ("a is FALSE")
}
# 'a' has a boolean value, true.
# If a is true, print a string.
# Otherwise (if a has any other value), print another string.

## On a single line
z <- runif(1) ##random number
if (z <= 0.5) {
  print ("Less than a quarter")
  }
# 'z' has a numeric value - a random number from the uniform distribution.
# If z is less than/equal to 0.5, print a string.

## For loop using a sequence
for (i in 1:100){
  j <- i * i
  print(paste(i, " squared is", j ))
}
# Loop over each integer in the range 1-100.
# 'j' has the value i^2.
# Print a concatenated string.
# Squares every number 1-100.

## For loop over vector of strings
for(species in c('Heliodoxa rubinoides',
                 'Boissonneaua jardini',
                 'Sula nebouxii'))
{
  print(paste('The species is', species))
}
# Loop over each object in a vector.
# Print a concatenated string.

## for loop using a vector
v1 <- c("a","bc","def")
for (i in v1){
  print(i)
}
# v1 has a vector value.
# For each object in the vector, print the object.

## While loop
i <- 0
while (i<100){
  i <- i+1
  print(i^2)
}
# The value of 'i' is 0.
# While i < 100, give i a new value, print i^2.
# R runs the function for the new i value, and keeps doing so until i < 100 is false.
# Prints square numbers between 1 and 10000 (100*100 = 10000).