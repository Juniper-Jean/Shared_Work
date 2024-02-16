# Calum Pennington (c.pennington@imperial.ac.uk)
# Jan 2017

# High Performance Computing Coursework

rm(list = ls())
graphics.off()

####################
# Neutral Theory Simulations
####################

# The state of the simulated system is a vector of individuals, 'community'.
# Each vector item is a number representing the individual's species.

## 1) Measures the species richness of (number of unique items in) a community.
species_richness <- function(community){
  length(unique(community))
}
# 'unique()' returns a vector but with duplicates removed.
# 'length()' gets the number of items in a vector.

# species_richness(c(1,4,4,5,1,6,1,2)) # Should return 5.
# Test 'species_richness' function.


## 2) Generates an intial state for the simulation community, with the maximum number of species.
initialise_max <- function(size){
  seq(size)
}
# With one numeric argument, 'seq()' generates a sequence 1:argument. See '?seq'.
# The argument 'size' is the community size (number of individuals).

# initialise_max(7) # Should return a vector 1:7.
# Test 'initialise_max'.


## 3) Generates an alternative intial state, with the minimum number of species (monodominance).
initialise_min <- function(size){
  rep(1, size)
}
# Replicate 1, 'size' times.

# initialise_min(4) # Should return a vector '1 1 1 1'.
# Test


## 4) Randomly chooses two different individuals from a community.
choose_two <- function(size){
  sample(size, 2, replace = F)
}
# Take a sample, size 2, from items 1:size, without replacement.
# 'replace = F' ensures the 1st and 2nd random numbers are not equal.

# ('sample()' takes a sample from items of x, but, if x has length 1 and is numeric, sampling is from 1:x.)

## Test
# choose_two(4)
# Should return one of the following vectors with equal probability: '1 2', '1 3', '1 4', '2 1', '2 3', '2 4', '3 1', '3 2', '3 4', '4 1', '4 2', '4 3'.


## 5)
# Performs one step of a simple neutral model simulation, without speciation, on a community.
# Picks an individual to die and another to reproduce to fill the gap.
# (They will not be the same individual, but they could be the same species.)
neutral_step <- function(community){
  indv <- choose_two(length(community))
  community[indv[1]] <- community[indv[2]]
  return(community)
}
# Do not confuse an index of the community vector (representing an individual) with the number in that index (representing the species of that individual).
# Thus, pass 'length(community)', not 'community', to 'choose_two'.
# 'length(community)' - community's size

# neutral_step(c(10,5,13))
# Test


## 6)
# Performs a neutral theory simulation.
# Returns a list of two vectors: a time series of species richness, and the community's state at the end.
# Arguments:
#  'initial' - initial state of a community - also determines simulation size
#  'duration' - number of time steps
#  'interval' - gap between time steps when species richness is recorded.
neutral_time_series <- function(initial, duration, interval){
  time_series <- c(species_richness(initial))
  state <- neutral_step(initial)
  for (i in 1:duration){
    state <- neutral_step(state)
    if (i %% interval == 0){
      time_series <- c(time_series, species_richness(state))
    }
  }
  return(list(time_series, state))
}
# Make a vector. The 1st item is the species richness at time 0 (the initial state).
# Perform one step of the simulation (an individual dies; another reproduces).
# For each time step, perform another step of the simulation (pass the current state to 'neutral_step'; save the output as the new state).
# At each interval, add the current species richness to 'time_series'.
# ('%%' gets the remainder after division. If 'interval' = 2, 'i %% interval' returns 0, every 2nd i. If it's 3, 'i %% interval' returns 0, every 3rd i, etc. So, in this way, we can do something at intervals between steps.)

# neutral_time_series(initial = initialise_max(7), duration = 20, interval = 2)
# Test


## 7)
# Runs a neutral model simulation and plots species richness against time.
question_7 <- function(){
  d <- neutral_time_series(initialise_max(100), 10000, 10)
  xd <- seq(0, 10000, by=10)
  yd <- d[[1]]
  plot(xd, yd, xlab = 'Time step', ylab = 'Species richness',
       cex.axis = 1.5, cex.lab = 2) # font size of axis annotations and titles
  # title(main = 'A Neutral Model Simulation',
  #       font.main=1, # Specify font of main title. '1' - plain text, not bold/italic
  #       line = 3) # Place title this many lines out from the plot edge.
  # mtext('initial state of max diversity; system size 100 individuals', line = 1) # Add text to the plot.
}
# Run a simulation:
#   - with an initial state of max diversity in a system size 100 individuals
#   - for 10 000 time steps; record the species richness every 10 steps.
# The x axis is the number of model steps. 'by=10' specifies the increment of the sequence.
# 'd[[1]]' is the time series of species richness ('d' is a list of two vectors).

## Test function; save plot
# pdf('../Results/Question_7.pdf') # Open a file to save the plot.
# par(mar = c(5,5,4,2)) # number of lines of margin on each side of the plot - bottom, left, top, right - specify so axis title is not cut off
# question_7()
# dev.off()


## 8)
# Performs one step of a neutral model with speciation.
# With probability v, replaces a dead individual with a new species.
# Otherwise the replacement is another individual's offspring.
neutral_step_speciation <- function(community, v){
  x <- runif(1, 0, 1)
  individuals <- choose_two(length(community))
  if (x >= v){
    community[individuals[1]] <- community[individuals[2]]
  } else{
    community[individuals[1]] <- max(community) + 1
  }
  return(community)
}
# Generate one random number between 0 and 1.
# Randomly choose two different individuals from the community.
# With probability 1-v, replace individual 1 with individual 2.
# With probability v, replace individual 1 with a new species.
# 'max()' returns the maxima of the input. 'max(community) + 1' ensures a new species (unique number) is generated. (The number in an index of the community vector represents an individual's species).

# neutral_step_speciation(c(10,5,13), v=0.2)
# Test


## 9) Performs a neutral theory simulation with speciation (otherwise performs like 'neutral_time_series').
# Argument 'v' is speciation rate.
neutral_time_series_speciation <- function(initial, duration, interval, v){
  time_series <- c(species_richness(initial))
  state <- neutral_step_speciation(initial, v)
  for (i in 1:duration){
    state <- neutral_step_speciation(state, v)
    if (i %% interval == 0){
      time_series <- c(time_series, species_richness(state))
    }
  }
  return(list(time_series, state))
}

# neutral_time_series_speciation(initial = initialise_max(7), duration = 20, interval = 2, v = 0.2)
# Test


## 10)
# Performs a neutral theory simulation with speciation and plots species richness against time.
# Plots two time series showing how the simulation progresses from two different initial states (community size 100).
question_10 <- function(){
  max <- neutral_time_series_speciation(initialise_max(100), 10000, 10, v = 0.1)
  # Initial state given by 'initialise_max'.
  
  min <- neutral_time_series_speciation(initialise_min(100), 10000, 10, v = 0.1)
  # Initial state given by 'initialise_min'.
  
  xd <- seq(0, 10000, by=10)
  yd_max <- max[[1]]
  yd_min <- min[[1]]
  plot(xd, yd_max,
       type = 'l', col = 'blue',
       xlab = 'Time step', ylab = 'Species richness', cex.axis = 1.5, cex.lab = 2,
       ylim = c(0,100))
  lines(xd, yd_min, col='red')
  legend('topright', # Legend location
         c('Initial state of max diversity (each individual is a unique species)',
           'Initial state of min diversity (100 individuals of the same species)'), # character vector of labels
         cex = 1.5,
         col = c('blue', 'red'), # colour of lines
         lty = c(1,1)) # line types
}

## Test function; save plot
# pdf('../Results/Question_10.pdf', 11.7, 8.3)
# par(mar = c(5,5,4,2))
# question_10()
# dev.off()


## 11) Returns the abundance of each species in a community
species_abundance <- function(community){
  x <- as.vector(table(community))
  sort(x, decreasing = T)
}
# 'table()' builds a table of counts of each factor level.
# 'as.vector()' extracts just the counts (view 'table(community)' output).
# Sort vector in descending order.

# species_abundance(c(1,5,3,6,5,6,1,1)) # Should return '3 2 2 1'.
# Test


## 12) Bins species abundances into octave classes
# (Records the species abundance distribution as an octave vector)

# The nth octave class tells you how many species have an abundance >= 2^n-1 but less than 2^n.
# E.g. the 2nd octave - how many species have an abundance of 2 or 3 individuals.
# **Explain why this is a useful way to display data

# 'abundances' - a vector - each item is a species's abundance

octaves <- function(abundances){
  bins <- floor(log2(abundances)) + 1
  max_bin <- max(bins)
  tally <- seq(0, 0, length.out = max_bin)
  for (i in bins){
    tally[i] <- tally[i] + 1
  }
    return(tally)
}
# 2^n = nlog2
# Take log2 of each abundance and round - 'floor()' rounds down to the nearest whole number. **Explain why
# Make an vector of 0s - length is the number of bins.
# ('length.out =' - length of sequence)
# Loop over items in 'bins'.
# Keep a running total
# Count (a running total - hence '+ 1') the occurence of each abundance. Save counts to the vector.

# octaves <- function(abundances){
#   bins <- floor(log2(abundances)) + 1
#   tabulate(bins)
# }

# octaves(c(100,64,63,5,4,3,2,2,1,1,1,1)) # Should return '4 3 2 0 0 1 2', in this order.
# Test


## 13) Returns the sum of two vectors.
sum_vect <- function(x,y){
  if (length(x) < length(y)){
    zeros <- rep(0, (length(y)-length(x))) # Replicate 0 a number of times equal to the difference between the vector lengths.
    x <- c(x, zeros) # Concatenate x and the vector of zeros.
  }
  if (length(x) > length(y)){
    zeros <- rep(0, (length(x)-length(y)))
    y <- c(y, zeros)
  }
  return(x + y)
}
# If x = c(1,3) and y = c(1,0,5,2), x + y would = c(2,3,6,5) - R recycles values in the shorter vector.
# To avoid this and get an accurate sum, extend the shorter vector with zeros, so the vectors are equal length.

# sum_vect(c(1,3),c(1,0,5,2)) # Should return '2 3 5 2'.
# Test


## 14)
# Runs a neutral model simulation.
# Plots the average species abundance distribution (as octaves), after a 'burn in' period of 10 000 time steps.
question_14 <- function(){
  
  ## Burn in
  # **We want to take readings after the system settles/reaches equilibrium - why?
  state <- neutral_time_series_speciation(initialise_max(100), 10000, 10, 0.1)
  # With probability 0.1, replace a dead individual with a new species.
  # Otherwise the replacement is another individual's offspring.
  # Return the community's state after 10 000 runs.
  
  abundance <- species_abundance(state[[2]])
  # 'state[[2]]' is the community's state.
  # Return the abundance (number of individuals) of each species.
  
  sum_octaves <- octaves(abundance)
  # Sort species into bins depending on abundance. Count the number of species per bin.
  
  ## Continue the simulation for a further 1000 steps, then record the species abundance distribution (as an octave vector).
  ## Repeat this 100 times. (To get a reliable mean, we run the simulation for a long time and take many readings.)
  for (i in 1:100){
    state <- neutral_time_series_speciation(state[[2]], 1000, 10, 0.1)
    abundance <- species_abundance(state[[2]])
    
    ## Sum the vectors, as we will calculate the average distribution.
    octave_i <- octaves(abundance)
    sum_octaves <- sum_vect(sum_octaves, octave_i)
    # The 1st record is stored as 'sum_octaves' (before the 'for' loop). 'sum_octaves' then becomes a running total.
  }
  
  ## Calculate, and make a bar chart of, the average species abundance distribution.
  average_octaves <- sum_octaves/101
  
  p <- barplot(average_octaves,
               ylab = 'Average number of species',
               ylim = c(0, 12), cex.axis = 1.5, cex.lab = 2)
  # mtext("At intervals during a neutral model simulation, we recorded the community's species abundance distribution.",
  #       line = 1)
  axis(1, # specify x-axis
       at = p, labels = c(1, '2-3', '4-7', '8-15', '16-31', '32-63'),
       las = 3, # vertical axis labels
       tick = F, # Do not draw tick marks and a line.
       cex.axis = 1.5)
  title(xlab = 'Abundance (number of individuals)', cex.lab = 2,
        line = 6) # Place title this many lines out from the plot.
}

## Test; save plot
# pdf('../Results/Question_14.pdf')
# par(mar = c(8,5,4,2))
# question_14()
# dev.off()


## 17)

## Per community size, calculates and plots mean species abundance distribution (as octaves)
# (We used four sizes, running 25 simulations per size.
# Species abundance distribution is a vector, where each item is the number of species with a certain abundance.
# Specifically, we sorted abundances into 'octave classes', e.g. how many species had an abundance of 2 or 3 individuals.)

question_17 <- function(){
  # Simulation results were saved as Rdata files.
  # Each file has objects of the same name - loading multiple files overwrites the objects.
  
  files_list <- list_file_names()
  
  ## For each community size, calculate and plot mean
  par(mfrow = c(2,2))
  # Initialise a multi-panel plot.
  
  mean_abundance500 <- mean_abundance(files_list, 1, 25, 500) # community size 500
  mean_abundance1000 <- mean_abundance(files_list, 26, 50, 1000)
  mean_abundance2500 <- mean_abundance(files_list, 51, 75, 2500)
  mean_abundance5000 <- mean_abundance(files_list, 76, 100, 5000)
  # Size is 500 for the first 25 files, 1000 for the next 25...
  
  return(list(mean_abundance500, mean_abundance1000, mean_abundance2500, mean_abundance5000))
}

## Lists names of result files
list_file_names <- function(){
  files_list <- list()
  
  for(i in 1:100){
    files_list <- c(files_list, paste('cluster_results_', i, '.Rdata', sep = '')) # file_path, ../Results/Cluster/cluster_result_
    # files_list <- c(files_list, paste('../Results/cpenning/Cluster_Results/cluster_results_', i, '.Rdata', sep = '')) # file_path, ../Results/Cluster/cluster_result_
    # '../Results/cpenning/Shell_Cluster/cluster_results_'
    # Overwrite 'files_list' each iteration.
  }
  
  return(files_list)
}
# Make an empty list.
# There are 100 files, named by number. Add each file to the list, by iterating through integers 1-100.

## Calculates and plots mean species abundance distribution for result files
# Input is a list of all result files, ordered by community size.
# 'first_file'/'last_file' - index of first/last file with a certain community size.
mean_abundance <- function(files_list, first_file, last_file, size){
  
  sum <- numeric()
  n <- 0
  # Make an empty vector, which we will fill with numeric values.
  # Initialise a counter.
  
  for(f in files_list[first_file:last_file]){
  # Iterate through each file name.
    
    load(f)
    # load file
    
    vector_1 <- burn_in_time / interval_oct + 1
    # For the whole simulation, including the burn in, we recorded species abundance distribution every 'interval_oct' generations.
    # Find the index of the 1st record outside the burn in, as we want a mean that excludes burn in data.
    
    ## Sum vectors
    for(vector in octaves_list[vector_1:length(octaves_list)]){
      sum <- sum_vect(sum, vector)
      n <- n + 1
      # 'sum' - a running total
      # Count the number of vectors.
      
      # We want a mean of data from all files.
      # The first 'for' loop iterates through files; the second through vectors in a file.
      # We initialise 'sum'/'n' outside the first loop. Each iteration of the second loop overwrites their value.
      # This sums and counts every vector in every file.
    }
  }
  
  mean_abundanceX <- sum / n
  
  ## Plot mean
  if(length(mean_abundanceX) < 12){
    zeros <- rep(0, (12 - length(mean_abundanceX)))
    mean_abundanceX <- c(mean_abundanceX, zeros)
  }
  # This function makes one graph.
  # Later, we plot several graphs in a multi-panel plot.
  # Make each vector the same length, so each graph has the same x-axis.
  # ('mean_abundanceX' is a vector - its length differs for each community size.)
  
  p <- barplot(mean_abundanceX,
               ylim = c(0, 20), # Specify so each graph has same y-axis.
               ylab = 'Average number of species',
               cex.axis = 0.8, # font size of axis title
               mgp = c(2, 0.6, 0)) # Move axis title and labels closer to the line (see '?par').
  
  axis(1, # specify x-axis
       at = p, labels = c(1, '2-3', '4-7', '8-15', '16-31', '32-63', '64-127', '128-255', '256-511', '512-1023', '1024-2047', '2048-4095'),
       las = 3, # vertical axis labels
       mgp = c(4, 0.2, 0), # Set so vertical labels do not overlap with title.
       tick = F, # Do not draw tick marks and a line.
       cex.axis = 0.8)
  title(xlab = 'Abundance (number of individuals)', cex.axis = 0.8,
        line = 4) # Place title 4 lines out from the plot.
  
  mtext(paste('community size: ', size, ' individuals', sep = ''), line = 1, cex = 0.8)
  # Add text to the plot.
  
  
  return(mean_abundanceX)
  # 'return()' must be last - it ends the function - code after it is ignored.
}

## Test; save plot
# pdf('../Results/Question_17.pdf')
# output_17 <- question_17()
# dev.off()


## Challenge question C

## Per community size, calculates and plots mean species richness
# (In my simulations, I recorded species richness at intervals during the burn in.)
challenge_C <- function(){
  files_list <- list_file_names()
  
  ## For each community size, calculate and plot mean
  par(mfrow = c(2,2))
  # Initialise a multi-panel plot.
  
  mean_richness500 <- mean_richness(files_list, 1, 25, 500) # community size 500
  mean_richness1000 <- mean_richness(files_list, 26, 50, 1000)
  mean_richness2500 <- mean_richness(files_list, 51, 75, 2500)
  mean_richness5000 <- mean_richness(files_list, 76, 100, 5000)
  # Size is 500 for the first 25 files, 1000 for the next 25...
  
  return(list(mean_richness500, mean_richness1000, mean_richness2500, mean_richness5000))
}

## Calculates and plots mean species richness for result files
# Input is a list of all result files, ordered by community size.
# 'first_file'/'last_file' - index of first/last file with a certain community size.
mean_richness <- function(files_list, first_file, last_file, size){
  
  sum <- numeric()
  # Make an empty vector, which we will fill with numeric values.
  
  for(f in files_list[first_file:last_file]){
    load(f)
    sum <- sum_vect(sum, time_series)
    # Iteratively load each file.
    # Sum the records.
  }
  
  mean_richnessX <- sum / 25
  # 25, as we recorded species richness once per simulation.
  
  ## Plot mean
  plot(log(mean_richnessX),
       xlab = 'generation number', ylab = 'log species richness',
       ylim = c(2, 10))
  mtext(paste('community size: ', size, ' individuals', sep = ''), line = 1, cex = 0.8)
  
  return(mean_richnessX)
}
# We can specify the x and y value of each point to plot. Here, we only specify one set of values.
# So, we plot just the value of each item in the 'mean_richnessX' vector.
# R will show this on the y-axis and automically generate x values.
# The x values will be the position of each item in the vector. So R plots, e.g., x1 = 1, y1 = 332.64 - index 1's value is 332.64.
# The max x value will be the total number of items. As we recorded species richness every generation (of the burn in), the x-axis represents generation number.

## Test; save plot
# pdf('../Results/Challenge_C.pdf')
# output_challenge_C <- challenge_C()
# dev.off()


## Challenge A

## Performs a number of Neutral Thoery simulations (community size 100, 10 000 time steps, speciation rate 0.1).
## One half of simulations have an initial state of max diversity; the other, min diversity.
## Per simulation, records a time series of species richness.
## Per initial state, plots mean species richness against time, with 97.2% confidence intervals.

# 'n' - number of simulations to run

challenge_A <- function(n){
  
  matrix_max <- matrix(0, n, 1001)
  matrix_min <- matrix(0, n, 1001)
  # Make two matrices of 0s, with n rows and 1001 columns.
  
  for(i in 1:n){
  # Do the following n times.
    
    max <- neutral_time_series_speciation(initialise_max(100), 10000, 10, 0.1)
    # Perform a neutral theory simulation.
    # (community size 100, initial state of max diversity, 10 000 time steps, speciation rate 0.1)
    # (With probability 0.1, replace a dead individual with a new species. Otherwise the replacement is another individual's offspring.)
    # Record the initial species richness, then record it every 10 steps.
    # length(max[[1]]) should = 10000/10 + 1 = 1001
    # Return a list of two vectors: a time series of species richness, and the community's state at the end.
    
    min <- neutral_time_series_speciation(initialise_min(100), 10000, 10, 0.1)
    # initial state of min diversity
    
    matrix_max[i,] <- max[[1]]
    matrix_min[i,] <- min[[1]]
    # Store the time series of species richness as a row in a matrix.
    # matrix_X[i,] - row i, all columns
    # At the end of the loop, we will have a matrix, where each row is a time series of species richness for one simulation.
  }
  
  ## Calculate and plot the mean, with 97.2% confidence intervals
  par(mfrow = c(2,1))
  # Initialise a multi-panel plot.
  
  plot(NULL, xlab = 'time step', ylab = 'species richness', cex.axis = 1.5, cex.lab = 2,
       xlim = c(0,10000), #**
       ylim = c(0,100))
  mtext('Initial state of max diversity (each individual is a unique species)', line = 1, cex = 2)
  stats_max <- calculate_stats(matrix_max, 0.972)
  # 'stats_X' is a list of vectors:
  #   mean time series
  #   lower bound (confidence interval) at each time point
  #   upper bounds.
  
  plot(NULL, xlab = 'time step', ylab = 'species richness', cex.axis = 1.5, cex.lab = 2,
       xlim = c(0,10000), ylim = c(0,100))
  mtext('Initial state of min diversity (100 individuals of the same species)', line = 1, cex = 2)
  stats_min <- calculate_stats(matrix_min, 0.972)
  
  return(c(stats_max, stats_min))
  # Merge and return the two lists.
}

## Calculates mean species richness and (on an open window) plots it against time
# Arguments:
#   'M' - a matrix, where each row is a time series of species richness for one simulation.
#   (So, each column in 'M' is a time point.)
#   'CI' (optional) - confidence intervals to plot (specify a decimal, e.g. 97.2% = 0.972)
#   The function draws a line on a plot. 'col' (optional) specifies its colour - useful if drawing multiple means on one graph.

calculate_stats <- function(M, CI = NULL, col = 'black'){
  # 'CI'/'col' have default values.
  
  ## Per time point, calculate:
  ##  mean species richness
  ##  standard error.
  mean <- apply(M, 2, mean)
  # Apply a function to each column in 'M'.
  # '2' specifies columns, not rows.
  # Vectorisation avoids a slow 'for' loop.
  
  #variance <- apply(M, 2, var)
  SD <- apply(M, 2, sd) # SD = sqrt(var)
  SE <- SD / sqrt(nrow(M)) # SE = SD / sqrt(n)
  # 'nrow(M)' = number of rows/simulations
  
  ## Plot mean
  x_data <- seq(0, 10000, by=10)
  # Generate the time points at which we recorded species richness.
  # We recorded species richness every 10 steps.
  # If we only plot the mean time series, the x-axis would show the number of recordings.
  # We want to plot species richness against time (number of steps).
  
  lines(x_data, mean,
        col = col) #
  #**
  
  ## If specified, calculate and plot confidence intervals
  if(!is.null(CI)){
    # if 'CI' is not 'NULL'
    lower_bounds <- mean - ((1 + CI) * SE) # e.g. 95% CI = mean -/+ 1.95 * SE
    upper_bounds <- mean + ((1 + CI) * SE)
    lines(x_data, lower_bounds, lty = 3)
    lines(x_data, upper_bounds, lty = 3)
    
    return(list(mean, lower_bounds, upper_bounds))
  } else {
    return(mean)
  }
}

## Test; save plot
# pdf('../Results/Challenge_A.pdf', 11.7, 12.3)
# par(mar = c(5,5,4,2))
# output_challenge_A <- challenge_A(10)
# dev.off()


## Challenge B
## Plots many averaged time series for various initial species richnesses

# 'size' - community size
# 'n_states' - number of initial states
# 'replicates' - number of simulations per initial state
challenge_B <- function(size, n_states, replicates){
  
  ## Generate initial states. Store them in a matrix, so each row is a state.
  initial_states <- matrix(0, n_states, size)
  
  for(i in 1:n_states){
    if(i == 1){
      initial_states[i,] <- initialise_min(size)
      # Generate min diversity state.
    } else{
      # richness <- (size / n_states) * i
      richness <- (size / (n_states - 1)) * (i - 1)
      richness <- floor(richness)
      # We could generate random richnesses, but they may be similar.
      # richness <- sample(1:size, 1)
      # It may be more telling to generate states spread evenly through the range of possible richnesses.
      # E.g., for 5 states and community size 100, the states would be 25, 50, 75, 100 (and 1) species.
      # A max, but not min, diversity state is always made. Thus the 'if' statement.
      # Subtract 1 from 'n_states'/i, as we previously made a state.
      # 'floor()' rounds down to the nearest whole number - we don't want richness as a decimal.
      
      initial_states[i,] <- initialise_species_richness(richness, size)
    }
  }
  
  ## **Per state, run many simulations and plot mean species richness.
  ## (Plot the many averages on one graph.)
  plot(NULL, xlab = 'time step', ylab = 'species richness', cex.axis = 1.5, cex.lab = 2,
       xlim = c(0, 10000),
       # **changed x to 10000
       # time series of 10000/10 + 1 = 1001 steps
       # (Simulations run for 10 000 steps. They record the initial species richness, then record it every 10 steps.)
       
       ylim = c(0, size)) # max number of species equals the community's size
  # an empty plot
  
  means <- apply(initial_states, 1, run_multiple, n = replicates)
  # Apply a function to each row in 'initial_states'. '1' specifies rows, not columns.
  # 'n = n_simulation' specifies the value of another argument to 'run_multiple'.
  # 'run_multiple':
  #   for a given initial state, performs n simulations
  #   returns mean species richness and (on an open window) plots it against time.
  # 'means' will be a matrix, where each row is a mean time series.
  
  return(means)
}
# Generates many initial states of various species richness.
# Per state, performs many simulations (community size 100, 10 000 time steps, speciation rate 0.1) and plots mean species richness against time.
# (Each simulation records a time series of species richness.)

## Generates an initial state for the simulation community, with any specified species richness
# 'n' - number of species
initialise_species_richness <- function(n, size){
  species <- seq(n)
  # Make a vector of species.
  
  initial_state <- seq(1:n)
  # There must be at least one individual per species.
  
  initial_state <- c(initial_state, sample(species, (size - n), replace = T))
  # The remaining individuals can take any species identity.
  # I.e., each species has a random abundance.
  
  initial_state <- sample(initial_state)
  # 'sample(x)' randomly permutates x.
  # An individual should be equally likely to take any species identity.
  # **why?
  # Without this line, the first n individuals always will be different species.
  
  return(initial_state)
}

## For a given initial state, performs n simulations (community size 100, 10 000 time steps, speciation rate 0.1)
## Returns mean species richness and (on an open window) plots it against time - calls 'calculate_stats'.
run_multiple <- function(initial, n){
  results <- replicate(n, neutral_time_series_speciation(initial, duration = 10000, interval = 10, v = 0.1)[[1]])
  # 'replicate()' repeats a function 'n' times.
  # We save all outputs to an object.
  # This object would be a list of lists, as 'neutral_time_series_speciation' returns a list (of two vectors).
  # But, using '[[1]]', we save only the first vector.
  # Thus, 'results' is a matrix (each column is a time series of species richness for one simulation).
  # (A simulation outputs a horizontal vector - it is bizarre these are stored as columns.)
  
  results <- t(results)
  # transpose matrix
  # 'calculate_stats' requires each row, not column, to represent one simulation.
  
  # mean <- calculate_stats(results, col = sample(100000:999999, 1))
  # mean <- calculate_stats(results, col = sample(colours(distinct = T), 1))
  mean <- calculate_stats(results)
  # 'calculate_stats' draws a line on an open plot - mean species richness against time.
  # You can specify line colour with '#RRGGBB' (see '?par') - we choose a random six-digit number.
  # To plot a mean for each initial state, we will call 'run_multiple' many times.
  # While not ideal, 'sample(...' should make each line (mean) a different colour.
  
  return(mean)
}

## Test; save plot
# pdf('../Results/Challenge_B.pdf', 11.7, 8.3)
# par(mar = c(5,5,4,2))
# output_challenge_B <- challenge_B(100, 10, 25)
# dev.off()


## Challenge D

## Runs a neutral model simulation using coalescence
# Arguments:
#   v - speciation rate
#   J - community size
challenge_D <- function(v, J){
  #}, rand_seed){
  # set.seed(rand_seed)
  
  lineages <- rep(1, J)
  # Initialise a vector of 1s, length J.
  
  abundances <- numeric() # an empty vector
  N <- J
  theta <- v * ((J - 1) / (1 - v))
  
  while(N > 1){
    # While N > 1, repeat the following:
    
    j <- sample(1:N, 1)
    # Randomly pick an index of 'lineages'.
    # (N - length of 'lineages')
    # (Don't use J - the length of 'lineages' changes, as does the value of N.)
    
    randnum <- runif(1, 0, 1)
    # Pick a random decimal between 0 and 1.
    
    if(randnum < (theta / (theta + N - 1))){
      abundances <- c(abundances, lineages[j])
      # Append index j of 'lineages' to 'abundances'.
      
    } else{ # if(randum >= x)
      i <- sample(1:N, 1) # **Note N, not J - explain
      # Randomly pick another index of 'lineages'.
      
      # Ensure index i and j are different.
      while(i == j){
        i <- sample(1:N, 1)
      }
      
      lineages[i] <- lineages[i] + lineages[j]
    }
    
    lineages <- lineages[-j]
    # Remove index J - 'lineage' is one item shorter.
    
    N <- N - 1
    # Subtract 1, so N still gives the length of 'lineages'.
  }
  
  # if(length(lineages) > 1){
  #   stop('lineages > 1') # return an error message
  # }
  # used to test that the code worked
  
  abundances <- c(abundances, lineages)
  # Add the only item left in 'lineages' to 'abundances'.
  
  # Calculate the species abundance distribution (as octaves)
  species_abundance_distribution <- octaves(abundances)
  # # 'abundances' - a vector - each item is a species's abundance
  
  return(list(abundances, species_abundance_distribution))
}

## Per community size:
##  runs n simulations (speciation rate 0.003617)
##  calculates and plots the mean species abundance distribution.
challenge_D2 <- function(n = 25){
  sizes <- c(500, 1000, 2500, 5000)
  
  par(mfrow = c(2,2))
  # Initialise a multi-panel plot.
  
  for(size in sizes){
    
    # Run n simulations.
    vectors <- replicate(n, challenge_D(0.003617, size)[[2]])
    
    # Calculate/plot mean.
    name <- paste('mean_abundance_', size, sep = '')
    assign(name, coalescence_calc_mean(vectors, size))
    # Save the output of each iteration to a different object.
    # 'assign()' assigns a name to a value.
  }
  
  return(list(mean_abundance_500, mean_abundance_1000, mean_abundance_2500, mean_abundance_5000))
}

# Calculates and plots mean
coalescence_calc_mean <- function(vectors, size){
  # 'vectors' - list of octave vectors
  
  sum <- numeric()
  for(i in vectors){
    sum <- sum_vect(sum, i)
  }
  
  mean_abundanceX <- sum/length(vectors)
  
  ## Plot mean
  if(length(mean_abundanceX) < 12){
    zeros <- rep(0, (12 - length(mean_abundanceX)))
    mean_abundanceX <- c(mean_abundanceX, zeros)
  }
  # Make each vector the same length, so each graph has the same x-axis.
  
  p <- barplot(mean_abundanceX,
               ylim = c(0, 25), # Specify so each graph has same y-axis.
               ylab = 'Average number of species', cex.axis = 0.8,
               mgp = c(2, 0.6, 0)) # Move axis title and labels closer to the line (see '?par').
  
  axis(1, # specify x-axis
       at = p, labels = c(1, '2-3', '4-7', '8-15', '16-31', '32-63', '64-127', '128-255', '256-511', '512-1023', '1024-2047', '2048-4095'),
       las = 3, # vertical axis labels
       mgp = c(4, 0.2, 0), # Set so vertical labels do not overlap with title.
       tick = F, # Do not draw tick marks and a line.
       cex.axis = 0.8)
  title(xlab = 'Abundance (number of individuals)', cex.axis = 0.8,
        line = 4) # Place title 4 lines out from the plot.
  
  mtext(paste('community size: ', size, ' individuals', sep = ''), line = 1, cex = 0.8)
  # Add text to the plot.
  
  return(mean_abundanceX)
}

# output_D2 <- challenge_D2()
# Test


##########
# Fractals
##########

## 19)
## Draws Sierpinski's triangle (a fractal) on an already-open plot

# Arguments:
#   A, B, C, X - each is a vector of two numbers, corresponding to graph coordinates. X is the initial position.
#   n - plot the first n points in a different colour, to help visualise how the fractal is drawn.
#   'distance' - distance of movement - default is halfway towards A, B or C
chaos_game <- function(A = c(0,0), B = c(3,4), C = c(4,1), X = c(0,0), n = 0, distance = 1/2){
  
  points(X[1], X[2], cex = 0.2)
  # Draw a small point at X.
  # 'X[1], X[2]':
  #   - X, y coordinates of points to plot
  #   - 1st and 2nd indices of the vector, X
  # 'cex' - size of points
  
  points_list <- list(A,B,C)
  for(i in 1:1000){
    random_point <- sample(points_list, 1)
    
    # Move X towards the chosen point
    X[1] <- (random_point[[1]][1] + X[1]) * distance
    X[2] <- (random_point[[1]][2] + X[2]) * distance
    
    if(i <= n){
      points(X[1], X[2], cex = 0.5, col = 'red',
             pch = 19) # Specify symbol of points
      # Emphasise the first n points.
      # (optional - skipped if n = i, as i starts at 1)
      
    } else{
      points(X[1], X[2], cex = 0.2)
    }
  }
  # Make a list of the points, A, B and C.
  # Repeat the following 1000 times:
  #   Randomly choose a point.
  #   Assign a new coordinate to X.
  #   (Specifically, assign to each index of X a new value: half the sum of the
  #   - current value
  #   - chosen point's corresponding index).
  #   Draw a point at the new X.
}

## Test function; save plot
# pdf('../Results/19_chaos_game.pdf')
# plot(NULL, # Make an empty plot.
#      xlim = c(0,5), ylim = c(0,5), # Specify its x/y limits.
#      xlab = '', ylab = '', # blank labels for axes
#      cex.axis = 1.5,
#      main = "Sierpinski Triangle", cex.main = 2,
#      font.main = 1) # Specify font of main title. '1' - plain text, not bold/italic
# chaos_game()
# dev.off()

# pdf('../Results/19_Classic_Sierpinski_Gasket.pdf')
# plot(NULL,
#      axes = F, # remove axes
#      xlim = c(0,4), ylim = c(0,4), xlab = '', ylab = '', cex.axis = 1.5,
#      main = "Classic Sierpinski Gasket", cex.main = 2, font.main = 1)
# chaos_game(A = c(0,0), B = c(2,4), C = c(4,0)) # points of an equilateral triangle
# dev.off()


## 20)
## On an already open plot, draws a line of a given length, from a given point, in a given direction.
## Returns the line's end point.
turtle <- function(start, direction, length){
  
  ## Finds the end point
  x <- start[1] + (length * cos(direction))
  y <- start[2] + (length * sin(direction))
  end <- c(x,y)
  
  ## Draws the line
  lines(c(start[1], x), c(start[2], y), type='l')
  # points(c(start[1], x), c(start[2], y))
  
  return(end)
}
# 'start' - a vector of the line's starting coordinates
# 'direction' - an angle in radians

# To find the end point, add a value to each start coordinate.
# Use trigonometry, with the line as the hypotenuse, and 'direction' an angle, of a triangle.
# For x, add the adjacent's length (= hypotenuse's length * cos(angle)).
# y, add opposite = hypotenuse * sin(angle)

# 'lines(x, y)' joins points with lines.
# Its arguments are counterintuitive: 'x' is vector of the x coords - y, y coords.
# So, use 'lines(c(x1, x2), c(y1, y2))', not 'lines(point 1, point 2)'.

## Open an empty plot and call 'turtle' with specified arguments.
# start <- c(-5,0)
# direction <- pi/4
# length <- 5
# plot(NULL, xlim = c(-10,10), ylim = c(-10,10), xlab = '', ylab = '')
# turtle(start, direction, length)


## 21) Draws two lines that join together, like an elbow
elbow <- function(start, direction, length){
  end <- turtle(start, direction, length)
  turtle(end, (direction - pi/4), (length * 0.95))
}
# Call 'turtle' - draws a line.
# Assign the line's end point to 'end'.
# Draw a 2nd line that:
#   - starts at the end of the 1st one
#   - has a direction 45 degrees to the right
#   - is 0.95 times the length.
# (A horizontal line is 0 degrees. Subtract 45 to go right.)

# elbow(start, direction, length)
# Test


## 22) Draws a spiral
spiral <- function(start, direction, length){
  end <- turtle(start, direction, length)
  spiral(end, (direction - pi/4), (length * 0.95))
}
# The basic function is to draw a line using 'turtle'.
# The function repeatedly calls itself, so draws lots of lines.
# There is no condition to stop the calls, so it is an infinite loop.
# Each time, it uses new argument values, so the next line is a different direction and length.
# The change is constant (- pi/4; * 0.95).
# As length is reduced with each call, the spiral is inwards.

## Test; save plot
# pdf('../Results/22_spiral.pdf')
# plot(NULL, xlim = c(-10,10), ylim = c(-10,10), xlab = '', ylab = '', cex.axis = 1.5)
# spiral(start, direction, length)
# dev.off()


## 23) Draws a spiral
spiral2 <- function(start, direction, length, e){
  if(length > e){
    end <- turtle(start, direction, length)
    spiral2(end, (direction - pi/4), (length * 0.95), e)
    # } else{
    #   return() # Go to the beginning of the function.
  }
}
# Like 'spiral', but only acts if it is called with a line length above a size specified by 'e'.
# 'length' gets smaller per call of 'spiral2'. Thus, to draw anything, 'e' must be smaller than the initial length.

## Test; save plot
# e <- 0.01
# pdf('../Results/23_spiral_2.pdf')
# par(mar = c(1,1,1,1)) # reduce margins
# plot(NULL, axes = F, xlim = c(-5.5,10), ylim = c(-10,5), xlab = '', ylab = '')
# spiral2(start, direction, length, e)
# dev.off()


## 24) Draws a tree
tree <- function(start, direction, length, e){
  if(length > e){
    end <- turtle(start, direction, length)
    tree(end, (direction - pi/4), (length * 0.65), e) # 45 degrees to the right
    tree(end, (direction + pi/4), (length * 0.65), e) # 45 degrees to the left
  }
}
# Draws a line.
# The function calls itself twice, drawing two more lines.
# They start at the end of the 1st line, have a different direction to it, and are smaller.
# Their directions are equal and opposite to each other, making a symmetrical, branching pattern.

# The function is recursive - it continually calls itself until you stop the process. (Here, it stops if the 'if' condition is not met.)
# So, the pattern is repeated at an ever smaller size and ever-changing angle.
# The function runs multiple times in parallel and, at each step, doubles the number of lines. (because each step initialises a further two calls)

# This draws a tree: clusters of small lines (leaves) at one end, and few, big, well-spaced lines (branches) at the other.

## Test; save plot
# start <- c(0,-5)
# direction <- pi/2 # Change 'direction', to draw an upright tree.
# pdf('../Results/24_tree.pdf')
# par(mar = c(1,1,1,1)) # reduce margins
# plot(NULL, axes = F, xlim = c(-10,10), ylim = c(-5,10), xlab = '', ylab = '')
# tree(start, direction, length, e)
# dev.off()


## 25)
fern <- function(start, direction, length, e){
  if(length > e){
    end <- turtle(start, direction, length)
    fern(end, (direction + pi/4), (length * 0.38), e)
    fern(end, (direction), (length * 0.87), e) # Draw a branch straight up.
  }
}
# Like 'tree', but, instead of right, one branch goes straight.

## Test
# start <- c(-10,-10)
# direction <- pi/4
# plot(NULL, axes = F, xlim = c(-10,20), ylim = c(-10,20), xlab = '', ylab = '')
# fern(start, direction, length, e)


## 26) Draws a fern
fern_2 <- function(start, direction, length, e, dir = -1){
  dir <- dir * -1
  if(length > e){
    end <- turtle(start, direction, length)
    fern_2(end, (direction + pi/4 * dir), (length * 0.38), e, -dir) # ** -dir
    fern_2(end, (direction), (length * 0.87), e, dir) # Draw a branch straight up.
  }
}
# Like 'fern', but the side branch's direction alternates while the function iteratively calls itself.
# Specifically:
# - 'dir' alternates between 1 and -1.
# - Drawing the side branch, multiply pi/4 by 'dir', to alternate between subtracting 45 degrees (go right) and adding (go left).

## Test; save plot
# start <- c(0,-10)
# direction <- pi/2
# length <- 2
# pdf('../Results/26_fern_2.pdf')
# par(mar = c(1,1,1,1)) # reduce margins
# plot(NULL, axes = F, xlim = c(-10,10), ylim = c(-10,7), xlab = '', ylab = '')
# fern_2(start, direction, length, e)
# dev.off()


## Challenge G

# On an already-open plot, draws a fern
# Question 26 written with as few characters as possible
challenge_G = function(){
  f=function(s,r,d,l,g){g=g*-1;if(l>0.01){x=s+l*cos(d);y=r+l*sin(d);lines(c(s,x),c(r,y));f(x,y,d+pi/4*g,l*0.38,-g);f(x,y,d,l*0.87,g)}};f(9,0,pi/2,2,-1)
}

## Test
# plot(NULL, axes = F, xlim = c(0,20), ylim = c(0,17), xlab = '', ylab = '')
# challenge_G()



####################
# Challenge F
# Experimenting with the variables of 'fern' and 'tree'
####################

## Draws a fern
challenge_F <- function(start = c(0,-10), direction = pi/2, length = 2, e = 0.01, dir = -1,
                        dc = pi/4,
                        lc = 0.38, lc2 = 0.87){ # changes to length
  
  dir <- dir * -1
  if(length > e){
    x <- start[1] + (length * cos(direction))
    y <- start[2] + (length * sin(direction))
    end <- c(x,y)
    lines(c(start[1], x), c(start[2], y))
    
    # if(length < 0.06){
    #   dc = runif(1, 0, 1)
    #   dc2 = runif(1, 0, 1)
    # }
    
    challenge_F(end, (direction + dc * dir), (length * lc), e, -dir)
    challenge_F(end, direction + pi/24, (length * lc2), e, dir)
    # pi/24 makes a curved fern
  }
}

## Test; save plot
# challenge_F(length = 1) # reduce length >> small fern (same proportions)
# challenge_F(length = 3) # increase length >> big fern

# A vertical line is 90 degrees (pi/2).
# challenge_F(direction = pi/3) # direction different to straight up >> slanted fern
# challenge_F(start = c(0,7), direction = -pi/3) # negative direction >> upside down fern

# pdf('../Results/Challenge_F_Fern.pdf')
# par(mar = c(1,1,1,1)) # reduce margins
# plot(NULL, axes = F, xlim = c(-10,10), ylim = c(-10,7), xlab = '', ylab = '')
# challenge_F(start = c(5,-7), lc=0.9) # Increases size of first branch
# dev.off()


## Draws a tree
challenge_F2 <- function(start = c(0,-5), direction = pi/2, length = 5, e = 0.01,
                         dc = pi/4, dc2 = pi/4, # changes to direction
                         lc = 0.65, lc2 = 0.65){ # changes to length
  
  if(length > e){
    
    if(length < 0.5){
      col = 'green'
    } else{
      col = 'brown'
    }
    
    x <- start[1] + (length * cos(direction))
    y <- start[2] + (length * sin(direction))
    end <- c(x,y)
    lines(c(start[1], x), c(start[2], y), col = col)
    
    challenge_F2(end, (direction - dc), (length * lc), e)
    challenge_F2(end, (direction + dc2), (length * lc2), e)
  }
}

## Test; save plot

# challenge_F2() # normal tree
# challenge_F2(lc = 0.3) # one side of tree is smaller
# challenge_F2(dc = pi/2) # one side of tree braches horizontally (0 degrees)

# pdf('../Results/Challenge_F_Tree.pdf')
# par(mar = c(1,1,1,1)) # reduce margins
# plot(NULL, axes = F, xlim = c(-10,10), ylim = c(-5,10), xlab = '', ylab = '')
# challenge_F2(dc = pi/2, dc2 = 0, lc = 0.3)
# dev.off()