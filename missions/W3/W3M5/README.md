# 1. Average Rating of Movies using MapReduce

# 2. File Upload
## 2.1. 디렉토리 생성
```bash
docker exec -it hadoop-master mkdir -p /usr/local/hadoop/mapreduce/movies/CSV
```
## 2.2. Docker로 File Copy
* mapper.py
```bash
docker cp scripts/mapper.py hadoop-master:/usr/local/hadoop/mapreduce/movies/mapper.py
```
* reducer.py
```bash
docker cp scripts/reducer.py  hadoop-master:/usr/local/hadoop/mapreduce/movies/reducer.py
```
* Twitter Sentiment Dataset
```bash
docker cp scripts/ratings.csv hadoop-master:/usr/local/hadoop/mapreduce/movies/CSV/ratings.csv
```

## 2.3. 컨테이너 접속
```bash
docker exec -it hadoop-master /bin/bash
```

### 2.3.1. 파일, 디렉토리 확인
```bash
ls -l /usr/local/hadoop/mapreduce/movies
```
```bash
ls -l /usr/local/hadoop/mapreduce/movies/CSV
```
### 2.3.2. 권한 설정
```bash
chmod 644 /usr/local/hadoop/mapreduce/movies/CSV/ratings.csv
```

# 3. HDFS
## 3.1. HDFS에 업로드
```bash
su - hdfs
```
```bash
hdfs dfs -mkdir -p /mapreduce/movies/CSV
```
```bash
hdfs dfs -put /usr/local/hadoop/mapreduce/movies/CSV/ratings.csv /mapreduce/movies/CSV
```
### 3.1.1. 잘 업로드 됐는지 확인
```bash
hdfs dfs -ls /mapreduce/movies/CSV
```

## 3.2. Mapreduce 실행
```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
    -input /mapreduce/movies/CSV/ratings.csv \
    -output /mapreduce/movies/output \
    -mapper /usr/local/hadoop/mapreduce/movies/mapper.py \
    -reducer /usr/local/hadoop/mapreduce/movies/reducer.py \
    -file /usr/local/hadoop/mapreduce/movies/mapper.py \
    -file /usr/local/hadoop/mapreduce/movies/reducer.py
```

## 3.3. Mapreduce 확인
```bash
hdfs dfs -cat /mapreduce/movies/output/part-00000
```

## 3.4. 로컬로 저장
```bash
hdfs dfs -get /mapreduce/movie/output/part-00000 /usr/local/hadoop/mapreduce/movies/output
```