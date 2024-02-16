#!/usr/bin/python

"""	Template to make an importable module that accepts a system argument. 
		Prints 'This is a boilerplate'."""
# The argument could be a file (an external file), if the module code can read it.

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

# To access the docstring(s) (description):
# 'import boilerplate' / 'help(boilerplate)'
# - useful at run time.
# Also shows file location, author, version, function names/arguments.

# imports
import sys # module to interface our program with the operating system
import using_name

# constants can go here

# functions can go here

def main(argv): # Gives a name (and argument) to the indented function. This function can now be reused by importing it.
	print 'This is a boilerplate'
	return 0 # Exit?

if (__name__ == "__main__"): #makes sure the "main" function is called from commandline
	# If the script is run from the commandline
	status = main(sys.argv) # Run the function 'main'. Run it with a system (commandline) argument.
	sys.exit(status) # Then exit.
	
# 'argv' is a variable that holds the arguments passed to the Python script when it's run.
# 'sys.argv' is an object, made by python using the sys module, that contains the names of the argument variables in the current script (or commandline).
# main(argv=sys.argv) passes the argument variables to the main function.

# '__name__' is a 'special variable', the script's name. '__name__ == "__main__"' when the script is run from the commandline.
