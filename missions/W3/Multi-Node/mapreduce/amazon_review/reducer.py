#!/usr/bin/python3

from sys import stdin

current_product_id = None
current_rating = 0
current_count = 0
product_id = None

for line in stdin:
    line = line.strip()
    product_id, rating, count = line.split('\t')

    try:
        rating = float(rating)
        count = int(count)
    except ValueError:
        continue

    if current_product_id == product_id:
        current_rating += rating
        current_count += count
    else:
        if current_product_id is not None and current_count > 0:
            average_rating = current_rating / current_count
            print(f'{current_product_id}\t{current_count}\t{average_rating:.1f}')
        current_product_id = product_id
        current_rating = rating
        current_count = count

if current_product_id == product_id and current_count > 0:
    average_rating = current_rating / current_count
    print(f'{current_product_id}\t{current_count}\t{average_rating:.1f}')
