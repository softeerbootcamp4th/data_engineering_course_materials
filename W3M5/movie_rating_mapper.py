#!/usr/bin/env python3

import sys # 자연어 없음 -> 그냥 콤마로 잘라도 됨

def mapper():
    for line in sys.stdin:
        line = line.strip()
        parts = line.split(',')
        if parts[0] != 'userId':  # 헤더 무시
            movieId = parts[1]
            rating = parts[2]
            print(f'{movieId}\t{rating}')

if __name__ == '__main__':
    mapper()
