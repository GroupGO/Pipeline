#!/usr/bin/env python


"""
Author: Henry Ehlers
WUR_Number: 921013218060

A script designed to run the command line tool CuffQuant.

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
    exit_code = subprocess.check_call(cmd_string, shell=True)
    if exit_code == 1:
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


def run_cuff_quant(sorted_sam_file, annotation, output_folder_path, overwrite):
    """
    Method to run CuffQuant on command line using the provided input arguments.

    :param sorted_sam_file: Path leading to the sorted SAM file to be quantified, given as a
    string.
    :param annotation: Path leading to the annotation.gtf file.
    :param output_folder_path: Path leading to the desired output folder.
    """
    if not os.path.exists('%s/abundances.cxb' % output_folder_path) or overwrite:
        print('CuffQuant started on %s' % sorted_sam_file)
        cmd = 'cuffquant %s -g %s -o %s' % (sorted_sam_file, annotation, output_folder_path)
        print('CuffQuant output saved to %s/abundances.cxb' % output_folder_path)
        execute_on_command_line(cmd)
    else:
        print('Cuffquant output directory %s already exists. Not overwritten.' %
              '%s/abundances.cxb' % output_folder_path)


def main():
    sorted_sam_path, annotation, output_folder_path, overwrite = \
        get_command_line_arguments(['', '', '', False])
    assert os.path.exists(sorted_sam_path), 'SAM file path "%s" not found.' % sorted_sam_path
    assert os.path.exists(annotation), 'Annotation file path "%s" not found.' % annotation
    assert os.path.exists(output_folder_path), 'Output path "%s" not found.' % output_folder_path
    run_cuff_quant(sorted_sam_path, annotation, output_folder_path, overwrite)


if __name__ == '__main__':
    main()
