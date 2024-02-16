#!/usr/bin/python

"""Print tuple indices on separate lines"""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

birds = ( ('Passerculus sandwichensis','Savannah sparrow',18.7),
          ('Delichon urbica','House martin',19),
          ('Junco phaeonotus','Yellow-eyed junco',19.5),
          ('Junco hyemalis','Dark-eyed junco',19.6),
          ('Tachycineata bicolor','Tree swallow',20.2),
        )

# Birds is a tuple of tuples of length three: latin name, common name, mass.
# write a (short) script to print these on a separate line for each species
# Hints: use the "print" command! You can use list comprehension!

# ANNOTATE WHAT EVERY BLOCK OR IF NECESSARY, LINE IS DOING! 

# ALSO, PLEASE INCLUDE A DOCSTRING AT THE BEGINNING OF THIS FILE THAT 
# SAYS WHAT THE SCRIPT DOES AND WHO THE AUTHOR IS

newline = ['%s\n%s\n%s\n'%(i[0],i[1],i[2]) for i in birds]
for x in newline:
	print x
# The variable 'newline' has the following value.
# Loop over objects in 'birds'. The objects are tuples of length three.
# '%s' is a placeholder for a string. Separate each string with a newline character (\n). The strings are i[0], i[1], i[2] in 'birds'.

# Same output:
#~ for i in birds:
	#~ print i[0]
	#~ print i[1]
	#~ print '%s\n'%i[2]

# More formatting:
#~ b = ['%s\t%s\t%s'%(i[0],i[1],i[2]) for i in birds]
#~ for x in b:
	#~ print x
# \t - tab
