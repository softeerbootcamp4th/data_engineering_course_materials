#!/usr/bin/env python3

import sys

def reducer():
    current_movie = None
    current_sum = 0
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        movieId, rating = line.split('\t')

        try:
            rating = float(rating)
        except ValueError:
            continue

        if current_movie == movieId:
            current_sum += rating
            current_count += 1
        else:
            if current_movie is not None:
                print(f'{current_movie}\t{current_sum / current_count}')
            current_movie = movieId
            current_sum = rating
            current_count = 1

    # 마지막 영화의 평균 평점 출력
    if current_movie is not None:
        print(f'{current_movie}\t{current_sum / current_count}')

if __name__ == '__main__':
    reducer()
