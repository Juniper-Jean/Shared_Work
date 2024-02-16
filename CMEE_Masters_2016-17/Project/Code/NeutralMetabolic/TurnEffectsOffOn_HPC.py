#!/usr/bin/env python

"""Script to run the neutral-metabolic model using high performance computing. On the cluster, it will be run multiple times concurrently, with different parameter values."""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import os
from NormalisationConstantsOff import * # file names
from RunSimOff import *


i = int(os.getenv('PBS_ARRAY_INDEX'))

temp_gradient = sc.around(sc.linspace(10, 25, 30) + 273.15, 2)
fixed_temps = sc.repeat(15, 30) + 273.15

R = 1.5
A = 1
c = sc.sqrt(R**2 + 1)
x = sc.sqrt(A / (sc.pi * c))
b_density = calculate_b_density(1000, (30, 30), c, x)
b_density100 = calculate_b_density(100, (30, 30), c, x)
b_density10 = calculate_b_density(10, (30, 30), c, x)

B_0_dispersal = calculate_B_0_dispersal(M = 1000, T = 30 + 273.15, row_index = 30, T_r = 30, T_theta = 30, x = x, distance = 1/3)
# Normalise so the mean dispersal distance of the biggest body mass in the bottom row (hottest, widest) is 1/3 of the row's circumference.

# Base neutral model
if (i >= 1) & (i <= 10):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 1000, # *
		T_birth_death = fixed_temps, T_dispersal = fixed_temps, # *
		b_density = b_density, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = True, fix_band_radius = True) # *

# Full area effect, no temp
# **Vary body size (but re-norm density), in case, with M = 1000, there's too much disp to see area effect
elif (i > 10) & (i <= 20):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 1000, # *
		T_birth_death = fixed_temps, T_dispersal = fixed_temps, # *
		b_density = b_density, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = False, fix_band_radius = False) # *

elif (i > 20) & (i <= 30):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 100, # *
		T_birth_death = fixed_temps, T_dispersal = fixed_temps, # *
		b_density = b_density100, # **
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = False, fix_band_radius = False) # *

elif (i > 30) & (i <= 40):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 10, # *
		T_birth_death = fixed_temps, T_dispersal = fixed_temps, # *
		b_density = b_density10, # **
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = False, fix_band_radius = False) # *

# Temp effect on birth/death (not dispersal) and full area effect
elif (i > 40) & (i <= 50):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 1000, # *
		T_birth_death = temp_gradient, T_dispersal = fixed_temps, # *
		b_density = b_density, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = False, fix_band_radius = False) # *

elif (i > 50) & (i <= 60):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 100, # *
		T_birth_death = temp_gradient, T_dispersal = fixed_temps, # *
		b_density = b_density100, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = False, fix_band_radius = False) # *

elif (i > 60) & (i <= 70):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 10, # *
		T_birth_death = temp_gradient, T_dispersal = fixed_temps, # *
		b_density = b_density10, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = False, fix_band_radius = False) # *

# Temp effect on disp (not birth/death) and full area effect
elif (i > 70) & (i <= 80):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 1000, # *
		T_birth_death = fixed_temps, T_dispersal = temp_gradient, # *
		b_density = b_density, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = False, fix_band_radius = False) # *

elif (i > 80) & (i <= 90):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 100, # *
		T_birth_death = fixed_temps, T_dispersal = temp_gradient, # *
		b_density = b_density100, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = False, fix_band_radius = False) # *

elif (i > 90) & (i <= 100):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 10, # *
		T_birth_death = fixed_temps, T_dispersal = temp_gradient, # *
		b_density = b_density10, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = False, fix_band_radius = False) # *

# Full temp effect, no area effect
elif (i > 100) & (i <= 110):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 1000, # *
		T_birth_death = temp_gradient, T_dispersal = temp_gradient, # *
		b_density = b_density, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = True, fix_band_radius = True) # *

elif (i > 110) & (i <= 120):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 100, # *
		T_birth_death = temp_gradient, T_dispersal = temp_gradient, # *
		b_density = b_density100, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = True, fix_band_radius = True) # *

elif (i > 120) & (i <= 130):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 10, # *
		T_birth_death = temp_gradient, T_dispersal = temp_gradient, # *
		b_density = b_density10, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = True, fix_band_radius = True) # *

# Abundance decreases with area
elif (i > 130) & (i <= 140):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 1000, # *
		T_birth_death = fixed_temps, T_dispersal = fixed_temps, # *
		b_density = b_density, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = False, fix_band_radius = True) # *


# Breaking down dispersal
## Temp but not area effect
elif (i > 140) & (i <= 150):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 1000, # *
		T_birth_death = fixed_temps, T_dispersal = temp_gradient, # *
		b_density = b_density, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = True, fix_band_radius = True) # *

elif (i > 150) & (i <= 160):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 100, # *
		T_birth_death = fixed_temps, T_dispersal = temp_gradient, # *
		b_density = b_density100, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = True, fix_band_radius = True) # *

elif (i > 160) & (i <= 170):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 10, # *
		T_birth_death = fixed_temps, T_dispersal = temp_gradient, # *
		b_density = b_density10, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = True, fix_band_radius = True) # *

## Area but not temp
elif (i > 170) & (i <= 180):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 1000, # *
		T_birth_death = fixed_temps, T_dispersal = fixed_temps, # *
		b_density = b_density, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = True, fix_band_radius = False) # *

elif (i > 180) & (i <= 190):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 100, # *
		T_birth_death = fixed_temps, T_dispersal = fixed_temps, # *
		b_density = b_density100, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = True, fix_band_radius = False) # *

elif (i > 190) & (i <= 200):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 10, # *
		T_birth_death = fixed_temps, T_dispersal = fixed_temps, # *
		b_density = b_density10, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = True, fix_band_radius = False) # *

## Temp and area
elif (i > 200) & (i <= 210):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 1000, # *
		T_birth_death = fixed_temps, T_dispersal = temp_gradient, # *
		b_density = b_density, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = True, fix_band_radius = False) # *

elif (i > 210) & (i <= 220):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 100, # *
		T_birth_death = fixed_temps, T_dispersal = temp_gradient, # *
		b_density = b_density100, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = True, fix_band_radius = False) # *

elif (i > 220) & (i <= 230):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 10, # *
		T_birth_death = fixed_temps, T_dispersal = temp_gradient, # *
		b_density = b_density10, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = True, fix_band_radius = False) # *

## Same as last 3
## + abundance decreases with area
### Temp but not area effect
elif (i > 230) & (i <= 240):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 1000, # *
		T_birth_death = fixed_temps, T_dispersal = temp_gradient, # *
		b_density = b_density, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = False, fix_band_radius = True) # *

elif (i > 240) & (i <= 250):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 100, # *
		T_birth_death = fixed_temps, T_dispersal = temp_gradient, # *
		b_density = b_density100, # **
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = False, fix_band_radius = True) # *

elif (i > 250) & (i <= 260):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 10, # *
		T_birth_death = fixed_temps, T_dispersal = temp_gradient, # *
		b_density = b_density10, # **
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = False, fix_band_radius = True) # *

### Temp and area
elif (i > 260) & (i <= 270):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 1000, # *
		T_birth_death = fixed_temps, T_dispersal = temp_gradient, # *
		b_density = b_density, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = False, fix_band_radius = False) # *

elif (i > 270) & (i <= 280):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 100, # *
		T_birth_death = fixed_temps, T_dispersal = temp_gradient, # *
		b_density = b_density100, # **
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = False, fix_band_radius = False) # *

elif (i > 280) & (i <= 290):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 10, # *
		T_birth_death = fixed_temps, T_dispersal = temp_gradient, # *
		b_density = b_density10, # **
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = False, fix_band_radius = False) # *


## Birth/death and dispersal (abundance doesn't decrease with area)
elif (i > 290) & (i <= 300):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 1000, # *
		T_birth_death = temp_gradient, T_dispersal = temp_gradient, # *
		b_density = b_density, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = True, fix_band_radius = False) # *


## Temp effect on birth/death only (no area, dispersal)
elif (i > 300) & (i <= 310):
	main(wall_time = 60*35, rand_seed = i, sample_size = 90, interval_rich = 20, sim_name = i,
		R = 1.5, A = 1, nrows = 30, ncols = 30,
		M = 1000, # *
		T_birth_death = temp_gradient, T_dispersal = fixed_temps, # *
		b_density = b_density, # *
		B_0_dispersal = B_0_dispersal, max_revolutions = 5, v = 0.01, variance_survival = 1,
		fix_abundance = True, fix_band_radius = True) # *

