#!/usr/bin/env python3
import sys


def reducer():
    current_movie_id = None
    current_sum = 0
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        movie_id, rating = line.split('\t')

        try:
            rating = float(rating)
        except ValueError:
            continue

        if current_movie_id == movie_id:
            current_sum += rating
            current_count += 1
        else:
            if current_movie_id:
                average_rating = current_sum / current_count
                print(f'{current_movie_id}\t{average_rating}')
            current_movie_id = movie_id
            current_sum = rating
            current_count = 1

    if current_movie_id == movie_id:
        average_rating = current_sum / current_count
        print(f'{current_movie_id}\t{average_rating}')


if __name__ == "__main__":
    reducer()
