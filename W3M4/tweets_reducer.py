#!/usr/bin/env python3

import sys

def read_input(file):
    for line in file:
        yield line.strip().split('\t')

def main():
    current_word = None
    current_count = 0
    word = None

    data = read_input(sys.stdin)
    for word, count in data:
        try:
            count = int(count)
        except ValueError:
            continue

        if current_word == word:
            current_count += count
        else:
            if current_word:
                print(f'{current_word}\t{current_count}')
            current_count = count
            current_word = word

    if current_word == word:
        print(f'{current_word}\t{current_count}')

if __name__ == "__main__":
    main()
