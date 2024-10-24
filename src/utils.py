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
    parser.add_argument("-h", "--help", type=str, help="prints a USEFUL help message")
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
    umi_set = {}
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
    if (flag&16)==16: 
        # Parse string to get number of trailing soft clipped bases 
        # Trim leading S, we don't care about it
        # add try except to handle lack of leading s
        cigar = cigar[cigar.index("S")+1:]
        re.findall("[0-9]+S", cigar)
        # Get number of Ns, Ds, trailing Ss, and Ms,
        # determine if 
        actual_pos = pos + M + N + D + trailing Ss
    else:
        # Get # of bases soft clipped at leading end 
        leading_s = int(cigar[:cigar.index("S")])
        actual_pos = pos - leading_s
    return actual_pos

'''
def write_line(line, file_handle):
'''
Writes a new line to a sam file
Input:
	line (str) - the line as read from the file
	file_handle - file handle (already opened) of output file
'''
	return

def parse_line(sam_line):
'''
Input:

Output:

'''
	return flag, pos, umi, chrom

'''

