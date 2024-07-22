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

- HDFS에 폴더 생성 및 텍스트 파일 업로드
```bash
hdfs dfs -mkdir -p /ebook
hdfs dfs -put ebook.txt /ebook
```
<br>

- MapReduce 실행
```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
    -input /ebook/ebook.txt \
    -output /ebook/output \
    -mapper mapper.py \
    -reducer reducer.py \
    -file /usr/local/hadoop/mapper.py \
    -file /usr/local/hadoop/reducer.py
```
<br>

- 결과 확인
```bash
hadoop fs -cat /ebook/output/part-00000
```
<br>

- 다시 해보기 위한 삭제 과정
```bash
hdfs dfs -rm /ebook/output/_SUCCESS
hdfs dfs -rm /ebook/output/part-00000
hdfs dfs -rmdir /ebook/output
```
<br>


## Error

- 파이썬 파일 앞에 없으면 경로 못찾음
```bash
#!/usr/bin/env python3
```
<br>


## Source

- Clear and Present Danger / Clancy, Tom
  
https://annas-archive.org/search?index=&page=1&q=Clear+and+Present+Danger&ext=txt&sort=

<br>