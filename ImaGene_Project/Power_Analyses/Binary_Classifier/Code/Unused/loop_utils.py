# Shebang line isn't necessary for Python module. It's primarily used in standalone scripts to indicate which interpreter should be used when script is run directly from cmd line.

"""
This module aids in processing & analysing multiple sets of simulation data. It includes functionality to loop over directories, each containing a set of simulation data. It enables repeated application of specific functions across various datasets.
"""

__author__ = 'cpenning@ic.ac.uk'
__version__ = '0.0.1' # 2024 Jan 6

#-----
# Imports
#-----
# Standard-Library Imports
import json  # module for working w/ JSON data


def iterate_dirs(config_file, task_function, **kwargs):
    """
    Iterates over directory paths specified in a JSON configuration file & applies a given function to data in each directory.

    Reads a JSON configuration file & iterates over each entry. Each entry contains details about 1 set of simulations, including the parameter set ID, the relative path to the parameter file used, the replicate number, and the directory where the output data of simulations is stored. For each entry, the function:
    - extracts the directory path where the simulation data is stored
    - calls the given task_function, passing the directory path & any additional keyword arguments.

    Parameters:
    - config_file_path (str): path to the JSON configuration file
    - task_function (function): function to be applied to ea set of simulation data. This function should accept a directory path as its main argument.
    - **kwargs: additional keyword arguments to be passed to `task_function`.

    The configuration file is expected to be in the following format:
    {
    "simulations": [
        {
            "output_dir": "path/to/simulation/output"
            // Additional simulation details...
        },
        // More simulation entries...
    ]
    }

    Example:
    ```
    def process_data(directory_path): # Function to process data in the given directory
    pass

    iterate_over_dirs('config.json', process_data, additional_param1=value1, additional_param2=value2)
    ```

    The `process_data` function will be called for each simulation directory, & `additional_param1` & `additional_param2` will be passed as keyword arguments.
    """
    
    with open(config_file, 'r') as file:
    # Open config file in read mode.
        
        config_data = json.load(file)
        # Read JSON content from file & convert it into Python dict.

        for simulation in config_data["simulations"]:
        # Access val associated w/ "simulations" key in `config_data` dict.
        # `config_data["simulations"]` ("simulations" key in dict) is list of dicts.
        # Loop over ea entry (dict) in "simulations" list.
            
            data_dir = simulation["output_dir"]
            # For ea dict, access val linked to "output_dir" key.
            # "output_dir" key stores path to output data of sims.
            # Path is stored as str in JSON file & remains str in Python- var `data_dir` holds this str.

            task_function(data_dir, **kwargs)
            # Call task-specific fn w/ path to sim data & any additional args.

            # [
            # # Nomenclature
            # Fn params: vars listed in fn definition- names & placeholders for vals (args) fn can accept. Params define data type fn expects.

            # Args: actual vals passed to fn when it's called (actual data passed to fn params). You can pass args as positional or keyword args.
            # Eg, in `func(1, 2)`, `1` & `2` are positional args.

            # Keyword args:
            # In fn call, keyword args allow you to specify args by naming corresponding params- to pass vals w/ key-val syntax.
            # This enhances readability & removes dependency on arg order.
            # Eg, `func(a=1, b=2)` uses keyword args.
            # You're not passing dict; you're just explicitly stating which param ea arg corresponds to.
            # Inside `func()`, `a` & `b` are treated as normal vars w/ vals 1 & 2.


            # # `**kwargs` Syntax in Fn Definitions
            # `**kwargs` syntax in fn param list allows fn to accept variable-length list of keyword args.
            # `kwargs` is dict that stores keyword args names as keys & their corresponding vals.

            # Eg, in fn defined as `def func(**kwargs):`, you can call `func(a=1, b=2, c=3)`.
            # Inside `func()`, `kwargs` is dict `{'a': 1, 'b': 2, 'c': 3}`. 
            # ```
            # def func(**kwargs):
            #     for key, value in kwargs.items():
            #         print(f"{key}: {value}")
            # ```
            # You can pass any nr of keyword args to `func()` & it'll iterate through them & print their names & vals.
            # This feature provides great flexibility.
            # ]
