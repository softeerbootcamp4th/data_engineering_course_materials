#!/usr/bin/env python3

import sys
import re

def main():
    # stdin으로 한 줄씩 읽어서 처리
    for line in sys.stdin:
        line = line.strip()
        # 정규식 이용 단어 분리
        words = re.findall(r'\b\w+\b', line.lower())
        # 각 단어에 대해 (word, 1) 출력
        for word in words:
            print(f"{word}\t1")

if __name__ == "__main__":
    main()
