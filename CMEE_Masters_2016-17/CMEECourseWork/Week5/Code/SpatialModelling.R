# load the raster library to handle GIS data files
library(raster)
## Loading required package: sp

# load the four variables from their TIFF files
rich <- raster('../Data/avian_richness.tif')
aet <- raster('../Data/mean_aet.tif')
temp <- raster('../Data/mean_temp.tif')
elev <- raster('../Data/elev.tif')

# split the figure area into a two by two layout
par(mfrow=c(2,2))

# plot a histogram of the values in each raster, setting nice 'main' titles
hist(rich, main='Avian species richness')
hist(aet, main='Mean AET')
hist(temp, main='Mean annual temperature')
hist(elev, main='Elevation')

# split the figure area into a two by two layout
par(mfrow=c(2,2))

# plot a map of the values in each raster, setting nice 'main' titles

plot(rich, main='Avian species richness')
plot(aet, main='Mean AET')
plot(temp, main='Mean annual temperature')
plot(elev, main='Elevation')

data <- stack(rich, aet, elev, temp)
print(data)

data_df <- as(data, 'SpatialPixelsDataFrame')
summary(data_df)

# plot a map of the data in data_df, chosing the column
# holding the richness data, changing the default colours
# and showing the geographic scales
spplot(data_df, zcol='avian_richness', col.regions=heat.colors(20),
       scales=list(draw=TRUE))

# Create three figures in a single panel
par(mfrow=c(1,3))
# Now plot richness as a function of each environmental variable
plot(avian_richness ~ mean_aet, data=data_df)
plot(avian_richness ~ mean_temp, data=data_df)
plot(avian_richness ~ elev, data=data_df)

# load the new function: clifford.test()
source('clifford.test.R')
# run the standard test
cor.test(~ avian_richness + mean_aet, data=data_df)

clifford.test(as.matrix(rich), as.matrix(aet))

# load the spatial dependence analysis package
library(spdep)

# All cells with centres closer than 150km are neighbours of a cell
neighbours <- dnearneigh(data_df, d1=0, d2=150)
# convert that to a weighted list of neighbours
neighbours.lw <- nb2listw(neighbours, zero.policy=TRUE)
# global Moran's I for avian richness
rich.moran <- moran.test(data_df$avian_richness,
                         neighbours.lw, zero.policy=TRUE)
rich.moran

# Use the same neighbour definition to get local autocorrelation
rich.lisa <- localmoran(data_df$avian_richness,
                        neighbours.lw, zero.policy=TRUE)
# The rich.lisa results contain several variables in columns: we
# add one to our dataframe to plot it
data_df$rich_lisa <- rich.lisa[,1]
# plot the values.
spplot(data_df, zcol='rich_lisa', col.regions=heat.colors(20),
       scales=list(draw=TRUE))

# Fit a simple linear model
simple_model <- lm(avian_richness ~ mean_aet + elev + mean_temp, data = data_df)
summary(simple_model)

# Fit a spatial autoregressive model: this is much slower and
# can take minutes to calculate
sar_model <- errorsarlm(avian_richness ~ mean_aet + elev + mean_temp,
                        data = data_df, listw = neighbours.lw, zero.policy = TRUE)
summary(sar_model)

# extract the predictions from the model into the spatial
# data frame
data_df$simple_fit <- predict(simple_model)
data_df$sar_fit <- predict(sar_model)
# Compare those two predictions with the data
spplot(data_df, c("avian_richness", "simple_fit", "sar_fit"),
       col.regions = heat.colors(20), scales = list(draw = TRUE))

# extract the residuals from the model into the spatial data
# frame
data_df$simple_resid <- residuals(simple_model)
data_df$sar_resid <- residuals(sar_model)
# Create a 21 colour ramp from blue to red, centred on zero
colPal <- colorRampPalette(c("cornflowerblue", "grey", "firebrick"))
colours <- colPal(21)
breaks <- seq(-600, 600, length = 21)
# plot the residuals side by side
spplot(data_df, c("simple_resid", "sar_resid"), col.regions = colours,
       at = breaks, scales = list(draw = TRUE))

# Install a missing library to calculate correlograms
library(ncf)
# extract the X and Y coordinates
data_xy <- data.frame(coordinates(data_df))
# calculate a correlogram for avian richness: a slow process!
rich.correlog <- correlog(data_xy$x, data_xy$y, data_df$avian_richness,
                          increment = 100, resamp = 0)
plot(rich.correlog)

par(mfrow = c(1, 2))
# convert three key variables into a data frame
rich.correlog <- data.frame(rich.correlog[1:3])
# plot the size of the distance bins
plot(n ~ mean.of.class, data = rich.correlog, type = "o")
# plot a correlogram for shorter distances
plot(correlation ~ mean.of.class, data = rich.correlog, type = "o",
     subset = mean.of.class < 5000)
# add a horizontal zero correlation line
abline(h = 0)

# Calculate correlograms for the residuals in the two models
simple.correlog <- correlog(data_xy$x, data_xy$y, data_df$simple_resid,
                            increment = 100, resamp = 0)
sar.correlog <- correlog(data_xy$x, data_xy$y, data_df$sar_resid,
                         increment = 100, resamp = 0)
# Convert those to make them easier to plot
simple.correlog <- data.frame(simple.correlog[1:3])
sar.correlog <- data.frame(sar.correlog[1:3])

# plot a correlogram for shorter distances
plot(correlation ~ mean.of.class, data = simple.correlog, type = "o",
     subset = mean.of.class < 5000)

# add the data for the SAR model to compare them
lines(correlation ~ mean.of.class, data = sar.correlog, type = "o",
      subset = mean.of.class < 5000, col = "red")
# add a horizontal zero correlation line
abline(h = 0)