#!/usr/bin/python3

from sys import stdin

current_word = None
current_count = 0
word = None

for line in stdin:
    line = line.strip()
    word, count = line.split('\t')

    try:
        count = int(count)
    except ValueError:
        continue

    if current_word == word:
        current_count += count
    else:
        if current_word is not None:
            print(f'{current_word}\t{str(current_count)}')
        current_word = word
        current_count = count

if current_word == word:
    print(f'{current_word}\t{str(current_count)}')
