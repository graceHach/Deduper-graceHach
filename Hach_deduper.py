#!/usr/bin/env python
import utils
import re

# Call parse_args to get input, output, UMI filenames
args = utils.parse_args()
# Call get_umis to get umi_set
umis = utils.get_umis(args.umi)
# Keep list of chromosomes in order
chrs = []
curr_chrom = None
# Initialize an empty set called seqs
# This set will store tuples for each unique read, and be cleared when curr_chrom is updated
# tuples are of the form (flag (bool), umi (str), 5' start position (int))
seqs = set()
# Open both input and output files
f_in = open(args.file, 'rt')
f_out = open(args.outfile, 'wt')
while f_in:
    in_line = f_in.readline()
    # While the lines of the input file start with "@":
    if in_line=="":
        break
    elif in_line[0]=="@":
        # Write each line to the output file
        f_out.write(in_line)
        if in_line[:7]=="@SQ	SN:":
            # If line begins with @SQ: Store chromosome name/number in list
            chrs.append(re.split("\t", in_line[7:],1)[0])
            # Set variable curr_chrom to be first chromsome in list
            curr_chrom = chrs[0]
    else:
        # header lines are done

        # Parse line
        #return umi, flag, chrom, pos, cigar
        umi, flag, chrom, pos, cigar = utils.parse_line(in_line)
        # get true start position
        actual_pos = utils.get_actual_pos(pos, cigar, flag)
        # tuples are of the form (flag (bool), umi (str), 5' start position (int))
        curr_tuple = (bool(int(flag)&16), umi, actual_pos)
        if not curr_chrom == chrom:
            seqs = set() # clear this
            curr_chrom = chrom
        if curr_tuple in seqs:
            # duplicate, don't write, don't alter seqs
            continue
        else:
            # unqiue
            if umi in umis:
                #print(in_line[:30])
                #print(curr_tuple)
                f_out.write(in_line)
                seqs.add(curr_tuple)
            
# Close files
f_in.close()
f_out.close()
