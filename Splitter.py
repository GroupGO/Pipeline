#!/usr/bin/env python


"""
Author: Henry Ehlers
WUR_Number: 921013218060
Contact: henry.ehlers@wur.nl

A collection of functions designed to split a merged, paired-end FASTQ file into its forward and
reverse components.

    -Inputs:    [1] Directory of merged, paired-end FASTQ file
                [2] Directory of output folder, last level will be created if not present.
                [3] Overwrite Option: True/False - overwrite existing output files.
    -Outputs:   [1] Two FASTQ files named output_file_reverse/forward.fastq, saved in the
                specified output folder directory.

In order to provide readable and understandable code, the right indentation margin has been
increased from 79 to 99 characters, which remains in line with Python-Style-Recommendation (
https://www.python.org/dev/peps/pep-0008/) .This allows for longer, more descriptive variable
and function names, as well as more extensive doc-strings.
"""


import subprocess
import time
import sys
import os
import re


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


def execute_on_command_line(cmd_string):
    """
    Method to parse a formatted string to the command line and execute it.

    :param cmd_string: The formatted string to be executed.
    """
    assert isinstance(cmd_string, str), 'Command Line String must be of type string.'
    exit_code = subprocess.check_call(cmd_string, shell=True)
    if exit_code == 1:
        exit(1)


def extract_record(fast_q_file):
    """
    Function to yield each record of a given FASTQ file, one at a time.

    :param fast_q_file: The name of the open input FASTQ file, given as a a string.
    :return: Yields the header, sequence and quality sequence per record, as a list of strings.
    """
    header, sequence, quality = '', '', ''
    for line in fast_q_file:
        line = line.strip()
        if line[0] == '@':
            header = line
        elif header and not sequence:
            sequence = line
        elif header and sequence and not quality:
            if line[0] != '+':
                quality = line
        if header and sequence and quality:
            yield header, sequence, quality
            header, sequence, quality = '', '', ''


def split_record(output_files, header, sequence, quality):
    """
    Function to split the contents of a merged FASTQ file into its forward and reverse components.

    :param output_files: The open output files, given as a list of strings.
    :param header: The header of the merged FASTQ file, given as a string.
    :param sequence: The sequence of the merged FASTQ file, given as a string.
    :param quality: The quality of the merged FASTQ file, given as a string.
    """
    seq_len = len(sequence)
    header = re.sub(r'length=%s' % seq_len, 'length=%s' % (seq_len/2), header)
    for index, lengths in enumerate([(0, seq_len/2), (seq_len/2, seq_len)]):
        start, end = lengths
        output = output_files[index]
        output.write('%s\n%s\n+\n%s\n' % (header, sequence[start:end], quality[start:end]))


def create_empty_folder(folder_path):
    """
    Method to create an empty folder to store the files.

    :param folder_path: The name of the folder to be created.
    """
    if not os.path.exists(folder_path):
        execute_on_command_line('mkdir %s' % folder_path)


def generate_output_paths(input_path, folder_path):
    """
    Function generate the output paths of the output files using the input file and output folder.

    :param input_path: The path of the input file, given as a string.
    :param folder_path: The name of the output folder, given as a string.
    :return: The output paths of forward and reverse FASTQ files, given as a list of strings.
    """
    split_name = re.split('\.|/', input_path)
    extension = split_name[-1]
    output_paths = ['', '']
    for index, name in enumerate(['forward', 'reverse']):
        output_paths[index] = '%s/%s_%s.%s' %\
                              (folder_path, '.'.join(split_name[-2:-1]), name, extension)
    return output_paths


def split_merged_data_set(input_path, output_directory, overwrite=True):
    """
    Method to split a merged, paired-end FASTQ read files into separate forward and reverse
    FASTQ files.

    :param input_path: The path of the merged, paired-end FASTQ file, given as a string.
    :param output_directory: The director of the output folder, given as a string.
    :param overwrite: A setting to overwrite existing split data stored in the same path.
    """
    assert isinstance(input_path, str), 'Input Path must be of type string.'
    assert isinstance(output_directory, str), 'Output Folder name must be of type string.'
    create_empty_folder(output_directory)
    output_paths = generate_output_paths(input_path, output_directory)
    print('Checking Directories...')
    if not all(os.path.exists(path) for path in output_paths) or overwrite:
        print('Started paired-end read file splitting.')
        start_time = time.clock()
        output_files = [open(output, 'w') for output in output_paths]
        input_file = open(input_path, 'r')
        for header, sequence, quality in extract_record(input_file):
            split_record(output_files, header, sequence, quality)
        input_file.close()
        for single_file in output_files:
            single_file.close()
        print('Completed paired-end read file splitting in %s seconds.' % (time.clock() - start_time))
    else:
        print('Splitting Aborted. Files already present and not overwritten.')


if __name__ == '__main__':
    input_file_path, output_folder_path, overwrite = get_command_line_arguments(['', '', False])
    split_merged_data_set(input_file_path, output_folder_path, overwrite)
