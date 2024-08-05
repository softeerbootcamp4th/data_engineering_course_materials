#!/usr/bin/env python3
import sys

for line in sys.stdin:
    values = line.strip().split(",")
    movieId, rating = values[1], values[2]
    print(f'{movieId}\t{rating}')
