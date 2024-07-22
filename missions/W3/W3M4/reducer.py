#!/usr/bin/env python3

import sys

current_sentiment = None
current_count = 0
sentiment_counts = {
    'positive': 0,
    'negative': 0,
    'neutral': 0
}

# Read from standard input
for line in sys.stdin:
    line = line.strip()
    
    sentiment = line.split('\t')[1]
    
    # Count the occurrences of each sentiment
    if sentiment in sentiment_counts:
        sentiment_counts[sentiment] += 1

# Output the final counts for each sentiment
for sentiment, count in sentiment_counts.items():
    print(f"{sentiment}\t{count}")

