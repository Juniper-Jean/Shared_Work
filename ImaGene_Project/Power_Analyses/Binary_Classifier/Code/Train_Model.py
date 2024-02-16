#!/usr/bin/env python3

"""
Uses a synthetic genetic dataset to train & test a binary classifier model.

When run as a standalone program, this script trains multiple ML models sequentially, one after the other - trains a new ML model on each unique set of training data.

The `main` function:
- Takes as input a run number - a unique, sequential identifier for each 
experimental run (set of simulations).
- Retrieves a JSON configuration file corresponding to the current run number. 
- Retrieves the directory path where the training dataset is stored for the run from the 
configuration file.
- Builds & compiles a convolutional neural network (CNN) model based on 
specified configuration.

[
The script is part of a bigger workflow. Overview of workflow:
Base analysis:
- Training data - run a set of many simulations to generate (synthetic) data 
used to train a machine-learning (ML) model.
- The script 'generate_dataset.sh' runs the simulations & takes as input a .txt 
file of parameter values.
- Train a ML model on the synthetic data.

Power analysis:
- extends base analysis
- Vary values of some simulation parameters to assess the ML model's performance 
across different scenarios.
- Re-run simulations multiple times using a different set of parameter values 
each time.
- Train a new ML model on each unique set of training data.
- Explore the influence of each parameter & their interactions on the ML model's 
performance.

'An experimental run' (model run / one run) refers to one execution/instance of 
simulations using a parameter set & training one model (one cycle of training a 
ML model on data generated from a unique set of simulation parameters & then 
evaluating the model).
]
"""

__author__ = 'cpenning@ic.ac.uk'
__version__ = '0.0.2' # 2024 Feb 15

#-----
# Imports
#-----
# Standard-Library Imports
import os
# Module provides way to use functionality dependent on operating system. 
# Incs fns to interact w file system in platform-independent way.

import csv
# module- provides functionality to read from & write to CSV files
# 'csv'- 'Comma-Separated Values'- common format to store tabular data

import json # module for working w/ JSON data

import pdb
# interactive debugger module- allows you to pause execution, inspect variables, 
# step through code, & evaluate expressions at runtime

import time
# module provides fns for working w/ times & dates
# It's essential for measuring performance / execution time, as it allows us to 
# capture precise time pts before & after code execution.

# Local-Application Imports
from ImaGene import *
# W/ ImaGene.py in same directory as this script, import everything from 
# 'ImaGene' module.


import gzip
import _pickle as pickle

import numpy as np
import scipy.stats
import arviz

import tensorflow as tf
from tensorflow import keras
from keras import models, layers, activations, optimizers, regularizers
from keras.utils.vis_utils import plot_model
from keras.models import load_model

import itertools
import matplotlib.pyplot as plt
import skimage.transform
from sklearn.metrics import confusion_matrix
import pydot


#----
# `ImaNet` Class
#----
# The `ImaNet` class was designed to facilitate analysis of model training & 
# testing. It stores/tracks training & validation scores, & has methods to:
# - plot training progress
# - use trained model to predict outcomes
# - plot model's predictions again true labels (confusion matrix, scatter plot).


def build_model(gene_sim, path_results):
    """
    Builds & compiles a Keras model. Dynamically sets the input shape of the 
    model's first layer based on dimensions of a batch of training data.
    
    Users can manually adjust the model architecture/configuration as needed. 
    Generates a graphical visualisation of the model's architecture & saves it 
    to a file.

    Parameters:
    - gene_sim: object (instance of) the `ImaGene` class, containing a batch of 
    training data
    - path_results (str): path to the directory in which to save a graphical 
    visualisation of the model's architecture.

    The function:
    - expects the `gene_sim.data` attribute to be a NumPy array.
    - uses the array's `.shape` attribute to set the input shape.

    Returns:
    - model: compiled Keras model ready for training
    - model_tracker: object (instance) of the `ImaNet` class.
    """

    #----
    # Build & compile Keras Sequential model.
    #----
    model = models.Sequential([
    # Make obj (instance) of Keras Sequential model class (linear stack of layers).

        layers.Conv2D(filters=32, kernel_size=(3,3), strides=(1,1), 
                      activation='relu', 
                      kernel_regularizer=regularizers.l1_l2(l1=0.005, l2=0.005), 
                      padding='valid', 
                      input_shape=gene_sim.data.shape[1:]),
                    #   input_shape=(198, 192, 1)),
        # Add 2D convolutional layer, configured w/ 32 filters, 3x3 kernel size, 
        # stride of 1, ReLU activation fn, Elastic Net regularisation, 'valid' padding.
        # Input shape dynamically matches dims of training data.
        # 'valid' padding means no padding- convolution operation is only 
        # applied to regions where filter fully fits inside input volume.
        # Dims of output volume may reduce.

        layers.MaxPooling2D(pool_size=(2,2)),
        # Add max pooling layer (instantiate obj of `MaxPooling2D` class from 
        # Keras API), which reduces spatial dims (width & height) of input volume.
        # `pool_size` param specifies size of pooling window (here, 2x2).

        layers.Conv2D(filters=32, kernel_size=(3,3), strides=(1,1), 
                      activation='relu', 
                      kernel_regularizer=regularizers.l1_l2(l1=0.005, l2=0.005), 
                      padding='valid'),

        layers.MaxPooling2D(pool_size=(2,2)),

        layers.Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), 
                      activation='relu', 
                      kernel_regularizer=regularizers.l1_l2(l1=0.005, l2=0.005), 
                      padding='valid'),
        # Add another convolutional layer w/ 64 filters.

        layers.MaxPooling2D(pool_size=(2,2)),

        layers.Flatten(),
        # `layers.Flatten()` layer flattens input. It transforms 
        # multidimensional output of preceding layers into a one-dimensional 
        # array (converts 2D arrays into a 1D array, reshapes input data into a 
        # flat vector).
        # It doesn't have params.
        # It's necessary because following dense layers expect vector input- 
        # prepares convolutionally processed data for fully connected (Dense) 
        # layers that follow.

        layers.Dense(units=128, activation='relu'),
        # Add dense (fully connected) layer to network.
        # Use 128 units w/ ReLU activation fn.

        layers.Dense(units=1, activation='sigmoid')
        # Another dense layer, but w/ single unit & sigmoid activation fn.
        # This is typical configuration for binary classification, where output 
        # is probability of input belonging to 1 of 2 classes.
        # Sigmoid fn outputs val b/w 0 & 1.
    ])

    # pdb.set_trace()
    model.compile(optimizer='rmsprop', loss='binary_crossentropy', 
                  metrics=['accuracy'])
    # Compile model & specify settings- optimisation algorithm to use, loss fn 
    # to be minimise during training, & performance metrics to evaluate during 
    # training & testing.
    # Binary crossentropy is used for binary classification tasks & measures 
    # performance of model whose output is probability val b/w 0 & 1.
    # Accuracy measures fraction of correctly classified instances.

    model_tracker = ImaNet(name='[C32+P]x2+[C64+P]+D128')
    # Instantiate `ImaNet` obj.
    
    model.summary()
    # Print summary of model's architecture.
    # Incs layers, their types, output shapes, & nr of params (both trainable & 
    # non-trainable) in ea layer.
    
    plot_model(model, os.path.join(path_results, 'net.binary.png'))
    # Generates a graphical visualisation of the model's architecture & saves it 
    # to a file.

    return model, model_tracker


def train_model(path_training_data, path_results):
    """
    Iteratively trains an artificial neural network model on training data 
    loaded in batches.
    
    Iterates over the first 9 batches of synthetic genetic data, training the 
    model on each. The function expects batches of training data to be saved in 
    a directory structure of the format `{path_training_data}/Simulations{i}/` 
    (where `i` is batch number).

    Parameters:
    - path_training_data (str): path to directory containing batches of training data
    - path_results (str): path to the directory in which to save training 
    results (plot of training & validation loss & accuracy over epochs).

    Returns:
    - model: trained neural network model
    - model_tracker: `ImaNet` object after training - contains history of 
    training & validation metrics.
    """

    # pdb.set_trace() # debugger entry point

    for i in range(1, 10):
    # We split ea set of (synthetic) training data into batches, so we can train 
    # a neural network with a 'simulation on-the-fly' approach.
    # Loop over nrs 1 to 9- iterate over batches.
    # Train on 1st 9 batches.
    # Reserve 10th batch for testing model's performance after training.
        

        #----
        # Load batch of synthetic data.
        #----
        print(f'Training on batch: {path_training_data}/Simulations{i}/')
        # Output specified message to the console.
        # Identifies param set, replicate nr, & batch nr of data currently being used.
        # f-string allows for dynamic insertion of var into string.
        
        batch_path = os.path.join(path_training_data, 
                                #   f'Simulations{i}', 
                                  f'gene_sim_Batch{i}.binary')
        # Construct path to batch of (processed, synthetic) data.

        with open(batch_path, 'rb') as file:
            gene_sim = pickle.load(file)
        # Deserialise data- `ImaGene` obj.
        # `process_simulations` fn in 'Process_Synthetic_Data' Python script 
        # called, for ea data batch, `.save()` method of `ImaGene` class to save it.
        # The method uses `pickle` module to serialise `ImaGene` (`gene_sim`) 
        # obj & save it in binary format.
        

        if i==1:
            model, model_tracker = build_model(gene_sim, path_results)
        # At 1st iteration, build & compile model.
        

        #----
        # Initiate model training on 1 data batch.
        #----
        score = model.fit(gene_sim.data, gene_sim.targets, batch_size=64, 
                          epochs=1, validation_split=0.10, verbose=1)
        # Initiate training for model on 1 data batch.
        # `model` is instance of Keras Sequential model class (linear stack of layers).
        # `.fit` method trains model for specified nr of epochs (iterations over 
        # the data).
        # Adjusts model's weights to minimise loss fn.

        # Within ea epoch, entire dataset is divided into subsets ("mini-batches").
        # Splitting is sequential by default, taking 1st 64 samples, then next 
        # 64, & so on, until it has processed all samples.
        # Model updates occur after ea subset has been processed.
        # Epoch is completed when model has been exposed to every sample in 
        # dataset once.

        # After ea epoch, model uses portion of data specified by 
        # `validation_split` (10% here) to evaluate its performance.
        

        model_tracker.update_scores(score)
        # Record training & validation metrics (eg, loss & accuracy) obtained 
        # from current training session into `model_tracker`.

        # `model_tracker` is instance of `ImaNet` class, which is designed to 
        # track & store these metrics over time.
        # `score` obj is result returned by `model.fit()` method during training 
        # of Keras model.
        # It contains history of training & validation metrics for ea epoch, eg 
        # loss & accuracy.
        # `update_scores` method of `ImaNet` class updates `model_tracker` obj 
        # w/ training & validation metrics from current training batch.
    

    # pdb.set_trace()

    model_tracker.plot_train(os.path.join(path_results, 'training_plot.png'))
    # Plot training & validation loss & accuracy over epochs.
    # Save plot to `path_results` dir.

    return model, model_tracker


def evaluate_model(path_test_data, model, model_tracker, path_results):
    """
    Evaluates the trained model on unseen, test data.

    Loads a batch of synthetic genetic data as test data. Evaluates the 
    model's performance on test dataset: prints & returns test accuracy & loss. 
    Predicts outcomes on test dataset & generates confusion matrix plot.

    Parameters:
    - path_test_data (str): path to directory containing test data
    - model (keras.Model): trained neural network model to evaluate, an instance 
    of the Keras model class
    - model_tracker: object (instance) of the `ImaNet` class
    - path_results (str): path to the directory in which to save testing results 
    (confusion matrix plot).
    """
    
    # pdb.set_trace()

    with open(path_test_data, 'rb') as file:
        gene_sim_test = pickle.load(file)
    # Deserialise data- `ImaGene` obj.
        
    test_loss, test_accuracy = model.evaluate(gene_sim_test.data, 
                                              gene_sim_test.targets, verbose=2)
    # Evaluate model's performance on test dataset.
    # Assign resulting loss & accuracy metrics to `test_loss` & `test_accuracy` respectively.

    print(f'Test Accuracy: {test_accuracy}, Test Loss: {test_loss}')
    # Output model's test accuracy & loss to console after evaluation.
    # Use f-string to dynamically insert vars into str.

    model_tracker.predict(gene_sim_test, model)
    # Use trained model to predict outcomes on test dataset (`gene_sim_test`).
    # Store predictions within `model_tracker` obj for further analysis.
    # `.predict` is method of `ImaNet` class.

    model_tracker.plot_cm(gene_sim_test.classes, file=os.path.join(path_results, 'confusion_matrix.png'), text=True)
    # Generate confusion matrix plot, used to evaluate performance of 
    # classification models.
    # It shows nr of correct & incorrect predictions made by model compared to 
    # actual outcomes.

    return test_loss, test_accuracy, model, model_tracker


def save_metrics_to_csv(path_results, test_loss, test_accuracy):
    """
    Saves test set metrics (loss & accuracy) to a CSV file.

    Parameters:
    - path_results (str): directory in which to save CSV file
    - test_loss (float): loss metric from test set evaluation
    - test_accuracy (float): accuracy metric from test set evaluation.
    """

    metrics_file_path = os.path.join(path_results, f'test_metrics.csv')
    # Construct path to CSV file.
    
    headers = ['Test_Loss', 'Test_Accuracy']
    # Define list to hold col headers (header row) for CSV.
    
    with open(metrics_file_path, 'w', newline='') as csvfile:
    # Open CSV file in write mode ('w').
        
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        # Make obj (instance) of `csv.DictWriter` class- class that writes 
        # dictionaries to CSV file.
        
        # `writerow()` method of `csv.DictWriter` class takes dict as arg.
        # Ea key-val pair in dict corresponds to a col & cell data for current 
        # row in CSV file, respectively.
        # Keys correspond to `fieldnames` param provided when `DictWriter` obj 
        # was made.
        # This method writes 1 row to CSV file.
        # (Order of cell data in row corresponds to order of `fieldnames`.)
        
        # `fieldnames` param provides header row vals, which `csv.DictWriter` 
        # uses when you invoke `.writeheader()` method.
        # `fieldnames` specifies order of cols in CSV file. This is necessary 
        # because dicts were not ordered until Python 3.7 (even then, order 
        # isn't guaranteed in all contexts). By providing `fieldnames`, you 
        # explicitly define order of cols.

        writer.writeheader() # Write col names to CSV file.
        
        writer.writerow({'Test_Loss': test_loss, 'Test_Accuracy': test_accuracy})
        # Write row w/ test metrics to file (write `test_loss` & 
        # `test_accuracy` in corresponding cols).


def main(analysis_version, run_nr):
    """
    Orchestrates execution of the script's primary task.
    
    Parameters:
    - analysis_version (str): version number of the analysis, used to construct 
    dir paths
    - run_nr (int): unique, sequential identifier for each experimental run (job).
    """
    
    config_file_path = os.path.join(analysis_version, 'Config_Files', 
                                    f'config{run_nr}.json')
    # Construct path to config file for current run nr.
    
    with open(config_file_path, 'r') as file:
    # Load config data- open config file in read mode.
        
        config_data = json.load(file)
        # Read JSON content from file & convert it into Python dict.
    
    path_training_data = os.path.join('..', 'Data', analysis_version, 
                                      config_data["run_output_dir"])
    # Construct path to dir where output data of sims are stored (synthetic 
    # genetic data for current run- training data).

    path_results = os.path.join('..', 'Results', analysis_version, 
                                      config_data["run_output_dir"])
    # Construct path to dir in which to save results.

    os.makedirs(path_results, exist_ok=True)
    # Make dir if it doesn't exist.


    # pdb.set_trace()
    model, model_tracker = train_model(path_training_data, path_results)
    # Call fn to train model on training data in batches.

    # pdb.set_trace()
    path_test_data = os.path.join(path_training_data, 
                                #   f'Simulations{10}', 
                                  f'gene_sim_Batch{10}.binary')
    # Construct path to test dataset- 10th/last batch of sims.

    test_loss, test_accuracy, model, model_tracker = evaluate_model(path_test_data, model, 
                                                                    model_tracker, path_results)
    # Evaluate trained model on unseen, test data.

    save_metrics_to_csv(path_results, test_loss, test_accuracy)
    # Save test set metrics (loss & accuracy) to a CSV file.

    model.save(os.path.join(path_results, 'model.binary.h5'))
    # Save trained Keras model to disk.
    # Serialise model to file in HDF5 format.

    # model = load_model(os.path.join(path_results, 'model.binary.h5')
    # Load model from file.

    model_tracker.save(os.path.join(path_results, 'model_tracker.binary'))
    # `.save(file)` method of `ImaNet` class serialises & saves `ImaNet` obj for 
    # later retrieval & analysis.
    # Construct file path where obj is saved, using `path_results` var.

    # model_tracker = load_imanet(os.path.join(path_results, 'model.binary.h5')
    # Deserialise & load `ImaNet` obj from binary file.


if __name__ == '__main__':
# Check if script is executed as standalone (main) program & call main fn if `True`.
    
    start_time = time.time()
    # start time
    # We'll use this to calculate script's total execution time by subtracting 
    # it from end time.
    
    # analysis_version = 'Version1'
    analysis_version = 'Version2'
    nr_runs = 3
    # nr_runs = 12
    # Specify version nr of analysis & nr of runs.
    # Adjust as necessary.
    
    for i in range(1, nr_runs + 1): # Iterate from 1 to `nr_runs` inclusive.

        run_start_time = time.time()
        # Capture current time at start of individual experimental run (job).

        main(analysis_version, i)
        # For ea run, call `main` fn, passing `analysis version` & current run 
        # nr as args.

        run_end_time = time.time() # end time for this run
        print(f'Execution time for run {i}: {run_end_time - run_start_time} s')
        # Calculate execution time for current run & output it to the console- 
        # show how long ea run took.
    
    end_time = time.time() # end time
    print(f'Total execution time: {end_time - start_time:.2f} s')
    # Subtract `start_time` from `end_time` to get duration of script execution in s.
    # Output duration to the console- show how long script took to run in total.
    # `:.2f`: a format specifier (syntax is specific to f-strings). Formats 
    # resulting floating-point nr to 2 decimal places for readability.

# Code block executes script's main task in sequential manner for specified nr 
# of runs.
# This is suitable for running on a local computer (as opposed to parallel 
# execution of task on high-performance computing cluster).
# Additionally, the dunder name main check enables us to execute script as 
# standalone (main) program. This allows us to prototype/test individual 
# components of workflow in isolation (for development purposes), ensuring they 
# work as expected before integrating them into bigger workflow.
