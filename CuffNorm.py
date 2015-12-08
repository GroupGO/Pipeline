#!/usr/bin/env python


"""
Author: Henry Ehlers, Samin Hosseini
WUR_Number: 921013218060

A script designed to run the command line tool cuffdiff.
    inputs:     -reference annotation file
                -output folder path
                -overwrite option [True/False]
                -sorted sam files

In order to provide readable and understandable code, the right indentation margin has been
increased from 79 to 99 characters, which remains in line with Python-Style-Recommendation (
https://www.python.org/dev/peps/pep-0008/) .This allows for longer, more descriptive variable
and function names, as well as more extensive doc-strings.
"""


import subprocess
import sys
import os


def execute_on_command_line(cmd_string):
    """
    Method to parse a formatted string to the command line and execute it.

    :param cmd_string: The formatted string to be executed.
    """
    assert isinstance(cmd_string, str), 'Command Line String must be of type string.'
    subprocess.check_call(cmd_string, shell=True)


def get_command_line_arguments(default_variable_values):
    """
    Function to get a variable number of input arguments from the command line, but use default
    values if none were given.

    :param default_variable_values: A list of default values given in order of their appearance in
    the command line.
    :return: A list of input variables.
    """
    assert isinstance(default_variable_values, list), \
        'The given default input variables values must be a list.'
    input_variables = [0]*len(default_variable_values)
    for index, default_value in enumerate(default_variable_values):
        try:
            input_variables[index] = sys.argv[index + 1]
        except IndexError:
            if default_value != '':
                input_variables[index] = default_value
            else:
                exit('Not enough command line input arguments. Critical Input Missing.')
    return input_variables


def get_variable_command_line_arguments(start_index):
    """
    Function to return a variable number of input arguments from the command line as of a
    certain index.

    :param start_index: The index of the first variable input argument on the command line.
    :return: A list of the parsed command line arguments.
    """
    variable_inputs = ['']*(len(sys.argv[:]) - start_index)
    for index, argument in enumerate(sys.argv[start_index:len(sys.argv)]):
        variable_inputs[index] = argument
    return variable_inputs


def run_cuff_norm(transcripts, sorted_sam_paths, output_path, overwrite=False):
    """
    Method to run Cuffnorm on command line.

    :param transcripts:
    :param sorted_sam_paths:
    :param output_path:
    :return:
    """
    if not os.path.exists(output_path) or overwrite:
        cmd = 'cuffnorm -p 4 -o %s %s ' % (output_path, transcripts)
        for sam_file in sorted_sam_paths:
            cmd += '%s ' % sam_file
        execute_on_command_line(cmd)


def main():
    """
    Method designed to run the command line tool cuffnorm.
    """
    transcripts, output_folder_path, overwrite = get_command_line_arguments(['']*3)
    sorted_sam_paths = get_variable_command_line_arguments(4)
    assert os.path.exists(transcripts), 'Transcripts file path "%s" does not exist.' % transcripts
    assert os.path.exists(output_folder_path), 'Folder "%s" does not exist.' % output_folder_path
    for sam_file in sorted_sam_paths:
        assert os.path.exists(sam_file), 'SAM file path "%s" no found.' % sam_file
    run_cuff_norm(transcripts, sorted_sam_paths, output_folder_path, overwrite)


if __name__ == '__main__':
    main()
