#!/usr/bin/env python

"""Loads results of simulations. Calculates and plots alpha, beta, and gamma diversity per altitudinal band."""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import pdb, pickle
import scipy as sc
from scipy import stats
import matplotlib.pyplot as plt


nreplicates = 20 # *
first_file_ID = 141
area_n_inds_fixed = False # *cylinder

alpha = sc.zeros((nreplicates, 30)) # 30 bands
beta = sc.zeros((nreplicates, 30))
gamma = sc.zeros((nreplicates, 30))
gamma_area = sc.zeros((nreplicates, 30))

for i in range(nreplicates):
	try:
		with open('../../Results/Aug17/%s.pickle' % (first_file_ID + i), 'rb') as f:
			overall_nspp, nspp_per_band, nspp_in_sample, octaves_list,\
			community, T_opt_map,\
			n_generations,\
			death_map, dispersal_map_birth, dispersal_map,\
			wall_time, rand_seed, sample_size, interval_rich, sim_name,\
			R, A, nrows, ncols, M, T,\
			b_density, B_0_dispersal, max_revolutions, v, variance_survival,\
			max_diversity, species_richness,\
			B_0_birth_death, alpha_birth_death, E_birth_death,\
			alpha_dispersal, E_dispersal = pickle.load(f)
		
		#~ with open('../../Results/Aug21/%s.pickle' % (first_file_ID + i), 'rb') as f:
			#~ overall_nspp, nspp_per_band, nspp_in_sample, octaves_list,\
			#~ community, cell_areas, cell_abundances, T_opt_map,\
			#~ n_generations,\
			#~ death_map, dispersal_map_birth, dispersal_map,\
			#~ wall_time, rand_seed, sample_size, interval_rich, sim_name,\
			#~ R, A, nrows, ncols, M, T_birth_death, T_dispersal,\
			#~ b_density, B_0_dispersal, max_revolutions, v, variance_survival,\
			#~ fix_abundance, max_diversity, species_richness,\
			#~ B_0_birth_death, alpha_birth_death, E_birth_death,\
			#~ alpha_dispersal, E_dispersal, fix_band_radius = pickle.load(f)
	
	except:
		print("Error opening the file, '%s.pickle', or reading the pickle data in it." % (first_file_ID + i))
		pass
	
	c = sc.sqrt(R**2 + 1)
	x = sc.sqrt(A / (sc.pi * c))
	# Derive the values of c and x from geometric equations (see dissertation method).
	
	abundance_per_m2 = b_density * M**-0.75 # Calculate the number of individuals in 1 m^2.
	S_r = sc.arange(nrows)
	T_r, T_theta = nrows, ncols
	cell_areas = (sc.pi * c * ((((S_r + 1) * x) / T_r)**2 - ((S_r * x) / T_r)**2)) / T_theta
	cell_abundances = sc.around(abundance_per_m2 * cell_areas, 0).astype(sc.int64, copy=False)
	# Using c, x, nrows, and ncols, calculate area and # individuals per cell.
	
	if area_n_inds_fixed == True:
		cell_areas = sc.repeat(cell_areas[14], nrows)
		cell_abundances = sc.repeat(cell_abundances[14], nrows)
	
	sample_size = cell_abundances[15] # *
	# area = # inds?
	
	## Per band, measure alpha diversity (mean # spp per cell)
	tmp = sc.zeros((nrows, ncols))
	for k in range(ncols):
		#~ pdb.set_trace()
		for j in range(nrows):
			
			#~ if (j == 0) & (M == 1000):
				#~ continue
			# Skip the top band for the biggest body mass - it has fewer individuals (30) than the sample size.
			
			first_index = cell_abundances[j] * k
			sample = community[j][community[j] > 0][first_index:(first_index + sample_size)]
			tmp[j, k] = sc.unique(sample).size
	
	#~ pdb.set_trace()
	alpha[i] = tmp.mean(axis=1) # mean # spp per cell
	
	## Per band, measure beta diversity
	tmp2 = sc.zeros((nrows, ncols))
	for j in range(nrows):
		#~ pdb.set_trace()
		for k in range(ncols):
			a = community[j, k][community[j, k] > 0]
			b = community[j, (k + 15) % 30][community[j, (k + 15) % 30] > 0] # cell on opposite side of mountain to `a`
			shared_spp = sc.intersect1d(a, b)
			probability = shared_spp.size / cell_abundances[j]
			tmp2[j, k] = probability
	
	#~ pdb.set_trace()
	beta[i] = tmp2.mean(axis=1)
	
	gamma[i] = nspp_per_band[-10:].mean(axis=0)
	band_areas = cell_areas * T_theta
	gamma_area[i] = gamma[i] / band_areas


alpha = alpha[alpha.sum(axis=1) > 0]
beta = beta[beta.sum(axis=1) > 0]
# Delete rows with no data (file ID doesn't exist).

mean_alpha = alpha.mean(axis=0)
SE_alpha = stats.sem(alpha, axis=0)

mean_beta = beta.mean(axis=0)
SE_beta = stats.sem(beta, axis=0)

mean_gamma = gamma.mean(axis=0)
SE_gamma = stats.sem(gamma, axis=0)

mean_gamma_area = gamma_area.mean(axis=0)
SE_gamma_area = stats.sem(gamma_area, axis=0)


temps = T.ravel() - 273.15 # When temp fixed, remove x-axis values.
#~ temps = T_dispersal.ravel() - 273.15
#~ temps = sc.arange(30)
f, ax = plt.subplots(4, sharex=True, figsize=(10, 20))
line1, = ax[0].plot(temps, mean_alpha, color='b', lw='0.8')
line2, = ax[1].plot(temps, mean_beta, color='g', lw='0.8')
line3, = ax[2].plot(temps, mean_gamma, color='r', lw='0.8')
line4, = ax[3].plot(temps, mean_gamma_area, color='k', lw='0.8')

ax[0].fill_between(temps, mean_alpha - (1.95 * SE_alpha), mean_alpha + (1.95 * SE_alpha), alpha=0.1, edgecolor='b', facecolor='b')
ax[1].fill_between(temps, abs(mean_beta - (1.95 * SE_beta)), mean_beta + (1.95 * SE_beta), alpha=0.1, edgecolor='g', facecolor='g')
#~ ax[1].fill_between(temps, mean_beta - (1.95 * SE_beta), mean_beta + (1.95 * SE_beta), alpha=0.1, edgecolor='g', facecolor='g')
ax[2].fill_between(temps, mean_gamma - (1.95 * SE_gamma), mean_gamma + (1.95 * SE_gamma), alpha=0.1, edgecolor='r', facecolor='r')
ax[3].fill_between(temps, mean_gamma_area - (1.95 * SE_gamma_area), mean_gamma_area + (1.95 * SE_gamma_area), alpha=0.1, edgecolor='k', facecolor='bk')

plt.gca().invert_xaxis()
plt.legend((line1, line2, line3, line4), ('alpha diversity', 'beta diversity', 'gamma diversity', 'gamma per unit area'), fontsize = 'xx-large')

ax[0].set_ylim((0, 30))
ax[1].set_ylim((0, 0.4))
ax[2].set_ylim((0, 350))
ax[3].set_ylim((2000, 8000))

ax[0].set_ylabel('No. of species', fontsize = 20)
ax[1].set_ylabel('Probability', fontsize = 20)
ax[2].set_ylabel('No. of species', fontsize = 20)
ax[3].set_ylabel('Species per unit area', fontsize = 20)
for i in range(4):
	ax[i].tick_params(labelsize = 15)
	#~ ax[i].axes.get_xaxis().set_visible(False) # *
plt.xlabel('Temperature (degrees C)', fontsize = 20)
plt.xticks(fontsize = 20)

#~ plt.savefig('../../Results/DiversityPlots/10TempNoArea.pdf')# % M)
plt.show()
