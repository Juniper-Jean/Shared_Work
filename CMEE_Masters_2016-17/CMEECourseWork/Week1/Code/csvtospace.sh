#!/bin/bash
# Author: Calum Pennington c.pennington@imperial.ac.uk
# Script: csvtospace.sh
# Desc: converts a comma- to a space-separated-values file
#		saves output to a different file
# Arguments: 1-> comma-separated-values file
# Date: Oct 2016

echo "Making a space-separated-values version of ../Data/$1.csv ..."

cat ../Data/$1.csv | tr "," " " > ../Data/$1Space.txt

echo "Done!"

exit
