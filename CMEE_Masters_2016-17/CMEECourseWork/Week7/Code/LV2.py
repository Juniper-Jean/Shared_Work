#!/usr/bin/python

# **CHANGE
""" The typical Lotka-Volterra Model simulated using scipy """

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import scipy as sc 
import scipy.integrate as integrate
import pylab as p # Contains matplotlib for plotting
import sys

# import matplotlip.pylab as p #Some people might need to do this

def dRC_dt(pops, t=0):
    """ Returns the growth rate of predator and prey populations at any 
    given time step """
    
    R = pops[0]
    C = pops[1]
    dRdt = r*R*(1-(R/K)) - a*R*C 
    dCdt = -z*C + e*a*R*C
    
    return sc.array([dRdt, dCdt])

# Define parameters:
if len(sys.argv) == 6:
	r = float(sys.argv[1])
	a = float(sys.argv[2])
	z = float(sys.argv[3])
	e = float(sys.argv[4])
	K = float(sys.argv[5])
	print '\nChosen parameter values: r = %r, a = %r, z = %r, e = %r, K = %r.\n'%(r,a,z,e,K)
else:
	print '\nParameter values not specified. Assigning default values (r = 1., a = 0.1, z = 1.5, e = 0.75, K = 25.).\n'
	r = 1. # Resource growth rate
	a = 0.1 # Consumer search rate (determines consumption rate) 
	z = 1.5 # Consumer mortality rate
	e = 0.75 # Consumer production efficiency
	K = 25. # Prey carrying capacity
# Take arguments for the five parameters from the commandline.
# 'float()' - convert the arguments to floats, if possible.
# Take default values, if there are not enough commandline arguments.

# Now define time -- integrate from 0 to 15, using 1000 points:
t = sc.linspace(0, 15, 1000)
#~ t
#~ ?sc.linspace
#~ len(t)
#~ type(t)
# 't' is numpy array of 1000 items.
# 'sc.linspace()' returns 1000 evenly spaced numbers between 0 and 15.

x0 = 10
y0 = 5 
z0 = sc.array([x0, y0]) # Initials conditions: 10 prey and 5 predators per unit area.

pops, infodict = integrate.odeint(dRC_dt, z0, t, full_output=True)
#~ ?integrate.odeint
# 'z0' and 't' are arguments passed to the 'dRC_dt' function.

# Solves ordinary differential equations formatted as follows:
# dy/dt = func(y, t0,...)
# Where y is a vector of the initial conditions.
# t is an array of time points for which to solve for y.

# Returns an array containing y for each time in t. Assign this to 'pops'.
# 'full_output=True' returns a dictionary of additional output. Assign to 'infofict'.

# It seems 'integrate.odeint' can repeatedly call 'dRC_dt' and append its single-row outputs to one array.


infodict['message']     # >>> 'Integration successful.'

prey, predators = pops.T # What's this for?
#~ a = pops.T
#~ ?pops.T
# Split 'pops' into 2 arrays, 'prey' and 'predators'.
# 'pops.T' transposes 'pops' - swaps columns and rows. 
# Change 'pops' from an array 2 columns * 1000 rows to 1000 * 2. Assign row 0 to 'prey', row 1 to 'predator'.
# I'm unsure why you need '.T', but 'prey, predators = pops' (without '.T') doesn't work.

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

#~ p.show() #Open figure.
# Hashed out, as the script pauses while the figure is open. The script continues to the code below, only once you close the plot.

f1.savefig('../Results/prey_and_predators_2.pdf') # Save figure.

print '\nFinal population value per unit area:\n\
Predator, %r\n\
Prey, %r\n'%(predators[-1], prey[-1])
# Print the final population values to screen.


#~ if prey[-1] > 0 and predators[-1] > 0:
	#~ print '\nPredator and prey persist with these parameter values. Final population value per unit area:\n\
	#~ Predator, %r\n\
	#~ Prey, %r\n'%(predators[-1], prey[-1])
#~ else:
	#~ print '\nPredator or prey did NOT persist with these parameter values. Final population value per unit area:\n\
	#~ Predator, %r\n\
	#~ Prey, %r\n'%(predators[-1], prey[-1])
# If you choose appropriate parameter values, such that both predator and prey persist, print the final population values.
# An issue with this if/else statement: you can generate tiny population values, but they do not seem to ever equal 0.

#~ pops[-1,0]
#~ pops[-1,1]
