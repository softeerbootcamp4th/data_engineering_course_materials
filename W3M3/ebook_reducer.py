#!/usr/bin/env python3

import sys

def main():
    current_word = None
    current_count = 0
    word = None

    # stdin으로 한 줄씩 읽어서 처리
    for line in sys.stdin:
        line = line.strip()
        # 입력 데이터 -> (word, count) 
        word, count = line.split('\t', 1)

        # count를 정수로 변환
        try:
            count = int(count)
        except ValueError:
            continue

        # 현재 단어와 새 단어가 같다면 카운트 누적
        if current_word == word:
            current_count += count
        else:
            # 새 단어가 나타나면 이전 단어와 그 카운트 출력
            if current_word:
                print(f"{current_word}\t{current_count}")
            current_word = word
            current_count = count

    # 마지막 단어 출력
    if current_word == word:
        print(f"{current_word}\t{current_count}")

if __name__ == "__main__":
    main()
