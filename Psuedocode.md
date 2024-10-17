# Define the problem
We are looking to identify PCR duplicates for single-end data, represented as a sam file of uniquely mapped reads. PCR duplicates will be on the same chromosome, they will have the same 5' start position (which may need to be adjusted for soft clipping), they will be on the same strand, and they will have the same UMI (which must be found un the file of 96 UMIs).

The sam file is already sorted. I'm not 100% sure what that means, but I'll take for granted that before the main algorithm, I will call samtools sort without any flags to sort by the mapping position, and though the POS column of the sam file starts at one at the start of each chromosome, it'll sort by the chromosome first, and the POS column second. 

Thus, if soft clipping has occurred, the soft-clipped sequences will come after their duplicates, because they have a later base position, reflecting when the actual alignment (not the sequence) starts. If the file is sorted like I think, it shouldn't be necessary to check the chromosome.
# Write Examples

See in.sam and out.sam in the repo.
# Algorithm
```
# Call parse_args to get input, output, UMI filenames
# Call get_umis to get umi_set
# Open both input and output files
# Store the first line in memory as a list of tab-separated components, call this # ref_line
# Store the subsequent line in memory as in the same manner as next_line
# define a bool, written, to indicate whether ref_line has already been written to 
# the output file. Set to false

# BEGIN MAIN LOOP FOR PARSING INPUT FILE:
	# Extract each UMI from the Qnames of ref_line and next_line
	
	# CHECK UMIS:
		# If ref_line UMI is not in umi_set, but next_line UMI is in umi_set:
			# replace ref_line with next_line and next_line with the next
			# line in the file
			# set written to false
		# If ref_line UMI is in umi_set, but next_line isn't:
			# replace next_line with the next line in the file
		# If neither UMIs are in UMI set:
			# replace ref_line with the next line in file
			# If ref_line is empty:
				# EOF has been reached, exit main loop
			# replace next_line with the next line in file
			# set written to false
		# If, after executing all above code, next_line is empty, EOF has been
		# reached, exit main loop
	
	# COMPARE REF_LINE TO NEXT_LINE:
		# call get_actual_pos() on ref_line and next_line, storing outputs
		# call is_dup(), passing in actual positions, flags, and UMIs
		# If is_dup returns true, and written is false:
			# call write_line to write ref_line to file
			# set written to true
			# set next_line to be the next line in the file
		# if is_dup returns true, and written is true:
			# set next_line to be the next line in the file 
		# If is_dup returns false:
			# set ref_line to be next_line, and next_line to be the next line in
			# the file
			# set written to false
		# If, after executing all above code, next_line is empty, EOF has been
		# reached, exit main loop

# Close input and output files
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
	umi_set (set of str) - set containing 
'''
	return umi_set 


def get_actual_pos(pos, cigar):
'''
Returns the actual start position of a read, given the POS column, and the cigar string
If actual_pos==pos, soft clipping at the leading end has not occured!
Input:
	pos (int) - 5' mapping position
	cigar (str) - cigar string
Output:
	actual_pos (int)
'''

	return actual_pos


def write_line(line_list, file_handle):
'''
Writes a new line to a sam file
Input:
	line_list (list of str) - list of all components in a sam line
	file_handle - file handle (already opened) of output file
'''

	return


def is_dup(true_pos1,flag1,umi1,true_pos2,flag2,umi2):
'''
Compares two positions, flags, and umis to determine if they're the same!
Input:
	
Output:
	dup (bool) - True if all are the same
'''
```

## Functions examples:

I don't think function IO examples are really applicable to `parse_args()`, or `write_line()`.

```
get_umis()
	Input: "umi_test.txt"
	Expected output: {"AACGCCAT","AAGGTACG","AATTCCGG"}

get_actual_pos()
	Input: 150, "14S62M2S"
	Expected output: 136
	Input: 765, "2S63M1S"
	Expected output: 763
	Input: 865, "56M3S"
	Expected output: 865

is_dup()
	Input: 1, 16, "AAGGTACG", 1, 48, "AAGGTACG" # Both reverse complimented
	Expected output: True
	Input: 1, 1, "AATTCCGG", 1, 32, "AATTCCGG"  # Neither reverse complimented
	Expected output: True
	Input: 1, 17, "AATTCCGG", 1, 32, "AATTCCGG" # Different strands
	Expected output: False
```
# Questions
Why don't PCR duplicates have the same sequence? -> B/c if they did, wouldn't be "uniquely mapped reads?"

Am I correct about how samtools sort works? See following:

I'll take for granted that before the main algorithm, I will call samtools sort without any flags to sort by the mapping position, and though the POS column of the sam file starts at one at the start of each chromosome, it'll sort by the chromosome first, and the POS column second. 

If above is correct, is it even necessary to check the chromosome? (I'm thinking no, but will add argument to is_dup if so.
