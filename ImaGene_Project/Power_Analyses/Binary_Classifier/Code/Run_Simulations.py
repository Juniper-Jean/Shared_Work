#!/Users/cpenning/anaconda3/bin/python

"""
Runs a set of (many) genetic simulations using parameter values specified in a 
.txt file. Saves the output data of simulations in a specified output directory. 
The simulations generate synthetic genetic data used later in the workflow to 
train a machine-learning model.

The `main` function:
- Takes as input a run number - a unique, sequential identifier for each 
experimental run (set of simulations).
- Retrieves a JSON configuration file corresponding to the current run number. 
This contains details/metadata about the run, e.g., parameters & output 
directory (a record to link parameter sets to outputs).
- Retrieves the parameter file path & output directory for the run from the 
configuration file.

When run as a standalone program, this script:
- Runs multiple sets of simulations, each set sequentially, one after the other.
- Organises output data into a structured directory format, separating 
simulations by parameter set ID & replicate number.

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
__version__ = '0.0.3' # 2024 Feb 6

#-----
# Imports
#-----
# Standard-Library Imports
import subprocess
# module to run commands external to Python, like you would in terminal

import os
# Module provides way to use functionality dependent on operating system. 
# Incs fns to interact w file system in platform-independent way.

import json # module for working w/ JSON data

import pdb
# interactive debugger module- allows you to pause execution, inspect variables, 
# step through code, & evaluate expressions at runtime

import time
# module provides fns for working w/ times & dates
# It's essential for measuring performance / execution time, as it allows us to 
# capture precise time pts before & after code execution.


def run_simulations(param_file_path, output_dir):
    """
    Runs a set of simulations using the given parameter file. Saves the 
    simulation data in the specified output directory.
    """
    
    cmd = ['bash', 'generate_dataset.sh', param_file_path, output_dir]
    subprocess.call(cmd)
    # Execute shell cmd from within Python- run 'generate_dataset.sh' shell script.
    # When you use `subprocess.call()`, you must pass cmd & args as list- ea 
    # item in list is 1 part of cmd.
    
    # 'Generate_Dataset.sh' generates (synthetic) data - it runs a set of many 
    # simulations using MSMS (a simulator, 
    # https://www.mabs.at/publications/software-msms/)
    # The script takes two arguments: an input .txt file specifying the 
    # simulations' parameters, & a directory path in which to save simulation outputs.
    # It splits simulations into batches, so, later, we can train a neural 
    # network with a 'simulation-on-the-fly' approach.


def main(analysis_version, run_nr):
    """
    Orchestrates execution of the script's primary task.
    
    Parameters:
    - analysis_version (str): version number of the analysis, used to construct 
    dir paths
    - run_nr (int): unique, sequential identifier for each experimental run (job).
    """
    
    print(f"Running simulations for run number: {run_nr}")
    # Output specified message to the console.
    # Use f-string to dynamically insert `run_nr` var into str.
    # Provides feedback about which run is currently in progress.
    # Gives user way to track progress of sims when running multiple sets of sims sequentially.
    
    config_file_path = os.path.join(analysis_version, 'Config_Files', 
                                    f'config{run_nr}.json')
    # Construct path to config file for current run nr.
    # Combine analysis version dir name, 'Config_Files' subdir, & config file 
    # name to dynamically generate path.
    # Use f-string to dynamically insert `run_nr` var into filename & access 
    # config file corresponding to current run nr.
    
    with open(config_file_path, 'r') as file:
    # Load config data- open config file in read mode.
        
        config_data = json.load(file)
        # Read JSON content from file & convert it into Python dict.
    
    
    param_file_path = os.path.join(analysis_version, config_data["param_file_path"])
    # Construct path to param file for current sim set.
    # In my case, `config_data["param_file_path"]` ("param_file_path" key in 
    # `config_data` dict) contains 2 parts: name of dir holding all param files 
    # ('Parameter_Files') & specific param file name for this sim set. This dir 
    # is located within analysis version dir, which itself is in the working dir.
    # `config_data` dict contains details/metadata about the run, e.g., 
    # parameters & output directory.
    # Param file contains all settings & vals used to configure sims.
    
    # [
    # # JSON Format
    # JSON obj (enclosed in curly braces `{}`): collection of key-val pairs. 
    # Keys are always strings, while vals can be various types: strings, nrs, 
    # arrays, or even other objs.
    # Array (enclosed in square brackets `[]`): ordered sequence of elements. 
    # Elements can be strings, nrs, arrays, objs, etc.
    
    # # Conversion to Python Data Structs
    # `json.load(file_object)` fn reads JSON data from file & converts it into 
    # Python obj- either dict or list, depending on structure of data.
    # JSON obj (enclosed in curly braces `{}`) becomes Python dict. Python dicts 
    # also consist of key-val pairs (unlike JSON, keys can be various types, not 
    # just strings).
    # JSON array (enclosed in square brackets `[]`) becomes Python list. Python 
    # list is ordered sequence of elements, where the elements can be of 
    # different types (mirrors concept of JSON array).
    # Params: `file_object`: file obj opened in read mode pointing to JSON file
    
    # # Provided JSON File
    # Composed of a single obj (set of key-val pairs enclosed in curly braces 
    # `{}`) containing details/metadata about a run.
    # Ea key represents specific detail about run.
    
    # # Python Representation of Provided JSON File
    # In Python, `config_data` is dict representing JSON file's obj.
    # `config_data["param_file_path"]`- "param_file_path" key in `config_data` dict
    # ]
    
    
    run_output_dir = os.path.join('..', 'Data', analysis_version, 
                                  config_data["run_output_dir"])
    # Construct path to dir in which to save output data of sims (current 
    # set/run of sims).
    # Combine: relative path to move up 1 dir ('..'), then down into 'Data' dir, 
    # followed by analysis version dir name.
    # Finally, append the run-specific output dir path stored in 
    # "run_output_dir" key in `config_data` dict.
    # "run_output_dir" val follows format `Param_Set[ID]/Replicate[number]`.
    
    os.makedirs(run_output_dir, exist_ok=True)
    # Make dir if it doesn't exist.
    # `os.makedirs` fn in `os` module recursively creates a dir & any missing 
    # intermediate dirs in specified path.
    # `exist_ok=True` keyword arg tells `os.makedirs()` to do nothing if dir 
    # already exists, preventing any deletion/modification of existing data.
    
    run_simulations(param_file_path, run_output_dir)
    # Call `run_simulations` fn: Runs a set of simulations using the given 
    # parameter file. Saves the simulation data in the specified output directory.


if __name__ == '__main__':
# Check if script is executed as standalone (main) program & call main fn if `True`.
    
    start_time = time.time()
    # start time
    # `time.time()` fn returns current time in seconds since the Epoch (January 1, 1970, 00:00:00 UTC).
    # We'll use this to calculate script's total execution time by subtracting 
    # it from end time.
    # Consider running code multiple times & averaging results to get more 
    # stable measure (variability in execution time can be due to many factors 
    # like background processes & system load).

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
        # f-string dynamically inserts run nr (`i`) & calculates execution time 
        # by subtracting `run_start_time` from `run_end_time`.
        # This helps track progress & performance.
    
    end_time = time.time() # end time
    print(f'Total execution time: {end_time - start_time:.2f} s')
    # Subtract `start_time` from `end_time` to get duration of script execution in s.
    # Output duration to the console- show how long script took to run in total.
    # When use f-string, Python evaluates expression inside braces & converts 
    # result to a str, embedding it into the surrounding text.
    # `:.2f`: a format specifier (syntax is specific to f-strings). Formats 
    # resulting floating-point nr to 2 decimal places for readability.
    
# Code within `if __name__ == "__main__":` block executes script's main task 
# in sequential manner for specified nr of runs.
# This is suitable for running on a local computer (as opposed to parallel 
# execution of task on high-performance computing cluster).
# It runs multiple sets of sims, ea set sequentially, one after the other.
# Additionally, the dunder name main check enables us to execute script as 
# standalone (main) program. This allows us to prototype/test individual 
# components of workflow in isolation (for development purposes), ensuring 
# they work as expected before integrating them into bigger workflow.
