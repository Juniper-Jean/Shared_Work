'Week5' Contents

Geographic Information Systems (GIS)
October 31 - November 4 2016

/Code
CMEE_Example_copy.py - Uses GIS to summarise mean annual temperature and total precipitation within land cover classes in the UK.

SpatialModelling.R - Fits statistical models to spatial data.

clifford.test.R - Clifford Test for spatial autocorrelation. Input for 'SpatialModelling.R'.

/Data
R:

Inputs (raster files) for 'CMEE_Example_copy.py':
	boi1_15.tif - Mean annual temperature for UK and west Europe.

	bio1_16.tif - Mean annual temperature for east Europe.

	bio12_15.tif - Total annual precipitation for UK and west Europe.

	bio12_16.tif - Total annual precipitation for east Europe.

	g250_06.tif - 2006 CORINE land cover classes for the EU.

	bio1_UK_BNG.tif - Reprojection of 'bio1_15.tif' using British National Grid coordinate system.

	bio12_UK_BNG.tif - Reprojection of 'bio1_16.tif' using British National Grid coordinate system.

	g250_06_UK_BNG.tif - Reprojection of 'g250_06.tif' using British National Grid coordinate system.

Inputs (raster files) for 'SpatialModelling.R':
	avian_richness.tif - Avian species richness across the Afrotropics.

	mean_aet.tif - Average annual actual evapotranspiration across the Afrotropics.

	mean_temp.tif - Average annual temperature across the Afrotropics.

	elev.tif - Mean elevation across the Afrotropics.

/Results
zonalstats.csv - Mean annual temperature and total precipitation within land cover classes in the UK. Output of 'CMEE_Example_copy.py'.
