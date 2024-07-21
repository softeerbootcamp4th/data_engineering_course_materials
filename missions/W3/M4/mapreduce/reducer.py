#!/usr/bin/env python3
import sys

class SentimentReducer:
    def __init__(self, input_stream):
        self.input_stream = input_stream

    def reduce(self):
        current_sentiment = None
        current_count = 0

        for line in self.input_stream:
            line = line.strip()
            if not line:
                continue
            
            try:
                sentiment, count = line.split('\t', 1)
                count = int(count)
            except ValueError:
                # Skip lines that don't match the expected format
                continue

            if current_sentiment == sentiment:
                current_count += count
            else:
                if current_sentiment is not None:
                    print(f'{current_sentiment}\t{current_count}')
                current_sentiment = sentiment
                current_count = count

        # Print the final count for the last sentiment
        if current_sentiment is not None:
            print(f'{current_sentiment}\t{current_count}')

def main():
    reducer = SentimentReducer(sys.stdin)
    reducer.reduce()

if __name__ == "__main__":
    main()
