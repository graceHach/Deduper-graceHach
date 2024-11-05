# Define the problem
We are looking to identify PCR duplicates for single-end data, represented as a sam file of uniquely mapped reads. PCR duplicates will be on the same chromosome, they will have the same 5' start position (which may need to be adjusted for soft clipping), they will be on the same strand, and they will have the same UMI (which must be found un the file of 96 UMIs).

The sam file is already sorted. I'm not 100% sure what that means, but I'll take for granted that before the main algorithm, I will call samtools sort without any flags to sort by the mapping position, and though the POS column of the sam file starts at one at the start of each chromosome, it'll sort by the chromosome first, and the POS column second. 

Thus, if soft clipping has occurred, the soft-clipped sequences will come after their duplicates, because they have a later base position, reflecting when the actual alignment (not the sequence) starts. If the file is sorted like I think, it shouldn't be necessary to check the chromosome.
# Rewritten Algorithm
The previous strategy doesn't work actually without an additional sort. If soft clipping is extensive, duplicate reads will appear well after the original reads in the sam file. Thanks Ben, and Shayal and Abraham for the feedback! Also, thanks to Carly and Ben, your pseudocode was very helpful in reworking mine.
- Rewritten to use a tuple-based hashing strategy, clearing after each chromosome
- Accounts for insertions/deletions from the reference on the minus strand
- Gets the true 5' start position correctly
```
# Call parse_args to get input, output, UMI filenames
# Call get_umis to get umi_set
# Open both input and output files
# While the lines of the input file start with "@":
	# Write each line to the output file
	# If line begins with @SQ: Store chromosome name/number in list
# Set variable curr_chrom to be first chromsome in list
# Initialize an empty set called seqs
# This set will store tuples for each unique read, and be cleared when curr_chrom is updated
# tuples are of the form (flag (bool), umi (str), 5' start position (int))
# ITERATE OVER SEQUENCE LINES:
	# Get a line
	# Call parse_line() on line to get flag, position, umi, and chromosome
	# if chromosome is the same as current chromsome: 
		# check if tuple is in seqs:
			# if yes:
				# continue 
			# if no
				# check if UMI is in the set of UMIs
					# if yes:
						# call write_line() to write it to the file
						# add to seqs set
					# if no
						# continue
	# else
		# clear the set  
# Close input and output files:
```
# Functions
```
def parse_args():
'''
Initalizes a parser object, adds the following arguments:
	`-f`, `--file`: designates absolute file path to sorted sam file
	`-o`, `--outfile`: designates absolute file path to deduplicated sam file
	`-u`, `--umi`: designates file containing the list of UMIs
	`-h`, `--help`: prints a USEFUL help message (see argparse docs)
And parses the args! 
'''
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
	if flag&16==16: # minus strand
		# Parse string to get number of trailing soft clipped bases
		# Get number of Ns, Ds, Ss, and Ms, 
		actual_pos + M + N + D + trailing Ss
	else:
		actual_pos - # soft clipped leading bases
	return actual_pos
```

**For more detailed documentation of functions, see the function doc strings in "utils.py". For function io testing, see test/unit_testing.py. For functional testing of entire deduper script, see functional_test.sh.**

