#!/usr/bin/python

""" Some (useless) functions used to demonstrate profiling. """

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

# Run the script using the ipython magic command, '%run -p'.

def a_useless_function(x):
	""" Sums values in the range 0 to 99 999 999 """
	y = 0
	# eight zeros!
	#~ for i in range(100000000):
	for i in xrange(100000000):
		y = y + i
	return 0
	# Loop over integers in the range 0 to 99 999 999.
	# Assign a new value to y per iteration.

# The output of '%run -p', shows that the function 'range()' is slow - we used 'xrange()' instead.

def a_less_useless_function(x):
	""" Sums values in the range 0 to 99 999 """
	y = 0
	# five zeros!
	#~ for i in range(100000):
	for i in xrange(100000):
		y = y + i
	return 0

def some_function(x):
	"""
			Prints x.
			Runs 'a_useless_function(x)' and 'a_less_useless_function(x)' for a value of x.
	"""
	print x
	a_useless_function(x)
	a_less_useless_function(x)
	return 0
# Note: 'a_useless_function(x)' and 'a_less_useless_function(x)' receive an argument x, but do not use it.

some_function(1000)
# Run 'some_function(x)' for x = 1000.
