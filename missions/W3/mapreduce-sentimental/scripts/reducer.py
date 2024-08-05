#!/usr/bin/env python3
import sys

current_sentiment = None
current_count = 0
sentiment = None

for line in sys.stdin:
    line = line.strip()
    sentiment, count = line.split('\t', 1)

    count = int(count)

    if current_sentiment == sentiment:
        current_count += count
    else:
        if current_sentiment:
            print(f'{current_sentiment}\t{current_count}')
        current_sentiment = sentiment
        current_count = count

if current_sentiment == sentiment:
    print(f'{current_sentiment}\t{current_count}')