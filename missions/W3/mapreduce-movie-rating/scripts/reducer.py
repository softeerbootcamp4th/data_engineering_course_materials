#!/usr/bin/env python3
import sys

current_movie = None
current_rating = 0
count = 0
movie = None

for line in sys.stdin:
    line = line.strip()
    try:
        movie, rating = line.split('\t', 1)
        rating = float(rating)
    except:
        continue


    if current_movie == movie:
        current_rating += rating
        count += 1
    else:
        if current_movie:
            print(f'{current_movie}\t{current_rating / count}')
        current_movie = movie
        current_rating = rating
        count = 1

if current_movie == movie:
    print(f'{current_movie}\t{current_rating / count}')



