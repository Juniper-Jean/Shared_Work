#!/usr/bin/python

""" Some functions used to demonstrate profiling with the 'time' and 'timeit' modules. """

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

####################
# range vs. xrange.
####################
import time
import timeit

def a_not_useful_function():
	"""
			Sums values in the range 0 to 99 999.
			Uses 'range()' to create values for iteration.
	"""
	y = 0
	for i in range(100000):
		y = y + i
	return 0
	# Loop over integers in the range 0 to 99 999.
	# Assign a new value to y per iteration.

def a_less_useless_function():
	"""
			Sums values in the range 0 to 99 999.
			Uses 'xrange()' to create values for iteration.
	"""
	y = 0
	for i in xrange(100000):
		y = y + i
	return 0

## One approach is to time it like this:
start = time.time()
a_not_useful_function()
print "a_not_useful_function takes %f s to run." % (time.time() - start)
#~ ?time.time()
# 'time.time()' returns the current time in seconds since the Epoch. Assign to 'start'.
# Run 'a_not_useful_function()'.
# Print the current time minus the start time - how much time 'a_not_useful_function()' takes to run.

start = time.time()
a_less_useless_function()
print "a_less_useless_function takes %f s to run." % (time.time() - start)

# But you'll notice that if you run it multiple times, the time taken changes a
# bit. So instead, you can also run:
#		%timeit a_not_useful_function()
#		%timeit a_less_useless_function()
# in iPython.

########################################
# for loops vs. list comprehensions.
########################################
my_list = range(1000)

def my_squares_loop(x):
	""" Lists i^2 for each value of i in x """
	out = []
	for i in x:
		out.append(i ** 2)
	return out
# Make an empty list.
# Append i^2 to the list, for each value of i in x.

def my_squares_lc(x):
	""" Lists i^2 for each value of i in x """
	out = [i ** 2 for i in x]
	return out
# List comprehension

# %timeit my_squares_loop(my_list)
# %timeit my_squares_lc(my_list)

##############################
# for loops vs. join method.
##############################
import string
my_letters = list(string.ascii_lowercase)
# Makes a list of all lowercase letters.

def my_join_loop(l):
	""" Concatenates strings using a loop """
	out = ''
	for letter in l:
		out += letter # 
	return out
# Make an empty string.
# Add to the string.
# '+=', instead of '=', ensures 'out' is appended to, not overwritten.
# Appends each object in 'l' to the string.

def my_join_method(l):
	""" Concatenates strings using '.join()' """
	out = ''.join(l)
	return out
#~ ?out.join(l)
# 'join()' returns a string that is the concatenation of strings in an iterable.

# %timeit(my_join_loop(my_letters))
# %timeit(my_join_method(my_letters))

####################
# Oh dear.
####################

def getting_silly_pi():
	""" Sums values in the range 0 to 99 999 """
	y = 0
	for i in xrange(100000):
		y = y + i # Assign a new value to y in each iteration.
	return 0

def getting_silly_pii():
	""" Sums values in the range 0 to 99 999 """
	y = 0
	for i in xrange(100000):
		y += i # Directly add a value to y in each iteration.
	return 0

# %timeit(getting_silly_pi())
# %timeit(getting_silly_pii())

# 'y += i' is faster than 'y = y + i'.
