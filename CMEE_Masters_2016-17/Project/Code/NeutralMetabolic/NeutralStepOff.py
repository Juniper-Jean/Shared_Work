#!/usr/bin/env python

"""Functions to run one step of the neutral-metabolic model."""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import pdb, sys
import scipy as sc
from scipy import stats

from SetUpOff import *
# file name
# May not need to import `SetUp`.


def check_offspring_survival(Topt, destination_temp, variance=1):
	"""Randomly decides if offspring survive after dispersal, given the parent's optimum temperature."""
	#~ pdb.set_trace()
	
	x = sc.random.uniform(0, 1 + sys.float_info.epsilon)
	constant = 1 / stats.norm.pdf(Topt, loc=Topt, scale=variance)
	if x > constant * stats.norm.pdf(destination_temp, loc=Topt, scale=variance):
		return False
	else:
		return True

def neutral_step(community, death_map, v, T_opt_map, band_temperatures, dispersal_map, variance_survival):
	""""""
	# `band_temperatures` - temperature of each altitudinal band
	# `variance_survival` -
	
	#~ pdb.set_trace()
	
	shape = community.shape # `shape` has 3 items if `community` is 3D, but 2 if `community` is 2D.
	landscape_size = shape[0] * shape[1]
	
	died = [0, 0, 0] # Initialise a list that the function will use to index the arrays, `community` and `T_opt_map`.
	death_z_index = sc.random.choice(sc.arange(landscape_size), p=death_map)
	died[:2] = get_xy(death_z_index, shape[1])
	# Randomly pick the cell where death occurs - picks an index, hence `sc.arange(landscape_size)`.
	
	if len(shape) == 2: # if `community` is 2D, not 3D - if number of individuals per cell (density) is 1
		#~ died[2] = None
		died = tuple(died[:2])
	else:
		died[2] = sc.random.choice(sc.nonzero(community[died[0],died[1]])[0])
		died = tuple(died)
		# From that cell, randomly pick an individual to die (*uniform distribution).
		# `sc.nonzero` returns the indices of non-zero elements. (A zero in `community` can represent the absence of an individual, if this is set up).
		# `sc.random.choice(a)` - `a` must be 1D, but `sc.nonzero(b)` returns a tuple of arrays (one for each dimension of `b`), thus `sc.nonzero(...)[0]`
		# - will get all the data as `community[x,y]` is 1D.
	
	x = sc.random.uniform(0, 1 + sys.float_info.epsilon)
	if x <= v:
		community[died] = sc.amax(community) + 1 # speciation
		T_opt_map[died] = band_temperatures[died[0]]
		# The Topt of a new species is the temperature of its position - the vacant position.
		# `band_temperatures[died[0]]` is the vacant position's temperature (the 1st dimension of `community` represents altitudinal bands).
		
	else: # dispersal
		#~ reproduced = [0, 0, 0]
		offspring_survived = False
		while offspring_survived == False: # rejection sampling
			reproduced = [0, 0, 0] # prob want to avoid extra tick of clock in while loop
			birth_z_index = sc.random.choice(sc.arange(landscape_size), p=dispersal_map[death_z_index])
			reproduced[:2] = get_xy(birth_z_index, shape[1])
			# Randomly pick the cell where birth occurs.
			# `dispersal_map[z]` is a nested dispersal map - a probability distribution - probability of dispersing to the cell with index z, from every cell.
			
			if len(shape) == 2: # if `community` is 2D, not 3D
				reproduced = tuple(reproduced[:2])
			else:
				reproduced[2] = sc.random.choice(sc.nonzero(community[reproduced[0],reproduced[1]])[0])
				reproduced = tuple(reproduced)
				# From that cell, randomly pick an individual to reproduce.
			
			offspring_survived = check_offspring_survival(T_opt_map[reproduced], band_temperatures[died[0]], variance_survival)
			# note - wasteful/inefficient - redoes both draws, if have to re-pick individual to reproduce - draw pos then ind (unsure if better way)
		
		community[died] = community[reproduced]
		T_opt_map[died] = T_opt_map[reproduced]
	
	return community, T_opt_map # comm, T_opt_map = neutral_step(...)

## Test
#~ nrows, ncols = 10, 10
#~ body_mass = 1000 # *kg?
#~ temps = sc.around(sc.linspace(0, 30, nrows) + 273.15, 2).reshape(-1, 1)

#~ community = initialise_community(nrows, ncols, b_density, body_mass, c, x)#, species_richness=1, max_diversity=False
#~ #community = sc.ones((nrows, ncols), dtype=sc.int64)
#~ #(nrows, ncols, 2) - for 3D system with given density

#~ dispersal_map_birth, dispersal_map = make_dispersal_map((nrows, ncols), body_mass, temps, B_0_dispersal,
	#~ 0.25, 0.65, 5, # alpha, E, max_revolutions
	#~ x = 1, c = 1, # *
	#~ birth_map = 1)

#~ # Set up death map.
#~ death_rate_per_temp = metabolic_scaling(M = body_mass, T = temps, B_0 = 1, alpha = -0.25) # note -0.25
#~ death_map = sc.tile(death_rate_per_temp, (1, ncols))
#~ death_map = death_map / death_map.sum() # re-normalise
#~ death_map = death_map.ravel()

#~ # Set up map of optimum temps.
#~ T_opt_map = sc.zeros(community.shape)
#~ for i in range(nrows):
	#~ T_opt_map[i] = temps[i]

#~ community, T_opt_map = neutral_step(community, death_map, 0.2, T_opt_map, temps, dispersal_map,
	#~ variance_survival = 1) # *
# vary surv var
