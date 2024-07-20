#!/usr/bin/python3

from sys import stdin

current_movie_id = None
current_rating = 0
current_count = 0
movie_id = None

for line in stdin:
    line = line.strip()
    movie_id, rating, count = line.split('\t')

    try:
        rating = float(rating)
        count = float(count)
    except ValueError:
        continue

    if current_movie_id == movie_id:
        current_rating += rating
        current_count += count
    else:
        if current_movie_id is not None and current_count > 0:
            average_rating = current_rating / current_count
            print(f'{current_movie_id}\t{average_rating:.1f}')
        current_movie_id = movie_id
        current_rating = rating
        current_count = count

if current_movie_id == movie_id and current_count > 0:
    average_rating = current_rating / current_count
    print(f'{current_movie_id}\t{average_rating:.1f}')
