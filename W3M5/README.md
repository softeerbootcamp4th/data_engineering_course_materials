# Average Rating of Movies using MapReduce

## Directotry

```
+ twitter_sentiment_analysis_using_mapreduce
    - movie_rating_mapper.py
    - movie_rating_reducer.py
    - movie_rating_mapred_script.sh
    - movie_rating.csv
    - movie_rating_sample.csv (디버그용 작은 샘플)
    + movie_rating_output
        - _SUCCESS
        - part-00000 (결과)
    + node
        - Dockerfile
        - hadoop-3.3.6.tar.gz
        - start-hadoop.sh
        + config
            - core-site.xml
            - hdfs-site.xml
            - mapred-site.xml
            - yarn-site.xml
    - docker-compose.yml
```

```
# container directory - 컨테이너 로컬 파일 시스템에선 temp 폴더만 사용

+ temp
    - ratings.csv
    - movie_rating_mapper.py
    - movie_rating_reducer.py
    + movie_rating_output (mapreduce 작업 이후 생성된 디렉터리를 컨테이너 로컬 파일 시스템으로 가져옴)
        - _SUCCESS
        - part-00000
```

```
# hdfs directory 

+ movie_rating_dir
    - ratings.csv
+ movie_rating_output (mapred 작업 후 생성 - 미리 존재하면 안됨 !)
    - _SUCCESS
    - part-00000
```

### movie_rating_mapper.py

```python
#!/usr/bin/env python3

import sys # 자연어 없음 -> 그냥 콤마로 잘라도 됨

def mapper():
    for line in sys.stdin:
        line = line.strip()
        parts = line.split(',')
        if parts[0] != 'userId':  # 헤더 무시
            movieId = parts[1]
            rating = parts[2]
            print(f'{movieId}\t{rating}')

if __name__ == '__main__':
    mapper()
```

### movie_rating_reducer.py

```python
#!/usr/bin/env python3

import sys

def reducer():
    current_movie = None
    current_sum = 0
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        movieId, rating = line.split('\t')

        try:
            rating = float(rating)
        except ValueError:
            continue

        if current_movie == movieId:
            current_sum += rating
            current_count += 1
        else:
            if current_movie is not None:
                print(f'{current_movie}\t{current_sum / current_count}')
            current_movie = movieId
            current_sum = rating
            current_count = 1

    # 마지막 영화의 평균 평점 출력
    if current_movie is not None:
        print(f'{current_movie}\t{current_sum / current_count}')

if __name__ == '__main__':
    reducer()
```

- MapReduce에서 데이터 스트림을 처리할 때, 입력 데이터가 키에 따라 정렬되어 리듀서로 전달
- 리듀서는 특정 키(여기서는 영화 ID)에 대한 모든 값(여기서는 평점)을 받고, 다음 키를 받기 전까지는 이전 키의 평균을 계산할 수 없음 !
- 그래서 마지막 키에 대한 처리가 별도로 필요

### movie_rating_mapred_script.sh

- 과정요약

    1. 컨테이너 내부로 ratings.csv, mapper, reducer 복사
    2. HDFS에 ratings.csv 업로드
    3. MapReduce 실행
    4. 결과를 호스트 머신으로 가져옴

```sh
#!/bin/bash


##### 컨테이너 내부로 tweets, mapper, reducer 복사

# tweets 컨테이너 내부로 복사
docker cp ratings.csv hadoop-master:/temp

# mapper, reducer 컨테이너 내부로 복사
docker cp movie_rating_mapper.py hadoop-master:/temp/movie_rating_mapper.py 
docker cp movie_rating_reducer.py hadoop-master:/temp/movie_rating_reducer.py

### 해당 파일들을 실행 가능한 파일로 변경 (chmod +x)
### !!!!!! #!/usr/bin/env python3 필수 !!!!!!!!
docker exec -it hadoop-master sudo chmod +x /temp/movie_rating_mapper.py /temp/movie_rating_reducer.py

##### HDFS에 tweets 옮기기

# hdfs에 tweets directory 생성
docker exec -it hadoop-master hdfs dfs -mkdir -p /movie_rating_dir

# 해당 디렉토리로 tweets 옮기기
docker exec -it hadoop-master hdfs dfs -put /temp/ratings.csv /movie_rating_dir


##### MapReduce 작업 실행
# movie_rating_output 디렉토리는 생성됨
docker exec -it hadoop-master hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -input /movie_rating_dir/ratings.csv \
  -output /movie_rating_output \
  -mapper movie_rating_mapper.py \
  -reducer movie_rating_reducer.py \
  -file /temp/movie_rating_mapper.py \
  -file /temp/movie_rating_reducer.py


##### 호스트 머신으로 결과 가져오기

# 컨테이너 로컬 파일 시스템의 /temp의 소유권을 hadoopuser로 변경
docker exec -it hadoop-master sudo chown hadoopuser:hadoopuser temp

# HDFS의 movie_rating_output 디렉토리를 컨테이너의 로컬 디렉토리로 가져옴
docker exec -it hadoop-master hdfs dfs -get /movie_rating_output /temp

# 결과를 호스트 머신(Mac)의 현재 폴더로 가져옴
docker cp hadoop-master:/temp/movie_rating_output .
```