#!/usr/bin/env python


"""
Author: Henry Ehlers
WUR_Number: 921013218060

A script designed to ...
    -input:
    -output:

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
    input_variables = ['']*len(default_variable_values)
    for index, default_value in enumerate(default_variable_values):
        try:
            input_variables[index] = sys.argv[index + 1]
        except IndexError:
            if default_value != '':
                input_variables[index] = default_value
            else:
                exit('Not enough command line input arguments. Critical Input Missing.')
    return input_variables


def make_directory(path):
    """

    :param path:
    :return:
    """
    if not os.path.exists(path):
        execute_on_command_line('mkdir %s' % path)


def get_file_of_extension(directory, extension):
    """

    :param directory:
    :param extension:
    :return:
    """
    found_files = []
    for a_file in os.listdir(directory):
        if a_file.endswith(extension):
            found_files.append('%s/%s' % (directory, a_file))
    return found_files


def run_splitter(rna_seq_folder, output_folder):
    """

    :param rna_seq_folder:
    :param output_folder:
    :return:
    """
    split_output_folder = '%s/Split_Data' % output_folder
    make_directory(split_output_folder)
    for folder_file in os.listdir(rna_seq_folder):
        if folder_file.endswith('.fastq'):
            file_directory = '%s/%s' % (rna_seq_folder, folder_file)
            cmd = 'python Splitter.py %s %s' % (file_directory, split_output_folder)
            execute_on_command_line(cmd)
    return split_output_folder


def run_his_hat_2(split_data_folder, genome_folder, output_folder):
    """

    :param split_data_folder:
    :param genome_folder:
    :param output_folder:
    :return:
    """
    his_hat_output = '%s/Hisat2_Data' % output_folder
    genome_path = '%s/cro_scaffolds.min_200bp.fasta' % genome_folder
    make_directory(his_hat_output)
    forward_reads = get_file_of_extension(split_data_folder, '_forward.fastq')[0]
    reverse_reads = get_file_of_extension(split_data_folder, '_reverse.fastq')[0]
    cmd = 'python Mapping.py %s %s %s' % (genome_path, forward_reads, reverse_reads)
    execute_on_command_line(cmd)
    execute_on_command_line('mv *.sam %s' % his_hat_output)
    execute_on_command_line('mv *.ht2 %s' % his_hat_output)
    return his_hat_output


def main():
    rna_seq_folder, genome_folder, output_folder = \
        get_command_line_arguments(['/local/data/BIF30806_2015_2/project/RNAseq/SRP041695',
                                    '/local/data/BIF30806_2015_2/project/genomes/Catharanthus_roseus',
                                    '/local/data/BIF30806_2015_2/project/groups/go/Data'])
    # Splitter
    split_folder = run_splitter(rna_seq_folder, output_folder)
    # Mapper
    his_hat_output = run_his_hat_2(split_folder, genome_folder, output_folder)
    # Sorter
    # Cufflinks
    # Find Differential Expression
    # BLAST2GO


if __name__ == '__main__':
    main()
