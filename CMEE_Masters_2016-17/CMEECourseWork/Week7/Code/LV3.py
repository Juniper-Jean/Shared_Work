#!/usr/bin/python

""" A discrete-time version of the Lotka-Volterra model, simulated using scipy """

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import scipy as sc 
import scipy.integrate as integrate
import pylab as p # Contains matplotlib for plotting
import sys

# import matplotlip.pylab as p #Some people might need to do this


## Define parameters
if len(sys.argv) == 6:
	r = float(sys.argv[1])
	a = float(sys.argv[2])
	z = float(sys.argv[3])
	e = float(sys.argv[4])
	K = float(sys.argv[5])
	print '\nChosen parameter values: r = %r, a = %r, z = %r, e = %r, K = %r.\n'%(r,a,z,e,K)
else:
	print 'Parameter values not specified. Assigning default values (r = 1., a = 0.1, z = 1.5, e = 0.75, K = 25.).\n'
	r = 1. # Resource growth rate
	a = 0.1 # Consumer search rate (determines consumption rate) 
	z = 1.5 # Consumer mortality rate
	e = 0.75 # Consumer production efficiency
	K = 25. # Prey carrying capacity
# Take arguments for the four parameters from the commandline.
# 'float()' - convert the arguments to floats, if possible.
# Take default values, if there are no commandline arguments.

x0 = 10.
y0 = 5.
# Initials conditions: 10 prey and 5 predators per unit area.

EndTime = 15
# Number of time points.
# ** Unsure what an appropriate amount is.

z0 = sc.zeros((EndTime,3))
z0[:,0] = xrange(EndTime)
z0[0] = [0., x0, y0]
# Pre-allocate an array with zeros. The array has 3 columns and 'EndTime' rows.
# Fill (replace the zeros in) column 1 with integers in the range 0 to 'EndTime'-1.
# Fill row 1 with the initial conditions.


## Uses the current row's values of predator and prey population, to calculate the next row's values (rows are time points).
for i, Rt, Ct in z0:
	if i < EndTime-1: # If i is not the last row.
		
		Rt1 = Rt*(1 + r*(1-(Rt/K)) - a*Ct)
		Ct1 = Ct*(1 - z + e*a*Rt)
		# The discrete-time model.
		
		z0[i+1] = [i+1, Rt1, Ct1]
# Loop over each row in 'z0'.
# 'i' is the value in column 1, 'Rt' column 2, 'Ct' column 3.
# Use 'Rt' and 'Ct' to calculate 'Rt1' and 'Ct1'.
# Add values to the next row.
# ('i'/column 1 is the current time point. It matches the current row index, which is why 'z0[i+1]' can refer to the next row.)

# I considered having a 1-D of the initial conditions, and using 'scipy.append' to append new values.
# But this would be slower - the program would need to find new memory space, big enough to take an increased data object each time.

pops = z0
# Rename z0


## Plot the model
t, prey, predators = pops.T
# Split 'pops' into 3 arrays.
# 'pops.T' transposes 'pops' - swaps columns and rows. 

f1 = p.figure() # Open empty figure object

p.plot(t, prey, 'g-', label='Resource density') # Plot
p.plot(t, predators  , 'b-', label='Consumer density')
# 'g-' specifies line colour as green.

p.grid() # Show grid lines.
p.legend(loc='best')
p.xlabel('Time')
p.ylabel('Population')
p.title('Consumer-Resource population dynamics')

p.annotate('r = %r, a = %r, z = %r, e = %r, K = %r'%(r, a, z, e, K), xy=(0,0), xytext=(4,15))
# Annotate plot - show the parameter values in the plot.
# '%r' is a placeholder for an exact representation of the item.
# 'xy=' - position of the element to annotate - irrelevant here.
# 'xytext=' - position of the label.

f1.savefig('../Results/prey_and_predators_3.pdf')
# Save figure.


## Print final population values
print '\nFinal population value per unit area:\n\
Predator, %r\n\
Prey, %r\n'%(predators[-1], prey[-1])
