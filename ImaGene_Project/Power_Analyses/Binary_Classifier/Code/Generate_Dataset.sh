#!/Users/cpenning/anaconda3/bin/python
# Shebang line specifies which interpreter to use when execute script.
# `#!`- the actual shebang/hashbang- special character sequence telling OS that what follows is path to interpreter. Only relevant on Unix-like OSs (Linux, macOS).
# Followed by full path to shell interpreter you want to use- points to Bash executable installed on your system.

# If make script executable (using `chmod +x your_script.sh`) & run it (eg `./your_script.sh`), system reads shebang- ensures script runs w/ intended shell interpreter- important if multiple shells installed.
# W/o shebang, can't directly execute script using `./your_script.sh` unless system has default way to interpret such files.
# Instead, must explicitly call interpreter followed by script name (eg `bash your_script.py`)- will run script using whatever shell is set as default in current env.

# If write script for multiple users, users may have different envs- path to interpreter may not be same on all systems.
# Common approach is to use generic shebang that relies on env's `PATH` to find interpreter, eg `#!/usr/bin/env bash` will use 1st Bash interpreter in user's `PATH`- may be more flexible across different systems.


# Bash is most common & widely used shell on Unix-like systems. It's default shell on many Linux distributions & macOS (until Catalina, after which zsh became default).
# Using Bash shebang (#!/bin/bash) increases likelihood that script will run w/o issues on most systems.

# If script relies on features unique to zsh or if targeting env where zsh is the standard, choosing a zsh shebang (#!/bin/zsh) would be more appropriate. But, this may limit script's portability to envs where zsh isn't the default or may not be installed.

# 'Shell' refers to a cmd-line interpreter that provides a user interface for access to OS's services. There are various types of shells, like sh (Bourne shell), zsh (Z Shell).
# Bash ('Bourne Again SHell')- type of Unix shell & enhanced replacement for original Bourne shell (sh). Incs additional features & is default shell on many Unix-based systems, inc most Linux distributions & macOS.


# This script runs simulations using the MSMS simulator (https://www.mabs.at/publications/software-msms/) to generate (synthetic) genomic data, which are later used to train a machine-learning (ML) model. The model is trained to predict parameters like selection coefficient & time of a natural-selection event.

# Usage: `./generate_dataset.sh <parameter_file> <output_directory>`
# Args:
# - <parameter_file>: Path to the file containing simulation parameters.
# - <output_directory>: Directory where simulation results will be stored.

# The script iterates over a range of selection coefficients & selection times, running simulations in batches & saving results in compressed format.

# This is a customised version of the 'generate_dataset.sh' script from tutorials for the ImaGene program. The following code includes both original code & edits by cpenning@ic.ac.uk. Customisations include dynamic output directory handling & enhanced parameter management to facilitate a more flexible simulation environment.

# ImaGene program:
# Original manuscript & citation: Torada, Luis; Lorenzon, Lucrezia; Beddis, Alice; Isildak, Ulas; Pattini, Linda; Mathieson, Sara; Fumagalli, Matteo. ImaGene: a convolutional neural network to quantify natural selection from genomic data. BMC Bioinformatics, Vol 20, Suppl 9, p337 (2019). doi:10.1186/s12859-019-2927-x.

# Original GitHub URL: https://github.com/mfumagalli/ImaGene, accessed 2023 November 5


date # Print current date & time.


source $1
# Source parameter file provided as 1st arg.

# `source` cmd (or its synonym `.`) executes cmds from a file.
# When use `source` followed by filename, the shell reads & executes cmds from that file as if they were typed directly into cmd line. (When source file, Bash reads it line by line. Ea line is interpreted & executed as regular shell cmd.)
# This is useful for eg setting vars & defining fns.
# File intended to be sourced should contain valid shell-script syntax, inc var assignments, fn definitions, & other shell cmds.

# Bash doesn't require specific file extension like '.sh' for sourcing.
# Eg param file, even though it has '.txt' extension, contains lines that set shell vars.

# Var assignments in params file become available in env of 'generate_dataset.sh' script.

# Positional params: In shell script, `$1`, `$2`, etc are placeholders for cmd-line args passed to script. `$1` is 1st arg, `$2` is 2nd, etc.
# When you execute script from cmd line & provide args, these args are assigned to these positional params.
# This allows script to access vals provided by user.
# Eg, say you run `./generate_dataset.sh Parameters_Binary.txt output_dir` in cmd line, 'Parameters_Binary.txt' is 1st arg provided to script, 'output_dir' is 2nd.
# In script, `$1` will hold val 'Parameters_Binary.txt', `$2` will hold val 'output_dir'.


OUTPUT_DIR=$2
# Assign 2nd cmd-line arg to OUTPUT_DIR -dir in which to save sim results.

# Use of `$`: When define (assign val to) var, you don't use `$`. Eg, OUTPUT_DIR=$2 means 'set var `OUTPUT_DIR` to val of $2'.
# To access val of var, use `$` (this tells the shell you're referring to content of var, not its name). Eg `$OUTPUT_DIR` gets replaced w/ val stored in `OUTPUT_DIR`.
# Assignment: no `$` sign. It's like saying, 'Store this val in this named container.'
# Accessing val: Use `$` sign- like saying, 'Give me content of container.'


for (( INDEX=1; INDEX<=$NBATCH; INDEX++ ))
do
# Loop through batches as defined by NBATCH.
# `do` is necessary part of loop syntax. It marks beginning of block of cmds that will be executed as part of loop.
# Similarly, `done` signifies end of loop block.

# Syntax of C-style `for` Loop in Bash:
# ```
# for (( initialization; condition; increment ))
# do
#     # cmds to execute in ea iteration of loop
# done
# ```
# `initialization`- initialise loop counter. In this script, `INDEX=1` initialises `INDEX` to 1.
# `condition`- test that's evaluated before ea iteration of loop. If condition evaluates to true, loop continues; if false, loop exits. `INDEX<=$NBATCH` checks if `INDEX` is less than / equal to val of `NBATCH`.
# `increment` defines how to update counter after ea iteration. `INDEX++` increments `INDEX` by 1 in ea iteration- shorthand for `INDEX = INDEX + 1`.


	FNAME=$OUTPUT_DIR/Simulations$INDEX # Construct file name using OUTPUT_DIR & batch index.
	echo $FNAME # `echo` cmd displays val of var to terminal.

	mkdir -p $FNAME
	# Make dir if it doesn't exist.
	# Make nested dirs: `-p` flag ensures entire dir path is made, inc any parent directories. Stands for 'parents'.

	# Nested loops for `SELRANGE` & `TIMERANGE` params.
	for SEL in $SELRANGE
	do
		for TIME in $TIMERANGE
		do
			
			java -jar $DIRMSMS -N $NREF -ms $NCHROMS $NREPL -t $THETA -r $RHO $LEN -Sp $SELPOS -SI $TIME 1 $FREQ -SAA $(($SEL*2)) -SAa $SEL -Saa 0 -Smark $DEMO -threads $NTHREADS | gzip > $FNAME/msms..$SEL..$TIME..txt.gz
            # Run MSMS simulator w/ set of param vals.
            # Compress its output data using `gzip`.
            # Redirect compressed data to specified file name & dir.
            # (Use of vars like `$DIRMSMS`, `$NREF`, etc, allow for dynamic execution based on vals defined in params file.)

            # Shell cmd- Java execution:
            # `java -jar $DIRMSMS`: runs Java application packaged in JAR file. `$DIRMSMS` var contains path to MSMS JAR file. `-jar` flag tells Java to execute JAR file located at path.

            # `-N $NREF -ms $NCHROMS $NREPL -t $THETA -r $RHO $LEN...`- MSMS params (params passed to MSMS application). Ea option (like `-N`) is followed by its val, which are stored in vars (`$NREF`). These vars are set in the sourced param file.
            # `$(($SEL*2))`- arithmetic expansion in Bash. Calculates val of `$SEL` multiplied by 2. Calculated val is then used as MSMS param.

			# Below is a breakdown of the meaning of some params. For a more comprehensive explanation of ea param, refer to annotations in the '.txt' template params file.
			# Eg, `-N $NREF`- reference effective population size. `$NREF`- var containing this val.
			# `-ms $NCHROMS $NREPL` specifies nr of simus to run. `$NCHROMS` is nr of chromosomal copies to simulate & `$NREPL` is nr of replicates (independent sim runs) for ea param set.
			# `-SI $TIME 1 $FREQ`- the time of a selective event (`$TIME`), proportion of the pop affected (`1` in this case, indicating the entire pop), & the initial frequency of the selected allele (`$FREQ`).

			# `-SAA $(($SEL*2)), -SAa $SEL, -Saa 0` defines the selection coefficients for different genotypes.
			# `-SAA $(($SEL*2))`- for the homozygous state of the selected allele
			# Doubling the val of `$SEL` for homozygotes is based on a common model in pop genetics where the fitness effect of having 2 copies of the advantageous allele (AA) is twice that of having just 1 (Aa).
			# This is a simplification & assumes additive effects, but it's a standard starting point for many models.
			# `-SAa $SEL`- for heterozygotes (1 copy of the selected allele & 1 copy of the alternative allele).
			# `-Saa 0`- for the homozygous state of the non-selected allele (aa)
			# A val of 0 suggests no selection against/for this genotype, or it could mean this is the baseline fitness against which the other genotypes are compared.
			
            # `| gzip` takes output of MSMS simulator & pipes it into `gzip` cmd, which compresses data.

            # `> $FNAME/msms..$SEL..$TIME..txt.gz`- redirect compressed output from `gzip` to a file. Construct filename using `$FNAME`, `$SEL`, & `$TIME` vars. Redirect operator (`>`) ensures output is written to this file.

		done
	done
done

date # Print date & time again at end of script.
