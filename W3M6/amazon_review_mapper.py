#!/usr/bin/env python3
import sys
import json


def mapper():
    for line in sys.stdin:
        try:
            data = json.loads(line.strip())
            asin = data.get('asin')
            rating = data.get('rating')
            print(f'{asin}\t{rating}')
        except Exception:
            continue

if __name__ == "__main__":
    mapper()