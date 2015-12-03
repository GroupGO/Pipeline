#!/usr/bin/env python


"""
Author: Henry Ehlers, Ronald de Jongh
WUR_Number: 921013218060, 930323409080

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
import re


def execute_on_command_line(cmd_string):
    """
    Method to parse a formatted string to the command line and execute it.
    -Ronald says: It is a useless function...

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

    -Ronald says: a function of 2 functional lines, meh...
    :param path:
    :param overwrite:
    :return: an exitcode
    """

    if not os.path.exists(path):
        execute_on_command_line('mkdir %s' % path)
        return 0
    else:
        return 1


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


def run_splitter(rna_seq_folder, split_folder):
    """

    :param rna_seq_folder:
    :param split_folder:
    """
    for folder_file in os.listdir(rna_seq_folder):
        if folder_file.endswith('.fastq'):
            file_directory = '%s/%s' % (rna_seq_folder, folder_file)
            cmd = 'python Splitter.py %s %s' % (file_directory, split_folder)
            execute_on_command_line(cmd)


def run_his_hat_2(split_data_folder, genome_folder, his_hat_output):
    """

    :param split_data_folder:
    :param genome_folder:
    :param his_hat_output:
    """
    genome_path = '%s/cro_scaffolds.min_200bp.fasta' % genome_folder
    forward_reads = sorted(get_file_of_extension(split_data_folder, '_forward.fastq'))
    reverse_reads = sorted(get_file_of_extension(split_data_folder, '_reverse.fastq'))
    for forward, reverse in zip(forward_reads, reverse_reads):
        cmd = 'python Mapping.py %s %s %s' % (genome_path, forward, reverse)
        execute_on_command_line(cmd)
    execute_on_command_line('mv *.sam %s' % his_hat_output)


def run_samsorter(his_hat_folder):
    """
    Runs the samsort python program to convert an unsorted samfile into a sorted bamfile

    :param his_hat_folder: Path leading to the hisat folder
    """
    for sam_file_path in os.listdir(his_hat_folder):
        if sam_file_path.endswith('test_100.sam'):
            cmd = 'python SamSort.py %s/%s %s' % (his_hat_folder, sam_file_path,False)
            execute_on_command_line(cmd)


def run_cufflinks(sorted_bam_path, annotation, output_folder_path, overwrite=False):
    for file_name in os.listdir(sorted_bam_path):
        if file_name.endswith('test_100.sorted.bam'):
            dirname = '%s/%s' % (output_folder_path, re.sub('.sorted.bam', '', file_name))
            make_directory(dirname)
            cmd = 'python CuffLinks.py %s/%s %s %s %s' % \
                  (sorted_bam_path, file_name, annotation, dirname, overwrite)
            execute_on_command_line(cmd)


def output_check(file_names, output_folder, extension, overwrite=False):
    output_files = ['%s%s' % (a_file, extension) for a_file in file_names]
    exitcode = make_directory(output_folder)
    if exitcode == 0 or overwrite:
        return True
    elif not any(list(a_file for a_file in output_files if a_file in os.listdir(output_folder))):
        return True
    else:
        return False


def run_cuff_merge(cufflinks_folder, cuffmerge_folder, run_name):
    cmd = 'python CuffMerge.py %s %s %s %s' % (cufflinks_folder, cuffmerge_folder, run_name, False)
    execute_on_command_line(cmd)


def run_cuff_norm(transcripts, sam_path, output_folder, overwrite):
    cmd = 'python CuffNorm.py %s %s %s ' % (transcripts, output_folder, overwrite)
    for sam in sam_path:
        cmd += "%s " % sam
    execute_on_command_line(cmd)


def main():
    #/local/data/BIF30806_2015_2/project/RNAseq/SRP041695
    run_name, rna_seq_folder, genome_folder, output_folder = \
        get_command_line_arguments(['Test',
                                    '/local/data/BIF30806_2015_2/project/groups/go/Data/',
                                    '/local/data/BIF30806_2015_2/project/genomes/Catharanthus_roseus',
                                    '/local/data/BIF30806_2015_2/project/groups/go/Data'])
    file_names = [i[0:-6] for i in os.listdir(output_folder) if i.endswith('.fastq')]

    # Splitter
    split_folder = '%s/Split_test_Data' % output_folder
    if output_check(file_names, output_folder, '_forward.fastq'):
        run_splitter(rna_seq_folder, split_folder)

    # Mapper
    his_hat_output = '%s/Hisat2_test_Data' % output_folder
    if output_check(file_names, his_hat_output, '.bam') or True:
        run_his_hat_2(split_folder, genome_folder, his_hat_output)
    quit()
    # Sorter
    run_samsorter(his_hat_output) #CURRENTLY ONLY WORKS ON *test.sam !!!!!!!!!!

    # Cuff package
    cuff_folder = '%s/Cuff_test_Data' % output_folder
    make_directory(cuff_folder)

    # Cufflinks
    cufflinks_folder = '%s/Cufflinks_test_Data' % cuff_folder
    if output_check(file_names, cufflinks_folder, ''):
        run_cufflinks(his_hat_output, '%s/cro_std_maker_anno.final.gff3' %
                      genome_folder, cufflinks_folder, False)
    else:
        print cufflinks_folder+'\nCufflinks directory exists'

    # Cuffmerge
    cuffmerge_folder = '%s/Cuffmerge_test_Data' % cuff_folder
    if output_check(['merged'], cuffmerge_folder, '.gtf'):
        run_cuff_merge(cufflinks_folder, cuffmerge_folder, run_name)
    else:
        print cuffmerge_folder+'\nCuffmerge directory exists'

    # Cuffnorm
    cuffnorm_folder = '%s/Cuffnorm_Data' % cuff_folder
    make_directory(cuffnorm_folder)
    norm_run_folder = '%s/%s' % (cuffnorm_folder,run_name)
    make_directory(norm_run_folder)
    if output_check(norm_run_folder, cuffnorm_folder, ''):
        transcript_path = '%s/merged.gtf' % cuffmerge_folder
        sam_paths = ['%s/%s.sorted.bam' % (his_hat_output, a_file) for a_file in file_names]
        cuff_norm_output = '%s/%s' % (cuffnorm_folder, run_name)
        run_cuff_norm(transcript_path, sam_paths, cuff_norm_output, False)
    else:
        exit('Cuffnorm failed')

    # Find Differential Expression
    # BLAST2GO


if __name__ == '__main__':
    main()
