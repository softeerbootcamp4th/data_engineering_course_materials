#!/usr/bin/env python3
import sys

class SentimentMapper:
    def __init__(self, input_stream):
        self.input_stream = input_stream

    def map(self):
        for line in self.input_stream:
            line = line.strip()  # Strip leading/trailing whitespace
            if not line:  # Skip empty lines
                continue
            
            fields = line.split(",")
            
            if len(fields) > 0:
                sentiment = fields[0].strip()
                if sentiment == "\"0\"":
                    print('negative\t1')
                elif sentiment == "\"2\"":
                    print('neutral\t1')
                elif sentiment == "\"4\"":
                    print('positive\t1')

def main():
    mapper = SentimentMapper(sys.stdin)
    mapper.map()

if __name__ == "__main__":
    main()
