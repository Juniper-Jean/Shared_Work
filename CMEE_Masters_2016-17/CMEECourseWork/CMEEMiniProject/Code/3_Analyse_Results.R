# Calum Pennington (c.pennington@imperial.ac.uk)
# January 2016

# **title, description

rm(list = ls()) # Remove objects.
graphics.off() # Close graphics devices.

library(reshape2)
library(ggplot2)

results <- read.csv('../Results/Model_Results.csv', stringsAsFactors = F)
load('../Results/Model_Results.Rdata')
thermal_data <- read.csv('../Data/Edited_Data.csv', stringsAsFactors = F)
# Import model-fitting results and raw data.

unique(results$Trait_name)
unique(results$Habitat)
sum(results$Habitat == 'estuarine') # 33
sum(results$Habitat == 'hot spring') # 2
sum(results$Habitat == 'saline lake') # 4
sum(results$Habitat == 'freshwater / terrestrial') # 4
sum(results$Habitat == 'aquatic') # 2
# See habitat and trait types.

table(results[,'Best_model'])
table(results[,'Best_cubic_Sch'])
# See model selection results.

cubic_but_NAs <- results[which(results[,'Best_model'] == 'cubic but NAs'),]$ID
results[,'Best_model'][which(results[,'Best_model'] == 'cubic but NAs')] <- NA
cubic_but_NA_Sch <- results[which(results[,'Best_cubic_Sch'] == 'cubic but NA Sch'),]$ID
results[,'Best_cubic_Sch'][which(results[,'Best_cubic_Sch'] == 'cubic but NA Sch')] <- NA
# If NLLS failed for the Boltzmann and Schoolfield models (no AIC), my code, by default, chose cubic as the best model.
# If the Boltzmann had the best AIC, I compared cubic and Schoolfield. If NLLS failed for the Schoolfield, my code, by default, chose cubic as the next best. **briefly say why
# Get these IDs.
# While I will discuss these curves, I exclude them from best model plots.

## Manually inspect certain plots.


####################################################
## Bar chart of best model (AIC) as proportions ####
####################################################

# I will:
#   per model, calculate the proportion of curves for which it was the best model (had the lowest AIC)
#   look for differences across habitat and trait categories.

row_names <- c('overall', 'growth rate', 'photosynthesis', 'respiration', 'freshwater', 'marine', 'terrestrial')
best_model_proportions <- matrix(NA, length(row_names), 3, dimnames = list(row_names, NULL))
cubic_vs_Sch <- matrix(NA, length(row_names), 2, dimnames = list(row_names, NULL)) # to compare cubic and Schoolfield AICs, if Boltzmann was the best
# Preallocate two matrices.

## Per category:
##  subset 'results'
##  per model, calculate the proportion of curves for which it was the best model (AIC).
for(i in 1:length(row_names)){
  # browser()
  
  group <- row_names[i]
  
  # Subset 'results'.
  if(group == 'overall'){
    tmp <- results
    
  } else if(group == 'growth rate'){
    tmp <- subset(results, results$Trait_name == 'growth rate')
    
  } else if((group == 'photosynthesis') || (group == 'respiration')){
    tmp <- results[grep(group, results$Trait_name),]
    # The data contain various measures of photosynthesis and respiration rates (e.g. gross and net photosynthesis).
    # I am doing broad comparison of the best model per trait. So, group the various measures for each trait.
    # ?grep - search for matches to a pattern.
    
  } else{
    tmp <- subset(results, results$Habitat == group)
  }
  
  n <- sum(!is.na(tmp[,'Best_model'])) # number of non-missing entries
  best_model_proportions[group,] <- table(tmp[,'Best_model']) / n # ?table - count each factor level.
  
  n_cubic_Sch <- sum(!is.na(tmp[,'Best_cubic_Sch']))
  cubic_vs_Sch[group,] <- c((sum(tmp[,'Best_cubic_Sch'] == 'cubic', na.rm = T) / n_cubic_Sch),
                            (sum(tmp[,'Best_cubic_Sch'] == 'Schoolfield', na.rm = T) / n_cubic_Sch)) # **error with 'table', more explicit
}

# best_model_proportions
# cubic_vs_Sch
# sum(best_model_proportions[1,]) # proportions should add up to 1
# Check matrices.

colnames(best_model_proportions) <- c('Boltzmann-Arrhenius', 'cubic polynomial', 'Schoolfield')
colnames(cubic_vs_Sch) <- c('cubic polynomail', 'Schoolfield')
# **

best_model_proportions_melt <- melt(best_model_proportions)
# cubic_vs_Sch_melt <- melt(cubic_vs_Sch)
colnames(best_model_proportions_melt) <- c('category', 'model', 'proportion')
# colnames(cubic_vs_Sch_melt) <- c('category', 'model', 'proportion')
# **

rm(row_names)
# Tidy name space.

# **annotate
p <- ggplot(best_model_proportions_melt, aes(x = '', y = proportion, fill = model)) +
  geom_bar(stat = 'identity',
           color = 'black', lwd = 0.2) +
  facet_grid(.~category) +
  facet_wrap(~category) +
  scale_x_discrete('') + scale_y_continuous('Proportion of curves') # titles of axes

p <- p + theme_bw() +
  theme(axis.ticks.x = element_blank(),
        # legend.title = element_blank(),
        legend.position = 'bottom',
        axis.text = element_text(size = 13),
        axis.title = element_text(size = 20),
        legend.text = element_text(size = 13),
        legend.title = element_text(size = 13, face = 'bold'))

p <- p + scale_fill_manual(values = c('cubic polynomial' = 'royalblue1', 'Boltzmann-Arrhenius' = 'seagreen3', 'Schoolfield' = 'orchid1'))
p
# text size
# 2-D faceting

pdf('../Results/Proportion_Best_Model.pdf')
print(p)
dev.off()

# If the Boltzmann is best, which is better between cubic and Schoolfield?
# Could report this in text, instead of a figure.


####################################
# Density plot of R^2 per model ####
####################################

# **annotate

which(is.infinite(results$R_squared_Sch)) # 510
results[510, 'R_squared_Sch'] # -Inf
results[510, 'R_squared_Sch'] <- NA

results[which(results$R_squared_cubic < 0),]$ID # none
results[which(results$R_squared_Bolt < 0),]$ID
results[which(results$R_squared_Sch < 0),]$ID
results[which(results$R_squared_Bolt < -1),]$ID # none
results[which(results$R_squared_Sch < -1),]$ID # ridiculously(?) high trait value at Tpk - **why?
# Manually check these plots

R2 <- cbind('cubic polynomial' = results$R_squared_cubic, 'Boltzmann-Arrhenius' = results$R_squared_Bolt, 'Schoolfield' = results$R_squared_Sch)
R2 <- melt(R2)
R2 <- R2[,-1]
dim(R2)
colnames(R2) <- c('model', 'R_squared')
sum(is.na(R2$R_squared)) # **
R2 <- R2[!is.na(R2$R_squared),]
dim(R2)

R2 <- R2[-which(R2$R_squared < 0),]
min(R2$R_squared)
max(R2$R_squared)
dim(R2)

R2_plot <- ggplot(R2, aes(x = R_squared, color = model)) +
  geom_density() +
  xlab(expression(R^2)) + ylab('number of curves') +
  theme_bw() +
  theme(legend.position = 'bottom',
        axis.text = element_text(size = 13),
        axis.title = element_text(size = 20),
        legend.text = element_text(size = 13),
        legend.title = element_text(size = 13, face = 'bold'))

R2_plot <- R2_plot + scale_color_manual(values = c('cubic polynomial' = 'royalblue1', 'Boltzmann-Arrhenius' = 'seagreen3', 'Schoolfield' = 'orchid1')) # note scale_color not scale_fill
R2_plot

pdf('../Results/R_Squared_Density.pdf')
print(R2_plot)
dev.off()


###########################################
# Comparison of R^2 and sum of squares ####
###########################################

column_names <- c('best', 'best_cubic_Sch')
highest_R2 <- data.frame(matrix(NA, nrow(results), 2, dimnames = list(NULL, column_names)))
lowest_RSS <- data.frame(matrix(NA, nrow(results), 2, dimnames = list(NULL, column_names)))

sum(is.na(results$R_squared_Bolt))
sum(is.na(results$R_squared_cubic))
sum(is.na(results$R_squared_Sch))
sum(is.na(results$RSS_Bolt))
sum(is.na(results$RSS_cubic))
sum(is.na(results$RSS_Sch))

report_best_stat <- function(Bolt_stat, cubic_stat, Sch_stat, best_stat){
  best <- NA
  best_cubic_Sch <- NA
  
  if((!is.na(Bolt_stat)) && (best_stat == Bolt_stat)){
    best <- 'Boltzmann-Arrhenius'
    
    if((!is.na(cubic_stat)) && (best_stat == cubic_stat)){
      best_cubic_Sch <- 'cubic polynomial'
    } else{
      best_cubic_Sch <- 'Schoolfield'
    }
    
  } else if((!is.na(cubic_stat)) && (best_stat == cubic_stat)){
    best <- 'cubic polynomial'
    
  } else if((!is.na(Sch_stat)) && (best_stat == Sch_stat)){
    best <- 'Schoolfield'
  }
  return(list(best, best_cubic_Sch))
}

for(i in 1:nrow(results)){
  Bolt_R2 <- results[i,]$R_squared_Bolt
  cubic_R2 <- results[i,]$R_squared_cubic
  Sch_R2 <- results[i,]$R_squared_Sch
  max_R2 <- max(c(Bolt_R2, cubic_R2, Sch_R2), na.rm = T)
  best_R2 <- report_best_stat(Bolt_R2, cubic_R2, Sch_R2, max_R2)
  highest_R2[i,1] <- best_R2[[1]]
  highest_R2[i,2] <- best_R2[[2]]
  
  Bolt_RSS <- results[i,]$RSS_Bolt
  cubic_RSS <- results[i,]$RSS_cubic
  Sch_RSS <- results[i,]$RSS_Sch
  min_RSS <- min(c(Bolt_RSS, cubic_RSS, Sch_RSS), na.rm = T)
  best_RSS <- report_best_stat(Bolt_RSS, cubic_RSS, Sch_RSS, min_RSS)
  lowest_RSS[i,1] <- best_RSS[[1]]
  lowest_RSS[i,2] <- best_RSS[[2]]
}

best_R2_proportions <- table(highest_R2$best) / sum(table(highest_R2$best))
best_RSS_proportions <- table(lowest_RSS$best) / sum(table(lowest_RSS$best))

tmp <- rbind(best_R2_proportions, best_RSS_proportions)
rownames(tmp) <- c('R squared', 'sum of squares')
tmp <- melt(tmp)
colnames(tmp) <- c('stat', 'model', 'proportion')

p2 <- ggplot(tmp, aes(x = '', y = proportion, fill = model)) +
  geom_bar(stat = 'identity',
           color = 'black', lwd = 0.2) +
  facet_grid(.~stat) +
  facet_wrap(~stat) +
  scale_x_discrete('') + scale_y_continuous('Proportion of curves') # titles of axes

p2 <- p2 + theme_bw() +
  theme(axis.ticks.x = element_blank(),
        legend.position = 'bottom')

p2 <- p2 + scale_fill_manual(values = c('cubic polynomial' = 'royalblue1', 'Boltzmann-Arrhenius' = 'seagreen3', 'Schoolfield' = 'orchid1'))
p2

################################################################
# Density plot of best-fit values of Schoolfield parameters ####
################################################################

sum(is.na(results$Sch_B0)) # should be 16 - number of IDs for which NLLS failed for Schoolfield
Sch_best_fit <- cbind(B0 = results$Sch_B0, E = results$Sch_E, Tpk = results$Tpk, Ed = results$Ed)
Sch_best_fit <- melt(Sch_best_fit)[-1]
colnames(Sch_best_fit) <- c('parameter', 'best_fit_value')
Sch_best_fit <- Sch_best_fit[!is.na(Sch_best_fit$best_fit_value),]

Sch_best_fit_values <- ggplot(Sch_best_fit, aes(x = best_fit_value)) +
  geom_density() +
  xlab('Best-fit value') +
  facet_grid(.~parameter) + facet_wrap(~parameter, scales = 'free') +
  theme_bw() +
  theme(axis.text = element_text(size = 13),
        axis.title = element_text(size = 20),
        strip.text = element_text(size = 13))
Sch_best_fit_values

pdf('../Results/Sch_Best_Fit_Values_Density.pdf')
print(Sch_best_fit_values)
dev.off()


results[which(results$Ed > 4),]$ID
results[which(results$Ed > 30),]$ID


#########################################################################
# Density plot of standard error for best-fit Schoolfield parameters ####
#########################################################################

results[which(results$Sch_B0_SE < 0),]$Sch_B0_SE
results[which(results$Sch_B0_SE < 0),]$ID

results[which(results$Sch_E_SE < 0),]$Sch_E_SE # none
results[which(results$Tpk_SE < 0),]$Tpk_SE # none
results[which(results$Ed_SE < 0),]$Ed_SE # none

Sch_SE <- abs(cbind(B0 = results$Sch_B0_SE, E = results$Sch_E_SE, Tpeak = results$Tpk_SE, Ed = results$Ed_SE)) # **abs
Sch_SE <- melt(Sch_SE)
Sch_SE <- Sch_SE[,-1]
colnames(Sch_SE) <- c('parameter', 'standard_error')
head(Sch_SE)
sum(is.na(Sch_SE$standard_error)) # 16*4
Sch_SE <- Sch_SE[!is.na(Sch_SE$standard_error),]

Sch_params_SE <- ggplot(Sch_SE, aes(x = standard_error)) +
  geom_density() +
  xlab('Standard error') +
  facet_grid(.~parameter) + facet_wrap(~parameter, scales = 'free') +
  theme_bw() +
  theme(axis.text = element_text(size = 10),
        axis.title = element_text(size = 20),
        strip.text = element_text(size = 13))
Sch_params_SE
# B0, T peak, Ed subscript

pdf('../Results/Sch_Params_SE_Density.pdf')
print(Sch_params_SE)
dev.off()


#####
# Inspect curves that:
#   represent only the rising part of the thermal response
#   have an initial decrease in the trait value
# 

IDs <- unique(thermal_data$FinalID)
# Make a vector of the IDs.

initial_decrease <- list()
no_rise <- list()
no_fall <- list()

for(i in 1:length(IDs)){
  d <- subset(thermal_data, thermal_data$FinalID == IDs[i])
  temps <- d$TempK
  traits <- d$Trait_minus_min_plus1
  
  if((length(unique(temps)) > 1) && (length(traits) >= 5)){
    
    if(traits[2] < traits[1]){
      initial_decrease[[length(initial_decrease) + 1]] <- IDs[i]
    }
    
    Tpk <- max(temps[which(traits == max(traits))])
    if(length(which(unique(temps) < Tpk)) <= 2){
      no_rise[[length(no_rise) + 1]] <- IDs[i]
    }
    if(length(which(unique(temps) > Tpk)) <= 2){
      no_fall[[length(no_fall) + 1]] <- IDs[i]
    }
  }
}

results_initial_decrease <- results[match(unlist(initial_decrease), results$ID),]
table(results_initial_decrease$Best_model) / sum(table(results_initial_decrease$Best_model))
# Seems cubic better in these cases

results_curve_rise_only <- results[match(unlist(curve_rise_only), results$ID),]
table(results_curve_rise_only$Best_model) / sum(table(results_curve_rise_only$Best_model))

########################
# Get example plots ####
########################