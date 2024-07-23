#!/usr/bin/env python3
import sys

class MovieRatingMapper:
    def __init__(self, input_stream):
        self.input_stream = input_stream

    def map(self):
        for line in self.input_stream:
            line = line.strip()
            # Skip header or empty lines
            if line.startswith('#') or not line:
                continue
            # Split the line into fields
            fields = line.split(',')
            if len(fields) == 4:
                movie_id = fields[1].strip()
                rating = fields[2].strip()
                # Output movieId and rating as key-value pairs
                print(f'{movie_id}\t{rating}')

def main():
    mapper = MovieRatingMapper(sys.stdin)
    mapper.map()

if __name__ == "__main__":
    main()
