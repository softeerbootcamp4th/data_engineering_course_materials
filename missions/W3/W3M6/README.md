# 1. Amazon Product Review using MapReduce

# 2. File Upload
## 2.1. 디렉토리 생성
```bash
docker exec -it hadoop-master mkdir -p /usr/local/hadoop/mapreduce/amazon_review/input
```
## 2.2. Docker로 File Copy
* mapper.py
```bash
docker cp scripts/mapper.py hadoop-master:/usr/local/hadoop/mapreduce/amazon_review/mapper.py
```
* reducer.py
```bash
docker cp scripts/reducer.py  hadoop-master:/usr/local/hadoop/mapreduce/amazon_review/reducer.py
```
* Amazon
```bash
docker cp scripts/download_category.sh hadoop-master:/usr/local/hadoop/mapreduce/amazon_review/input/download_category.sh
```

## 2.3. 컨테이너 접속
```bash
docker exec -it hadoop-master /bin/bash
```

### 2.3.1. 파일, 디렉토리 확인
```bash
ls -l /usr/local/hadoop/mapreduce/amazon_review
```
```bash
ls -l /usr/local/hadoop/mapreduce/amazon_review/input
```
### 2.3.2. 권한 설정
```bash
chmod +x /usr/local/hadoop/mapreduce/amazon_review/input/download_category.sh
```

# 3. HDFS
## 3.1. HDFS에 업로드
```bash
su - hdfs
```

```bash
hdfs dfs -mkdir -p /user/root/mission6/input
```

```bash
hdfs dfs -put /usr/local/hadoop/mapreduce/amazon_review/input/download_category.sh /user/root/mission6/input/
```
### 3.1.1. 잘 업로드 됐는지 확인
```bash
hdfs dfs -ls /user/root/mission6/input/
```

## 3.2. Mapreduce 실행
```bash
hadoop jar /usr/local/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -file /usr/local/hadoop/mapreduce/amazon_review/mapper.py \
  -file /usr/local/hadoop/mapreduce/amazon_review/reducer.py \
  -mapper /usr/local/hadoop/mapreduce/amazon_review/mapper.py \
  -reducer /usr/local/hadoop/mapreduce/amazon_review/reducer.py \
  -input /user/root/mission6/data \
  -output /user/root/mission6/output
```

## 3.3. Mapreduce 확인
```bash
hdfs dfs -get /user/root/mission6/output/part-00000 ~/missions/mission6/output/
```
