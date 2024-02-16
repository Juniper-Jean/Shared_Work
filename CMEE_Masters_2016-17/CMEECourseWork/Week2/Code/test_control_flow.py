#!/usr/bin/python

"""Illustrates unit testing with doctest."""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import sys
import doctest # Import the doctest module

def even_or_odd(x=0):
	"""Find whether a number x is even or odd.

	>>> even_or_odd(10)
	'10 is Even!'

	>>> even_or_odd(5)
	'5 is Odd!'

	whenever a float is provided, then the closest integer is used:
	>>> even_or_odd(3.2)
	'3 is Odd!'

	in case of negative numbers, the positive is taken:
	>>> even_or_odd(-2)
	'-2 is Even!'

	"""
	# >>> even_or_odd(5)
	# '5 is Odd!' - this is what the function should return.
	
	
	#Define function to be tested
	if x % 2 == 0:
		return "%d is Even!" % x
	return "%d is Odd!" % x

## I SUPPRESSED THIS BLOCK: WHY?
# ?? We are not running the script with a commandline argument, but test arguments embedded in the docstring.

#~ def main(argv):
	#~ print even_or_odd(22)
	#~ print even_or_odd(33)
	#~ return 0

#~ if (__name__ == "__main__"):
	#~ status = main(sys.argv)

doctest.testmod() # To run with embedded tests

# To run the test, 'run test_control_flow.py -v' ('-v' for verbose feedback).
