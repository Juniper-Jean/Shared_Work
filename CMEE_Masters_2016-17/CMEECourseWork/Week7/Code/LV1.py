#!/usr/bin/python

""" The typical Lotka-Volterra Model simulated using scipy """

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import scipy as sc 
import scipy.integrate as integrate
import pylab as p # Contains matplotlib for plotting

# import matplotlip.pylab as p #Some people might need to do this

def dRC_dt(pops, t=0):
    """ Returns the growth rate of predator and prey populations at any 
    given time step """
    
    R = pops[0]
    C = pops[1]
    dRdt = r*R - a*R*C 
    dCdt = -z*C + e*a*R*C
    
    return sc.array([dRdt, dCdt])

# Define parameters:
r = 1. # Resource growth rate
a = 0.1 # Consumer search rate (determines consumption rate) 
z = 1.5 # Consumer mortality rate
e = 0.75 # Consumer production efficiency

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

#~ p.show() # Open figure.
# Hashed out, as the script pauses while the figure is open. The script continues to the code below, only once you close the plot.

f1.savefig('../Results/prey_and_predators_1.pdf') # Save figure.
