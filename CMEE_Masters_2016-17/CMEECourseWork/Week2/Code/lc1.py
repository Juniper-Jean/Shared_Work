#!/usr/bin/python

"""	Making lists via a single code line, then loops.
		List a specific tuple index."""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

birds = ( ('Passerculus sandwichensis','Savannah sparrow',18.7),
          ('Delichon urbica','House martin',19),
          ('Junco phaeonotus','Yellow-eyed junco',19.5),
          ('Junco hyemalis','Dark-eyed junco',19.6),
          ('Tachycineata bicolor','Tree swallow',20.2),
         )
# Make a tuple of tuples.


# (1) Write three separate list comprehensions that create three different
# lists containing the latin names, common names and mean body masses for
# each species in birds, respectively. 

# (2) Now do the same using conventional loops (you can shoose to do this 
# before 1 !). 

# ANNOTATE WHAT EVERY BLOCK OR IF NECESSARY, LINE IS DOING! 

# ALSO, PLEASE INCLUDE A DOCSTRING AT THE BEGINNING OF THIS FILE THAT 
# SAYS WHAT THE SCRIPT DOES AND WHO THE AUTHOR IS


# 1) List comprehensions

# Prints a list of all latin names in 'birds'.
latin_lc = list(i[0] for i in birds)
print latin_lc
# Make a list, called 'latin_lc', of the first index (latin name) of all tuples in 'birds'.
# Print the list.
# See "for i in birds: / print 'i'" - or 'i[0]'. Python reads each tuple in 'birds' as an object. 'i[0]' tells Python to just read the first index of each tuple.

# Prints a list of all common names in 'birds'.
common_lc = list(i[1] for i in birds)
print common_lc
# Make a list of the second index of all tuples in 'birds'.

# Prints a list of all body masses in 'birds'.
mass_lc = list(i[2] for i in birds)
print mass_lc


# 2) Loops

# Prints a list of all latin names in 'birds'.
latin_loop = []
for i in birds:
	latin_loop.append(i[0])
print latin_loop
# Make an empty list called 'latin_loop'.
# Loop over each object in 'birds'.
# Add the first index of all tuples to the list.
# Print the list.

# ** Should you be able to type any name and get its mass, or type any mass, get the name...?

# Prints a list of all common names in 'birds'.
common_loop = []
for i in birds:
	common_loop.append(i[1])
print common_loop

# Prints a list of all body masses in 'birds'.
mass_loop = []
for i in birds:
	mass_loop.append(i[2])
print mass_loop
