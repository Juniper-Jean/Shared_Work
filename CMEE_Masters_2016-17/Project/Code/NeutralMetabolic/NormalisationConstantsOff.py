#!/usr/bin/env python

"""
Calculates the normalisation constants for the dependence of:
- abundance on body mass
- dispersal distance on body mass and temperature.
"""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.2' # Imports `SetUpOff` instead of `SetUp`, otherwise no change from v0.0.1.

import pdb
import scipy as sc
from SetUpOff import * # file name
from scipy import stats


def calculate_b_density(biggest_body_mass, highest_resolution, c, x):
	"""Calculates the normalisation constant for the scaling of density and body mass. Normalises so the lowest abundance of a cell in the simulation is 1."""
	#~ pdb.set_trace()
	
	abundance_biggest_M = biggest_body_mass**-0.75
	# The guild with the biggest body mass has the fewest individuals per m^2.
	# *Does Damuth's rule apply to non-animal spp?
	
	T_r, T_theta = highest_resolution
	smallest_cell_area = (sc.pi * c * (((0 + 1) * x) / T_r)**2) / T_theta
	# Cells at the mountain top represent the smallest area.
	# area of top altitudinal band (a cone's lateral surface) is pi*R*s = pi*c*R^2
	# Divide by T_theta to get cell area - T_theta is the array's width in # cells.
	# s = cR, so s/c = R
	# R = (S_r + 1) / c
	# Multiply by cx/T_r, to convert to metres:
	# R = (S_r + 1)x / T_r
	# 'S_r + 1' is top band's (outer) radius in number of cells.
	
	lowest_cell_abundance = abundance_biggest_M * smallest_cell_area # *round?
	b_density = 1 / lowest_cell_abundance
	return b_density


def calculate_B_0_dispersal(M, T, row_index, T_r, T_theta, x, distance, alpha=0.25, E=0.65): # percentile
	"""Calculates the normalisation constant for the dependence of dispersal distance on body mass and temperature."""
	#~ pdb.set_trace()
	
	y = metabolic_scaling(M, T,
		1, # = B_0
		alpha, E)
	mean_variate = stats.halfnorm.mean() # half-normal as want probability of mean distance in either direction
	#variate_Xpercentile = stats.norm.ppf(percentile / 100) # Note: 50th percentile is median, not mean
	d_theta = y * mean_variate
	circumference = 2*sc.pi*(row_index + 0.5)
	n_theta = (d_theta * T_r * T_theta) / (circumference * x)
	B_0 = (T_theta * distance) / n_theta
	return B_0

# Sets the mean dispersal distance
	# for a given body mass, altitude (row), and temperature
	# to a given proportion of the circumference.
# Later, the program uses this as a reference to set distance for other body masses, altitudes, and temperatures.


#~ b_density = calculate_b_density(1000, (30, 30), c, x)
#~ B_0_dispersal = calculate_B_0_dispersal(M = 1000, T = 30 + 273.15, row_index = 30, T_r = 30, T_theta = 30, x = x, distance = 1/3)

