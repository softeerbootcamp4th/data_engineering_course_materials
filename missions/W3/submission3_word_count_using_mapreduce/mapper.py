#!/usr/bin/env python3

import sys


class Mapper:
    def map(self):
        for line in sys.stdin:
            line = line.strip()
            words = line.split()
            for word in words:
                print(f'{word}\t1')


if __name__ == "__main__":
    mapper = Mapper()
    mapper.map()
