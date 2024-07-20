#!/usr/bin/env python3
import sys
import csv


def mapper():
    reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
    for row in reader:
        if len(row) < 4:
            continue
        product_id = row[1]
        rating = row[2]

        print(f'{product_id}\t{rating}')


if __name__ == "__main__":
    mapper()
