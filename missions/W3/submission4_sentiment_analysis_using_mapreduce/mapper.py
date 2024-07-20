#!/usr/bin/env python3
import sys
import csv

# Predefined keywords for sentiment classification
POSITIVE_KEYWORDS = {'good', 'happy', 'love', 'excellent', 'great'}
NEGATIVE_KEYWORDS = {'bad', 'sad', 'hate', 'terrible', 'poor'}


def classify_sentiment(text):
    words = set(text.lower().split())
    if POSITIVE_KEYWORDS.intersection(words):
        return 'positive'
    elif NEGATIVE_KEYWORDS.intersection(words):
        return 'negative'
    else:
        return 'neutral'


def mapper():
    reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
    for row in reader:
        if len(row) < 6:
            continue
        text = row[5]
        sentiment = classify_sentiment(text)
        print(f"{sentiment}\t1")


if __name__ == "__main__":
    mapper()
