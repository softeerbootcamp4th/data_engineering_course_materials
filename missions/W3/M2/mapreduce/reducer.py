#!/usr/bin/env python

import sys

# 리듀스 함수: 각 단어별로 빈도수를 합산하여 출력
def main():
    current_word = None
    current_count = 0
    word = None

    # 표준 입력으로부터 각 줄을 읽어서 처리
    for line in sys.stdin:
        # 줄을 공백으로 분리하여 단어와 빈도수를 추출
        line = line.strip()
        word, count = line.split('\t', 1)

        # 현재 단어와 새로운 단어가 다를 경우
        if current_word != word:
            # 새로운 단어가 등장하면 기존 단어의 결과를 출력
            if current_word:
                print('%s\t%s' % (current_word, current_count))
            current_count = 0
            current_word = word

        # 단어의 빈도수를 합산
        current_count += int(count)

    # 마지막 단어에 대한 결과 출력
    if current_word == word:
        print('%s\t%s' % (current_word, current_count))

if __name__ == "__main__":
    main()
