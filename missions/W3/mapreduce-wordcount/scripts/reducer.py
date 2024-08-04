#!/usr/bin/env python3
import sys

current_word = None
current_count = 0
word = None

# 입력 데이터를 줄 단위로 읽음
for line in sys.stdin:
    # Mapper의 출력(단어와 카운트)을 탭('\t')을 기준으로 분할
    word, count = line.strip().split('\t', 1)

    # 문자열을 정수로 변환
    count = int(count)

    # 현재 단어와 이전 단어를 비교
    if current_word == word:
        current_count += count
    else:
        if current_word:
            # 이전 단어의 카운트를 출력
            print(f'{current_word}\t{current_count}')
        current_word = word
        current_count = count

# 마지막 단어의 카운트를 출력
if current_word == word:
    print(f'{current_word}\t{current_count}')
