#!/usr/bin/env python3
from collections import defaultdict
import sys

rating_counts = defaultdict(int)
rating_sums = defaultdict(float)

for line in sys.stdin:
    try:
        # Remove whitespaces and split the line
        line = line.strip()
        movieId, rating = line.split('\t')
        movieId = int(movieId)
        rating = float(rating)
    except:
        continue

    # Add the count word-wise
    rating_counts[movieId] += 1
    rating_sums[movieId] += rating

assert rating_counts.keys() == rating_sums.keys()

# Output movie ID and rating (Sorted by movie ID in numerical order)
for movieId in sorted(rating_sums.keys()): 
    print(movieId, round(rating_sums[movieId]/rating_counts[movieId],1))