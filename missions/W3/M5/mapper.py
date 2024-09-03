#!/usr/bin/env python3

import sys

# 첫 줄 여부를 확인하기 위한 플래그
is_first_line = True

for line in sys.stdin:
    # 입력 줄에서 앞뒤 공백 제거
    line = line.strip()
    # 첫 줄(헤더)인 경우 스킵
    if is_first_line:
        is_first_line = False
        continue
    # 콤마로 분리
    user_id, movie_id, rating, timestamp = line.split(',')

    # movie_id와 rating만 출력
    print(f'{movie_id}\t{rating}')