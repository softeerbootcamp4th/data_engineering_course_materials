#!/usr/bin/env python3
import sys

prev_prod_id = None
cnt = 0
rating_total = 0.0

for line in sys.stdin:
    prod_id, rating = line.strip().split()
    try:
        rating = float(rating)
    except ValueError:
        continue

    if prev_prod_id == prod_id:
        cnt += 1
        rating_total += rating
    else:
        if prev_prod_id:
            print(f"{prev_prod_id}\t{cnt}\t{rating_total/cnt}")
        prev_prod_id = prod_id
        cnt = 1
        rating_total = rating

if prev_prod_id:
    print(f"{prev_prod_id}\t{cnt}\t{rating_total/cnt}")