#!/usr/bin/env python3
import sys

current_product = None
sum_of_ratings = 0
count = 0
product = None

for line in sys.stdin:
    line = line.strip()
    try:
        product, count = line.split('\t', 2)
        count = float(count)
    except Exception as e:
        print(e)
        continue

    if current_product == product:
        sum_of_ratings += count
        count += 1
    else:
        if current_product:
            print(f'{current_product}\t{count}\t{sum_of_ratings/count}')
        current_product = product
        sum_of_ratings = count
        count = 1

if current_product == product:
    print(f'{current_product}\t{count}\t{sum_of_ratings/count}')


