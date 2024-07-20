#!/usr/bin/env python3
from collections import defaultdict
import sys

sentiment_counts = defaultdict(int) # Stores words and counts

for line in sys.stdin:
    try:
        # Remove whitespaces and split the line
        line = line.strip()
        sentiment, count = line.split()
        count = int(count)
    except:
        continue

    # Add the count word-wise
    sentiment_counts[sentiment] += count

# Output word counts
for sentiment, count in sentiment_counts.items():
    print(sentiment, count)