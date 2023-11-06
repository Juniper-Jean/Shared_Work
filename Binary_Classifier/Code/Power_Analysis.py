#!/Users/cpenning/anaconda3/bin/python
# *

""" """
# *

__author__ = 'cpenning@ic.ac.uk'
__version__ = '0.0.2' # 2023 Nov 4


#-----
# Imports
#-----
import os # module to interact with operating system
import gzip # module to work with gzip-compressed files
import _pickle as pickle # module to (de)serialise Python objects

import numpy as np # library for numerical operations
import scipy.stats # library for scientific & statistical functions
import arviz # ArviZ library for Bayesian data analysis

import tensorflow as tf # deep-learning library
from tensorflow import keras # high-level API to build & train neural networks
from keras import models, layers, activations, optimizers, regularizers  # Keras components to build models
from keras.utils.vis_utils import plot_model # utility to visualise Keras models
from keras.models import load_model # function to load pre-trained Keras models

import itertools # module to iterate & loop efficiently
import matplotlib.pyplot as plt # Matplotlib- library to make plots
import skimage.transform # part of scikit-image library for image processing
from sklearn.metrics import confusion_matrix # function to calculate confusion matrices
import pydot # optional, required by Keras to plot model (module to generate graph diagrams)
# *
# Order of imports as in '01_binary.ipynb' ImaGene tut.
# Need all?

import subprocess # module to run commands external to Python, like you would in terminal
from ImaGene_CP import * # W/ ImaGene_CP.py in same directory as this script, import everything from 'ImaGene' module.
from Functions_Binary_Classifier import *

# %run -i ../ImaGene.py
# *
# Use `%run` magic command to execute 'ImaGene.py' script & access its functionality.
# `-i` flag- run script in interactive mode. Means script run in such a way it can interact with current Python environment. Allows you to use functions & objects defined in 'ImaGene.py' within current session.
# *? ```
# cd Documents/PhD_Imperial_2023-27/ImaGene_LQTS/Binary_Classifier/Code
# conda activate ImaGene
# ipython
# %run -i ../ImaGene.py
# ```


# (
# Alt+Z to toggle word wrap for the session.
# Cmd+/ to comment out selected line.
# )


#-----
# Generate synthetic data, which will be used to train a neural network.
#-----

# parameter_files = [
#     'params_binary_Selection_Neutral_Strong.txt',
#     'params_binary_Selection_Neutral_Weak.txt',
#     'params_binary_Selection_Ancient.txt',
#     'params_binary_Selection_Recent.txt',
#     'params_binary_Locus_Length_200kbp.txt',
#     'params_binary_Locus_Length_300kbp.txt'
# ]
# # I have multiple .txt files / sets of parameter values- make a list of file names (string variables).

# for parameter_file in parameter_files: # Iterate through list of file names / sets of parameter values; run simulations for each.

#     command = f"bash generate_dataset.sh {parameter_file}"
#     # Make a string variable to hold a shell command.
#     # `f` at start of string indicates it's a formatted string (f-string)- let's you embed Python expressions in string in `{}` (curly braces; expression evaluated at runtime, then included in string).
#     # `{parameter_file}` gets replaced by value of `parameter_file` in ea iteration.
#     # 'generate_dataset.sh' (shell script) generates synthetic data by running simulations using MSMS (a simulator, https://www.mabs.at/publications/software-msms/).
#     # The script accepts an input .txt file that specifies the simulations' parameters.
#     # It splits simulations into batches, so, later, we can train a neural network with a 'simulation-on-the-fly' approach.

#     subprocess.call(command, shell=True)
#     # Execute shell command from within Python- run 'generate_dataset.sh' shell script.
#     # *? `shell=True`


#-----
# Process training data.
#-----

sim_directories = [
    'Selection_Neutral_Strong',
    # 'Selection_Neutral_Weak',
    # 'Selection_Ancient',
    # 'Selection_Recent',
    # 'Locus_Length_200kbp',
    # 'Locus_Length_300kbp'
]
# Make a list of directory names.
# 'generate_dataset.sh' (shell script) runs simulations to generate synthetic data (in batches). The script is run multiple times, with a different parameter value changed ea run. Ea directory (listed here) contains data from simulations run with a specific parameter value.

path_data = '../Data' # string variable holding relative path to directory that stores data

for sim_directory in sim_directories:
    print(f'processing set of simulations: {sim_directory}')
    process_training_data(path_data, sim_directory)
    print('done')
# Iterate through list of directory names; process data in ea folder.


#-----
# Train neural networks.
#-----

path_results = '../Results'  # string variable holding relative path to directory that stores data

for sim_directory in sim_directories:
    print(f'training model on data from directory: {sim_directory}')
    train_model(path_data, sim_directory, path_results)
    print('done')
# Iterate through list of directory names; process data in ea folder.

# *
# Need same axis scaling for ea plot
# Understand results, may need to edit analysis
# May have wrongly structured power analysis- train 1 model or train fresh models for diff training data?


#-----
# Evaluate training on test data, i.e., last batch of synthetic data.
#-----

for sim_directory in sim_directories:
    print(f'evaluating training on test data for model from directory: {sim_directory}')
    evaluate_training(path_data, sim_directory, path_results)
    print('done')


#-----
# Read genomic data from VCF file, store it in `ImaGene` object, & process data.
#-----

# *
# Annotate code, understand (commands, classes, objs, args, opts)
# Understand ea step in processing data, why do

# Test to debug error
# file_LCT = ImaFile(nr_samples=198, VCF_file_name='../Data/LCT.CEU.vcf') # CP added '../Data/'.
# gene_LCT = file_LCT.read_VCF()
# gene_LCT.summary()
# gene_LCT.filter_freq(0.01)
# gene_LCT.plot()


LQTS_file = ImaFile(nr_samples=198, VCF_file_name=f'{path_data}/LCT.CEU.vcf')
# Store genomic data in `ImaFile` object, specifying name of VCF file & number of samples (number of chromosomal copies- twice number of individuals for diploid organism). Latter parameter is not strictly necessary, but useful to check whether VCF we're analysing contains data we expect.

LQTS_gene = LQTS_file.read_VCF()
# *? Make an `ImaGene` object, reading VCF file & generating matrix of haplotypes.
# Annotate- how fn works, what is matrix of haplotypes, why use, what looks like?

# LQTS_gene.summary()
# LQTS_gene
# Look at data stored in object.
# Annotate- how .summary() fn works, why this ncols, nrows?

LQTS_gene.filter_freq(0.01)

# LQTS_gene.plot() # Look at resulting image.

# LQTS_gene.sort?
LQTS_gene.sort('rows_freq')
# LQTS_gene.plot()

LQTS_gene.convert(flip=True)
LQTS_gene.plot(file=f'{path_data}/LQTS_Gene_Image.png') # Save resulting image.
# LQTS_gene.summary()
# Annotate- why this ncols, nrows?

LQTS_gene.save(file=f'{path_data}/LQTS_gene') # *actually LCT gene at mo
# LQTS_gene = load_imagene(file=f'{path_data}/LQTS_gene') # Load `ImaGene` object.


#-----
# Deploy trained networks on real genomic data.
#-----

LQTS_gene = load_imagene(file=f'{path_data}/LQTS_gene') # Load `ImaGene` object.
print(deploy_trained_network(path_data, 'Selection_Neutral_Strong', LQTS_gene))

# *
# Loop- append vals to growing vector/list, save as CSV/table?
