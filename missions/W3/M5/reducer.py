#!/usr/bin/env python3

import sys

current_movie_id = None
total_rating = 0
count = 0

for line in sys.stdin:
    # 입력 줄에서 앞뒤 공백 제거
    line = line.strip()

    # 탭으로 분리
    movie_id, rating = line.split('\t')

    # 문자열을 숫자로 변환
    rating = float(rating)

    # 새로운 movie_id를 만나면 이전 movie_id의 평균 계산
    if current_movie_id and current_movie_id != movie_id:
        average_rating = total_rating / count
        print(f'{current_movie_id}\t{average_rating:.2f}')
        total_rating = 0
        count = 0

    # 현재 movie_id 업데이트
    current_movie_id = movie_id
    total_rating += rating
    count += 1

# 마지막 movie_id 처리
if current_movie_id:
    average_rating = total_rating / count
    print(f'{current_movie_id}\t{average_rating:.2f}')