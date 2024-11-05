#!/usr/bin/env python

import argparse 
import re

def parse_args():
    '''
    Initalizes a parser object, adds the following arguments:
        `-f`, `--file`: designates absolute file path to sorted sam file
        `-o`, `--outfile`: designates absolute file path to deduplicated sam file
        `-u`, `--umi`: designates file containing the list of UMIs
        `-h`, `--help`: prints a USEFUL help message (see argparse docs)
    And parses the args! 
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="designates absolute file path to sorted sam file")
    parser.add_argument("-o", "--outfile", type=str, help="designates absolute file path to deduplicated sam file")
    parser.add_argument("-u", "--umi", type=str, help="designates file containing the list of UMIs")
    #parser.add_argument("-h", "--help", type=str, help="prints a USEFUL help message")
    args = parser.parse_args()
    return args


def get_umis(umi_filename):
    '''
    Reads file with one umi per line, returns a set of all UMIs in the file.
    Closes the file
    Input:
        umi_filename (str) - filename containing umis
    Output:
        umi_set (set of str) - set containing the umis from the file
    '''
    umi_set = set()
    with open(umi_filename, 'r') as fh:
        for line in fh:
            umi_set.add(line.strip())
    return umi_set 


def get_actual_pos(pos, cigar, flag):
    '''
    Returns the actual 5' start position of a read, given the POS column, and the cigar string
    If actual_pos==pos, soft clipping at the leading end has not occured!
    Input:
        pos (int) - mapping position
        cigar (str) - cigar string
        flag (int) - bitwise flag
    Output:
        actual_pos (int) - Actual 5' starting position
    '''
    # sequence being reverse complimented == it's the minus strand
    if (int(flag)&16)==16: 
        # Parse string to get number of trailing soft clipped bases 
        # Trim leading S, we don't care about it
        split = re.split("^[0-9]+S", cigar, 1)
        if split[0] == "":
            # Case where there was a leading S
            cigar = split[1]
        else:
            # Case where there wasn't
            cigar=split[0]
        # Get number of Ns, Ds, trailing Ss, and Ms,
        split = re.split("[MNDS]", cigar)
        # splits on chars of interest, last char will be a ""
        split = split[:-1]
        return int(pos) + sum([int(x) for x in split])
        #actual_pos = pos + M + N + D + trailing Ss
    else:
        # Get # of bases soft clipped at leading end 
        # returns [] if no leading s
        leading_s = re.findall("^[0-9]+S", cigar)
        #print(leading_s)
        if len(leading_s)==0:
            return int(pos)
        else:
            #print(leading_s[:-1])
            return int(pos) - int(leading_s[0][:-1])

def parse_line(sam_line):
    '''
    Input:

    Output:

    '''
    split = sam_line.split("\t")
    umi = split[0].split(":")[1]
    flag = split[1]
    chrom = split[2]
    pos = split[3]
    cigar = split[5]
    return umi, flag, chrom, pos, cigar
