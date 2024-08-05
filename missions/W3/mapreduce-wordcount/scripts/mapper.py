#!/usr/bin/env python3
import sys

# 입력 데이터를 줄 단위로 읽음
for line in sys.stdin:
    # 줄을 공백을 기준으로 단어로 분할
    words = line.strip().split()

    # 각 단어에 대해 "word\t1" 형식으로 출력
    for word in words:
        print(f'{word}\t1')
