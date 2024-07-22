#!/usr/bin/env python3
from collections import defaultdict
import sys

word_counts = defaultdict(int) # Stores words and counts

for line in sys.stdin:
    try:
        # Remove whitespaces and split the line
        line = line.strip()
        word, count = line.split()

        # Get each word's individual count
        count = int(count)
    except:
        continue

    # Add the count word-wise
    word_counts[word] += count

# Output word counts
for word, count in word_counts.items():
    print(word, count)