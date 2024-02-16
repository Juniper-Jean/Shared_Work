#!/usr/bin/python

"""Shows how Python reads and writes text files"""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

#############################
# FILE INPUT
#############################

# Prints each line in the file - does not separate lines with a blank one.

f = open('../Sandbox/test.txt', 'r') # Open a file for reading
for line in f:
	print line, # the "," prevents adding a new line
# use "implicit" for loop:
# if the object is a file, python will cycle over lines

f.close() # close the file


# Same example, skip blank lines

f = open('../Sandbox/test.txt', 'r')
for line in f:
	if len(line.strip()) > 0: # If the line length is greater than 0
		print line,

f.close()

#############################
# FILE OUTPUT
#############################

# Save the elements of a list to a file

list_to_save = range(100) # This variable's value is a list of all integers in the range 0-99.

f = open('../Sandbox/testout.txt','w') # Makes an empty file, if one does not exist.
for i in list_to_save:
# A 'for' loop is one way for Python to read variables. Python loops over objects in the variable. If the variable is a file, Python loops through the lines. (Here, the variable is an array of integers.) You can specify Python to only loop over specific objects e.g. i[0].
	f.write(str(i) + '\n')
	# Add a new line at the end. You can not concatenate numeric and string variables. 'i' is an integer - make it a string, to write it with a new line character.

f.close()

#############################
# STORING OBJECTS
#############################

# To save an object (even complex) for later use
# Save a dictionary in a new file for later use

my_dictionary = {"a key": 10, "another key": 11}
# Make a dictionary, called 'my_dictionary', of two keys, each with one value.

import pickle # Import 'pickle' package

f = open('../Sandbox/testp.p','wb') # note the b: accept binary files
pickle.dump(my_dictionary, f)
f.close()
# Writes the dictionary into a file.


# Loads the data again.
# Loads a previously saved dictionary

f = open('../Sandbox/testp.p','rb')
another_dictionary = pickle.load(f) # Load the dictionary, calling it 'another_dictionary'.
f.close()

print another_dictionary
