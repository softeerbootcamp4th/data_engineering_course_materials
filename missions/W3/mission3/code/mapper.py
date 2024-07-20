#!/usr/bin/env python3
import sys

for line in sys.stdin:
    # Remove whitespaces and split the line
    line = line.strip()
    words = line.split()

    # Output each word's individual count
    for word in words: 
        print(word, '\t', 1)