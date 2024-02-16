#!/usr/bin/python

""" """

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import subprocess
# A module that allows us to interface with the base terminal
import os.path

subprocess.Popen("Rscript --verbose 1_Edit_Data.R > \
../Results/1_Edit_Data.Rout 2> ../Results/1_Edit_Data.R_errFile.Rout",\
shell=True).wait()

# say 'running...' etc

if os.path.isfile('../Data/Edited_Data.csv')==True:
	print '\nOutput file successfully made.'
else:
	print '\nCannot find output file. Check R script for errors.'
	

subprocess.Popen("Rscript --verbose 2_Fit_Models.R > \
../Results/2_Fit_Models.Rout 2> ../Results/2_Fit_Models_errFile.Rout",\
shell=True).wait()

if os.path.isfile('../Results/Model_Results.csv')==True:
	print '\nOutput file successfully made.'
else:
	print '\nCannot find output file. Check R script for errors.'
	
	
subprocess.Popen("Rscript --verbose 3_Analyse_Results.R > \
../Results/3_Analyse_Results.Rout 2> ../Results/3_Analyse_Results_errFile.Rout",\
shell=True).wait()

if os.path.isfile('../Results/Proportion_Best_Model.pdf')==True:
	print '\nOutput file successfully made.'
else:
	print '\nCannot find output file. Check R script for errors.'


subprocess.Popen("bash Word_Count.sh",\
shell=True).wait()


subprocess.Popen("bash CompileLaTeX.sh Report",\
shell=True).wait()

if os.path.isfile('../Results/Report.pdf')==True:
	print '\nOutput file successfully made.'
else:
	print '\nCannot find output file. Check R script for errors.'

# Latex compile
# bash CompileLaTeX.sh *name of .tex file* without '.tex'
