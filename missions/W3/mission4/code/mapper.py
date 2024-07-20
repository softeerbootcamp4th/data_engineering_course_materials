#!/usr/bin/env python3
import sys
import csv

reader = csv.reader(sys.stdin, delimiter=',')

for line in reader:
    sentiment, _, _, _, _, _ = line
    if sentiment == '0':
        sentiment_str = 'negative'
    elif sentiment == '2':
        sentiment_str = 'neutral'
    else:
        sentiment_str = 'positive'
    print(sentiment_str, '\t', 1)