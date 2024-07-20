#!/usr/bin/env python3
import sys


def reducer():
    current_sentiment = None
    current_count = 0

    for line in sys.stdin:
        sentiment, count = line.strip().split('\t')
        count = int(count)

        if current_sentiment == sentiment:
            current_count += count
        else:
            if current_sentiment:
                print(f"{current_sentiment}\t{current_count}")
            current_sentiment = sentiment
            current_count = count

    if current_sentiment:
        print(f"{current_sentiment}\t{current_count}")


if __name__ == "__main__":
    reducer()
