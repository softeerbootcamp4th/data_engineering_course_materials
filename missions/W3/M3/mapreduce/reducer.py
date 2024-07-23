#!/usr/bin/env python3

import sys

class WordCountReducer:
    def __init__(self, input_stream):
        self.input_stream = input_stream

    def reduce(self):
        current_word = None
        current_count = 0
        word = None

        for line in self.input_stream:
            line = line.strip()
            word, count = line.split('\t', 1)

            if current_word != word:
                if current_word:
                    print(f'{current_word}\t{current_count}')
                current_count = 0
                current_word = word

            current_count += int(count)

        if current_word == word:
            print(f'{current_word}\t{current_count}')

def main():
    reducer = WordCountReducer(sys.stdin)
    reducer.reduce()

if __name__ == "__main__":
    main()
