#!/usr/bin/env python3
import sys
import csv

reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
for line in reader:
    if len(line) < 4:
        continue
    prod_id = line[1]
    rating = line[2]

    print(f'{prod_id}\t{rating}')