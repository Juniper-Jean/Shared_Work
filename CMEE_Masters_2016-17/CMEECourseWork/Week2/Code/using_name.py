#!/usr/bin/python

# Filename: using_name.py

"""	Illustrates the function of 'if __name__ == '__main__''.
		Prints one string if it's imported, prints another if it's run from the commandline."""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

if __name__ == '__main__': # If the script is run from the commandline
	print 'This program is being run by itself'
else:
	print 'I am being imported from another module'
	# Otherwise, print 'I am...'. I.e. print if this module is being imported.
