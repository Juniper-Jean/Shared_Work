#!/usr/bin/python

""" Count the number of directories or files in /home beginning with lower or upper case 'c' """

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

# Use the subprocess.os module to get a list of files and  directories 
# in your ubuntu home directory 

# Hint: look in subprocess.os and/or subprocess.os.path and/or 
# subprocess.os.walk for helpful functions

import subprocess
import pickle

#################################
# Get a list of files and 
# directories in your home/ that start with an uppercase 'C'

# Type your code here:

home = subprocess.os.path.expanduser("~")
# Get the user's home directory.

FilesDirsStartingWithC = []
# Create a list to store the results.

# Use a for loop to walk through the home directory.
for (dir, subdir, files) in subprocess.os.walk(home):
	for SName in subdir:
		if SName.startswith('C') is True:
			FilesDirsStartingWithC.append(SName)
	for FName in files:
		if FName.startswith('C') is True:
			FilesDirsStartingWithC.append(FName)
# 'for dir in subprocess.os.walk(home): /print dir'
# prints tuples of: relative path (from home), subdirectories, and files.
# Loop over subdirectory names. If it begins with 'C', append it to the list.
# Do the same for file names.

# **Try to avoid a nested for loop.
# Initially tried:
#~ for (dir, subdir, files) in subprocess.os.walk(home):
	#~ if subdir.startswith(('C','c')) is True:
		#~ FilesDirsStartingWithC.append(subdir)
# But 'subdir' is a tuple, so I must iterate over its objects - thus 2nd loop.

print "%r items in /home start with 'C'"%len(FilesDirsStartingWithC)

f = open('../Results/FilesDirsStartingWithC.p', 'wb')
pickle.dump(FilesDirsStartingWithC, f)
f.close()
# Save the list to a file.
# Saving via pickle allows you to load the list, so you can use it in another Python script.

f = open('../Results/FilesDirsStartingWithC_2.txt', 'wb')
for i in FilesDirsStartingWithC:
	f.write("%r\n" % i)
f.close()
# Save in a more reader-friendly format - just the names, and each name on a new line.

#################################
# Get files and directories in your home/ that start with either an 
# upper or lower case 'C'

StartWithCc = []

# Type your code here:
for (dir, subdir, files) in subprocess.os.walk(home):
	for SName in subdir:
		if SName.startswith(('C','c')) is True:
			StartWithCc.append(SName)
	for FName in files:
		if FName.startswith(('C','c')) is True:
			StartWithCc.append(FName)
# '.startswith()' returns True if object starts with a specified prefix. Prefix can be a tuble of strings to try.

print "%r items in '/home' start with 'C' or 'c'"%len(StartWithCc)

#################################
# Get only directories in your home/ that start with either an upper or 
# lower case 'C' 

DirsStartWithCc = []

# Type your code here:
for (dir, subdir, files) in subprocess.os.walk(home):
	for SName in subdir:
		if SName.startswith(('C','c')) is True:
			DirsStartWithCc.append(SName)

print "%r directories in /home start with 'C' or 'c'"%len(DirsStartWithCc)
