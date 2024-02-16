#!/usr/bin/env python

"""Makes a dispersal map (with parameters manually entered) and saves it to a binary file. (`HeatMapMultiPanel.R` opens and plots the maps.)"""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import scipy as sc
from SetUpOff import *
from NormalisationConstantsOff import *


shape = (30, 30) # (10, 10)
# Number of rows and columns in the array (resolution of landscape).

temps = sc.around(sc.linspace(10, 25, shape[0]) + 273.15, 2).reshape(-1, 1) # 10-25, 0-15
# temperature of each altitudinal band

#~ temps = sc.repeat(15 + 273.15, shape[0]).reshape(-1, 1) # fixed temperature
M = 100 # body mass

R = 1.5 # 1
# Ratio of cone's height and base radius.

A = 1 # cone area fixed to 1

c = sc.sqrt(R**2 + 1)
x = sc.sqrt(A / (sc.pi * c))
# Derive the values of c and x from geometric equations (see dissertation method).

B_0_dispersal = calculate_B_0_dispersal(M = 1000, T = 30 + 273.15,
	row_index = 30, # widest altitudinal band (row)
	T_r = 30, T_theta = 30, # array shape
	x = x, distance = 1/5)
# Normalise so the mean dispersal distance of the biggest body mass in the bottom row (hottest, widest) is 1/3 of the row's circumference.

nested_dispersal_map_birth, nested_dispersal_map = make_nested_dispersal_map(
	(29, 0), # (29, 0)
	# [row, column] index of dispersal destination
	
	shape,
	M,
	T = temps,
	B_0 = B_0_dispersal,
	alpha = 0.25, E = 0.65,
	max_revolutions = 5,
	x = x, c = c,
	birth_map = 1, fix_band_radius=True)

a = nested_dispersal_map.reshape(30, 30)
# The dispersal map is flattened (1D) - to help plotting, make it 2D.

sc.save('../../Results/DispMaps/TempNoArea_Top.npy', a) #% M
#~ print(a)
print(sc.around(a, 4))
#~ print(sc.around(sc.log(a), 1))
# Save and print dispersal map.
