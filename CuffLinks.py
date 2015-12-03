#!/usr/bin/env python


"""
Author: Henry Ehlers, Samin Hosseini
WUR_Number: 921013218060

A script designed to run the command line tool cufflinks.
    inputs:     -sorted sam file
                -reference annotation file
                -output folder path
                -overwrite option [True/False]

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


def run_cuff_links(sam_sorted_path, annotation, cuff_links_output, overwrite=False):
    """
    Method for running Cufflinks on the command line using the provided input arguments.

    :param sam_sorted_path: Path leading to the sorted sam file to be run through cufflinks,
    given as a string.
    :param annotation: Path leading to the reference annotation gtf/gff file to be run through
    cufflinks, given as a string.
    :param cuff_links_output: Path leading to the desired folder to contain the cufflinks output.
    """
    if not os.path.exists(cuff_links_output) or overwrite:
        print('Running Cufflinks on %s.' % sam_sorted_path)
        cmd = 'cufflinks -p 4 %s -g %s -o %s' % (sam_sorted_path, annotation, cuff_links_output)
        execute_on_command_line(cmd)
        print('Saved SAM output to %s' % cuff_links_output)
    else:
        print('Directory %s already there. Not overwritten.' % cuff_links_output)


def main():
    """
    Method designed to run the command line tool cufflinks.
    """
    sorted_sam_path, annotation, output_folder_path, overwrite = \
        get_command_line_arguments(['', '', '', False])
    assert os.path.exists(sorted_sam_path), 'Directory to Sorted Sam file does not exist.'
    assert os.path.exists(annotation), 'Directory to Annotation file does not exist.'
    run_cuff_links(sorted_sam_path, annotation, output_folder_path, overwrite)


if __name__ == '__main__':
    main()
