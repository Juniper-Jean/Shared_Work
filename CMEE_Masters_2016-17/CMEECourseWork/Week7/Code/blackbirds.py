#!/usr/bin/python

"""Captures the kingdom, phylum and species name for each species in 'blackbirds.txt'"""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import re

f = open('../Data/blackbirds.txt', 'r')
text = f.read()
f.close()
# Read the file

text = text.replace('\t',' ')
text = text.replace('\n',' ')
# Remove \t\n and put in a space.
#~ text # Check 'text'.

# Note that there are "strange characters" (these are accents and non-ascii symbols).
# As we don't care for them, first transform to ASCII:
text = str(text.decode('ascii', 'ignore'))
# I changed this from: 'text = text.decode('ascii', 'ignore')', which generated u's in the lists below. 'u' indicates the object is in unicode. 'str()' extracts just the object.
#~ text


# Now write a regular expression my_reg that captures the Kingdom, 
# Phylum and Species name for each species and prints it out neatly:
# my_reg = ??????

# Hint: you will probably want to use re.findall(my_reg, text).
# Keep in mind that there are multiple ways to skin this cat!


## Extracts the kingdom, phylum and species name for each species.

Kingdom = re.findall(r'Kingdom\s[A-Z][a-z]+', text)
#~ Kingdom
# 're.findall' searches a string and returns a list of all the matches of the given pattern.
# Find 'Kingdom' followed by a space, any capital letter, and 1 or more lower case letters.
# Alternatively: 'Kingdom\s\w+', but '\w' is less precise than '[A-Z][a-z]'.

Phylum = re.findall(r'Phylum\s[A-Z][a-z]+', text)

Species = re.findall(r'Species\s[A-Z][a-z]+\s[a-z]+', text)
# Species name is two words, 'Genus species'.
# Alternatively: 'Species\s\w*\s\w*'.


## Prints it neatly.
for i in xrange(len(Kingdom)):
	num = 1 + i
	print '\nBlackbird species', num, 'is:'
	print Kingdom[i]
	print Phylum[i]
	print Species[i]
# 'xrange()' makes a list of integers that is the number of items in 'Kingdom'.
# Loop over integers.
# Per species, I want to print a string, 'species n is', starting with species 1, not 0. Give 'num' the value 1 + the current integer.
# Print, on separate lines, a string and index i in each list.
