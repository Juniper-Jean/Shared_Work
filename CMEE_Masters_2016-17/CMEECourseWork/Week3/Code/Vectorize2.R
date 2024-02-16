# Calum Pennington (c.pennington@imperial.ac.uk)
# Oct 2016

# This scripts shows:
# - that R is slow at running loops
# - it is quicker to apply a function to a whole matrix with vectorisation.

# rm(list=ls())

# Runs the stochastic (with gaussian fluctuations) Ricker Eqn.
stochrick<-function(p0=runif(1000,.5,1.5),r=1.2,K=1,sigma=0.2,numyears=100)
{
  #initialize
  N<-matrix(NA,numyears,length(p0))
  N[1,]<-p0
  
  for (pop in 1:length(p0)) #loop through the populations
  {
    for (yr in 2:numyears) #for each pop, loop through the years
    {
      N[yr,pop]<-N[yr-1,pop]*exp(r*(1-N[yr-1,pop]/K)+rnorm(1,0,sigma))
    }
  }
  return(N)
}

# Make a function, 'stochrick', which has 5 arguments. The arguments have default values.
# p0 is a matrix of 1000 random deviates, between 0.5 and 1.5, from the uniform distribution.

# Make a matrix, N, of NAs. N's dimensions are 'numyears' x length of p0 - 100 x 1000 by default.
# Give row 1 of N the same values as row 1 of p0.

# R iterates through every column in N. Within a column, R iterates through every row, except row 1.
# Give each cell a value using this equation.
# The equation multiplies the previous cell's value by an exponential function.

# Return the updated dataframe, N.


# Now write another code called stochrickvect that vectorizes the above 
# to the extent possible, with improved performance:

stochrickvect <- function(p0=runif(1000,.5,1.5),r=1.2,K=1,sigma=0.2,numyears=100) {
  
  N<-matrix(NA,numyears,length(p0))
  N[1,]<-p0
  
  for (yr in 2:numyears) {
    N[yr,]<-N[yr-1,]*exp(r*(1-N[yr-1,]/K)+rnorm(1,0,sigma))
  }
  
  return(N)
}

# A 'for' loop that iterates over each matrix row, applies the function to each column by default. I.e., by default, it uses vectorisation.
# Thus, the first 'for' loop, which tells R to iterate through each column, is unnecessary.
# It actually slows the function, as it stops vectorisation.
# If we want to apply a function to specific columns, this would be useful. But here, we want to apply a function to the whole matrix.

print("'Loopy' Stochastic Ricker takes:")
print(system.time(res1<-stochrick()))

print("Vectorized Stochastic Ricker takes:")
print(system.time(res2<-stochrickvect()))