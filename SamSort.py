#!/usr/bin/env python


"""
Author: Henry Ehlers
WUR_Number: 921013218060

A script designed to sort a given SAM file and save it to a BAM file.
    inputs:     -sam file directory
                -sorted sam file directory
                -overwrite

In order to provide readable and understandable code, the right indentation margin has been
increased from 79 to 99 characters, which remains in line with Python-Style-Recommendation (
https://www.python.org/dev/peps/pep-0008/) .This allows for longer, more descriptive variable
and function names, as well as more extensive doc-strings.
"""


import subprocess
import sys
import os
import re


def execute_on_command_line(cmd_string):
    """
    Method to parse a formatted string to the command line and execute it.

    :param cmd_string: The formatted string to be executed.
    """
    assert isinstance(cmd_string, str), 'Command Line String must be of type string.'
    exit_code = subprocess.check_call(cmd_string, shell=True)
    if exit_code != 0:
        exit('Critical Command Line Error: %s' % cmd_string)


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


def sort_sam(sam_file_path, overwrite=False):
    """
    Method to run samtools sort on command line to sort a given SAM file to a given Sorted SAM
    file.

    :param sam_file_path: Directory of the input SAM file.
    :param overwrite: [True/False] statement that determines whether files are overwritten or not.
    """
    bam_output_path = '%s.bam' % ''.join(sam_file_path.split('.')[0:-1])
    #print bam_output_path
    bam_sorted_output_path = '%s.sorted' % ''.join(sam_file_path.split('.')[0:-1])
    #print bam_sorted_output_path
    #exit()
    if not os.path.exists(bam_output_path) or overwrite:
        print('Sorting SAM file %s' % sam_file_path)
        cmd = '{0} view -S {1} -b -o {2}; {0} sort {2} {3}'.format(
            'samtools', sam_file_path, bam_output_path,bam_sorted_output_path)
        execute_on_command_line(cmd)
        print('Sorted SAM file saved to %s' % bam_output_path)
    else:
        print('Output Directory %s already exists. Not overwritten.' % bam_output_path)


def main():
    """
    Method designed to sort a given SAM file using SAMTOOLS sort.
    """
    sam_file_path, overwrite = get_command_line_arguments(['', False])
    assert os.path.exists(sam_file_path), '%s file does not exist.' % sam_file_path
    sort_sam(sam_file_path, overwrite)


if __name__ == '__main__':
    main()
