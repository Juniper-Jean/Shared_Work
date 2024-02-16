#!/usr/bin/env python

"""	Shows how to combine loops in a single code line.
		Finds just oak trees in a species list."""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

## Let's find just those taxa that are oak trees from a list of species

taxa =	[	'Quercus robur',
					'Fraxinus excelsior',
					'Pinus sylvestris',
					'Quercus cerris',
					'Quercus petraea',
				]
# Make a list, called 'taxa', of these strings.

def is_an_oak(name):
	return name.lower().startswith('quercus ')
# Name this function, 'is_an_oak'. It takes an argument called 'name'.
# Get names starting with the string 'quercus ' - the string can be in any case. (Useful to search lists with bad punctuation.)

##Using for loops
oaks_loops = set()
for species in taxa:
	if is_an_oak(species):
		oaks_loops.add(species)
print oaks_loops
# Make a set.
# Loop through objects (which we'll call 'species') in 'taxa' list.
# Pass 'species' as an argument to 'is_an_oak'. If 'is_an_oak' returns it, add it to the set.
# Print the set.


##Using list comprehensions

oaks_lc = set([species for species in taxa if is_an_oak(species)])
print oaks_lc
# Make a set of objects from 'taxa', which 'is_an_oak' function returns.
# Print the set.

##Get names in UPPER CASE using for loops
oaks_loops = set()
for species in taxa:
	if is_an_oak(species):
		oaks_loops.add(species.upper()) # Add returned 'species' in upper case format.
print oaks_loops

##Get names in UPPER CASE using list comprehensions
oaks_lc = set([species.upper() for species in taxa if is_an_oak(species)])
print oaks_lc
