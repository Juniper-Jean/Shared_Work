#!/Users/cpenning/anaconda3/bin/python

"""
Generates a CSV file containing all combinations of simulation-parameter values 
for a full factorial design.

For each parameter, the user simply names the parameter & lists its values. The 
script automatically generates all combinations of given parameter values. It 
eases parameter management & streamlines the workflow. Users can easily adapt 
the script without major changes to the code:
- edit or add values for parameters already written here
- add new parameters whose values they want to vary & the values.

This script is part of a bigger workflow that performs a power analysis. Testing 
every possible combination - i.e., a full factorial design - is essential in a 
power analysis. It means we can assess the effect of each factor & their 
interactions, ensuring a balanced, unbiased evaluation of each factor's impact.


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
__version__ = '0.0.5' # 2024 Feb 7

#-----
# Imports
#-----
# Standard-Library Imports
# Standard Library- collection of built-in modules & libraries that come bundled 
# w/ Python language, included in Python installation- needn't install 
# separately like w/ 3rd-party libraries

import itertools
# module- collection of fast, memory-efficient tools useful in making iterators 
# for efficient looping
# iterable- any obj / data struct you can loop over- can go through its elements 
# 1 by 1-, eg list, tuple, string, dicts

import csv
# module- provides functionality to read from & write to CSV files
# 'csv'- 'Comma-Separated Values'- common format to store tabular data

import os
# Module provides way to use functionality dependent on operating system. 
# Incs fns to interact w file system in platform-independent way.

import pdb
# interactive debugger module- allows you to pause execution, inspect variables, 
# step through code, & evaluate expressions at runtime


def generate_parameter_combinations(parameters):
    """
    Generates all combinations of given parameter values. Computes the Cartesian 
    product (yields all possible combinations) of values across all parameters.
    
    Parameters:
    parameters (dict): dictionary where each key is a parameter name & the value 
    is a list of values for the parameter.
    
    Returns a list of tuples, where each tuple is a unique combination of 
    parameter values.
    """
    
    parameters.values()
    param_values = [values for values in parameters.values()]
    param_values
    # Extract vals for ea param in `parameters` dict.
    # Make list of lists, where ea inner list contains vals for 1 param.
    
    
    print(*param_values)
    itertools.product(*param_values)
    list(itertools.product(*param_values))
    
    combinations = list(itertools.product(*param_values))
    combinations
    # Compute Cartesian product (all possible combinations) of param vals.
    # Result is list of tuples- ea tuple is a unique combination of param vals.
    
    
    return combinations


def write_combinations_to_csv(parameters, combinations, csv_file_path):
    """
    Writes parameter sets (combinations of parameter values) to a CSV file.
    
    Takes a list of parameter sets & a file path, & writes a CSV file, where 
    each row is a unique parameter set. For each row, the first column is a 
    number - a unique identifier ('Param_Set_ID') for that parameter set.
    
    Parameters:
    - parameters: dictionary where each key is a parameter name, used to 
    generate column headers for the CSV file
    - combinations: list of tuples, where each tuple is a set of parameter values
    - csv_file_path (str): path to the CSV file to be written.
    """
    
    with open(csv_file_path, 'w', newline='') as file:
    # Open CSV file in write mode ('w'). If file exists, it'll be overwritten; 
    # if it doesn't, it'll be made.
    # `with` statement automatically handles closing file once code block is 
    # exited, even if exceptions (errors) occur.
    # This simplifies code & makes it more robust by eliminating need for 
    # explicit `file.close()` calls, reducing risk of leaving files open & 
    # causing resource leaks.
        
        writer = csv.writer(file)
        # Make instance of `csv.writer` class (instantiate/make `csv.writer` 
        # obj) to handle CSV operations on an opened file.
        
        headers = ['Param_Set_ID', 'Sel_Coeff_ID'] + list(parameters.keys())
        # Define list to hold col headers (header row) for CSV.
        # Result is 1 list starting w/ 'Param_Set_ID' & 'Sel_Coeff_ID', followed 
        # by param names.
        
        writer.writerow(headers)
        # `writer.writerow()` method writes 1 row to CSV file- write col headers- 
        # param names, w/ 2 extra cols 'Param_Set_ID' & 'Sel_Coeff_ID' at start.
        
        for count, combination in enumerate(combinations, start=1):
        # Use `enumerate()` to loop over `combinations` w/ a counter starting at 1.
        # `combinations` is list of tuples, where ea tuple is set of param vals.
            
            # pdb.set_trace()
            
            sel_coeff_values = combination[list(parameters.keys()).index('SELRANGE')]
            # Extract selection coefficient (SELRANGE) vals from current param set.
            
            sel_coeff_ID = sel_coeff_values.replace(' ', '_')
            # Make unique identifier for selection coefficient vals used in 
            # param set / experimental run.
            # Val of `sel_coeff_values` is str like '0 300 300'.
            # Replace all spaces in str `sel_coeff_values` w/ underscore, 
            # producing format '0_300_300'.
            
            # Later in workflow, we use ANOVA as part of power analysis to 
            # assess impact of sim params (used to generate synthetic training 
            # data) on model performance.
            # Our examination focused on how variations in training datasets 
            # (representing different evolutionary scenarios) affect predictive accuracy.
            
            # In context of this workflow, 'one experimental run' (observation) 
            # refers to executing a set of sims using 1 set of param vals & 
            # training 1 model.
            # Sel coeff is target var for NNs (var we train NNs to predict).
            # So, this param inherently comprises multiple vals within single 
            # experimental run, unlike other sim params.
            # This poses challenge in context of ANOVA.
            
            # For ANOVA, we treat sel coeff as single factor.
            # This is to streamline investigation of its & other params' 
            # influence on NN's predictive accuracy.
            # The approach accomodates, for ea observation, only 1 val per factor.
            # So, for stat analysis, we condense & encode sel coeff classes into 
            # distinct, non-overlapping categories (a single categorical unit).
            # In this encoding scheme, ea unique identifier, like '0_400' or 
            # '200_400', represents combination of sel coeff classes (in bin 
            # classification) or min & max limits of a val range (regr model).
            
            # We make col in CSV file for these identifiers.
            
            
            row = [count, sel_coeff_ID] + list(combination)
            writer.writerow(row)
            # Write row to CSV- row contains nr (current counter val, `count`) 
            # & 1 set of param values.
            # Counter val serves as sequential identifier for ea set of param 
            # vals (row in CSV). This helps keep track of ea param set & make 
            # data organised.


def main(parameters, analysis_version):
    """
    Orchestrates execution of the script's primary task.
    
    Parameters:
    - parameters (dict): dictionary where each key is a parameter name & the 
    value is a list of values for the parameter
    - analysis_version (str): version number of the analysis, used to construct 
    file paths.
    """
    
    # pdb.set_trace()
    # debugger entry point
    # When you run this fn, execution will pause at `pdb.set_trace()` & you'll 
    # enter interactive debugging mode. You can then inspect variables, step 
    # through code, & evaluate expressions to understand state of program.
    # Use commands like `n` (next), `c` (continue), `l` (list), `p` (print), & 
    # `q` (quit) within debugger.
    
    combinations = generate_parameter_combinations(parameters)
    # Generate all combinations of given parameter values.
    
    os.makedirs(analysis_version, exist_ok=True)
    # Make dir if it doesn't exist.
    # `os.makedirs` fn in `os` module recursively creates a dir & any missing 
    # intermediate dirs in specified path.
    # `exist_ok=True` keyword arg tells `os.makedirs()` to do nothing if dir 
    # already exists, preventing any deletion/modification of existing data.
    
    csv_file_path = os.path.join(analysis_version, 'Parameter_Combinations.csv')
    # Construct full path to CSV file by concatenating analysis version dir name 
    # w/ CSV file name.
    
    write_combinations_to_csv(parameters, combinations, csv_file_path)
    # Write param sets to CSV file.


if __name__ == '__main__':
# Check if script is executed as standalone (main) program & call main fn if `True`.
    
    
    # Make a dict to store sim params. Keys are param names; values are lists of 
    # values for ea param.
    # Ea item in dict is key-value pair: key- unique identifier; value- data 
    # associated w/ key.
    parameters = {
        
        'SELRANGE': ['0 300 300', '0 20 20'],
        # In context of this workflow, 'one run' refers to executing a set of 
        # sims using 1 set of param vals.
        # But, for selection coefficient (SELRANGE), we simulate multiple vals 
        # or classes in 1 run.
        # Aim of running sims is to train ML model to predict selection 
        # coefficient & this necessitates exposing model to various selection 
        # coefficients (to enhance its predictive capability & robustness).
        # Code that runs sims specifies vals of selection coefficient in 
        # specific format. An annotated excerpt from code explains format:
        # ```
        # SELRANGE=`seq {SELRANGE}`
        # # Execute cmd in backticks & assign its output to `SELRANGE` var.
        # # `seq FIRST INCREMENT LAST`- cmd used in Unix-like systems- generates 
        # # sequence of nrs:
        # # `FIRST`- sequence's start nr
        # # `INCREMENT` (optional)- increment step. If not specified, it 
        # # defaults to 1.
        # # `LAST`- end nr.
        # # Eg, `seq 0 300 300` generates sequence from 0 to 300, w/ a step of 
        # # 300. In this case, it's just 2 vals: 0 & 300.
        # ```
        
        'TIMERANGE': ['800/40000', '2000/40000', '200/40000'],
        # time of selection event, scaled to 4N_e generations ago
        
        'LEN': [80000] # length of genomic locus in base pairs (bp)
        # length of DNA sequence (genomic locus) being simulated
        # unit: base pairs (bp)
        
        # Add new parameters here as needed.
    }


    analysis_version = 'Version1'
    # Manage versions- set up directory in which to save CSV file.
    # Define var- label for current version of analysis.
    # Var ensures ea version of analysis is stored separately, maintaining clear 
    # historical record of sims.
    # Var is used to make distinct dirs for ea version, preventing data overlap 
    # & facilitating clean, organised structure for storing sim data.
    # Manually update var if want to generate new CSV (eg w/ different params / 
    # param vals- for new version of analysis) / param files / sim data & don't 
    # want to overwrite old data.
    # [
    # Though automation is valuable, manual labeling is simple.
    # Script is part of bigger workflow & simplicity keeps overall workflow easy 
    # to manage & straightforward (avoids need for additional logic to handle 
    # automatic versioning).
    # ]
    
    main(parameters, analysis_version)
