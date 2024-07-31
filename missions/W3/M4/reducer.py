#!/usr/bin/env python3
import sys
from collections import defaultdict

sentiment_counts = defaultdict(int)

for line in sys.stdin:
    sentiment, count = line.strip().split('\t')
    sentiment_counts[sentiment] += int(count)

for sentiment, count in sentiment_counts.items():
    print(f"{sentiment}\t{count}")
