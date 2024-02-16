#!/usr/bin/python

"""Populate a dictionary from a list of tuples"""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

taxa = [ ('Myotis lucifugus','Chiroptera'),
         ('Gerbillus henleyi','Rodentia',),
         ('Peromyscus crinitus', 'Rodentia'),
         ('Mus domesticus', 'Rodentia'),
         ('Cleithrionomys rutilus', 'Rodentia'),
         ('Microgale dobsoni', 'Afrosoricida'),
         ('Microgale talazaci', 'Afrosoricida'),
         ('Lyacon pictus', 'Carnivora'),
         ('Arctocephalus gazella', 'Carnivora'),
         ('Canis lupus', 'Carnivora'),
        ]
# Make a list, called 'taxa', of tuples length two.


# Write a short python script to populate a dictionary called taxa_dic 
# derived from  taxa so that it maps order names to sets of taxa. 
# E.g. 'Chiroptera' : set(['Myotis lucifugus']) etc. 

# ANNOTATE WHAT EVERY BLOCK OR IF NECESSARY, LINE IS DOING! 

# ALSO, PLEASE INCLUDE A DOCSTRING AT THE BEGINNING OF THIS FILE THAT 
# SAYS WHAT THE SCRIPT DOES AND WHO THE AUTHOR IS

# Write your script here:

taxa_dic = {}
for species, order in taxa:
	if order not in taxa_dic:
		taxa_dic[order] = set([species])
	else:
		taxa_dic[order].add(species)
print taxa_dic
# Make an empty dictionary, called 'taxa_dic'.
# Loop over tuples in 'taxa' list. For tuple index 0 (called 'species') and index 1 (called 'order').
# Dictionaries are made of keys with values. You cannot add a key without a value. Add to a dictionary using 'taxa_dic[key] = value'. 
# If index 1 is not in the dictionary, add as a key with a value.
# The value is a set. This lets you add multiple values to the key. Add index 0 to the set.
# Add an object to a set using 'set()'. Write 'species' in '[]' so it is added as a string. Otherwise a set(s, p, i, e, c, e, s) is made.
# The handle (name) of this set is 'taxa_dic[order]'.
# Otherwise add 'species' to the set.
# The 'if/else' statements add a new value to the key without overwriting existing ones.

# Alternative:
#~ taxa_dic = {}
#~ for i in taxa:
	#~ if i[1] not in taxa_dic:
		#~ taxa_dic[i[1]] = set([i[0]])
	#~ else:
		#~ taxa_dic[i[1]].add(i[0])
		
# I had to solve 2 problems:
# - separately call objects in a tuple (from a list of tuples)
# - add multiple values to a dictionary key.

# How to format dictionary - bells and whistles
# Can say 'taxa.dic.keys()'.
