#!/Users/cpenning/anaconda3/bin/python

"""
Generates a .txt file for each set of simulation-parameter values.

Inputs:
- template of the input .txt file for the 'generate_dataset.sh' script - the 
script to run simulations
- CSV file of sets of parameter values.
Using these, the script makes copies of the template file, but with specific 
parameter values edited.

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
__version__ = '0.0.7' # 2024 Feb 7

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

import pdb
# interactive debugger module- allows you to pause execution, inspect variables, 
# step through code, & evaluate expressions at runtime


def generate_parameter_files(output_dir, csv_file_path, template_file_name):
    """
    Generates a .txt file for each set of parameter values.
    
    Reads each row from the provided CSV file & uses row values to replace 
    placeholders in a template .txt file. It makes a unique .txt file for each 
    row. It uses the 'Param_Set_ID' col in the CSV file for file naming & 
    directory organisation.
    
    Parameters:
    - csv_file_path (str): path to CSV file - each row is a unique parameter set
    - template_file_name (str): path to template .txt file, containing 
    placeholders for parameter values
    - output_dir (str): directory in which to save parameter files.
    """
    
    os.makedirs(output_dir, exist_ok=True)
    # Make dir if it doesn't exist.
    # `os.makedirs` fn in `os` module recursively creates a dir & any missing 
    # intermediate dirs in specified path.
    # `exist_ok=True` keyword arg tells `os.makedirs()` to do nothing if dir 
    # already exists, preventing any deletion/modification of existing data.
    
    with open(csv_file_path, newline='') as csv_file:
    # Open CSV file- opened in read mode by default (as haven't specified mode 
    # like `'r'` or `'w'`).
    # `newline=''` arg tells Python to keep newline chars as they are & not 
    # automatically convert them into platform-specific line endings.
    # Ensures newline chars are interpreted correctly, regardless of OS.
        
        reader = csv.DictReader(csv_file)
        # Make instance of `csv.DictReader` class (make `csv.DictReader` obj)- 
        # obj designed to read CSV files in dict-like format.
        # `reader` obj reads file line by line & returns ea row as dict.
        # Dict keys are col headers from 1st row & vals are data in ea cell of 
        # current row.
        
        with open(template_file_name, 'r') as file: # Open template file in read mode.
            template_content = file.read() # Read file's entire content into 1 str.
        
        #-----
        # Replace placeholders w/ vals from CSV row.
        #-----
        for row in reader:
        # Loop over ea row in CSV file (ea dict in `reader`).
        # `row`- dict where ea key is col name in CSV file & corresponding val 
        # is data for that col in current row.
            
            modified_content = template_content
            # Initialise var- copy content of template file (`template_content`). 
            # We'll modify this copy, keeping original template unchanged for 
            # subsequent iterations.
            
            for key, value in row.items():
            # Loop over ea col (key-value pair) in current row (dict). `key` is 
            # col name, `value` is data for that col in this row.
                
                if key not in ['Param_Set_ID', 'Sel_Coeff_ID']:
                # Check whether `key` var does not match any element in list 
                # ['Param_Set_ID', 'Sel_Coeff_ID'].
                # Check if current col is not 'Param_Set_ID' or 'Sel_Coeff_ID'- 
                # skip these cols, as they're not used to replace placeholders 
                # in template.
                # For each row, the first column is a number - a unique 
                # identifier ('Param_Set_ID') for that parameter set.
                # 2nd col ('Sel_Coeff_ID') contains unique label for set of 
                # selection coefficients used in one run.
                # [
                # Sel coeff is target var for NNs (var we train NNs to predict).
                # So, this param inherently comprises multiple vals within 
                # single experimental run, unlike other sim params.
                # Ea unique identifier, like '0_400' or '200_400', represents 
                # combination of sel coeff classes (in bin classification) or 
                # min & max limits of a val range (regr model).
                # ]
                    
                    placeholder = f'{{{key}}}'
                    # `f'{{{key}}}'`- use f-string to make str matching 
                    # placeholder, eg '{SELRANGE}'. Need 3 braces as 1 brace 
                    # used for formatting in f-strings- to inc literal brace, 
                    # need to double it.
                    
                    modified_content = modified_content.replace(placeholder, value)
                    # Replace placeholder in `modified_content` w/ actual val 
                    # from CSV. This customises template file w/ specific param 
                    # vals for current row.
            
            
            #-----
            # Make new param file for ea row.
            #-----
            new_file_name = f'Parameters{row["Param_Set_ID"]}.txt'
            # Use f-string to make str for new file name. f-string allows for 
            # dynamic insertion of var into string.
            # `row`- dict where ea key is col name in CSV file & corresponding 
            # val is data for that col in current row.
            # For each row, the first column is a number - a unique identifier 
            # ('Param_Set_ID') for that parameter set.
            # `row["Param_Set_ID"]` accesses val associated w/ 'Param_Set_ID' key.
            # Insert val in file name, resulting in file name like 'Parameters1.txt'.
            
            with open(os.path.join(output_dir, new_file_name), 'w') as new_file:
            # Construct path to where we save param file by concatenating 
            # `output_dir` &`new_file_name`.
            # Open new file in write mode.
                
                new_file.write(modified_content)
                # Write `modified_content` str to file.
                # `modified_content` contains updated template text & it's 
                # saved in new file.


def main(analysis_version, template_file_name):
    """
    Orchestrates execution of the script's primary task.
    
    Parameters:
    - analysis_version (str): version number of the analysis, used to construct 
    file paths
    - template_file_name (str): path to template .txt file, containing 
    placeholders for parameter values.
    """
    
    output_dir = os.path.join(analysis_version, 'Parameter_Files')
    # Specify directory in which to save parameter files- in my case, subdir of 
    # analysis version dir.
    
    csv_file_path = os.path.join(analysis_version, 'Parameter_Combinations.csv')
    # path to CSV file
    
    generate_parameter_files(
        output_dir=output_dir,
        csv_file_path=csv_file_path,
        template_file_name=template_file_name
    )
    # Call `generate_parameter_files()` fn- Generates a .txt file for each set 
    # of parameter values.

if __name__ == '__main__':
# Check if script is executed as standalone (main) program & call main fn if `True`.
    
    analysis_version = 'Version1'
    template_file_name = 'Template_Parameters_Binary.txt'
    # Specify version nr of analysis & path to template .txt file, containing 
    # placeholders for parameter values.
    # Adjust as necessary.
    
    main(analysis_version, template_file_name)
    # Run main fn w/ specified version nr & template file path.
