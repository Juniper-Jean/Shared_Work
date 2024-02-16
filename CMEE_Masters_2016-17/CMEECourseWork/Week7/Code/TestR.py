#!/usr/bin/python

"""
		Runs the R script 'TestR.R', writing the output to a file.
		Writes a log of errors and what ran to another file.
"""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import subprocess
# A module that allows us to interface with the base terminal

print __doc__

subprocess.Popen("/usr/lib/R/bin/Rscript --verbose TestR.R > \
../Results/TestR.Rout 2> ../Results/TestR_errFile.Rout",\
shell=True).wait()
# 'subprocess' allows Python to interface with the bash terminal.
# A bash command to run an R script, writing the output to a file.
# '--verbose' prints a log of what ran and catches error messages. (Type 'man Rscript' into the bash terminal.) Note '2>' to write this to a file.
# Backslashes allow Python to read the mutliline script as a single line.

# '.wait()' tells Python to run processes one after the other, not all at once (wait until the process ends).
# ?subprocess.Popen.wait
