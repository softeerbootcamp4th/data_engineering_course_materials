#!/usr/bin/python3

from sys import stdin

for line in stdin:
    line = line.strip()
    words = line.split()

    for word in words:
        print(f'{word}\t1')
