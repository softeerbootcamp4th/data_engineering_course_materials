#!/usr/bin/env python3

import sys
import csv

# Define keywords for positive and negative sentiments
positive_keywords = ['good', 'great', 'happy', 'love', 'awesome', 'amazing', 'nice', 'fine', 'yay', 'excellent', 'best', 'cool', 'fantastic']
negative_keywords = ['bad', 'sad', 'upset', 'angry', 'bummed', 'hate', 'terrible', 'awful', 'worst', 'cry', 'itchy', 'mad', 'blah']

def determine_sentiment(text):
    # Lowercase the text to ensure the keywords match regardless of case
    text = text.lower()
    
    # Check for positive keywords
    for word in positive_keywords:
        if word in text:
            return 'positive'
    
    # Check for negative keywords
    for word in negative_keywords:
        if word in text:
            return 'negative'
    
    # If no keywords are found, return 'neutral'
    return 'neutral'

# Read from standard input (which will be the input file)
for line in sys.stdin:
    line = line.strip()
    reader = csv.reader([line])
    for row in reader:
        if len(row) == 6:
            sentiment = determine_sentiment(row[5])
            print(f"{row[5]}\t{sentiment}")

