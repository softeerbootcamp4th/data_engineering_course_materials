#!/usr/bin/env python3
import sys
import os

import zipfile


# 압축 파일을 해제하는 함수
def unzip_env(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


# 현재 파일의 디렉토리를 기준으로 경로 설정
current_dir = os.path.dirname(__file__)
zip_path = os.path.join(current_dir, 'sentiment_env.zip')
extract_to = os.path.join(current_dir, 'sentiment_env')

# 가상 환경 압축 파일 해제
unzip_env(zip_path, extract_to)

# 가상 환경의 패키지 경로를 sys.path에 추가
sys.path.insert(0, extract_to)
from afinn import Afinn

# Initialize the Afinn sentiment analyzer
afinn = Afinn()


def classify_sentiment(tweet):
    sentiment_score = afinn.score(tweet)
    if sentiment_score > 0:
        return 'positive'
    elif sentiment_score < 0:
        return 'negative'
    else:
        return 'neutral'


for line in sys.stdin:
    line = line.strip()
    tweet = line.split(',')[-1]
    sentiment = classify_sentiment(tweet)
    print(f"{sentiment}\t1")
