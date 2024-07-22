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

- csv 파일 위치로 이동
```bash
cd usr/local/hadoop
```
<br>

- HDFS에 폴더 생성 및 csv 파일 업로드
```bash
hdfs dfs -mkdir -p /ratings
hdfs dfs -put ratings.csv /ratings
```
<br>

- MapReduce 실행
```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
    -input /ratings/ratings.csv \
    -output /ratings/output \
    -mapper mapper.py \
    -reducer reducer.py \
    -file /usr/local/hadoop/mapper.py \
    -file /usr/local/hadoop/reducer.py
```
<br>

- 출력 파일 확인
```bash
hdfs dfs -ls /ratings/output
```
<br>

- 결과 확인
```bash
hadoop fs -cat /ratings/output/part-00000
```
<br>

- 다시 해보기 위한 삭제 과정
```bash
hdfs dfs -rm /ratings/output/_SUCCESS
hdfs dfs -rm /ratings/output/part-00000
hdfs dfs -rmdir /ratings/output
```
<br>