#!/usr/bin/env python3
import sys


def reducer():
    current_product = None
    current_count = 0
    current_sum = 0.0

    for line in sys.stdin:
        product_id, rating = line.strip().split("\t")
        try:
            rating = float(rating)
        except ValueError:
            continue

        if current_product == product_id:
            current_count += 1
            current_sum += rating
        else:
            if current_product:
                avg_rating = current_sum / current_count
                print(f"{current_product}\t{current_count}\t{avg_rating}")
            current_product = product_id
            current_count = 1
            current_sum = rating

    if current_product:
        avg_rating = current_sum / current_count
        print(f"{current_product}\t{current_count}\t{avg_rating}")


if __name__ == "__main__":
    reducer()
