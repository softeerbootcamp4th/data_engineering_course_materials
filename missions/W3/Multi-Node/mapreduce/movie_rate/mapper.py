#!/usr/bin/python3

from sys import stdin

for line in stdin:
    line = line.strip()
    _, movie_id, rating, _ = line.split(',')

    print(f'{movie_id}\t{rating}\t1')
