#!/bin/bash
#SBATCH --partition=bgmp
#SBATCH --account=bgmp
#SBATCH --job-name=dedup
#SBATCH --output=LOG/dedup_%j.out
#SBATCH --error=LOG/dedup_%j.err
#SBATCH --mem=50G
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=ghach@uoregon.edu

{ /usr/bin/time -v ./Hach_deduper.py -f "/projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam" -o "C1_SE_uniqAlign_OUTPUT.sam" -u STL96.txt 2> timed.txt ; }

