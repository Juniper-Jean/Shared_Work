# Calum Pennington (c.pennington@imperial.ac.uk)
# January 2016

# **title, description

rm(list = ls()) # Remove objects.
graphics.off() # Close graphics devices.

library(minpack.lm)
library(ggplot2)

thermal_data <- read.csv('../Data/Edited_Data.csv', stringsAsFactors = F)
# Import data.
# 'stringsAsFactors = F' - some columns have string values; do not make these factors.
# I use these values later, so want them 'as is'.

# d <- subset(thermal_data, thermal_data$FinalID == 'MTD2818') # Get data for one thermal response curve.
# temps <- d$TempK
# traits <- d$Trait_minus_min_plus1
# Get the temperature and trait values.

Tref <- 10 + 273.15
k <- 8.617 * 10^-5
# assign('Tref', 10 + 273.15, envir = .GlobalEnv) # **justify value
# assign('k', 8.617 * 10^-5, envir = .GlobalEnv) # Boltzmann constant (unit is eV * K^-1)
# ?assign - assign value to a name in an environment.
# Set global variables - **why - usable within functions?
# **if I define a variable outside a function, isn't by default a global variable?


################
# Functions ####
################

## Calculates initial guesses of parameters for non-linear regression
# **finish annotations
get_start_values <- function(temps, traits){
  
  ## Tpeak - temperature at which trait peaks
  Tpk_st <- max(temps[which(traits == max(traits))])
  # Max trait may occur more than once and at multiple temperatures.
  # ?which - which indices are TRUE (which of an object's indices are T for a logical condition)?
  # Get indices with the max trait (it could occur more than once).
  # Get the max temp at which the max trait occurs.
  # **Could use:
  # ?which.max - get the index of the (first) maximum of a vector.
  # temp[which.max(trait)].
  
  
  ## E - activation energy (unit is eV), which controls the curve's rise up to the peak
  curve_rise <- which(temps <= Tpk_st)
  if(length(curve_rise) > 1){
    m <- lm(log(traits[curve_rise]) ~ I(1 / (k * temps[curve_rise])))
    E_st <- tryCatch(abs(summary(m)$coefficients[2,1]),
                     error = function(e) 0.6)
  } else{
    E_st <- 0.6
  }
  # Get indices of temps <= Tpeak
  # - these correspond to the curve's rise.
  # For the rise, calculate linear regression for the relationship between log(trait) and 1/kT (inverse of temp).
  # **explain, justify
  # Get the linear model's gradient - best-fit value of the slope.
  # ?abs - get a number's absolute value - its magnitude without regard to its sign.
  # **
  #   why abs
  #   explain tryCatch
  #   slope may be NA - why - return 0.6
  # Can not calculate regression if there one/no data points - return 0.6.
  # **average all species - cite
  
  
  ## B0 - trait value at Tref
  if(min(temps) > Tref){
    # If data have NAs, 'min()/max()' return NA.
    # 'min(temps, na.rm=T)' removes NAs, then returns min.
    
    B0_st <- log(min(traits[1]))
    # There may be > 1 min. 'traits[1]' gets one value - ensures B0 is not a vector.
    
  } else{
    B0_st <- log(traits[max(which(temps <= Tref))])
    # which(temps <= Tref) # Get indices of temps <= Tref.
    # 'trait[max(...)]' - get trait at max temp, for temps <= Tref.
  }
  # May not be a recording at Tref - use the temp closest to it.
  # If the min temp > Tref, 'B0_st' is the trait at the min temp.
  # Otherwise, it is the trait at the max temp, for temps below Tref.
  # **Get the log of B0.
  
  return(list(B0 = B0_st, # **
              Tpk = Tpk_st,
              E = E_st))
}


## **Boltzmann Arrhenius model
# Returns B (y/trait value), as predicted by the equation, for given temperature values.
Boltzmann_Arrhenius <- function(B0, E, temps){
  # **arguments
  
  return(B0 - (E/k) * ((1/temps) - (1/Tref)))
  # **log
}


## **Schoolfield model
Schoolfield <- function(B0, E, Ed, Tpk, temps){
  # **parameters
  
  return(B0 + log(exp((-E/k) * ((1/temps) - (1/Tref))) / (1 + (E/(Ed - E)) * exp((Ed/k) * ((1/Tpk) - (1/temps))))))
  # return(B0 + log(exp((-E/k) * ((1/temps) - (1/Tref))) / (1 + exp((Ed/k) * ((1/Tpk) - (1/temps))))))
  # **justify this version - not in silbio pdf
  # T/F opt, if else - alt version
}


## Runs NLLS for the Boltzmann-Arrhenius model.
## It is run within 'try()', in case it fails.
## Returns model output or 'try-error'.
# **is Boltzmann non-linear - log?
try_Boltzmann <- function(d, B0_st, E_st){
  # Arguments:
  #   d - data
  #   B0_st - B0 start value
  #   E_st - E start value
  
  model <- tryCatch(
    nlsLM(log(Trait_minus_min_plus1) ~ Boltzmann_Arrhenius(B0, E, TempK),
          # **why log
          start = c(B0 = B0_st, E = E_st), # vector of starting estimates
          lower = c(B0 = -Inf, E = 0), # vector of lower bounds on each parameter
          # **justify bounds, explain why we constrain them
          upper = c(B0 = Inf, E = Inf),
          control = list(minFactor=1 / 2^16, maxiter=1e4), # *?
          data = d,
          na.action = na.omit), # **Remove NAs in the data - need?
    # silent = T) # Do not print error messages.
  error = function(e) NULL)
  
  return(model)
  # 'model' may be a 'try-error'.
}


## **
try_Schoolfield <- function(d, B0_st, E_st, Tpk_st){
  model <- tryCatch(
    nlsLM(log(Trait_minus_min_plus1) ~ Schoolfield(B0, E, Ed, Tpk, TempK), # **have explained parameters
          start = c(B0 = B0_st, E = E_st, Ed = 0.1, Tpk = Tpk_st),
          # **justify Ed
          lower = c(B0 = -Inf, E = 0, Ed = 0, Tpk = 0),
          # lower = c(B0 = -Inf, E = 0, Ed = -Inf, Tpk = Tref),
          upper = c(B0 = Inf, E = Inf, Ed = Inf, Tpk = 273.15 + 150),
          # upper = c(B0 = Inf, E = Inf, Ed = Inf, Tpk = Inf),
          # **justify bounds
          control = list(minFactor=1 / 2^16, maxiter=1e4), # *? - see 'Thermal_nlls' - different to 'TPCFitting'
          data = d,
          na.action = na.omit),
    # silent = T)
  error = function(e) NULL)
  
  return(model)
}


## **
fit_models <- function(d,
                       enter_debug = F){ # an optional argument, with default F
  
  if(enter_debug == T){browser()}
  # ?browser - interrupts execution, allowing inspection of the environment where browser was called.
  # Later, I call many functions in a 'for' loop.
  # Using 'browser' in the loop, I cannot inspect functions.
  # So it is hard to find bugs.
  # The 'enter_debug' argument allows me to optionally enter the function - inspect its environment and run code line by line.
  
  try_original <- 1
  try_deviant <- 0
  insuf_data_Bolt <- 0
  Bolt_fail <- 0
  # Initialise objects used to record if a fit fails, or the number of tries till it succeeds.
  
  temps <- d$TempK
  traits <- d$Trait_minus_min_plus1
  # Save temp and trait data as vectors.
  
  
  ## Fit a cubic polynomial model.
  tempsC <- d$ConTemp
  cubic_model <- lm(log(traits) ~ poly(tempsC, 3, raw = T))
  # 'poly(tempsC, 3)' evaluates a polynomial of degree 3 over the points.
  # **
  #   not log?
  #   why temp in C?
  #   'raw=T' - use a raw, not orthogonal polynomial
  
  
  ## Get NLLS start values.
  start_values <- get_start_values(temps, traits)
  B0_start <- start_values$B0
  Tpk_start <- start_values$Tpk
  E_start <- start_values$E
  
  set.seed(1)
  deviants <- abs(rnorm(100, mean = E_start))
  # Generate 100 random deviants of 'E_start'
  # - sample from a normal distribution with mean 'E_start'.
  # As E is small, close to zero, 'rnorm' could generate negative values.
  # Use 'abs' - E must not be negative, as it controls the curve's rise (positive gradient).
  
  
  ## Try to fit the Boltzmann model.
  # **explain why - they may fail, I try different start values
  
  curve_rise <- which(temps <= Tpk_start)
  curve_rise <- d[curve_rise,]
  # Fit the Boltzmann to the curve's rise, as it models only this.
  # Get indices of temps <= Tpk (these correspond to the rise).
  # (Tpk - temperature at which trait peaks)
  # Get rows in 'd' that correspond to the rise.
  # 'd' is a 2-D dataframe (not a vector) - use a comma to specify certain rows, not columns (I want all columns).
  
  if(length(unique(curve_rise$TempK)) >= 3){ # **4?
    # If there are enough data points
    # **why is this enough?
    
    Boltzmann_NLLS <- try_Boltzmann(curve_rise, B0_start, E_start)
    
    for(dv in deviants){
      if(is.null(Boltzmann_NLLS)){
        Bolt_fail <- 1
        Boltzmann_NLLS <- try_Boltzmann(curve_rise, B0_start, E_start)
        if(!is.null(Boltzmann_NLLS)){
          Bolt_fail <- 0
          dv_Bolt <- dv
        }
      } else{break()}
    }
    # I previously generated deviants of E's start value - loop over them.
    # If NLLS failed (returned a NULL object):
    #   set 'fail_Bolt' to 1 (1 indicates NLLS failed; 0, succeeded)
    #   try NLLS again, with a different start value for E.
    # Keep trying new values, till NLLS succeeds (does not return a NULL object), up to 100 tries.
    # If it succeeds, save the new start value, reset 'fail_Bolt' to 0, and stop the loop.
    # If it never succeeds, 'Boltzmann_NLLS' stays NULL.
    
    if(is.null(Boltzmann_NLLS)){
      print(paste('Boltzmann failed to fit - ID:', unique(d$FinalID), sep = ''))
      # Print a message, if the Boltzmann did fit for an ID.
      # As part of my project workflow, Python code will run this script and save to a text file, outputs to the terminal.
      # So, I can quickly look up this information.
    }
  } else{
    # If there are not enough data to fit the Boltzmann
    Boltzmann_NLLS <- NULL
    insuf_data_Bolt <- 1
    print(paste('Insufficient data to fit Boltzmann - ID:', unique(d$FinalID))) # Print a message.
  }
  
  
  ## Try to fit the Schoolfield model.
  Schoolfield_NLLS <- try_Schoolfield(d, B0_start, E_start, Tpk_start)
  
  for(dv in deviants){
    if(is.null(Schoolfield_NLLS)){
      try_original <- 0 # Indicate that the 1st try to fit the Schoolfield failed.
      Schoolfield_NLLS <- try_Schoolfield(d, B0_start, dv, Tpk_start)
      if(!is.null(Schoolfield_NLLS)){
        try_deviant <- 1 # Indicate that the fit succeeded with a different start value for E.
        dv_Sch <- dv
      }
    } else{break()}
  }
  if(is.null(Schoolfield_NLLS)){
    print(paste('Schoolfield failed to fit - ID:', unique(d$FinalID)))
    # Print a message, if the Schoolfield did fit for an ID.
  }
  
  return(list(cubic = cubic_model,
              Bolt = Boltzmann_NLLS,
              Insuf_curve_rise = insuf_data_Bolt,
              Curve_rise_data = curve_rise,
              Fail_Bolt = Bolt_fail, # **
              Sch = Schoolfield_NLLS,
              try1 = try_original,
              try100 = try_deviant,
              B0_st = B0_start,
              Tpk_st = Tpk_start,
              E_st = E_start,
              Edv_Bolt = tryCatch(dv_Bolt, error = function(e) NA),
              Edv_Sch = tryCatch(dv_Sch, error = function(e) NA)
  ))
}


## **
calculate_R2 <- function(d, model, enter_debug = F){
  if(enter_debug == T){browser()}
  
  # R^2 = 1 - (residual sum of squares / total sum of squares)
  
  traits <- d$Trait_minus_min_plus1
  
  TSS <- sum((traits - mean(traits))^2)
  # sum of the squared difference of each observation from the mean
  
  predicted_y <- predict(model)
  RSS <- sum((traits - exp(predicted_y))^2)
  # 'exp()' - calculate R^2 in linear scale - **why?
  
  R2 <- 1 - (RSS / TSS)
  
  return(list('RSS' = RSS, 'R2' = R2))
}


## **
get_results <- function(d, models, enter_debug = F){
  if(enter_debug == T){browser()}
  
  headers <- c('ID', 'AIC_cubic', 'AIC_Boltzmann', 'AIC_Schoolfield', 'Best_model', 'Best_cubic_Sch',
               'R_squared_cubic', 'R_squared_Bolt', 'R_squared_Sch',
               'RSS_cubic', 'Cubic_F_statistic', 'Cubic_p',
               'RSS_Bolt', 'Bolt_B0', 'Bolt_B0_SE', 'Bolt_E', 'Bolt_E_SE',
               'RSS_Sch', 'Sch_B0', 'Sch_B0_SE', 'Sch_E', 'Sch_E_SE', 'Ed', 'Ed_SE', 'Tpk', 'Tpk_SE',
               'B0_st', 'E_st', 'E_st_dv_Bolt', 'E_st_dv_Sch', 'Tpk_st',
               'Trait_name', 'Habitat')
  results <- data.frame(matrix(NA, 1, length(headers), dimnames = list(NULL, headers)))
  # Preallocate an empty dataframe for storing results.
  
  results[,'ID'] <- unique(d$FinalID)
  results[,'Trait_name'] <- unique(d$Trait_name)
  results[,'Habitat'] <- unique(d$Habitat)
  # 'd$FinalID' gets each row's ID (which is the same).
  # 'unique' - get only one copy.
  
  results[,'B0_st'] <- models$B0_st
  results[,'Tpk_st'] <- models$Tpk_st
  results[,'E_st'] <- models$E_st
  results[,'E_st_dv_Bolt'] <- models$Edv_Bolt
  results[,'E_st_dv_Sch'] <- models$Edv_Sch
  # Save NLLS start values.
  
  
  results[,'AIC_cubic'] <- AIC(models$cubic)
  results[,'R_squared_cubic'] <- summary(models$cubic)$r.squared
  results[,'RSS_cubic'] <- sum(residuals(models$cubic)^2)
  results[,'Cubic_F_statistic'] <- anova(models$cubic)[1,4]
  results[,'Cubic_p'] <- anova(models$cubic)[1,5]
  # Linear regression results for the cubic polynomial model.
  # check - 'sum(is.na(results[,'R_squared_cubic']))' should be 0
  
  if(!is.null(models$Bolt)){ # If NLLS for the Boltzmann did not fail
    
    results[,'AIC_Boltzmann'] <- AIC(models$Bolt)
    
    results[,'R_squared_Bolt'] <- calculate_R2(models$Curve_rise_data, models$Bolt, enter_debug)[[2]]
    results[,'RSS_Bolt'] <- calculate_R2(models$Curve_rise_data, models$Bolt, enter_debug)[[1]]
    # I manually calculate R^2 - use data for the curve's rise.
    
    results[,'Bolt_B0'] <- coef(models$Bolt)[[1]]
    results[,'Bolt_B0_SE'] <- summary(models$Bolt)$coefficients[1,1] # Standard error of best-fit B0 value.
    results[,'Bolt_E'] <- coef(models$Bolt)[[2]]
    results[,'Bolt_E_SE'] <- summary(models$Bolt)$coefficients[2,2]
  }
  
  if(!is.null(models$Sch)){
    results[,'AIC_Schoolfield'] <- AIC(models$Sch)
    results[,'R_squared_Sch'] <- calculate_R2(d, models$Sch, enter_debug)[[2]]
    results[,'RSS_Sch'] <- calculate_R2(d, models$Sch, enter_debug)[[1]]
    results[,'Sch_B0'] <- coef(models$Sch)[[1]]
    results[,'Sch_B0_SE'] <- summary(models$Sch)$coefficients[1,1]
    results[,'Sch_E'] <- coef(models$Sch)[[2]]
    results[,'Sch_E_SE'] <- summary(models$Sch)$coefficients[2,2]
    results[,'Ed'] <- coef(models$Sch)[[3]]
    results[,'Ed_SE'] <- summary(models$Sch)$coefficients[3,3]
    results[,'Tpk'] <- coef(models$Sch)[[4]]
    results[,'Tpk_SE'] <- summary(models$Sch)$coefficients[4,4]
  }
  return(results)
}


# **
model_selection <- function(models, enter_debug = F){
  if(enter_debug == T){browser()}
  
  cubic_AIC <- AIC(models$cubic)
  Bolt_AIC <- tryCatch(AIC(models$Bolt), error = function(e) NA)
  Sch_AIC <- tryCatch(AIC(models$Sch), error = function(e) NA)
  # 'models$Bolt'/'models$Sch' may be NULL objects, if the NLLS failed, thus 'tryCatch()'.
  
  AICs <- c(cubic_AIC, Bolt_AIC, Sch_AIC) # Concatenate the AICs.
  best_model <- NA
  best_cubic_Sch <- NA
  
  if(sum(is.na(AICs)) == 2){
    # If the Boltzmann and Schoolfield AICs are missing
    
    best_model <- 'cubic but NAs'
    
  } else{
    best_model <- min(AICs, na.rm = T)
    # The best model has the lowest AIC.
    
    if(best_model == cubic_AIC){
      # If the cubic has the lowest AIC
      
      best_model <- 'cubic'
      
    } else if((!is.na(Bolt_AIC)) && (best_model == Bolt_AIC)){
      # If the Boltzmann AIC is not missing and is the lowest
      
      best_model <- 'Boltzmann'
      
      # The Boltzmann only models the curve's rise.
      # If it is the best model, it is worthwhile comparing the cubic and Schoolfield, which model the whole curve.
      
      cubic_Sch_AIC <- c(cubic_AIC, Sch_AIC) # Concatenate the cubic and Schoolfield AICs.
      
      if(is.na(Sch_AIC)){
        best_cubic_Sch <- 'cubic but NA Sch'
      } else{
        best_cubic_Sch <- min(cubic_Sch_AIC)
        
        if(best_cubic_Sch == cubic_AIC){
          best_cubic_Sch <- 'cubic'
        } else{
          best_cubic_Sch <- 'Schoolfield'
        }
      }
    } else if((!is.na(Sch_AIC)) && (best_model == Sch_AIC)){
      best_model <- 'Schoolfield'
      
    } else{
      stop("Error determining best model - review 'model_selection' function.")
      # Stop execution and print this message (test of code).
    }
  }
  return(list(best_model, best_cubic_Sch))
}


## **
plot_data <- function(d, models,
                      gg = F, # Set to T, to use ggplot instead of R plot. By default, do not use ggplot, as it is slower.
                      enter_debug = F){
  
  if(enter_debug == T){browser()}
  
  temps <- d$TempK
  traits <- d$Trait_minus_min_plus1
  # Save temp and trait data as vectors.
  
  curve_rise <- models$Curve_rise_data
  # Get data for the curve's rise.
  
  plot_cubic <- data.frame(tempsC = seq(min(d$ConTemp), max(d$ConTemp), len = 200))
  plot_Bolt <- data.frame(TempK = seq(min(curve_rise$TempK), max(curve_rise$TempK), len = 200))
  plot_Sch <- data.frame(TempK = seq(min(temps), max(temps), len = 200))
  # To plot models, generate their predictions for y (trait), using x (temperature) data.
  # You need a lot of data points to plot smooth curves.
  # As there are not many in the raw data, generate 200 x points (within the raw data's range).
  # Do this separately for each model, as the cubic is uses Celsius, not Kelvin, and the Boltzmann only models the curve's rise.
  
  if(gg == F){
    plot(temps, log(d$Trait_minus_min_plus1), # **Boltzmann returns log(B)
         main = unique(d$FinalID)) # title is the ID
    # Plot raw data.
    
    lines(plot_Sch$TempK, predict(models$cubic, newdata = plot_cubic), col = 'blue')
    # Plot cubic model.
    # Make predictions using temps in C, but plot them against temps in K. Otherwise, the line is outside the plot's limits (as K = c + 273.15 and we plot the models on the same graph).
    # 'predict()' generates predictions from the results of a model-fitting function (e.g. 'lm'). By default, it uses the x values passed to the function.
    # 'newdata=' specifies new x values - you must specify a dataframe.
    # 'lines()' needs a vector of x coordinates.
    # Used with 'predict()', you must specify a dataframe column. The column's name must be the same as the x object in the model-fitting function.
    
    if(!is.null(models$Bolt)){
      lines(plot_Bolt$TempK, predict(models$Bolt, newdata = plot_Bolt), col = 'green')
      # Plot the Boltzmann, if NLLS succeeded.
    }
    
    if(!is.null(models$Sch)){
      lines(plot_Sch$TempK, predict(models$Sch, newdata = plot_Sch), col = 'red')
    }
  } else{
    
    plot_cubic$cubic_predict <- predict(models$cubic, newdata = plot_cubic)
    p <- ggplot(d, aes(x = TempK, y = log(Trait_minus_min_plus1))) +
      geom_point(shape = I(1)) + # Plot raw data as points.
      scale_x_continuous('Temperature (K)') + scale_y_continuous('Trait') + # titles of axes
      ggtitle(d$FinalID) + # plot title
      theme_bw() +
      geom_line(aes(x = (tempsC + 273.15), y = cubic_predict, color = 'cubic polynomial'), data = plot_cubic) + # Plot the cubic model.
      
      scale_color_manual(name = 'Model', values = c('cubic polynomial' = 'blue', 'Boltzmann Arrhenius' = 'green', 'Schoolfield' = 'red')) +
      theme(legend.position = 'bottom') +
      guides(color = guide_legend(nrow = 1))
      # Plot each model a different colour; make a legend.
      # Put the legend at the bottom; arrange it horizontally.
    
    if(!is.null(models$Bolt)){
      plot_Bolt$Bolt_predict <- predict(models$Bolt, newdata = plot_Bolt)
      p <- p + geom_line(aes(x = TempK, y = Bolt_predict, color = 'Boltzmann Arrhenius'), data = plot_Bolt)
    }
    
    if(!is.null(models$Sch)){
      plot_Sch$Sch_predict <- predict(models$Sch, newdata = plot_Sch)
      p <- p + geom_line(aes(x = TempK, y = Sch_predict, color = 'Schoolfield'), data = plot_Sch)
    }
    
    print(p) # Print the ggplot object.
  }
}


####################
# Run functions ####
####################

IDs <- unique(thermal_data$FinalID)
# Make a vector of the IDs. **have explained what an ID is/described data

insuf_data <- list()
try1 <- 0
try100 <- 0
fail_Sch_NLLS <- list()
not_converged_Sch <- list()
converged_Sch <- matrix(NA, length(IDs), 2)
insuf_data_Bolt <- list()
fail_Bolt_NLLS <- list()
curve_rise_only <- list()
# Initialise counters and empty lists, to:
#   Save the IDs where:
#     NLLS for the Boltzmann and Schoolfield models failed
#     there were insufficient data to run NLLS.
#   Count the number of IDs where NLLS for the Schoolfield succeeded with original and deviant start values.

headers <- c('ID', 'AIC_cubic', 'AIC_Boltzmann', 'AIC_Schoolfield', 'Best_model', 'Best_cubic_Sch',
             'R_squared_cubic', 'R_squared_Bolt', 'R_squared_Sch',
             'RSS_cubic', 'Cubic_F_statistic', 'Cubic_p',
             'RSS_Bolt', 'Bolt_B0', 'Bolt_B0_SE', 'Bolt_E', 'Bolt_E_SE',
             'RSS_Sch', 'Sch_B0', 'Sch_B0_SE', 'Sch_E', 'Sch_E_SE', 'Ed', 'Ed_SE', 'Tpk', 'Tpk_SE',
             'B0_st', 'E_st', 'E_st_dv_Bolt', 'E_st_dv_Sch', 'Tpk_st',
             'Trait_name', 'Habitat')
results <- data.frame(matrix(NA, length(IDs), length(headers), dimnames = list(NULL, headers)))
# Preallocate an empty dataframe for storing results.
# I will save the best-fit parameters and their standard error, for the Bolzmann and Schoolfield models.

thermal_data <- thermal_data[-20354,]
# Remove a row.
# The trait name or ID of row 20354 is wrong - trait name differs to the other rows for this ID (MTD2095).

pdf('../Results/Thermal_Response_Plots.pdf')
# Open a pdf to which plots will be saved.

for(i in 1:length(IDs)){
  # Loop over integers, not IDs, so indexing to store results is easy.
  # For each ID, repeat the following:
  
  debug_functions <- F
  # This variable is passed to the functions. Set to T, to debug them.
  
  # i <- 3
  # d <- subset(thermal_data, thermal_data$FinalID == 'MTD4338')
  # browser()
  # Run the code for/inspect a certain ID.
  
  d <- subset(thermal_data, thermal_data$FinalID == IDs[i])
  # Get the ID's data.
  
  if((length(unique(d$TempK)) > 1) && (length(d$Trait_minus_min_plus1) >= 5)){
    # Only run if there is > 1 temp and at least 5 trait values.
    # **why
    
    models <- fit_models(d, debug_functions)
    
    try1 <- try1 + models$try1
    try100 <- try100 + models$try100
    # 'models$try1'/'models$try100' equals 0 or 1 - add 1 to the counter, if appropriate.
    
    if((models$try1 == 0) && (models$try100 == 0)){
      fail_Sch_NLLS[[length(fail_Sch_NLLS) + 1]] <- unique(d$FinalID)
      # If NLLS for the Schoolfield failed, add the ID to the end of the 'fail_Sch_NLLS' list.
    }
    
    
    ## Check if NLLS for the Schoolfield converged.
    check_convergence <- models$Sch
    if(!is.null(models$Sch)){ # If NLLS succeeded...
      
      if(check_convergence$convInfo[[1]] == F){ # ...but did not converge
        not_converged_Sch[[length(not_converged_Sch) + 1]] <- IDs[i]
        # print(paste('NLLS for the Schoolfield did not converge - ID:', IDs[i]))
      } else{
        converged_Sch[i,] <- c(IDs[i], check_convergence$convInfo[[2]])
      }
    }
    
    if(models$Fail_Bolt == 1){
      fail_Bolt_NLLS[[length(fail_Bolt_NLLS) + 1]] <- unique(d$FinalID)
    }
    
    if(models$Insuf_curve_rise == 1){
      insuf_data_Bolt[[length(insuf_data_Bolt) + 1]] <- unique(d$FinalID)
    }
    
    results[i,] <- get_results(d, models, debug_functions)
    
    best_model <- model_selection(models, debug_functions)
    results[i, 'Best_model'] <- best_model[[1]]
    results[i, 'Best_cubic_Sch'] <- best_model[[2]]
    
    plot_data(d, models, gg = F, debug_functions)
    
    
    ## List IDs where the curve only represents the rise of a thermal response.
    traits <- d$Trait_minus_min_plus1
    trait_at_max_temp <- max(traits[which(d$TempK == max(d$TempK))])
    if(trait_at_max_temp == max(traits)){
      # If the trait value at the max temp (i.e. the last data point) is the curve's peak
      
      curve_rise_only[[length(curve_rise_only) + 1]] <- IDs[i]
    }
    
  } else{
    insuf_data[[length(insuf_data) + 1]] <- IDs[i]
  }
}
dev.off() # Close pdf.

sum(is.na(results[,'ID']))
results <- subset(results, !is.na(results[,'ID']))
# Count the IDs missing from 'results' - should equal length of 'insuf_data'.
# Remove these rows.

write.csv(results, '../Results/Model_Results.csv', row.names = F)
# Save 'results' table to a csv.

converged_Sch <- converged_Sch[which(!is.na(converged_Sch[,1])),]
save(insuf_data,
     try1,
     try100,
     fail_Sch_NLLS,
     not_converged_Sch,
     converged_Sch,
     insuf_data_Bolt,
     fail_Bolt_NLLS,
     curve_rise_only,
     results,
     file = '../Results/Model_Results.Rdata')
# Save all results objects to an Rdata file.