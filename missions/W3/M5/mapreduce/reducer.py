#!/usr/bin/env python3
import sys

class MovieRatingReducer:
    def __init__(self, input_stream):
        self.input_stream = input_stream

    def reduce(self):
        current_movie_id = None
        total_rating = 0
        count = 0

        for line in self.input_stream:
            line = line.strip()
            movie_id, rating = line.split('\t', 1)

            try:
                rating = float(rating)
            except ValueError:
                continue

            if current_movie_id == movie_id:
                total_rating += rating
                count += 1
            else:
                if current_movie_id:
                    # Output the average rating for the previous movie_id
                    average_rating = total_rating / count
                    print(f'{current_movie_id}\t{average_rating}')
                # Reset for the new movie_id
                current_movie_id = movie_id
                total_rating = rating
                count = 1

        # Output the average rating for the last movie_id
        if current_movie_id:
            average_rating = total_rating / count
            print(f'{current_movie_id}\t{average_rating}')

def main():
    reducer = MovieRatingReducer(sys.stdin)
    reducer.reduce()

if __name__ == "__main__":
    main()
