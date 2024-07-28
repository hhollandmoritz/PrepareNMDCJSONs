# Code to prepare json input files for NMDC ReadQC workflow


# Usage:

```
fastq_to_json.py --help
usage: fastq_to_json.py [-h] [-i SEQUENCE_READS_FP] [-f FOREWARD_READS_SUFFIX] [-r REVERSE_READS_SUFFIX] [-p PROJECT_NAME]
                        [-s SHORT_READS] [-o OUTPUT_DIR]

Convert a directory of raw fastq files for nmdc processing.

options:
  -h, --help            show this help message and exit
  -i SEQUENCE_READS_FP, --sequence_reads_fp SEQUENCE_READS_FP
                        The directory containing sequence reads in fastq format
  -f FOREWARD_READS_SUFFIX, --foreward_reads_suffix FOREWARD_READS_SUFFIX
                        The suffix indicating foreward sequence reads in fastq names
  -r REVERSE_READS_SUFFIX, --reverse_reads_suffix REVERSE_READS_SUFFIX
                        The suffix indicating reverse sequence reads in fastq names
  -p PROJECT_NAME, --project_name PROJECT_NAME
                        The name of the nmdc project to use
  -s SHORT_READS, --short_reads SHORT_READS
                        Whether or not the shortreads method will be used
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        The output directory where json files will be stored

```

Examples:

```
python fastq_to_json.py -i <full/path/to/directory/with/reads> -o <my_proj_jsons> -f "R1.fastq.gz" -r "R2.fastq.gz" -p MyProjectName -s True
```
