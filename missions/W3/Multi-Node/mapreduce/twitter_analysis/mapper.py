#!/usr/bin/python3
import sys

NUM2SENTIMENT = {
    0: 'negative',
    2: 'neutral',
    4: 'positive',
}

for line in sys.stdin:
    line = line.strip()
    num = line.split(",")[0][1:-1]

    try:
        num = int(num)
    except ValueError:
        continue

    print(f'{NUM2SENTIMENT[num]}\t1')