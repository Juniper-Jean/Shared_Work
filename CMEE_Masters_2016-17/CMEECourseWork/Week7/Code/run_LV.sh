#!/bin/bash
# Author: Calum Pennington (c.pennington@imperial.ac.uk)
# Script: run_LV.sh
# Desc: Runs and profiles 'LV1.py', 'LV2.py', 'LV3.py', and 'LV4.py'.
# Date: Nov 2016

echo -e "\nRunning and profiling 'LV1.py', 'LV2.py', 'LV3.py', and 'LV4.py'..."

echo -e "\nProfile outputs will be saved to '../Results/scriptname_Profile.txt'.\n"

python -m cProfile LV1.py > ../Results/LV1_Profile.txt
# '-m' searches for the module 'cProfile'.
# Redirect output to a file.

python -m cProfile LV2.py 1. 0.1 1.5 0.75 25. > ../Results/LV2_Profile.txt

python -m cProfile LV3.py  > ../Results/LV3_Profile.txt

python -m cProfile LV4.py  > ../Results/LV4_Profile.txt

#exit
