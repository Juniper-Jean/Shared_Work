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


def process_training_data(path_data, sim_directory):
    """
    processes training (synthetic) data & saves them
    """
        
    i = 1
    while i <= 10: # *
        print(f'batch {i}')

        # *
        # Annotate code, understand (commands, classes, objs, args, opts)
        # Understand ea step in processing data, why do

        data_directory = f'{path_data}/{sim_directory}' # string variable holding relative path to directory containing synthetic data

        sim_file = ImaFile(simulations_folder=f'{data_directory}/Simulations{i}', nr_samples=198, model_name='Marth-3epoch-CEU')
        # Read batch of simulations & store in `ImaFile` object.
        # Annotate, eg make instance of `ImaFile` class
        
        sim_gene = sim_file.read_simulations(parameter_name='selection_coeff_hetero', max_nrepl=2000)
        # *? Populate `ImaGene` object, specifying variable we want to estimate/predict (selection_coeff_hetero) & *how many data points per class to retain.
        # As a quick example, we will use only 2000 data points per class. CP: 'hetero'? Retain how many data points per class? Mean we discard some- why?
        
        # sim_gene.summary() # Look at data stored in object.
        
        sim_gene.filter_freq(0.01)
        sim_gene.sort('rows_freq')
        # sim_gene.summary()
        
        # ?sim_gene.resize # Explore different options for resizing.
        sim_gene.resize((198, 192))
        # sim_gene.summary()
        # **Resize images to match dimensions of real data- to have shape (198, 192).
        # CP: Wouldn't this lose data?

        sim_gene.convert(flip=True)
        # sim_gene.summary()
        # Convert images to numpy float matrices, flip black/white pixels, & normalise data.

        # for sel in sim_gene.classes:
        #     print(sel)
        #     sim_gene.plot(np.where(sim_gene.targets == sel)[0][0])
        # Plot 1 random image per class.

        sim_gene.subset(get_index_random(sim_gene)) # Randomly shuffle images.

        sim_gene.targets = to_binary(sim_gene.targets)
        # Targets represent the 2 possible classes. Since this analysis does binary classification, vectorise them as required by Keras.
        
        # os.makedirs(data_directory, exist_ok=True)
        # Build path to directory in which to store processed data. Make directory & any missing parent directories (if directories already exist, fn has no effect).

        sim_gene.save(file=f'{data_directory}/Sim_Gene_Batch{i}.binary') # Save `ImaGene` object.
        # sim_gene = load_imagene(file=path_data + 'sim_gene.binary') # Load it.

        i += 1


def train_model(path_data, sim_directory, path_results):
    """
    """
    
    data_directory = f'{path_data}/{sim_directory}' # string variable holding relative path to directory containing synthetic data
    sim_gene = load_imagene(file=f'{data_directory}/Sim_Gene_Batch1.binary') # Load 1st batch of training data.

    
    # *
    # Annotate code, understand (commands, classes, objs, args, opts)
    # Understand ea step, why do
    model = models.Sequential([
        layers.Conv2D(filters=32, kernel_size=(3,3), strides=(1,1), activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.005, l2=0.005), padding='valid', input_shape=sim_gene.data.shape[1:]), # *
        layers.MaxPooling2D(pool_size=(2,2)),
        layers.Conv2D(filters=32, kernel_size=(3,3), strides=(1,1), activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.005, l2=0.005), padding='valid'),
        layers.MaxPooling2D(pool_size=(2,2)),
        layers.Conv2D(filters=64, kernel_size=(3,3), strides=(1,1), activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.005, l2=0.005), padding='valid'),
        layers.MaxPooling2D(pool_size=(2,2)),
        layers.Flatten(),
        layers.Dense(units=128, activation='relu'),
        layers.Dense(units=1, activation='sigmoid')
    ])
    # Build network (build model in Keras with convolutional, pooling & dense layers- 3 layers of 2D convolutions & pooling, followed by fully-connected layer. Specify data's dimensions in 1st layer with the option `input_shape=gene_sim.data.shape[1:]`.)

    model.compile(optimizer='rmsprop',
        loss='binary_crossentropy',
        metrics=['accuracy'])
    # Compile Keras model.

    # model.summary()
    # plot_model(model, path + 'net.binary.png') # *Save- Results dir?
    # Look at & plot summary of model.


    score = model.fit(sim_gene.data, sim_gene.targets, batch_size=64, epochs=1, verbose=1, validation_split=0.10) # Train model on 1st data batch.
    
    net_LQTS = ImaNet(name='[C32+P]x2+[C64+P]+D128') # Initialise a network object, `ImaNet`.
    
    net_LQTS.update_scores(score) # Keep track of accuracy & loss scores across iterations.
    

    i = 2
    while i < 10:
        print(i)
        sim_gene = load_imagene(file=f'{data_directory}/Sim_Gene_Batch{i}.binary')
        score = model.fit(sim_gene.data, sim_gene.targets, batch_size=64, epochs=1, verbose=1, validation_split=0.10)
        net_LQTS.update_scores(score)
        i += 1
    # Repeat for remaining data batches, leaving 1 for testing.
    
    results_directory = f'{path_results}/{sim_directory}' # string variable holding relative path to directory in which to store results
    os.makedirs(results_directory, exist_ok=True)
    # Build path to directory in which to store results. Make directory & any missing parent directories (if directories already exist, fn has no effect).

    net_LQTS.plot_train(file=f'{results_directory}/Loss_Validation_Accuracy.png')
    # *? Plot loss & validation accuracy during training to check, e.g., for overfitting.
    # & save plot.

    model.save(f'{data_directory}/model.binary.h5') # Save trained model.
    net_LQTS.save(f'{data_directory}/net_LQTS.binary') # Save network itself.

# *loss: 1.1001 - accuracy: 0.8172 - val_loss: 1.8665 - val_accuracy: 0.4800


def evaluate_training(path_data, sim_directory, path_results):
    """
    """

    data_directory = f'{path_data}/{sim_directory}' # string variable holding relative path to data directory containing synthetic data
    i = 10
    sim_gene_test = load_imagene(file=f'{data_directory}/Sim_Gene_Batch{i}.binary') # Load last batch of training data.


    # *
    # Annotate code, understand (commands, classes, objs, args, opts)
    # Understand ea step, why do

    rnd_idx = get_index_random(sim_gene_test) # no need to create this extra variable
    sim_gene_test.subset(rnd_idx)

    sim_gene_test.targets = to_binary(sim_gene_test.targets)

    model = load_model(f'{data_directory}/model.binary.h5') # Load trained model.
    net_LQTS = load_imanet(f'{data_directory}/net_LQTS.binary') # Load network.

    net_LQTS.test = model.evaluate(sim_gene_test.data, sim_gene_test.targets, batch_size=None, verbose=0)
    print(net_LQTS.test) # Report [loss, accuracy] on test set. *save/append?

    # *? For binary (or multiclass) classification, it is convenient to plot confusion matrix after predicting responses from test data.
    net_LQTS.predict(sim_gene_test, model)

    results_directory = f'{path_results}/{sim_directory}' # string variable holding relative path to directory in which to store results
    net_LQTS.plot_cm(sim_gene_test.classes, file=f'{results_directory}/Confusion_Matrix.png', text=True)
    # Save plot.


def deploy_trained_network(path_data, sim_directory, LQTS_gene):
    """
    """

    data_directory = f'{path_data}/{sim_directory}' # string variable holding relative path to data directory containing synthetic data
    model = load_model(f'{data_directory}/model.binary.h5') # Load trained model.
    
    # *
    # Annotate code, understand (commands, classes, objs, args, opts)
    # Understand stats, ML analysis/method, results
    class_score = model.predict(LQTS_gene.data, batch_size=None)[0][0]
    print(class_score)
    # Use trained network to predict natural selection on locus of interest. Command outputs class score (can be interpreted as posterior probability with uniform prior) of locus under positive selection under conditions simulated.

    return class_score

