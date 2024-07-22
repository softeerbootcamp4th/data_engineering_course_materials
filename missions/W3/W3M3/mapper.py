#!/usr/bin/env python3

import sys

# Mapper function
for line in sys.stdin:
    line = line.strip()
    words = line.split()
    for word in words:
        print(f"{word.lower()}\t1")
