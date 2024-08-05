#!/usr/bin/env python3
import sys

for line in sys.stdin:
    values = line.strip().split(",")

    if values[0] == '"0"':
        print('negative\t1')
    elif values[0] == '"2"':
        print('neutral\t1')
    else:
        print('positive\t1')
