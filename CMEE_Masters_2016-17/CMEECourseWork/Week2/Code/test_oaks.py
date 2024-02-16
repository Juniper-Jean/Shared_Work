#!/usr/bin/python

"""	Finds just oak trees in a species list.
		My first time debugging a script."""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import csv
import sys
import pdb
import doctest

import re

#Define function
def is_an_oak(name):
    """ Returns True if name is 'quercus'
        >>> is_an_oak('quercus')
        True
        
        Returns False if name is 'quercuss'
        >>> is_an_oak('quercuss')
        False
        
        Return True if name is 'Quercus'
        >>> is_an_oak('Quercus')
        True
    """
    
    return name.lower()=='quercus'
    
print(is_an_oak.__doc__) # ??

def main(argv): 
    f = open('../Data/TestOaksData.csv','rb') # Changed from '../../Data'.
    # Open the file to read.
    g = open('../Results/JustOaksData.csv','wb') # Changed from '../../Data'.
    # If file does not exist, make it, and open for writing.
    taxa = csv.reader(f)
    csvwrite = csv.writer(g)
    oaks = set() # Makes an empty set, which doesn't seem to be used later. No apparent affect on script.
    for row in taxa:
        print row
        print "The genus is", row[0]
        if is_an_oak(row[0]):
            print row[0]
            print 'FOUND AN OAK!'
            print " "
            csvwrite.writerow([row[0], row[1]])    
    # 'csv.read()' reads each line as a list. Store as 'taxa'.
    # Make an empty set, 'oaks'. This otherwise s
    # Loop over each line (list) in 'csvread'.
    # Print the list.
    # Print this string and index 0 (genus).
    # Pass index 0 to 'is_an_oak'. If it's returned (i.e. it's the oaks genus)
    # Print the genus and this string.
    # Write indices 0 and 1 (genus, species) to a new csv file as comma-delimted objects.
    
    f.close()
    g.close()
    # Added to close files.
    
    return 0
    
if (__name__ == "__main__"):
    status = main(sys.argv)

doctest.testmod() # To run with embedded tests.

# Bugs
# 	No input file -> saved one.
#		No oaks are found. Input file is a csv - commas separate genus and species. With 'csv.reader', 'row[0]' (index 0, the genus) is column 1 of a row. 'row[0]' is passed to 'is_an_oak'. An object (entry) in a csv would not normally end in a space, so a search for 'quercus ' will return nothing.
#		-> Changed to 'quercus' without a space.
#		Returns objects starting with 'quercus', so would return e.g. 'quercuss', which we are not looking for.
#		-> Changed 'startswith('quercus')' to '=='quercus'', to only return (case insensitive) exact matches. A disadvantage is this won't match common spelling errors.
# 	Changed output file's relative path, so it's made in the Results, not Data, directory.
