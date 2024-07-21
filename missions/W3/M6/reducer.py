#!/usr/bin/env python3

import sys

current_product = None
current_count = 0
current_sum = 0.0

for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) != 2:
        continue

    product_id, rating = parts
    try:
        rating = float(rating)
    except ValueError:
        continue

    if current_product is None:
        current_product = product_id

    if product_id != current_product:
        if current_count > 0:
            average_rating = current_sum / current_count
            print(f"{current_product}\t{current_count}\t{average_rating}")

        current_product = product_id
        current_count = 0
        current_sum = 0.0

    current_count += 1
    current_sum += rating

if current_product is not None and current_count > 0:
    average_rating = current_sum / current_count
    print(f"{current_product}\t{current_count}\t{average_rating}")
