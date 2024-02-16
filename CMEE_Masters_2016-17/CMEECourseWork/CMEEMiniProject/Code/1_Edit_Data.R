# Calum Pennington (c.pennington@imperial.ac.uk)
# January 2016

# This script prepares the data, 'GrowthRespPhotoData.csv', for analysis:
#   removes unneeded columns
#   handles missing, negative and zero values
#   converts temperatures to Kelvin.

rm(list = ls()) # Remove objects.
graphics.off() # Close graphics devices.

raw_data <- read.csv('../Data/GrowthRespPhotoData.csv',
                     stringsAsFactors = F) # Do not convert character vectors to factors. **why
# Import data.

dim(raw_data) # 21978*165
head(raw_data)
colnames(raw_data)
# See:
#   size and top part of data
#   column names.

raw_data <- raw_data[,c('FinalID', 'OriginalTraitName', 'OriginalTraitDef', 'StandardisedTraitName', 'StandardisedTraitDef', 'OriginalTraitValue', 'OriginalTraitUnit', 'OriginalErrorPos', 'OriginalErrorNeg', 'OriginalErrorUnit', 'StandardisedTraitValue', 'StandardisedTraitUnit', 'StandardisedErrorPos', 'StandardisedErrorNeg', 'StandardisedErrorUnit', 'Replicates', 'Habitat', 'Labfield', 'AmbientTemp', 'AmbientTempUnit', 'Climate', 'LocationDate', 'Consumer', 'ConCommon', 'ConKingdom', 'ConPhylum', 'ConClass', 'ConOrder', 'ConFamily', 'ConGenus', 'ConSpecies', 'ConTemp', 'ConTempUnit', 'ConSize', 'ConSizeUnit', 'ConSizeType', 'ConSizeSI', 'ConSizeUnitSI', 'ConMassValueSI', 'ConMassUnitSI')]
dim(raw_data) # 21978*40
# Cut unneeded columns.


#####
# The dataset's authors converted values of the same trait from different sources to the same unit.
# Except for growth rate, this was either not completed or done wrongly.
# Often, an original value is missing a standardised version.
# For many IDs, standardised values were equal when original ones differed. Maybe the first value was standardised and mistakenly copied to subsequent rows.
# So, for growth rate, I use standardised values; otherwise, I use original ones.

raw_data$Trait_value <- ifelse((raw_data$OriginalTraitName == 'growth rate'), raw_data$StandardisedTraitValue, raw_data$OriginalTraitValue)
# Make a new column.
# For each row, if 'OriginalTraitName' is 'growth rate', copy the standardised value to this column. Otherwise, copy the original value.


#####
unique(raw_data$StandardisedTraitName)
sum(is.na(raw_data$StandardisedTraitName)) # 8182
unique(raw_data$OriginalTraitName)
sum(is.na(raw_data$OriginalTraitName)) # 0
# See the unique standardised and original trait names.
# Count the rows missing a name.

raw_data$Trait_name <- ifelse(is.na(raw_data$StandardisedTraitName), raw_data$OriginalTraitName, raw_data$StandardisedTraitName)
dim(raw_data) # 21978*42
# Sources often used different names for the same trait. So, the dataset's authors devised standardised names.
# For rows missing a standardised name, I use the original one.


#################
# Remove NAs ####
#################

sum(is.na(raw_data$AmbientTemp)) # 21819
sum(is.na(raw_data$ConTemp)) # 0
# **explain why ambient temp is preferable
# Could replace NAs in the 'AmbientTemp' column with corresponding values from 'ConTemp':
# **explain why - see metadata
  # raw_data$Temp <- raw_data$AmbientTemp
  # NAs <- is.na(raw_data$AmbientTemp)
  # raw_data$Temp[NAs] <- raw_data$ConTemp[NAs]
  # Copy 'AmbientTemp' to a new column, 'Temp'.
  # 'NA' is a missing value indicator. 'is.na' shows which elements are missing - returns a vector of booleans.
  # 'df[]' calls parts of a dataframe that meet a condition.
  # If the 'AmbientTemp' value is NA, replace the corresponding value in 'Temp' with that from 'ConTemp'.
# Nearly all rows are missing ambient temp, but all have consumer temp. Instead of mixing the two, I think it is best to keep the data type constant, and use consumer temp for all rows.

sum(is.na(raw_data$Trait_value)) # 63
filtered_data <- subset(raw_data, !is.na(raw_data$Trait_value))
dim(filtered_data) # 21915*42
# Remove rows with missing trait values
# 21978 - 63


###############################################
# Deal with negative and zero trait values ####
###############################################

# **explain why

negatives_zeros <- function(d){
  # browser()
  min_val <- min(d$Trait_value)
  if((min_val <= 0)){
    d$Trait_minus_min <- d$Trait_value - min_val
    # If there are negative trait values, substract the min from all trait values.
    # Save this as a new column, 'Trait_minus_min'.
    # **explain why this works
    # (Rows with the min value now have value 0.)
    # dim(filtered_data) # 18754*41
    # filtered_data$Trait_minus_min # Check new column.
    # dim(d) # 8093*43
    # d$Trait_minus_min # Check new column.
    
    if(length(which(d$Trait_minus_min == 0)) > 0){
      d$Trait_minus_min_plus1 <- d$Trait_minus_min + 1
      # Add 1 to 'Trait_minus_min', if there are values of 0.
    }
  } else{
    if(length(which(d$Trait_value == 0)) > 0){
      d$Trait_plus1 <- d$Trait_value + 1
      # If there values of 0 but no negative values, add 1 to 'Trait_value'.
    }
  }
  return(d)
}
# **may be better to remove rows with 0s

# I handle growth rate separately, as this data is standardised. (To deal with negatives, I substract the min value.)

growth_rate <- filtered_data[filtered_data$Trait_name == 'growth rate',] # Get rows where the trait is 'growth rate'.
other_traits <- filtered_data[filtered_data$Trait_name != 'growth rate',] # '!=' - not equal
# Get all columns, so, when I later recombine these subsets, rows are not jumbled
# - corresponding cells in different columns stay in the same row.

min(growth_rate$Trait_value) # ~ -0.000005
min(other_traits$Trait_value) # ~ -285
growth_rate <- negatives_zeros(growth_rate)
other_traits <- negatives_zeros(other_traits)

filtered_data2 <- filtered_data # Copy the data, so I can undo changes.
filtered_data2 <- rbind(growth_rate, other_traits)
dim(filtered_data2) # 21915*44
min(filtered_data2$Trait_minus_min_plus1) # check


#####################################
# Convert temperatures to Kelvin ####
#####################################

unique(filtered_data2$ConTempUnit)
# See factor levels - check original unit is Celsius.

filtered_data2$TempK <- filtered_data2$ConTemp + 273.15
# dim(filtered_data)
# filtered_data$TempK


###########################################
# Rearrange columns; cut unneeded ones ####
###########################################

if(!is.null(filtered_data2$Trait_minus_min_plus1)){
  thermal_data <- filtered_data2[,c('FinalID', 'OriginalTraitName', 'OriginalTraitDef', 'StandardisedTraitName', 'StandardisedTraitDef', 'Trait_name', 'Trait_minus_min_plus1', 'ConTemp', 'TempK', 'StandardisedTraitValue', 'StandardisedTraitUnit', 'StandardisedErrorPos', 'StandardisedErrorNeg', 'StandardisedErrorUnit', 'OriginalTraitValue', 'OriginalTraitUnit', 'OriginalErrorPos', 'OriginalErrorNeg', 'OriginalErrorUnit', 'Replicates', 'Habitat', 'Labfield', 'Climate', 'LocationDate', 'Consumer', 'ConKingdom', 'ConPhylum', 'ConClass', 'ConOrder', 'ConFamily', 'ConGenus', 'ConSpecies', 'ConSize', 'ConSizeUnit', 'ConSizeType', 'ConSizeSI', 'ConSizeUnitSI', 'ConMassValueSI', 'ConMassUnitSI')]
  
} else if(!is.null(filtered_data2$Trait_minus_min)){
  thermal_data <- filtered_data2[,c('FinalID', 'OriginalTraitName', 'OriginalTraitDef', 'StandardisedTraitName', 'StandardisedTraitDef', 'Trait_name', 'Trait_minus_min', 'ConTemp', 'TempK', 'StandardisedTraitValue', 'StandardisedTraitUnit', 'StandardisedErrorPos', 'StandardisedErrorNeg', 'StandardisedErrorUnit', 'OriginalTraitValue', 'OriginalTraitUnit', 'OriginalErrorPos', 'OriginalErrorNeg', 'OriginalErrorUnit', 'Replicates', 'Habitat', 'Labfield', 'Climate', 'LocationDate', 'Consumer', 'ConKingdom', 'ConPhylum', 'ConClass', 'ConOrder', 'ConFamily', 'ConGenus', 'ConSpecies', 'ConSize', 'ConSizeUnit', 'ConSizeType', 'ConSizeSI', 'ConSizeUnitSI', 'ConMassValueSI', 'ConMassUnitSI')]
  
} else if(!is.null(filtered_data2$Trait_plus1)){
  thermal_data <- filtered_data2[,c('FinalID', 'OriginalTraitName', 'OriginalTraitDef', 'StandardisedTraitName', 'StandardisedTraitDef',  'Trait_name','Trait_plus1', 'ConTemp', 'TempK', 'StandardisedTraitValue', 'StandardisedTraitUnit', 'StandardisedErrorPos', 'StandardisedErrorNeg', 'StandardisedErrorUnit', 'OriginalTraitValue', 'OriginalTraitUnit', 'OriginalErrorPos', 'OriginalErrorNeg', 'OriginalErrorUnit', 'Replicates', 'Habitat', 'Labfield', 'Climate', 'LocationDate', 'Consumer', 'ConKingdom', 'ConPhylum', 'ConClass', 'ConOrder', 'ConFamily', 'ConGenus', 'ConSpecies', 'ConSize', 'ConSizeUnit', 'ConSizeType', 'ConSizeSI', 'ConSizeUnitSI', 'ConMassValueSI', 'ConMassUnitSI')]
  
} else{
  thermal_data <- filtered_data2[,c('FinalID', 'OriginalTraitName', 'OriginalTraitDef', 'StandardisedTraitName', 'StandardisedTraitDef',  'Trait_name', 'Trait_value', 'ConTemp', 'TempK', 'StandardisedTraitValue', 'StandardisedTraitUnit', 'StandardisedErrorPos', 'StandardisedErrorNeg', 'StandardisedErrorUnit', 'OriginalTraitValue', 'OriginalTraitUnit', 'OriginalErrorPos', 'OriginalErrorNeg', 'OriginalErrorUnit', 'Replicates', 'Habitat', 'Labfield', 'Climate', 'LocationDate', 'Consumer', 'ConKingdom', 'ConPhylum', 'ConClass', 'ConOrder', 'ConFamily', 'ConGenus', 'ConSpecies', 'ConSize', 'ConSizeUnit', 'ConSizeType', 'ConSizeSI', 'ConSizeUnitSI', 'ConMassValueSI', 'ConMassUnitSI')]
}


#####
rm(raw_data, growth_rate, other_traits, filtered_data, filtered_data2)
# Tidy namespace.

write.csv(thermal_data, '../Data/Edited_Data.csv', row.names = F)
# Save edited data to a csv.