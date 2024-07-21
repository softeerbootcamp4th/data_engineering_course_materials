#!/usr/bin/env python3

import json
import sys

for line in sys.stdin:
    try:
        # JSON 형식의 줄을 파싱
        data = json.loads(line.strip())
        # 제품 ID와 평점 추출
        product_id = data.get("asin")
        rating = data.get("rating")
        # 제품 ID와 평점이 존재하는지 확인
        if product_id and rating is not None:
            print(f"{product_id}\t{rating}")
    except json.JSONDecodeError:
        continue
