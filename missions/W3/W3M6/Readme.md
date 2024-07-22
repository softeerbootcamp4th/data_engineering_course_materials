## Docker image build
```bash
docker-compose build
```

<br>
<br>

## Docker container run
```bash
docker-compose up -d
```

<br>
<br>

## Data Operations

- jsonl 파일 위치로 이동
```bash
cd usr/local/hadoop
```
<br>

- HDFS에 폴더 생성 및 jsonl 파일 업로드
- (나머지 데이터 생략)
```bash
hdfs dfs -mkdir -p /reviews
hdfs dfs -put All_Beauty.jsonl /reviews
hdfs dfs -put Amazon_Fashion.jsonl /reviews
hdfs dfs -put Appliances.jsonl /reviews
...
```
<br>

- MapReduce 실행
- (나머지 데이터 생략)
```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
    -input /reviews/All_Beauty.jsonl \
    -input /reviews/Amazon_Fashion.jsonl \
    -input /reviews/Appliances.jsonl \
    ... \
    -output /reviews/output \
    -mapper mapper.py \
    -reducer reducer.py \
    -file /usr/local/hadoop/mapper.py \
    -file /usr/local/hadoop/reducer.py
```
<br>

- 출력 파일 확인
```bash
hdfs dfs -ls /reviews/output
```
<br>

- 결과 확인
```bash
hadoop fs -cat /reviews/output/part-00000
```
<br>

- 다시 해보기 위한 삭제 과정
```bash
hdfs dfs -rm /reviews/output/_SUCCESS
hdfs dfs -rm /reviews/output/part-00000
hdfs dfs -rmdir /reviews/output
```
<br>