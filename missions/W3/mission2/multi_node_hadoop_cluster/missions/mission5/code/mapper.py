#!/usr/bin/env python3
import sys
import csv

reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
for line in reader:
    if len(line) < 4:
        continue
    _,	movieId, rating, _ = line
    print(f'{movieId}\t{rating}')