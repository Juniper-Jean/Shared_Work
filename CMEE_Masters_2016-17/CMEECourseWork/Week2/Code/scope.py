#!/usr/bin/python

"""Illustrates how local and global variables differ"""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

## Try this first

_a_global = 10
# This is a global variable, as it is outside a function.

def a_function():
	"""Sets and prints two local variables"""
	_a_global = 5
	_a_local = 4
	# These are local variables, as they are inside a function. They are only accessible inside the function. Thus, '_a_global = 5' won't overwrite the earlier variable of the same name.
	print "Inside the function, the value is ", _a_global # Returns 5
	print "Inside the function, the value is ", _a_local # Returns 4
	return None # What does this do?

a_function() # What does this do?
print "Outside the function, the value is ", _a_global # Returns 10


## Now try this

_a_global = 10

def a_function():
	"""Sets and prints one global and one local variable"""
	global _a_global
	_a_global = 5
	# The variable '_a_global', inside the fuction, is made global. It overwrites an earlier variable sharing the same name.
	_a_local = 4
	print "Inside the function, the value is ", _a_global # Returns 5
	print "Inside the function, the value is ", _a_local # Returns 4
	return None

a_function()
print "Outside the function, the value is", _a_global # Returns 5

# Variables inside functions neither are visible outside the function, nor persist after it runs. They are 'local' variables.
# 'Global' variables, however, are visible inside and outside functions.
# You can turn a variable inside a function global, using the 'global' command.
