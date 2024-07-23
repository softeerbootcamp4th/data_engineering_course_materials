#!/usr/bin/env python3

import sys

class ReviewReducer:
    def __init__(self, input_stream):
        self.input_stream = input_stream

    def reduce(self):
        current_asin = None
        current_count = 0
        current_sum = 0.0

        for line in self.input_stream:
            asin, rating = line.strip().split('\t')
            rating = float(rating)

            if current_asin == asin:
                current_count += 1
                current_sum += rating
            else:
                if current_asin:
                    average_rating = current_sum / current_count
                    print(f"{current_asin}\t{current_count}\t{average_rating:.2f}")

                current_asin = asin
                current_count = 1
                current_sum = rating

        if current_asin:
            average_rating = current_sum / current_count
            print(f"{current_asin}\t{current_count}\t{average_rating:.2f}")

if __name__ == "__main__":
    reducer = ReviewReducer(sys.stdin)
    reducer.reduce()
