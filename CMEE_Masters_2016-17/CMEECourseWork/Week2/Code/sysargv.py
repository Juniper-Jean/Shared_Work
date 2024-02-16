#!/usr/bin/python

"""Illustrates how 'sys.argv' contains names of argument variables in the commandline"""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import sys
# Import module to interface our program with the operating system.

print "This is the name of the script: ", sys.argv[0]
# Print a string, and the first commandline argument (the script's file name).
# (In the commandline, you enter a command followed by arguments, which can be files or variables.)

print "Number of arguments: ", len(sys.argv)
# Print a string and the number of commandline arguments. One, if you just run the script. Two, if you type 'run sysargv.py var1'.

print "The arguments are: " , str(sys.argv)
# Print two strings. The first is in quotation marks, the second is all commandline arguments.
