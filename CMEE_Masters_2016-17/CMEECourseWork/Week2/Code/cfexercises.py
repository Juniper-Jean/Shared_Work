#!/usr/bin/env python

"""Functions illustrating the use of control statements"""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

# How many times will 'hello' be printed?
# 36

# 1)
for i in range(3, 17):
	print 'hello'
# Prints 'hello' 14 times.

# 2)
for j in range(12):
	if j % 3 == 0:
		print 'hello'
# Range is 0-11.
# Prints 'hello' 4 times - 'if' statement is true for 0, 3, 6 and 9.

# 3)
for j in range(15):
	if j % 5 == 3:
		print 'hello'
	elif j % 4 == 3:
		print 'hello'
# Prints 'hello' 5 times - 'if' statement is true for 3/8/13, 'elif' for 7/11.
# (Why 'if' true for 3? 8/5 = 1 3/5. 1 is the quotient, 3 the remainder. 13/5 = 2 3/5. 3/5 has quotient 0, remainder 3.)

# 4)
z = 0
while z != 15:
	print 'hello'
	z = z + 3
# The variable z has value 0.
# While z is not = 15, print 'hello' and give z a new value of z+3.
# Prints 'hello' 5 times (for z = 0, 3, 6, 9, 12). Stops when z = 15.
# Try:
#~ z = 0
#~ while z != 15:
	#~ print 'hello'
# Where z is not = 15, this is an infinite loop.

# 5)
z = 12
while z < 100:
	if z == 31:
		for k in range(7):
			print 'hello'
	elif z == 18:
		print 'hello'
	z = z + 1
# While z is less than 100, if it = 31, print 'hello' 7 times.
# Otherwise, if z = 18, print 'hello' once.
# Give z a new value z+1.
# Prints 'hello' 8 times (seven for 31, one for 18 - no other z value satisfies 'if'/'elif' statements).
# For z = 31 or 18, if z was not given a new value, this would be an infinite loop.


# What does fooXX do?
# 'fooX' is the function name. The function takes an argument '(x)', which the user specifies. For these functions, the argument should be a number variable.

import sys

def foo1(x):
	"""Returns x ^ 0.5"""
	return x ** 0.5

def foo2(x, y):
	"""Returns the biggest of two numbers"""
	if x > y:
		return x
	return y
# Returns the biggest of x, y.

def foo3(x, y, z):
	"""	Puts x, y, z in size order.
			May need multiple runs."""
	if x > y:
		tmp = y
		y = x
		x = tmp
	# If x > y, swap the values of x, y.
	if y > z:
		tmp = z
		z = y
		y = tmp
	# If y > z, swap y, z.
	return [x, y, z]
	# Return the (potentially new) values of x, y, z.

# (4, 6, 5) returns [4, 5, 6].
# But (4, 5, 6) returns [7, 2, 9]. Set these as new x, y, z values and re-run to put in size order. To do in one run, edit to repeat first 'if' function before 'return'.

def foo4(x):
	"""Returns x!"""
	result = 1
	for i in range(1, x + 1):
		result = result * i
	return result
# Returns x!, the factorial of x. I.e. 4! = (4*0)+(4*1)+(4*2)+(4*3).

def foo5(x):
	"""Returns x!"""
	if x == 1:
		return 1
	return x * foo5(x - 1)
# Returns x! via a different way. 4! also = 4*3*2*1.
# This is a recursive function, meaning the function calls itself
# read about it at
# en.wikipedia.org/wiki/Recursion_(computer_science)

foo5(10)

def main(argv):
	print foo1(2)
	print foo2(2, 9)
	print foo3(2, 4, 3)
	print foo4(4)
	print foo5(10)
	return 0

if (__name__ == "__main__"):
	status = main(sys.argv)
	sys.exit(status)
