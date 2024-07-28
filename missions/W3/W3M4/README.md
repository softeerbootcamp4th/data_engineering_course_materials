# 1. Sentiment140 dataset with 1.6 million tweets Download

# 2. File Upload
## 2.1. 디렉토리 생성
```bash
docker exec -it hadoop-master mkdir -p /usr/local/hadoop/mapreduce/twitter
```
## 2.2. Docker로 File Copy
* mapper_twitter.py
```bash
docker cp scripts/mapper_twitter.py hadoop-master:/usr/local/hadoop/mapreduce/twitter
```
* reducer_twitter.py
```bash
docker cp scripts/reducer_twitter.py  hadoop-master:usr/local/hadoop/mapreduce/twitter
```
* Twitter Sentiment Dataset
```bash
docker cp Twitter_Sentiment_Dataset.csv hadoop-master:usr/local/hadoop/mapreduce/twitter/input
```

## 2.3. 컨테이너 접속
```bash
docker exec -it hadoop-master /bin/bash
```

### 2.3.1. 파일, 디렉토리 확인
```bash
ls -l /usr/local/hadoop/mapreduce/twitter
```

# 3. HDFS
## 3.1. HDFS에 업로드
```bash
hdfs dfs -put /usr/local/hadoop/mapreduce/twitter/input/Twitter_Sentiment_Dataset.csv /mapreduce/twitter/input
```
### 3.1.1. 잘 업로드 됐는지 확인
```bash
hdfs dfs -ls /mapreduce/twitter/input
```

## 3.2. hdfs user로 접속
```bash
su - hdfs
```

## 3.3. Mapreduce 실행
```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
    -input /mapreduce/twitter/input/Twitter_Sentiment_Dataset.csv \
    -output /mapreduce/twitter/output \
    -mapper /usr/local/hadoop/mapreduce/twitter/mapper_twitter.py \
    -reducer /usr/local/hadoop/mapreduce/twitter/reducer_twitter.py \
    -file /usr/local/hadoop/mapreduce/twitter/mapper_twitter.py \
    -file /usr/local/hadoop/mapreduce/twitter/reducer_twitter.py
```

### 3.3.1. Mapreduce 확인
```bash
hdfs dfs -cat /mapreduce/twitter/output/part-00000
```