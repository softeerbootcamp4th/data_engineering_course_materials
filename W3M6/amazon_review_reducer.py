#!/usr/bin/env python3

import sys

def reducer():
    current_asin = None
    total_rating = 0
    total_count = 0
    
    for line in sys.stdin:
        line = line.strip()
        asin, rating = line.split('\t')
        rating = float(rating)
        
        if current_asin == asin:
            total_rating += rating
            total_count += 1
        else:
            if current_asin:
                # 이전 결과
                print(f'{current_asin}\t{total_count}\t{total_rating/total_count:.1f}')
            current_asin = asin
            total_rating = rating
            total_count = 1
    
    # last
    if current_asin:
        print(f'{current_asin}\t{total_count}\t{total_rating/total_count:.1f}')

if __name__ == '__main__':
    reducer()
