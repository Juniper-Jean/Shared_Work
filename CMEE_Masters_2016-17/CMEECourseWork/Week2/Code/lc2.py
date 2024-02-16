#!/usr/bin/python

"""	Making lists via a single code line, then loops.
		List specific tuple indices."""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

# Average UK Rainfall (mm) for 1910 by month
# http://www.metoffice.gov.uk/climate/uk/datasets
rainfall = (('JAN',111.4),
            ('FEB',126.1),
            ('MAR', 49.9),
            ('APR', 95.3),
            ('MAY', 71.8),
            ('JUN', 70.2),
            ('JUL', 97.1),
            ('AUG',140.2),
            ('SEP', 27.0),
            ('OCT', 89.4),
            ('NOV',128.4),
            ('DEC',142.2),
           )
# Make a tuple of tuples length two: month, rainfall.


# (1) Use a list comprehension to create a list of month,rainfall tuples where
# the amount of rain was greater than 100 mm.
 
# (2) Use a list comprehension to create a list of just month names where the
# amount of rain was less than 50 mm. 

# (3) Now do (1) and (2) using conventional loops (you can choose to do 
# this before 1 and 2 !). 

# ANNOTATE WHAT EVERY BLOCK OR IF NECESSARY, LINE IS DOING! 

# ALSO, PLEASE INCLUDE A DOCSTRING AT THE BEGINNING OF THIS FILE THAT 
# SAYS WHAT THE SCRIPT DOES AND WHO THE AUTHOR IS


# List comprehensions
# 1)
rain100_lc = list(i for i in rainfall if i[1] > 100)
print rain100_lc
# Make a list, called 'rain100_lc'.
# Loop over tuples in 'rainfall'.
# Add both indices of a tuple to the list, if the second index (amount of rain) is greater than 100.
# Print the list.

# 'i[1] > 100 for i in rainfall' returns the boolean, not the object.
#~ rain100_lc = list(i[1] > 100 for i in rainfall)
#~ print rain100_lc

# 2)
rain50_lc = list(i[0] for i in rainfall if i[1] < 50)
print rain50_lc
# Add index 0 of a tuple to the list if...

# 3) Loops

rain100_loop = list()
for i in rainfall:
	if i[1] > 100:
		rain100_loop.append(i) # Need colon/indent after every conditional.
print rain100_loop
# Make an empty list.
# Loop over tuples in 'rainfall'.
# If the second index (amount of rain) is greater than 100, add both tuples (month, rainfall) to the list.

# Prints a list of months where the amount of rain was less than 50 mm.
rain50_loop = list()
for i in rainfall:
	if i[1] < 50:
		rain50_loop.append(i[0])
print rain50_loop
