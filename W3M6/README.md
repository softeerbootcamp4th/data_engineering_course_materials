# Amazon Product Review using MapReduce

## Directory

```
+ amazon_product_review_using_mapreduce
    + node
        + config
            - core-site.xml
            - hdfs-site.xml
            - mapred-site.xml
            - yarn-site.xml
        - Docker
        - hadoop-3.3.6.tar.gz
        - start-hadoop.sh
    - docker-compose.yml
    + amazon_reviews
        - All_Beauty.jsonl
        - Amazon_Fashion.jsonl
        - Appliances.jsonl
    - amazon_review_mapper.py
    - amazon_review_reducer.py
    - amazon_review_mapred_script.sh
```

## amazon_review_mapper.py

```python
#!/usr/bin/env python3
import sys
import json


def mapper():
    for line in sys.stdin:
        try:
            data = json.loads(line.strip())
            asin = data.get('asin')
            rating = data.get('rating')
            print(f'{asin}\t{rating}')
        except Exception:
            continue

if __name__ == "__main__":
    mapper()
```

## amazon_review_reducer

```python
#!/usr/bin/env python3

import sys

def reducer():
    current_asin = None
    total_rating = 0
    total_count = 0
    
    for line in sys.stdin:
        line = line.strip()
        asin, rating = line.split('\t')
        rating = float(rating)
        
        if current_asin == asin:
            total_rating += rating
            total_count += 1
        else:
            if current_asin:
                # 이전 결과
                print(f'{current_asin}\t{total_count}\t{total_rating/total_count:.1f}')
            current_asin = asin
            total_rating = rating
            total_count = 1
    
    # last
    if current_asin:
        print(f'{current_asin}\t{total_count}\t{total_rating/total_count:.1f}')

if __name__ == '__main__':
    reducer()
```

## amazon_review_mapred_script_sh

- 과정 요약
    1. 컨테이너 내부로 amazon_reviews, mapper, reducer 복사
    2. HDFS에 amazon_reviews 업로드
    3. MapReduce 실행
    4. 결과를 호스트 머신으로 가져옴
    
```sh
#!/bin/bash


##### 컨테이너 내부로 amazon_reviews, mapper, reducer 복사

# amazon_reviwes를 컨테이너 내부로 복사
docker cp amazon_reviews hadoop-master:/temp

# mapper, reducer 컨테이너 내부로 복사
docker cp amazon_review_mapper.py hadoop-master:/temp/amazon_review_mapper.py 
docker cp amazon_review_reducer.py hadoop-master:/temp/amazon_review_reducer.py

### 해당 파일들을 실행 가능한 파일로 변경 (chmod +x)
### !!!!!! #!/usr/bin/env python3 필수 !!!!!!!!
docker exec -it hadoop-master sudo chmod +x /temp/amazon_review_mapper.py /temp/amazon_review_reducer.py

##### HDFS에 amazon_reviews 옮기기

# hdfs에 tweets directory 생성
docker exec -it hadoop-master hdfs dfs -mkdir -p /amazon_review_dir 

# 해당 디렉토리로 tweets 옮기기
docker exec -it hadoop-master hdfs dfs -put /temp/amazon_reviews /amazon_review_dir


##### MapReduce 작업 실행
# amazon_review_output 디렉토리는 생성됨
docker exec -it hadoop-master hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -input /amazon_review_dir/amazon_reviews/* \
  -output /amazon_review_output \
  -mapper amazon_review_mapper.py \
  -reducer amazon_review_reducer.py \
  -file /temp/amazon_review_mapper.py \
  -file /temp/amazon_review_reducer.py

##### 호스트 머신으로 결과 가져오기

# 컨테이너 로컬 파일 시스템의 /temp의 소유권을 hadoopuser로 변경
docker exec -it hadoop-master sudo chown hadoopuser:hadoopuser temp

# HDFS의 amazon_review_output 디렉토리를 컨테이너의 로컬 디렉토리로 가져옴
docker exec -it hadoop-master hdfs dfs -get /amazon_review_output /temp

# 결과를 호스트 머신(Mac)의 현재 폴더로 가져옴
docker cp hadoop-master:/temp/amazon_review_output .
```