#!/Users/cpenning/anaconda3/bin/python

"""
Generates a JSON configuration file for each experimental run.

Each configuration file is a JSON object containing details/metadata about a 
run. The files are named based on a unique, sequential run number, aligning with 
PBS array job indices for parallel processing on a high-performance computing 
cluster. The script supports any number of parameter sets & any number of 
replicates per parameter set by dynamically calculating run numbers and 
generating corresponding configuration files.

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
__version__ = '0.0.3' # 2024 Feb 7

#-----
# Imports
#-----
# Standard-Library Imports
import os
# Module provides way to use functionality dependent on operating system. 
# Incs fns to interact w file system in platform-independent way.

import json # module for working w/ JSON data

import pdb
# interactive debugger module- allows you to pause execution, inspect variables, 
# step through code, & evaluate expressions at runtime


def generate_config_files(nr_param_sets, nr_replicates, param_files_dir, 
                          config_files_dir):
    """
    Generates a JSON configuration file for each experimental run.
    
    Each configuration file is a JSON object containing details/metadata about a
      run, including:
    - parameter set ID (a unique identifier for the parameter set used in this 
    set of simulations)
    - relative path to the parameter file used in this set of simulations
    - replicate number
    - directory structure `[version number of analysis]/Param_Set[ID]/Replicate[number]`, 
    integral to both `../Data/` & `../Results/` directories. This is used, for 
    each run, to locate & access output data of simulations & save analysis results.
    This makes a record to link parameter sets to outputs, streamlining data 
    management. The files are named `config{run_nr}.json`, where `run_nr` is a 
    unique, sequential identifier for each experimental run (job).
    
    Parameters:
    - nr_param_sets (int): total number of parameter sets
    - nr_replicates (int): number of replicates per parameter set (determines 
    how many configuration files will be created for each parameter set)
    - param_files_dir (str): directory where parameter files are stored
    - config_files_dir (str): directory in which to save configuration files.
    """
    
    for param_set_index in range(1, nr_param_sets + 1):
    # Iterate from 1 to `nr_param_sets` inclusive to align w/ param set 
    # numbering starting at 1.
    # `range()` fn generates nrs up to, but not including, `stop` val.
    # `range(1, nr_param_sets + 1)` generates nrs starting from 1 to 
    # `nr_param_sets`, inclusive of 1 & exclusive of `nr_param_sets + 1`.
    # `stop` arg is `nr_param_sets + 1`: `+ 1` ensures `range()` fn & loop inc 
    # last param set in sequence it generates.
        
        for replicate_index in range(1, nr_replicates + 1):
        # Iterate from 1 to `nr_replicates` inclusive to align w/ replicate 
        # numbering starting at 1.
            
            run_nr = ((param_set_index - 1) * nr_replicates) + replicate_index
            # We assign ea experimental run (job) a unique, sequential 
            # identifier (run nr).
            # Formula is designed to be universal & robust for calculating run 
            # nrs across any nr of param sets & any nr of replicates per param 
            # set (w/ assumption that count starts at 1 for both param sets & 
            # replicates).
            # Numbering starting at 1 aligns w/ `PBS_ARRAY_INDEX` env var 
            # provided by PBS job scheduler when running parallel jobs on HPC cluster.
            
            param_file_name = f'Parameters{param_set_index}.txt'
            # Use f-string to make str for param file name.
            # f-string allows for dynamic insertion of var into str (inclusion 
            # of `param_set_index` var directly in str, forming dynamic str).
            
            param_file_path = os.path.join(param_files_dir, param_file_name)
            # Construct path to param file.
            
            run_output_dir = os.path.join(f'Param_Set{param_set_index}', 
                                          f'Replicate{replicate_index}')
            # Construct path to / define run_output_dir.
            
            
            # Make dict to store details of ea run (ea replicate set of sims).
            # Ea key represents specific detail about run & key val is assigned 
            # from corresponding var's val.
            # Makes record to link parameter sets to outputs, streamlining data management.
            
            config_data = {
                "param_set_ID": param_set_index,
                # Key "param_set_ID" stores a unique identifier for the 
                # parameter set used in this set of simulations.
                
                "param_file_name": param_file_name,
                "param_file_path": param_file_path,
                # relative path to the parameter file used in this set of simulations
                # Param file contains all settings & vals used to configure sims.
                # Storing filename allows for easy reference & traceability of 
                # sim settings.
                
                "replicate_nr": replicate_index, # replicate nr
                
                "run_output_dir": run_output_dir
                # directory structure `[version number of analysis]/Param_Set[ID]/Replicate[number]`, 
                # integral to both `../Data/` & `../Results/` directories. This 
                # is used, for each run, to locate & access output data of 
                # simulations & save analysis results.
            }
            
            config_file_name = f'config{run_nr}.json'
            config_file_path = os.path.join(config_files_dir, config_file_name)
            # Specify config file name, using f-string to embed run nr.
            # Construct path to config file.
            
            with open(config_file_path, 'w') as config_file:
            # Open config file in write mode.
                
                json.dump(config_data, config_file, indent=4)
                # Write config data to file in JSON format.
                # `indent=4` arg formats JSON data in file for easy readability, 
                # using 4-space indent.
            
            print(f'Generated {config_file_name}')
            # `print()` fn outputs specified message to the console.
            # Indicates config file has been generated.
            # Provides feedback to track script execution & output files.


def main(analysis_version, nr_param_sets, nr_replicates):
    """
    Orchestrates execution of the script's primary task.
    
    Parameters:
    - analysis_version (str): version number of the analysis, used to construct 
    dir paths
    - nr_param_sets (int): total number of parameter sets
    - nr_replicates (int): number of replicates per parameter set (determines 
    how many configuration files will be created for each parameter set).
    """
    
    param_files_dir = 'Parameter_Files'
    # Specify directory where parameter files are stored.
    
    config_files_dir = os.path.join(analysis_version, 'Config_Files')
    # directory in which to save configuration files- in my case, subdir of 
    # analysis version dir
    
    os.makedirs(config_files_dir, exist_ok=True)
    # Make dir if it doesn't exist.
    # Analysis version dir already exists- previous script in workflow made it.
    # `os.makedirs` fn in `os` module recursively creates a dir & any missing 
    # intermediate dirs in specified path.
    # `exist_ok=True` keyword arg tells `os.makedirs()` to do nothing if dir 
    # already exists, preventing any deletion/modification of existing data.
    # `os.makedirs(config_dir, exist_ok=True)` makes specified dir within 
    # analysis version dir & won't overwrite any existing data in analysis 
    # version dir (inc .txt parameter files).
    
    generate_config_files(nr_param_sets, nr_replicates, param_files_dir, config_files_dir)
    # Call `generate_config_files` fn- Generates a JSON configuration file for 
    # each experimental run.


if __name__ == "__main__":
# Check if script is executed as standalone (main) program & call main fn if `True`.
    
    analysis_version = 'Version1'
    nr_param_sets = 6
    nr_replicates = 2
    # Specify version nr of analysis, nr of param sets, & nr of replicates per 
    # param set.
    # Adjust as necessary.
    
    main(analysis_version, nr_param_sets, nr_replicates)
    # Run main fn w/ specified args.
