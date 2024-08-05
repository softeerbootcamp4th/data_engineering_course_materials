#!/usr/bin/env python3
import sys
import csv

for line in csv.reader(sys.stdin):
    asin = line[1]
    rating = line[2]

    print(f'{asin}\t{rating}')

