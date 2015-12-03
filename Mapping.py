#!/usr/bin/env	python

"""
Author : Linh Nguyen
WUR Number: 940830599020
"""

import subprocess
import sys
import os.path
import re


def execute_on_command_line(cmd_string):
    """
    Runs a command line
    
    Parameter
    cmd_string: a command line string 
    """
    assert isinstance(cmd_string, str),\
    'Command Line String must be of type string.'
    subprocess.check_call(cmd_string, shell=True)


def create_index_base_string(genome_file_path):
    """
    Returns a base string for the hisat2 genome index.
    
    Parameter
    genome_file_path: the path to the genome file
    
    The name of the genome file will be used as base string 
    """
    base_string = re.findall('(\w+\.\w+\.\w+)$', genome_file_path)[0]
    base_string = base_string.split('.')
    base_string = base_string[0] + "." + base_string[1]
    return base_string


def hisat2_builder(genome_file_path, base_string):
    """
    Creates an index for the hisat2 aligner.
    
    Parameter
    genome_file_path: the path to the genome file
    base_string: the base string for the output files   
    """
    if not os.path.isfile(base_string + '.1.ht2'):
        cmd_string = 'hisat2-build -p 8 %s %s' % (genome_file_path, base_string)
        execute_on_command_line(cmd_string)


def create_sam_base_string(read_file_path):
    """
    Returns a sam base string for the hisat2 aligner.
    
    Parameter
    read_file_path: the path to the read file
    """
    
    sam_base_string = re.findall('(\w+\.\w+)$', read_file_path)[0]
    str_list = sam_base_string.split('_')
    sam_base_string = '_'.join(str_list[0:-1]) + '.sam'
    return sam_base_string


def hisat2_aligner(base_string, read1_path, read2_path, sam_base_string):
    """
    Creates an index for the hisat2 aligner.
    
    Parameter
    base_string: the base string of the index files
    read1_path: the path to the forward read file
    read2_path: the path to the reverse read file
    sam_base_string: the base string for the output sam file
    """
    if not os.path.isfile(sam_base_string):
        cmd_string = 'hisat2 -p 8 -t --no-unal --dta-cufflinks -x %s -1 %s -2 %s -S %s' % (
            base_string, read1_path, read2_path, sam_base_string)
        #--sra-accession SRR1271857
        execute_on_command_line(cmd_string)


def parse_cmd_lines(cmd_file):
    """
    Returns the path to the genome file, the forward reads file  
    and the reverse reads file
    
    Parameter:
    cmd_file: a file containing the path to the genome file, forward read file,
    and reverse file
    """    
    
    input_file = open(cmd_file)

    genome_path = False

    for line in input_file:
        if genome_path == False:
            genome_path = line.strip('\n')
        else:
            assert len(line.split()) == 2
            read1_path, read2_path = line.split()
            yield genome_path, read1_path, read2_path


if __name__ == '__main__':
    genome_path, read1_path, read2_path = sys.argv[1], sys.argv[2], sys.argv[3]
    base_string = create_index_base_string(genome_path) 
    hisat2_builder(genome_path, base_string)
    sam_base_string = create_sam_base_string(read1_path)

    hisat2_aligner(base_string, read1_path, read2_path, sam_base_string)











