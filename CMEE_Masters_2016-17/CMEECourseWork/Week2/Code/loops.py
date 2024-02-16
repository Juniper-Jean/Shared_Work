#!/usr/bin/env python

"""'for' and 'while' loops in Python"""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

# for loops

for i in range(5):
	print i
# Loop over integers 0-4.
# Print integer.
# The loop stops at 4, the last integer in range(5).
# Prints 0-4, each number on a new line.

my_list = [0, 2, "geronimo!", 3.0, True, False]
for k in my_list:
	print k
# Make a list, called 'my_list', with 2 integers, a string, float and 2 booleans.
# Loop over objects in the list.
# Print object.

total = 0
summands = [0, 1, 11, 111, 1111]
for s in summands:
	print total + s
# Give 'total' the value 0.
# Make a list of these integers.
# Loop over integers in the list.
# Print the answer to '0 + integer'.
# (May be useful for printing lines of binary code.)


# while loops

z = 0
while z < 100:
	z = z + 1
	print (z)
# While 'z < 100' is true, give z a new value z+1. Print z (its new value).
# The loop stops when z > 100.
# Prints 1-100.

b = True
while b:
	print "GERONIMO! infinite loop! ctrl+c to stop!"
# ctrl + c to stop!
# As long as b is true, this is an infinite loop. It prints the string until you stop it.
