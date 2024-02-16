#!/usr/bin/env python

"""
Functions to set up the simulated community and birth/death and dispersal maps, for given parameter arguments.

Change from version 0.0.1: option to remove the effect of area on dispersal (gives each altitudinal band the same radius).
"""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.2'

# important which shebang you use - p60 SilBioComp

import pdb, sys
import scipy as sc
from scipy import stats


def get_xy(z, n):
	"""Finds x and y, given z and n.
	n is number of columns.
	(Items in a 2D array can instead be held in a 1D array. If you want to keep 2D positions, you can still reduce the number of dimensions: Use the formula, z = nx + y, to convert an [x, y] pair of indices to an index, z, in a 1D array.)"""
	y = z % n
	x = int((z - y) / n)
	return (x, y) # immutable tuple


####################
## Function to set up the simulated community and its initial species richness
####################

# The simulated system is a 3D array representing a community of individuals on a mountain.
# Each item in the array is an integer and represents an individual. The integer's value is the individual's species.
# Consider a 3D array as a group of 2D arrays. The 2D arrays represent altitudinal bands.
# Rows in a 2D array are positions along a band.
# The amount of non-zero integers in a row is the position's density of individuals.
# Zero is not a species identity. If an item is zero, it does not represent an individual and the simulation ignores it. This allows the program to have positions with different abundances (and is needed as an array dimension has fixed length).

# (Occasionally, the program represents the system as a 2D array - ignoring density/the 3rd dimension. Then, rows are altitudinal bands, and columns, positions along a band.)
# Consider the 1st and 2nd dimensions as the landscape: the position of individuals on the simulated mountain.
# Occasionally the program uses a 2D array, ignoring density/the 3rd dimension. Then...

def initialise_community(nrows, ncols, b_density, M, c, x, fix_abundance=False, species_richness=1, max_diversity=False):
	"""
	Sets up:
	- the simulated community (a 3D array)
	- its initial species richness (amount of unique integers)
	- abundance of positions (amount of individuals per position - length of array's 3rd dimension).
	"""
	#~ pdb.set_trace()
	
	abundance_per_m2 = b_density * M**-0.75
	# Calculate the number of individuals in 1 m^2.
	
	S_r = sc.arange(nrows)
	T_r, T_theta = nrows, ncols
	cell_areas = (sc.pi * c * ((((S_r + 1) * x) / T_r)**2 - ((S_r * x) / T_r)**2)) / T_theta
	cell_abundances = sc.around(abundance_per_m2 * cell_areas, 0).astype(sc.int64, copy=False)
	# For each altitudinal band, calculate the number of individuals in, and area of, a cell.
	# Amount of individuals corresponds to array size, so round abundance to the nearest whole number.
	# A mountain base covers more area than the top. I use a cone's surface as a model of a mountain, but, in silico, I represent the surface as a square array. Each row in the array is an altitudinal band. Going up the mountain, each [row, column] position in the array represents an increasingly narrow area.
	
	if fix_abundance == True:
		community = sc.ones((nrows, ncols, cell_abundances[14]), dtype=sc.int64)
		# fix abundances - use that of middle altitudinal band
	else:
		max_cell_abundance = sc.amax(cell_abundances)
		community = sc.zeros((nrows, max_cell_abundance), dtype=sc.int64)
		for i in range(nrows):
			community[i, :cell_abundances[i]] = 1
		community = sc.repeat(community, ncols, axis=0).reshape(nrows, ncols, max_cell_abundance)
		# Make a 2D array of zeros. Each row is an altitudinal band. The 2nd dimension's length is the max cell abundance.
		# For each row, change the first x items to 1; x is the cell abundance in the band.
		# Replicate each row; the number of replicates is the number of positions along a band (ncols).
		# `sc.repeat(a, repeats, axis)` repeats array elements. `repeats` - number of repeats per element. `axis` - axis along which to repeat values. Returns a flat array.
		# -`sc.reshape` reshapes an array.
	
	#~ pdb.set_trace()
	community_size = sc.flatnonzero(community).size
	# Count non-zero items - individuals. (The total differs slightly from `density`, as the function rounds cell abundances.)
	# `sc.flatnonzero(a)` returns indices of non-zero items (in the flattened version of a).
	# `sc.size` returns the number of elements.
	
	if species_richness > community_size:
		sys.exit("The number of species (`species_richness`) cannot exceed number of individuals (the system's size, which is `nrows` * `ncols` * `density`).")
		# Exit the program and print an error message.
	if max_diversity == True:
		community.ravel()[sc.flatnonzero(community)] = sc.arange(community_size) + 1
		# Generate an initial state with the max number of species for the community size.
		# `sc.flatnonzero` - don't change the value of zeros - these aren't individuals.
		# '+ 1' as 0 is not a species identity.
	elif species_richness > 1:
		species = sc.arange(species_richness) + 1
		# Make a 1D array of species identities (integers).
		
		community.ravel()[sc.flatnonzero(community)[:species_richness]] = species
		# There must be at least one individual per species.
		
		community.ravel()[sc.flatnonzero(community)[species_richness:]] = sc.random.choice(species, size=community_size - species_richness, replace=True)
		# The remaining individuals can take any species identity. I.e., each species has random abundance.
	
	community.ravel()[sc.flatnonzero(community)] = sc.random.permutation(community.ravel()[sc.flatnonzero(community)])
	# Randomly permutate the non-zero items of `community` (i.e. keep zeros in place), so an individual is equally likely to take any species identity.
	# Without this line, the first `species_richness` individuals always will be different species.
	
	return community, cell_areas, cell_abundances

# `sc.arange` generates values in the half-open interval `[start, stop)` (including `start`, excluding `stop`).
# `sc.around` rounds to the given number of decimals.
# `sc.zeros` makes an array of given shape and type, filled with zeros.
# `sc.ravel` returns a contiguous flattened (1D) version of an array.
# `sc.random.choice` generates a random sample of a given size, from a 1D array (assumes a uniform distribution).

# *
	# density constant in a sim, but varies across guilds
	# -precipitation
	# parameterise - **Damuth equation - cells don't represent area in m
	
	# use initial richness of max/min/other? sensitivity?

## Test `initialise_community` function
#~ community, cell_areas, cell_abundances = initialise_community(30, 30, b_density, 10**3, c, x)#, fix_abundance=True, species_richness=1, max_diversity=False
#~ community[community > 0].size
# To get `b_density`, c, and x, see 'NormConstantsDensityDispersal_Aug7Mon.py'.


####################
## Functions to set up dispersal map
####################

def metabolic_scaling(M, T, B_0, alpha, E=0.65): # temp in kelvin (K) (C + 273.15)
	"""Returns the output of the central equation of the Metabolic Theory of Ecology."""
	
	k = 8.617*10**-5 # eV/K (electronvolts per kelvin)
	# Boltzmann constant
	
	return B_0*M**alpha*sc.exp(-E/(k*T))

# The approximate effect of:
	# body mass is a power law (alpha is the exponent)
	# temperature is exponential and described by the Arrhenius equation.
# M - body mass
# T - temperature (kelvin)
# B_0 - a normalisation constant, independent of body mass and temperature
# E - activation energy

# *
	# describe better
	
	# tiny
	# How parameterise B0?
	
	# need Tref? Say why not in method
	
	# Body size relations have a constant
	# -take form y = aW^b, a and b are empirically derived constants
	# how inc in central equation?


def probability_of_theta_distance(n_theta, mean_radius, x, T_r, T_theta, y):
	""""""
	#~ pdb.set_trace()
	
	circumference = 2*sc.pi*mean_radius
	variate = (n_theta * x * circumference) / (T_theta * T_r * y)
	probability = stats.norm.pdf(variate)
	return probability

# The program runs this function with multiple arguments to `n_theta` at once.
# `stats.norm.pdf(x, loc=0, scale=1)` evaluates at x, the probability density function of the normal distribution. `loc`/`scale` - location/scale parameter


def make_nested_dispersal_map(destination, shape, M, T, B_0, alpha, E, max_revolutions, x, c, birth_map, fix_band_radius=False):
	"""Calculates the probability of dispersing to a given cell, from every cell in the simulated landscape. Factors in each position's birth rate."""
	#~ pdb.set_trace()
	
	nrows, ncols = shape
	indices_axis0 = sc.arange(nrows).reshape(-1, 1)
	indices_axis1 = sc.arange(ncols)
	# A 2D array has two axes: axis 0 runs vertically across rows, axis 1 runs horizontally across columns.
	# `reshape(-1, 1)`
		# So the program can use broadcasting to vectorise operations like outer product, it occasionally swaps the axes of 1D arrays.
		# (Items in these arrays are often data, such as temperature, about rows in the simulated system).
		# `-1` - the dimension's length is inferred from the array's size and other dimensions (i.e., it is as long as needed).
	
	y = metabolic_scaling(M, T, B_0, alpha, E)
	# no `reshape(-1, 1)`/`[:, sc.newaxis]` as done for temperatures
	
	## Theta displacements (horizontally across columns)
	radii = (sc.arange(nrows) + 0.5).reshape(-1, 1)
	if fix_band_radius == True:
		radii = sc.repeat(radii[14], nrows).reshape(-1, 1)
	# To remove the effect of area on dispersal, fix the radius of altitudinal bands (the cone becomes a cylinder).
	# use radius of middle band
	# middle of 30 rows is index 14 (middle of indices 0-29) - must change, if change # rows
	
	mean_radial_position = (radii + radii[destination[0]]) / 2 # (S_r + 0.5 + E_r + 0.5) / 2
	
	# *explain
	displacements_negative_direction = (indices_axis1 - destination[1]) % ncols # going left
	displacements_positive_direction = (destination[1] - indices_axis1) % ncols # right
	
	distance_of_x_revolutions = sc.arange(max_revolutions + 1).reshape(-1, 1) * ncols
	distances_neg_dir = displacements_negative_direction + distance_of_x_revolutions # broadcasting - result is 2D
	distances_pos_dir = displacements_positive_direction + distance_of_x_revolutions
	
	probabilities_theta_displacements = sc.zeros((nrows, ncols))
	for i in range(nrows):
		probabilities_neg_displacements = probability_of_theta_distance(-distances_neg_dir, mean_radial_position[i], x, nrows, ncols, y[i]).sum(axis=0)
		# Note '-'.
		# `distances_neg_dir` and output are 2D arrays -> sum along axis 0 -> 1D
		
		probabilities_pos_displacements = probability_of_theta_distance(distances_pos_dir, mean_radial_position[i], x, nrows, ncols, y[i]).sum(axis=0)
		probabilities_theta_displacements[i] = probabilities_neg_displacements + probabilities_pos_displacements
	
	## r displacements (vertically across rows)
	#~ pdb.set_trace()
	n_r = indices_axis0 - destination[0] # r displacements
	T_r = nrows
	variate = (n_r * c * x) / (T_r * y)
	probabilities_r_displacements = stats.norm.pdf(variate)
	
	
	nested_dispersal_map = probabilities_theta_displacements * probabilities_r_displacements
	nested_dispersal_map_birth = nested_dispersal_map * birth_map
	# Multiply arrays element-wise.
	
	nested_dispersal_map_birth = nested_dispersal_map_birth / nested_dispersal_map_birth.sum()
	nested_dispersal_map = nested_dispersal_map / nested_dispersal_map.sum()
	# Re-normalise so probabilities sum to 1.
	# `sc.sum` sums array elements.
	
	return nested_dispersal_map_birth.ravel(), nested_dispersal_map.ravel()
	# Return the probability distribution as a 1D array.

## Test
#~ shape = (30, 30)
#~ community = sc.ones(shape, dtype=sc.int64)
#~ temps = sc.around(sc.linspace(0, 30, shape[0]) + 273.15, 2).reshape(-1, 1)
#~ #temps = sc.repeat(15 + 273.15, shape[0]).reshape(-1, 1)
#~ nested_dispersal_map_birth, nested_dispersal_map = make_nested_dispersal_map((0, 0), # (29, 0)
	#~ shape,
	#~ M = 1000, # kg?
	#~ T = temps,
	#~ B_0 = B_0_dispersal, #1.5*10**10, # *
	#~ alpha = 0.25, # positive 0.25 for velocity?
	#~ E = 0.65,
	#~ max_revolutions = 5, x = 1, c = 1, # *
	#~ birth_map = 1)#, fix_band_radius = True)


def make_dispersal_map(shape, M, T, B_0, alpha, E, max_revolutions, x, c, birth_map, fix_band_radius):
	"""Makes a 2D array.
	The position of each nested 1D array corresponds to that of a cell in the simulated landscape.
	The 1D array contains the probability of dispersing to that cell, from every cell (i.e. a probability distribution)."""
	#~ pdb.set_trace()
	
	landscape_size = shape[0] * shape[1]
	dispersal_map_birth = sc.zeros((landscape_size, landscape_size)) # Preallocate a 2D array.
	dispersal_map = sc.zeros((landscape_size, landscape_size)) # Preallocate a 2D array.
	for i in range(landscape_size):
		dispersal_map_birth[i], dispersal_map[i] = make_nested_dispersal_map(get_xy(i, shape[1]), shape, M, T, B_0, alpha, E, max_revolutions, x, c, birth_map, fix_band_radius)
	return dispersal_map_birth, dispersal_map

## Test
#~ dispersal_map_birth, dispersal_map = make_dispersal_map(shape, M = 1000, T = temps, B_0 = B_0_dispersal, alpha = 0.25, E = 0.65, max_revolutions = 5,
	#~ x = 1, c = 1, # *
	#~ birth_map = 1, fix_band_radius = False)#True)

