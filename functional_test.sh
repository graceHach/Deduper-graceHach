#!/bin/bash 

./deduper.py -f "test/in1.sam" -o "test/test_out1.sam" -u "STL96.txt"
echo "Tested and contrived output files should be the same"
diff -s "test/test_out1.sam" "test/out1.sam"
./deduper.py -f "test/in2.sam" -o "test/test_out2.sam" -u "STL96.txt"
diff -s "test/test_out2.sam" "test/out2.sam"