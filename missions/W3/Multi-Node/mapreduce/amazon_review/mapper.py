#!/usr/bin/python3

import json
from sys import stdin

for line in stdin:
    line = line.strip()
    
    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        continue

    product_id = obj['asin']
    rating = obj['rating']

    print(f'{product_id}\t{rating}\t1')
