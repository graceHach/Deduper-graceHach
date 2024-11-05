#!/usr/bin/env python

# for talapas /usr/bin/env
import unittest
import sys
sys.path.append('../')
import utils

umi_set = set(["AACGCCAT", "AAGGTACG", "AATTCCGG"])

class TestStringMethods(unittest.TestCase):

    def test_get_umis(self):
        output = utils.get_umis("umi_test.txt")
        self.assertEqual(output, umi_set)

    def test_get_actual_pos(self):
        #get_actual_pos(pos, cigar, flag):
        self.assertEqual(utils.get_actual_pos(313,"13S4M3D54M", 0),300)
        self.assertEqual(utils.get_actual_pos(800,"14M20N36D", 16),870)
        self.assertEqual(utils.get_actual_pos(800,"14M888I12N36D", 16),862)
        self.assertEqual(utils.get_actual_pos(800,"14M888I12N36D89I", 16),862)
        self.assertEqual(utils.get_actual_pos(802,"2S12M20N36D", 16),870)
        self.assertEqual(utils.get_actual_pos(802,"2S12M20N36D3S", 16),873)

    def test_parse_line(self):
        # outputs umi (str), flag (bool), chrom (str), pos (str), cigar (str)
        line1 = "Unique_3_umi:TTCGTTCG	1	1	7	36	71M	*	0	0	TGCTGTCAGGATGTAAGCCCCACTATCCGTTCTTGAGGAATCCTTGTTTATCAGATGAGTGGAGAAGTCTG	6AEEEEEEEEEEEEEEEEEAEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE \n"
        output1 = ["TTCGTTCG", "1", "1", "7", "71M"]
        line2 = "Test_3_include:GAGAAGTC	1	1	75	36	71M	*	0	0	TGCTGTCAGGATGTAAGCCCCACTATCCGTTCTTGAGGAATCCTTGTTTATCAGATGAGTGGAGAAGTCTG	6AEEEEEEEEEEEEEEEEEAEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE \n"
        output2=["GAGAAGTC", "1", "1", "75", "71M"]
        line3 = "Test_3_discard:GAGAAGTC	3	1	7	36	70M1S	*	0	0	TTCCACTGTTGCTTCATAACTGCAGTCCTAACATAAATGTCTGACATGTAGGATGATCTTAAGCAACCCCT	6AEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE<EEAAAEE \n"
        output3 = ["GAGAAGTC","3","1","7","70M1S"]
        line4 = "Unique_3_flag:GAGAAGTC	16	1	7	36	71M	*	0	0	TGCTGTCAGGATGTAAGCCCCACTATCCGTTCTTGAGGAATCCTTGTTTATCAGATGAGTGGAGAAGTCTG	6AEEEEEEEEEEEEEEEEEAEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE \n"
        output4 = ["GAGAAGTC","16","1","7","71M"]
        tested_outputs = [list(utils.parse_line(line1)),list(utils.parse_line(line2)),list(utils.parse_line(line3)),list(utils.parse_line(line4)) ]
        outputs = [output1, output2, output3, output4]
        for tested_output, output in zip(tested_outputs, outputs):
            self.assertListEqual(tested_output, output)

if __name__ == '__main__':
    unittest.main()