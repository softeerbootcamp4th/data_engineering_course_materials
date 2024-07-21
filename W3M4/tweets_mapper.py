#!/usr/bin/env python3

import csv
import sys
import re

def classify(text, positive_keywords, negative_keywords):
    # lower
    text = text.lower()
    # divide
    words = re.findall(r'\w+', text)
    positive_matches = any(key in words for key in positive_keywords)
    negative_matches = any(key in words for key in negative_keywords)
    if positive_matches and not negative_matches:
        return 'positive'
    elif negative_matches and not positive_matches:
        return 'negative'
    else:
        return 'neutral'

def main():

    # predefined keywords
    positive_keywords = {"happy", "great", "love", "excellent", "good"}
    negative_keywords = {"sad", "bad", "hate", "terrible", "worse"}
    
    reader = csv.reader(sys.stdin)
    for row in reader:
        tweet_text = row[5]
        sentiment = classify(tweet_text, positive_keywords, negative_keywords)
        print(f'{sentiment}\t1')

if __name__ == "__main__":
    main()


## 분명 mapper 에서 에러가 나는건데... yarn 에서 확인했는데 ...
## cat tweets.csv | python3 tweets_mapper.py | sort | python3 tweets_reducer.py
## 분명 전수조사까지 했는데...왜...

################### 중요 !!!!!!!!!!!!
#### #!/usr/bin/env python3 <== 필수였음 !!!!!!!!