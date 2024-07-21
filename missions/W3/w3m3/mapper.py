
#!/usr/bin/env python3

import sys
import re

def map_function():
    for line in sys.stdin:
        line = line.strip()
        words = re.findall(r'\w+', line)
        for word in words:
            print(f"{word.lower()}\t1")

if __name__ == "__main__":
    map_function()