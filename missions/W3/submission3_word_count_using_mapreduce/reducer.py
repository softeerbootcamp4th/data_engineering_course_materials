#!/usr/bin/env python3

import sys


class Reducer:
    def __init__(self):
        self.current_word = None
        self.current_count = 0

    def reduce(self):
        for line in sys.stdin:
            line = line.strip()
            word, count = line.split('\t', 1)
            try:
                count = int(count)
            except ValueError:
                continue

            if self.current_word == word:
                self.current_count += count
            else:
                if self.current_word:
                    print(f'{self.current_word}\t{self.current_count}')
                self.current_count = count
                self.current_word = word

        if self.current_word == word:
            print(f'{self.current_word}\t{self.current_count}')


if __name__ == "__main__":
    reducer = Reducer()
    reducer.reduce()
