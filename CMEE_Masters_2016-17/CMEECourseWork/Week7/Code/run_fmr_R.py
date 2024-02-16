#!/usr/bin/python

""" Runs 'fmr.R' and screens whether the run was successful """

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import subprocess
import os.path

subprocess.Popen("/usr/lib/R/bin/Rscript --verbose fmr.R", shell=True).wait()

if os.path.isfile('../Results/fmr_plot.pdf')==True:
	print '\nOutput file successfully made.'
else:
	print '\nCannot find output file. Check R script for errors.'
# Check if the R script successfully made its output file.
# Note: check only works if the file does not already exist (e.g. from a previous run).
# 'os.path.isfile()' tests whether a path is a regular file (a file of ASCII text).

#> \../Results/TestR.Rout 2> ../Results/TestR_errFile.Rout",\
