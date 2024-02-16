Overview of Week2 Contents

/Code
basic_io.py - modules show how Python reads and writes text files

basic_csv.py - modules show how Python reads and writes csv files

boilerplate.py - prints 'This is a boilerplate'. A template to make an importable module that accepts a system argument.

using_name.py - illustrates the function of 'if __name__ == '__main__''. Prints one string if it's imported, prints another if it's run from the commandline.

sysargv.py - illustrates the function of 'sys.argv'

scope.py - illustrates variable scope - how local and global variables differ

control_flow.py - functions illustrating the use of control statements - some maths functions

cfexercises.py - more functions illustrating the use of control statements. Solution to 5.10 practical 1 in Samraat Pawar's 'Introduction to Biological Computing' (SilBioComp.pdf).

loops.py - examples of 'for' and 'while' loops

oaks.py - shows how to combine loops in a single code line. Finds just oaks trees in a species list.

Solutions to 5.10 practical 2
	lc1.py - making lists via list comprehensions, then loops. List a specific tuple index.

	lc2.py - making lists via list comprehensions, then loops. List specific tuple indices.

	tuple.py - print tuple indices on separate lines. 

	dictionary.py - populate a dictionary from a list of tuples

align_seqs.py - find and score the best alignment of 2 DNA strings. Run with a file of sequences as an argument in the commandline. I.e. type 'run align_seqs.py [sequences file].csv'. In this directory, you can run with '.../Data/Merged_fasta.csv'.

align_seqs_fasta.py - find and score the best alignment of 2 DNA strings. Run with two FASTA files, with one sequence each.

test_control_flow.py - illustrates unit testing with doctest

test_oaks.py - finds oaks in a list of species


/Data
Sequences.csv - 2 short DNA sequences - input for align_seqs.py

407228326.fasta, 407228412.fasta - 2 DNA sequences

326_noline.txt - copy of 407228326.fasta, without header and newline characters.

412_noline.txt - copy of 407228412.fasta, without header and newline characters.

Merged_fasta.csv - contains two DNA sequences, separated by a comma. Input for align_seqs.py. 326_noline.txt and 412_noline.txt were merged into this (merged manually, and using bash commands). 

TestOaksData.csv - input for test_oaks.py - list of species names. Some, but not all are oak species.


/Results
best_align.txt - alignment of 2 short DNA sequences - output of align_seqs.py run on Sequences.csv

best_align_fasta.txt - alignment of 407228326.fasta and 407228412.fasta - output of align_seqs.py

407228326_407228412_align.txt - alignment of 407228326.fasta and 407228412.fasta. Output of align_seqs_fasta.py.

JustOaksData.csv - oaks species extracted from a list of species (TestOaksData.csv) - output of test_oaks. py


/Sandbox
test.txt - input for the first two modules in basic_io.py - text lines to be read by a Python 'for' loop

testout.txt - each integer, 0-100, on a new line - written by the third module in basic_io.py

testp.p - a Python dictionary saved for later - output of the last module in basic_io.py

testcsv.csv - input for basic_csv.py - contains 'Species','Infraorder','Family','Distribution','Body mass male (Kg)'

bodymass.csv - the first and fourth columns of testcsv.csv - output of the last module in basic_csv.py
