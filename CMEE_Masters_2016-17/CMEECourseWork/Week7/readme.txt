'Week7' Contents

Advanced Python
November 14-18 2016

####################
## 'Code' Directory
####################

### Profiling ###
Profiling shows which parts of code take the most time, helping you optimise speed.

profileme.py - Functions used to demonstrate profiling.

run_LV.sh - Runs and profiles (using 'cProfile') 'LV1.py', 'LV2.py', 'LV3.py', and 'LV4.py'.

timeitme.py - Functions used to demonstrate profiling with the 'time' and 'timeit' modules.

### Regular expressions ###
blackbirds.py - Using regular expressions, captures the kingdom, phylum and species name for each species in 'blackbirds.txt'.

re4.py - Parsing email addresses using regexes.

regexs.py - Examples of regular expressions - a tool to find patterns in strings. Shows the use of the 're.search' function.

### 'scipy' (for number crunching) and 'matplotlib' (for plotting) packages ###
LV1.py - Shows 'scipy.integrate' (a sub-package for numerical integration) and 'matplotlib' (for plotting). Simulates and plots the Lotka-Volterra Model using scipy.

LV2.py - Simulates and plots the Lotka-Volterra Model with prey density dependence. Takes arguments for the parameters from the commandline, and shows chosen values in the plot.

LV3.py - Simulates and plots a discrete-time version of the Lotka-Volterra Model.

LV4.py - A discrete-time Lotka-Volterra model, with a random Gaussian fluctuation in the resource's growth rate.

### Plot/visualise networks ###
DrawFW.py - Uses the 'networkx' Python package to plot a food web network.

Nets.R - Uses the 'igraph' R package to plot the QMEE CDT collaboration network. Saves the plot to '../Data/QMEENet.svg'.

### Databases ###
Db_SQLite.py - 

SQLite.R - Shows how to access, update and manage SQLite databases.

### Workflows ###
fmr.R - Plots metabolic rate against body mass, for the Nagy et al 1999 dataset.

run_fmr_R.py - Runs 'fmr.R' and checks if the run was successful.

TestR.R - Prints 'Hello, this is R!'.

TestR.py - Uses the 'subprocess' package to run the R script 'TestR.R', writing the output to a file.

using_os.py - Uses 'subprocess.os.walk' to count the number of directories or files in /home beginning with lower or upper case 'c'.

├── Nets2.py
├── Nets3.py
├── Nets.py


####################
## 'Data' Directory
####################
blackbirds.txt - Input for 'blackbirds.py'. Taxonomic ranks of four blackbird species.

NagyEtAl1999.csv - Input for 'fmr.R'. Body mass and metabolic rate of various species.

QMEE_Net_Mat_edges.csv - Edges/links data for the QMEE CDT collaboration network. 'Nets.R' input.

QMEE_Net_Mat_nodes.csv - Data on nodes and their weightings for the QMEE CDT collaboration network. 'Nets.R' input.


####################
## 'Results' Directory
####################
FilesDirsStartingWithC_2.txt - A list of directories in 'home' starting with 'C'.

FilesDirsStartingWithC.p - A list of directories in 'home' starting with 'C'. This file was made using the 'pickle' module, allowing you to load the list in Python.

fmr_plot.pdf - 'fmr.R' output. Plot of metabolic rate against body mass, for the Nagy et al 1999 dataset.

'run_LV.sh' outputs:
	LV1_Profile.txt - How long various parts of 'LV1.py' executed.

	LV2_Profile.txt - As above, but for 'LV2.py'.

	LV3_Profile.txt - for 'LV3.py'

	LV4_Profile.txt - for 'LV4.py'

LV1.py - Shows 'scipy.integrate' (a sub-package for numerical integration) and 'matplotlib' (for plotting). Simulates and plots the Lotka-Volterra Model using scipy.

LV2.py - Simulates and plots the Lotka-Volterra Model with prey density dependence. Takes arguments for the parameters from the commandline, and shows chosen values in the plot.

LV3.py - Simulates and plots a discrete-time version of the Lotka-Volterra Model.

LV4.py - A discrete-time Lotka-Volterra model, with a random Gaussian fluctuation in the resource's growth rate.

prey_and_predators_1.pdf - 'LV1.py' output. Plot of the Lotka-Volterra Model.

prey_and_predators_2.pdf - 'LV2.py' output. Plot of the Lotka-Volterra Model with prey density dependence.

prey_and_predators_3.pdf - 'LV3.py' output. Plot of a discrete-time version of the Lotka-Volterra Model.

prey_and_predators_4.pdf - 'LV4.py' output. Plot of a discrete-time Lotka-Volterra model, with a random Gaussian fluctuation in the resource's growth rate.

QMEENet.svg - Visualisation of the QMEE CDT collaboration network. 'Nets.R' output.

TestR_errFile.Rout - 'TestR.py' runs 'TestR.R', printing to this file a log (of errors and what ran).

TestR.Rout - 'TestR.py' prints the output of 'TestR.R' to this file.
