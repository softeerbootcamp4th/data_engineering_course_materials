#!/usr/bin/env python3

import sys
import json

class ReviewMapper:
    def __init__(self, input_stream):
        self.input_stream = input_stream

    def map(self):
        for line in self.input_stream:
            try:
                review = json.loads(line)
                asin = review.get("asin")
                rating = review.get("rating")
                if asin and rating is not None:
                    print(f"{asin}\t{rating}")
            except json.JSONDecodeError:
                continue

if __name__ == "__main__":
    mapper = ReviewMapper(sys.stdin)
    mapper.map()
