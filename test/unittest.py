#!/usr/bin/env python

# for talapas /usr/bin/env
import unittest
import sys
sys.path.append('../src/')
import utils

umi_set = set("AACGCCAT", "AAGGTACG", "AATTCCGG")

class TestStringMethods(unittest.TestCase):

    def test_get_umis(self):
        output = utils.get_umis("umi_test.txt")
        self.assertEqual(output, umi_set)

if __name__ == '__main__':
    unittest.main()