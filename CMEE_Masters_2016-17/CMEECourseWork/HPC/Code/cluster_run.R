# Calum Pennington (c.pennington@imperial.ac.uk)
# Jan 2017

# Script to run a neutral model simulation using high performance computing (HPC)
# It will be run multiple times concurrently on the cluster.

rm(list = ls())
graphics.off()

####################
# Simulation
####################

# Records at intervals, and saves to an .Rdata file:
#   species richness during the burn in
#   species abundance distribution (as octaves)
#   final community state.

# Arguments:
#   'size' - number of individuals in the community
#   'wall_time' - minutes the code runs for
#   'rand_seed' - the seed for random number generation
#   Thus, we ensure each parallel simulation has a different seed. The simulation is stochastic, but simulations with the same seed give the same result.
#   'burn_in_time' - duration (number of generations) of burn in

cluster_run <- function(speciation_rate, size, wall_time, rand_seed, interval_rich, interval_oct, burn_in_time){
  
  ## Set the seed for random number generation.
  set.seed(rand_seed)
  
  ## Set up a timer.
  start_time <- proc.time()[[3]]
  # The start is the current 'elapsed' time.
  # (View output of 'proc.time()' - '[[3]]' extracts the 'elapsed' value.)
  # We use 'elapsed', as it is a timer that runs continuously.
  
  finish_time <- start_time + wall_time * 60
  # 'proc.time()' is in seconds, whereas 'wall_time' is in minutes.
  
  ## Generate an initial state for the simulation community, with the maximum number of species for the community size.
  state <- initialise_max(size)
  
  ## Initialise a generation count.
  generation_n <- 0
  
  
  time_series <- vector('numeric')
  # Make an empty vector, which we will fill with numeric values.
  
  octaves_list <- list()
  # Make an empty list.
  
  while(proc.time()[[3]] <= finish_time){
    # Run the simulation for a time given by 'wall_time'.
    # 'while()' is a loop. It performs the code below once, then keeps repeating it, until the above condition is not met.
    
    ## Run the neutral model for one generation.
    ## One generation involves a birth or death for every individual. If size is 100, one generation is 50 time steps. **Explain
    for(i in 0:(size/2)){
      # Note - start at time step 0.
      state <- neutral_step_speciation(state, speciation_rate)
      # Overwrite the community state each iteration.
    }
    
    ## During the burn in, record species richness every 'interval_rich' generations.
    if((generation_n <= burn_in_time)&&(generation_n %% interval_rich == 0)){
      time_series <- c(time_series, species_richness(state))
    }
    
    ## For the whole simulation, record the species abundance distribution (as octaves) every 'interval_oct' generations.
    if(generation_n %% interval_oct == 0){
      octaves_list[[length(octaves_list) + 1]] <- octaves(species_abundance(state))
      # Append the octaves vector to the end of the list.
    }
    
    ## Update the generation counter.
    generation_n <- generation_n + 1
    
    ## The 'while' loop repeats this code for the next generation.
  }
  
  ## The time consumed by the simulation.
  time_taken <- finish_time - start_time
  
  ## Only used to check outputs when testing function:
  # print('Time series of species richness, recorded during the burn in:')
  # print(time_series)
  # print('Species abundance octaves:')
  # print(octaves_list)
  # print('Community state at the end:')
  # print(state)
  # print('Time taken:')
  # print(time_taken)
  # print('Number of generations:')
  # print(generation_n)
  
  ## Save results to an Rdata file.
  save(time_series, # Time series of species richness, recorded during the burn in.
       octaves_list, # List of species abundance octaves.
       state, # Community state at the end of the simlation.
       time_taken,
       speciation_rate, # The 7 input parameters:
       size,
       wall_time,
       rand_seed,
       interval_rich,
       interval_oct,
       burn_in_time,
       file = paste("cluster_results_",rand_seed,".Rdata",sep = ""))
       # 'paste()' concatenates character vectors.
       # The file's name is 'cluster_result_' followed by the seed number.
}

# Computers do not generate truly random values; they use a pseudo-random number generator (PRNG).
# A PRNG is an algorithm for generating a number sequence that approximates a sequence of random numbers.
# A PRNG is not truly random as it is determined by initial values (seeds).

# 'proc.time()'
#   'user' - time (in seconds) the CPU spent performing processes in the current R session.
#   'system' - time the CPU spent calling the operating system on behalf of processes (e.g. to open files, look at the system clock, start other processes - resources other processes share).
#   How long in total the CPU has been used = 'user' + 'system' times.
#   'elapsed' - how long the session has been open.


####################
# Functions called by 'cluster_run'
####################

## Generates an intial state for the simulation community, with the maximum number of species.
initialise_max <- function(size){
  seq(size)
}

## Randomly chooses two different individuals from a community.
choose_two <- function(x){
  sample(x, 2, replace = F)
}

## Performs one step of a neutral model with speciation.
## With probability v, replaces a dead individual with a new species.
## Otherwise the replacement is another individual's offspring.
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

## Measures the species richness of (number of unique items in) a community.
species_richness <- function(community){
  length(unique(community))
}

## Returns abundance of each species in a community.
species_abundance <- function(community){
  x <- as.vector(table(community))
  sort(x, decreasing = T)
}

## Bins species abundances into octave classes.
# ** Explain this
octaves <- function(abundances){
  #max_bin <- floor(log2(max(abundances))) # ** Where should +1 go?
  bins <- floor(log2(abundances)) + 1
  max_bin <- max(bins)
  tally <- seq(0, 0, length.out = max_bin)
  for (i in bins){
    tally[i] <- tally[i] + 1
  }
  return(tally)
}


####################
# Choose parameters
####################

speciation_rate <- 0.003617

iter <- as.numeric(Sys.getenv("PBS_ARRAY_INDEX")) # **Explain
# iter <- 1 # Test

# We will use four community sizes and run 25 simulations per size. Use 'iter' to choose a simulation's size.
if((iter > 0)&&(iter <= 25)){
# if 0 < iter <= 25
  size <- 500
}

if((iter > 25)&&(iter <= 50)){
  size <- 1000
}

if((iter > 50)&&(iter <= 75)){
  size <- 2500
}

if((iter > 75)&&(iter <= 100)){
  size <- 5000
}

rand_seed <- iter
# Use 'iter' to ensure each parallel simulation has a different seed.

wall_time <- 60 * 11.5 # 11.5 hours = 60 minutes * 11.5
interval_rich <- 1
interval_oct <- size/10
burn_in_time <- size*8


####################
# Test the code before running it on the HPC
####################

# test_results <- cluster_run(speciation_rate, size, 0.5, iter, 2, 3, 5) # Quick test
# 
# cat("\nRunning a 10-minute test of 'cluster_run'...") # 'print()' cannot print new line characters - use 'cat()'.
# test_results <- cluster_run(speciation_rate, size, 10, iter, 2, 3, 5)
# cat("\nTest complete")
# # 1 generation is 500/2 = 250 time steps.
# # No. of generations is a function of 'wall_time' and computer speed.
# # Expected outputs:
# #   3 values in 'time_series' (burn in is 5 generations)
# #   No. of vectors in 'octaves_list' = no. of generations / 3
# 
# ## View test results
# load('cluster_result_1.Rdata')
# 
# rm(time_taken,
#    speciation_rate,
#    size,
#    wall_time,
#    iter,
#    interval_rich,
#    interval_oct,
#    burn_in_time,
#    test_results)
# # Tidy namespace
# 
# time_series
# 
# length(octaves_list)
# length(octaves_list) * 3 # Should equal no. of generations
# octaves_list[[1]] # View 1st and last octave vectors
# octaves_list[[length(octaves_list)]]
# 
# state
# length(state) # Should be 500.


####################
# Call 'cluster_run'
####################

# Run simulation for given parameter values
cluster_run(speciation_rate, size, wall_time, rand_seed, interval_rich, interval_oct, burn_in_time)