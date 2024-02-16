#!/usr/bin/python

"""Find and score the best alignment of 2 DNA strings."""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

# These are the two sequences to match
#~ seq2 = "ATCGCCGGATTACGGG"
#~ seq1 = "CAATTCGGAT"
# Suppress, so can define these as sequences from an external file.

# The input file should be a single .csv, with two sequences at the top, separated by a comma.
# To run, type 'run align_seqs.py [file].csv' in the iPython commandline.

import sys
import csv
# Import outside of functions to avoid errors.

def calculate_score(s1, s2, l1, l2, startpoint):
	"""Scores an alignment"""
	# Moved up this function - generally avoid declaring one function within another.
	# startpoint is the point at which we want to start
	
	# function that computes a score
	# by returning the number of matches 
	# starting from arbitrary startpoint
	
	matched = "" # contains string for alignment
	score = 0
	for i in range(l2):
			if (i + startpoint) < l1:
					# if it's matching the character
					if s1[i + startpoint] == s2[i]:
							matched = matched + "*"
							score = score + 1
					else:
							matched = matched + "-"
	
	# Name a function that takes 5 arguments.
	# Make an empty string called 'matched'.
	# Give 'score' a value 0.
	# l2 is an integer. If l2 = 16, range(l2) is 0-15. Python loops over integers in the range.
	# If the integer + startpoint is < l1 - if 'startpoint' is before the last character in s1.
	# 'startpoint' is an integer defined below. It's where in s1, Python "aligns" s2.
	# And if the character at s1[i + sp] matches that at s2[i]
	# - If the character at index [i + sp] in s1 matches
	# Add a value '*' to 'matched', and 1 to 'score'.
	# Otherwise add '-' to 'matched' (there's no match).
	# 'matched' becomes a string of '*'s (matches) and '-'s (non-matches).
	
	# build some formatted output
	#~ print "." * startpoint + matched
	#~ print "." * startpoint + s2
	#~ print s1
	#~ print score 
	#~ print ""

	return score
	# Represents output of 'for' loop to the user.
	# Prints a string of '.'s, '*'s, '-' to show how far along the alignment started, and the number of matches.
	# Prints s1 (the long string, to which we align the short string) below.
	# Returns 'score' - this can be used as an argument in other functions.
	# The input file has long sequences. Suppress this section, so long strings are not printed to the terminal, and the code is faster.
	
	calculate_score(s1, s2, l1, l2, 0)
	calculate_score(s1, s2, l1, l2, 1)
	calculate_score(s1, s2, l1, l2, 5)
	# A test - run 'calculate_score' with startpoint of 0, 1, 5.
	# However, suppressing the formatted output (in calculate_score) makes these tests useless. We can't see their output to check the code is working.
	
def align(DataFile):
	"""	Finds and scores alignments.
			Prints the best to a new file."""
	# function that computes a score
	# by returning the number of matches 
	# starting from arbitrary startpoint
	
	f = open(DataFile,'rb') # Open the file for reading.
	
	csvread = csv.reader(f)
	for i in csvread:
		seq1 = i[0]
		seq2 = i[1]
	# Assigns the first csv column to 'seq1', the second column 'seq2'.
	
	f.close()
		
	# Assign the longest sequence to s1, and the shortest, s2.
	# l1 is the length of the longest, l2 that of the shortest.
	l1 = len(seq1)
	l2 = len(seq2)
	if l1 >= l2:
			s1 = seq1
			s2 = seq2
	else:
			s1 = seq2
			s2 = seq1
			l1, l2 = l2, l1 # Swap the two lengths.
	# Assign l1 as the length of seq1, l2 length of seq2.
	# If l1 is longer, assign seq1 as s1, seq2 s2.
	# Otherwise, assign seq2 as s1, seq1 s2. Swap the lengths, so l1 is seq2, the longest.
					
	# now try to find the best match (highest score)
	my_best_align = None
	my_best_score = -1
	# Assigns 2 variables. 'my_best_align' will be a string - use 'None' to specify no current value.
	# 'my_best_score' - -1 so if there is no match, the function below can assign a value of 0 to this.

	for i in range(l1):
		z = calculate_score(s1, s2, l1, l2, i)
		if z > my_best_score:
				my_best_align = "." * i + s2
				my_best_score = z
	# Loop over integers in range(l1).
	# If 'calculate_score' output is more than 'my_best_score' value (if the current match has the highest score so far)
	# Update my_best_align. This is a concatenated string of, '.'s up to the startpoint and s2 string.
	# Update my_best_score.

	with open('../Results/best_align.txt','wb') as g: # Open a file for writing.
		print >> g, my_best_align
		print >> g, s1
		print >> g, "Best score:" + str(my_best_score)
	# Represent the best alignment to the user and print the score. Write these to a new file 'best_align.txt'.
	
def main(argv):
	if len(sys.argv) > 1:
		align(argv[1])
	else:
		align('../Data/Merged_fasta.csv')
	return 0
	# If the system argument's length is > 1, i.e. if there is a file argument
	# Pass the file argument to 'align' function.
	# Otherwise (i.e. script is run without a file argument), pass the default file to 'align' function.
	# This allows the function to be run with or without an external input file.
	# In the commandline, an argument is anything after the command. So, in 'run [script]', the script name is the first argument. 'if len(sys.argv) > 1' checks whether there are arguments in addition to the script name.
	
if (__name__ == "__main__"):
	status=main(sys.argv)
	sys.exit(status)
