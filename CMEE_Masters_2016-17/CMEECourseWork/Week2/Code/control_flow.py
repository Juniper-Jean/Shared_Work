#!/usr/bin/env python

"""Some functions exemplifying the use of control statements"""
# Docstrings are considered part of the running code (normal comments are #stripped). Hence, you can access your docstrings at run time.

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import sys

def even_or_odd(x=0): # if not specified, x should take value 0.
	"""Find whether a number x is even or odd."""
	if x % 2 == 0: #The conditional if
		return "%d is Even!" % x
	return "%d is Odd!" % x
	
	# If the remainder of x/2 is 0:
	# return "x is Even!'.
	# Otherwise, return 'x is Odd!'
	# '%d', '%s' etc are placeholders. '%d' is a placeholder for a number, '%s' for a string, '%f' a float, '%e' float in exponential format.
	# 'return' and 'print' are statements, not functions. 'print' shows the user a string. 'return' is how a function gives a value. If there is no 'return' statement, it will return 'None'. A returned value can be stored as a variable, printed, or used as an argument in another function. Try:
	#~ def func_print():
		#~ print 'I print'
		
	#~ def func_return():
		#~ return 'I return'
	
	#~ var = func_print()
	#~ var2 = func_return()
	#~ print var # Returns 'None'
	#~ print var2 # Returns 'I return'

def largest_divisor_five(x=120):
	"""Find which is the largest divisor of x among 2,3,4,5."""
	largest = 0 # The variable 'largest' currently has value 0.
	if x % 5 == 0:
		largest = 5 # If this statement is true, give 'largest' a new value of 5.
	elif x % 4 == 0: #means "else, if" - otherwise, if
		largest = 4
	elif x % 3 == 0:
		largest = 3
	elif x % 2 == 0:
		largest = 2
	else: # When all other (if, elif) conditions are not met
		return "No divisor found for %d!" % x # Each function can return a value or a variable.
	return "The largest divisor of %d is %d" % (x, largest)
	# Return a string "...of x is 'largest'"
	
	# The function tries to find the biggest divisor 2-5, so it starts with 5, the biggest number.

def is_prime(x=70):
	"""Find whether an integer is prime."""
	for i in range(2, x): # "range" returns a sequence of integers
		if x % i == 0:
			print "%d is not a prime: %d is a divisor" % (x, i) #Print formatted text "%d %s %f %e" % (20,"30",0.0003,0.00003)
			
			return False
	print "%d is a prime!" % x
	return True
	
	# Loop over integers from 2 to x-1. ('print range(2, 5)' prints 2-4.)
	# If the remainder of x/i is 0, print a string and return False. Returning False stops the 'for' loop. Returns False as soon as the 'if' statement is true, so prints one string even if there are more divisors.
	# Otherwise, print another string and return True.
	
def find_all_primes(x=22):
	"""Find all the primes up to x"""
	allprimes = []
	for i in range(2, x + 1):
		if is_prime(i):
			allprimes.append(i)
	print "There are %d primes between 2 and %d" % (len(allprimes), x)
	return allprimes
	
	# Make a list, 'allprimes'.
	# Loop over integers from 2 to x+1.
	# Run 'is_prime()' function for the integer.
	# If 'is_prime()' returns True, add integer to list.
	# Print a string that reports the number of objects in the list, and x.
	# Return all objects in the list.

def main(argv):
	# sys.exit("don't want to do this right now!")
	print even_or_odd(22)
	print even_or_odd(33)
	print largest_divisor_five(120)
	print largest_divisor_five(121)
	print is_prime(60)
	print is_prime(59)
	print find_all_primes(100)
	return 0
# This receives the commandline argument. It prints the outputs of each earlier function. For each function, it specifies an x value (specifies the variable argument).
# The earlier functions 'return' outputs. As a result, the outputs can be passed to and printed by this function.

if (__name__ == "__main__"):
	status = main(sys.argv)
	sys.exit(status)
# This passes the commandline argument through the main function.
