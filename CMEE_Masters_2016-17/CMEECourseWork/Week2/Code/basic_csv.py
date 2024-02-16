#!/usr/bin/python

"""Shows how Python reads and writes '.csv' files"""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import csv # Import 'csv' package.

# Read a file containing:
# 'Species','Infraorder','Family','Distribution','Body mass male (Kg)'.
# Identify the species name.

f = open('../Sandbox/testcsv.csv','rb')

csvread = csv.reader(f)
temp = []
for row in csvread:
	temp.append(tuple(row))
	print row
	print "The species is", row[0]

f.close()

# Open the file for reading.
# Convert each line in the file to a list. Store all this as 'csvread'.
# Make an empty list.
# Python will loop over each line (list) in 'csvread'.
# Add the list as a tuple in 'temp'. 
# Print the list.
# Print a string followed by the first index in the list.
# After the loop, close the file.
# 'temp' becomes a list of tuples.

# Python loops over each line in a text file (i.e. each line is an object in the file variable). Each character in the line is an index.
# We want to specify and print specific strings (species names), but we can not due to how Python reads csv's. 'row[0]' specifies the first letter in the string object. (Try f = open / for i in f: / print i[0])
# 'csv.read', however, reads each line as a list. Text delimited by commas (here, strings) becomes a list index.

# temp and tuples step is not necessary for the output, but converts the nested lists to immutable tuples.


# Write a file containing only species name and body mass

f = open('../Sandbox/testcsv.csv','rb') # Open the file to read.
g = open('../Sandbox/bodymass.csv','wb') # If file does not exist, make it, and open for writing.

csvread = csv.reader(f)
csvwrite = csv.writer(g)
for row in csvread:
	print row
	csvwrite.writerow([row[0], row[4]])

f.close()
g.close()

# 'csv.read()' reads each line as a list. Store as 'csvread'.
# Loop over each line (list) in 'csvread'.
# Print the list.
# Write the first and fourth indices to a new csv file as comma-delimted objects.
