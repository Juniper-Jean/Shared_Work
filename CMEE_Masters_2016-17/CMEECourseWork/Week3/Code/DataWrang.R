################################################################
################## Wrangling the Pound Hill Dataset ############
################################################################

############# Load the dataset ###############
MyData <- as.matrix(read.csv("../Data/PoundHillData.csv",header = F))
# **
# The function 'read.csv()' takes a file path as an argument and reads the file's comma-separated data.
# We return the values as a matrix, which we assign to the object 'MyData'.
# We assign the values returned by 'read.csv()' to the object 'MyData'.
# Import data from a csv and store as a matrix, 'MyData'.
# Matrices store objects as one type only, so R homogenises data when it is imported as a matrix. This ensures data is imported as it is, so is useful before wrangling.
# 'header = false' - the raw data do not have real headers. 'read.csv' would otherwise convert the first row to column headers.

MyMetaData <- read.csv("../Data/PoundHillMetaData.csv",header = T, sep=";", stringsAsFactors = F)
# Import the data's documentation (metadata).
# header = true because we do have metadata headers.
# Characters are converted to factors by default - we do not want this.
# Character variables are converted to
# read.csv converts character variables to factors - interprets every text column as a grouping variable.

############# Inspect the dataset ###############
head(MyData)
dim(MyData)
str(MyData)
# See the first part, size and structure of the data.

############# Transpose ###############
MyData <- t(MyData)
head(MyData)
dim(MyData)
# t() transposes the data - rotate it - swap the columns and rows.
# The data is in a wide format: a species' repeated observations are in one row. This is not ideal for analysis. Convert to a long format, where each row is an observation per species.
# Easier to work with
# But this is done later - so what is transpose?

############# Replace species absences with zeros ###############
MyData[MyData == ""] = 0
#

############# Convert raw matrix to data frame ###############

TempData <- as.data.frame(MyData[-1,],stringsAsFactors = F) #stringsAsFactors = F is important!
colnames(TempData) <- MyData[1,] # assign column names from original data


############# Convert from wide to long format  ###############
require(reshape2) # load the reshape2 package

?melt #check out the melt function
MyWrangledData <- melt(TempData, id=c("Cultivation", "Block", "Plot", "Quadrat"), 
variable.name = "Species", value.name = "Count")
MyWrangledData[, "Cultivation"] <- as.factor(MyWrangledData[, "Cultivation"])
MyWrangledData[, "Block"] <- as.factor(MyWrangledData[, "Block"])
MyWrangledData[, "Plot"] <- as.factor(MyWrangledData[, "Plot"])
MyWrangledData[, "Quadrat"] <- as.factor(MyWrangledData[, "Quadrat"])
MyWrangledData[, "Count"] <- as.numeric(MyWrangledData[, "Count"])

str(MyWrangledData)
head(MyWrangledData)
dim(MyWrangledData)

############# Start exploring the data (extend the script below)!  ###############
