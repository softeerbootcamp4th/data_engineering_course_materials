#!/usr/bin/env python3

import sys
import re

class WordCountMapper:
    """
    Mapper class for word count
    """
    
    def __init__(self, input_stream):
        """
        Constructor
        
        :param input_stream: input stream
        """
        
        self.input_stream = input_stream


    def clean_word(self, word : str) -> str:
        """
        Clean word by removing special characters
        
        :param word: word to clean
        :return: cleaned word
        """
        
        # 정규 표현식을 사용하여 알파벳과 공백만 남기고 나머지는 제거
        return re.sub(r'[^a-zA-Z]', '', word)

    
    def read_input(self) -> iter:
        """
        Read input stream
        
        :return: generator of words
        """
        
        for line in self.input_stream:
            # Q. 문장 전처리를 여기서 수행 vs 전처리된 데이터를 받아서 수행?
            
            # 줄을 공백으로 분리하여 단어를 추출
            words = line.split()
            
            # 특수문자를 제거하고 알파벳만 남긴 단어를 필터링
            cleaned_words = [self.clean_word(word) for word in words if self.clean_word(word)]
            yield cleaned_words


    def map(self) -> None:
        """
        Map function
        """
        
        data = self.read_input()
        for words in data:
            for word in words:
                print(f'{word}\t1')


def main() -> None:
    """
    Main function
    """
    
    mapper = WordCountMapper(sys.stdin)
    mapper.map()


if __name__ == "__main__":
    """
    Entry point
    """
    
    main()
