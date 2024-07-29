#!/usr/bin/env python

__author__ = "Hannah Holland-Moritz"
__email__ = "hannah.holland-moritz@unh.edu"
__version__ = "0.0.1"

import sys
import os
import logging
import re
import json
#from time import gmtime, strftime
#from itertools import izip
#import gzip
import argparse


parser = argparse.ArgumentParser(description=
                                 "Convert a directory of raw fastq files to JSON format for nmdc processing.")
parser.add_argument('-i', '--sequence_reads_fp', required=True, \
                    help='The directory containing sequence reads in fastq format (string; no default; required)'),
parser.add_argument('-f', '--foreward_reads_suffix', required=False, \
                    help='The suffix indicating foreward sequence reads in fastq names (default: %(default)s)', \
                    default="R1_"),
parser.add_argument('-r', '--reverse_reads_suffix', required=False, \
                    help='The suffix indicating reverse sequence reads in fastq names (default: %(default)s)', \
                    default="R2_"),
parser.add_argument('-p', '--project_name', required=False, \
                    help='The name of the nmdc project to use, this will become the prefix of all fastq outputs (default: %(default)s)', \
                    default="MyProject"),
parser.add_argument('-s', '--short_reads', required=False, \
                    help='Whether or not the shortreads method will be used (default: %(default)s)', \
                    default="True"),
parser.add_argument('-o', '--output_dir', required=False, \
                    help='The output directory for sequence reads to be stored (default: %(default)s)',
                    default= "output")
parser.add_argument('-jo', '--json_output_dir', required=False, \
                    help='The output directory where json files will be stored (default: %(default)s)',
                    default= "jsonout")


def main():
    args = parser.parse_args()

    sequence_reads_fp = args.sequence_reads_fp
    foreward_suff = args.foreward_reads_suffix
    reverse_suff = args.reverse_reads_suffix
    proj_name = args.project_name
    shortreads = args.short_reads
    output_dir = args.output_dir
    joutput_dir = args.json_output_dir

#    sys.stdout.write('Start time: ' + time + '\n')
    
    # first get a dictionary of paired files
    filelist = get_file_list(sequence_reads_fp, foreward_suff, reverse_suff)
    #print(filelist)
    # next create dictionary of json output
    json_out = make_json_output(filelist, proj_name, output_dir, shortreads)
    #print(json_out)
    # write json files
    write_json_output(json_out, joutput_dir)
    # Make directory to hold processing output
    os.makedirs(os.getcwd() + "/" + output_dir, exist_ok=True)

    


def get_file_list(seq_file_path, fwd_suf, rev_suf):
    directory = os.fsencode(seq_file_path)
    
    # get forward and reverse pattern
    pattern = re.compile("|".join([fwd_suf, rev_suf]))

    # Initialize dictionary
    fastqfiles = {}

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        #print(filename)
        if filename.endswith(".fastq") or filename.endswith("fastq.gz"):
            # First get prefix that doesn't have fastq/fastq.gz or read suffix
            prefix = re.sub(".fastq.gz|.fastq", "", filename) 
            prefix = re.sub(pattern, "", prefix)
            #print(prefix)
            fastqfiles.setdefault(prefix, [])
            # we have to process these in reverse-first order so they'll be in the correct order in the json 
            if rev_suf in filename:
                #print("Reverse found!")
                fastqfiles[prefix].append(os.path.join(seq_file_path, filename))
            elif fwd_suf in filename:
                #print("Foreward found!")
                fastqfiles[prefix].append(os.path.join(seq_file_path, filename))
            else:
                logging.warning("No read direction suffixes found in " + filename)
        else:
            continue
        # Check that each entry has two values or throw warning
    
    not_enough_files = []
    for sample in fastqfiles:
        #print(fastqfiles[sample])
        if len(fastqfiles[sample]) < 2:
            logging.warning(sample + " does not have 2 fastq files, removing from dictionary. " +
                          "No json will be generated.")
            not_enough_files.append(sample)
    # Remove items from dictionary with not enough fastqs
    for i in not_enough_files:
        del fastqfiles[i]
    #print(fastqfiles)

    return fastqfiles

def make_json_output(file_dict, proj_name, outdir, shortreads):
    # takes a dictionary of sequence files

    json_out_dict = {}

    for prefix in file_dict:
        json_out_dict[prefix] = {}
        json_out_dict[prefix]['rqcfilter.input_files'] = file_dict[prefix]
        json_out_dict[prefix]['rqcfilter.proj'] = proj_name + "_" + prefix
        json_out_dict[prefix]['rqcfilter.outdir'] = os.getcwd() + "/" + outdir
        json_out_dict[prefix]['rqcfilter.shortRead'] = shortreads

    return json_out_dict


def write_json_output(json_dict, outdir):
    # make directory if it doesn't exist
    print(os.path.dirname(outdir))
    os.makedirs(outdir, exist_ok=True)

    for prefix in json_dict:
        file_out_name = os.path.join(outdir, prefix + "_input")
        with open(f'{file_out_name}.json', "w") as fp:
            json.dump(json_dict[prefix], fp, indent=3)

if __name__ == "__main__":
    main()
