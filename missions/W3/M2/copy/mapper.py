#!/usr/bin/env python

import sys

# 표준 입력으로부터 데이터를 읽어서 처리하는 함수
def read_input(file):
    for line in file:
        # 각 줄을 공백으로 분리하여 단어를 추출
        yield line.split()

# 맵 함수: 각 단어를 (단어, 1) 쌍으로 출력
def main():
    data = read_input(sys.stdin)
    for words in data:
        for word in words:
            # 단어 출력
            print('%s\t%s' % (word, 1))

if __name__ == "__main__":
    main()
