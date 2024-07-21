#!/usr/bin/env python3

import sys

def map_function():
    for line in sys.stdin:
        parts = line.strip().split(',', 5)  # 변경: 5개로 split하고 나머지는 그대로 둠
        if len(parts) > 5:
            sentiment = parts[0].strip('"')  # 감정값을 추출
            if sentiment == '0':
                print('negative\t1')
            elif sentiment == '2':
                print('neutral\t1')
            elif sentiment == '4':
                print('positive\t1')

if __name__ == "__main__":
    map_function()
