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

- 샘플 텍스트 파일 생성
```bash
echo "Hello Hadoop Hello World" > input.txt
```
<br>

- HDFS에 샘플 텍스트 파일 업로드
```bash
hadoop fs -mkdir -p /user/hadoop/input
hadoop fs -put input.txt /user/hadoop/input
```
<br>

- 업로드 확인
```bash
hdfs dfs -ls /user/hadoop/input
```
<br>

- WordCount.java 파일 생성
```bash
sudo vi WordCount.java
```
<br>

- 프로그램 컴파일 및 패키징
```bash
mkdir wordcount_classes
javac -classpath `hadoop classpath` -d wordcount_classes WordCount.java
jar -cvf wordcount.jar -C wordcount_classes/ .
```
<br>

- MapReduce 작업 실행
```bash
hadoop jar wordcount.jar WordCount /user/hadoop/input /user/hadoop/output
hadoop fs -rm -r hdfs://hadoop-master:9000/user/hadoop/output (삭제 명령어)
```
<br>

- 결과 확인
```bash
hadoop fs -cat /user/hadoop/output/part-r-00000
```
<br>

- `localhost:8088`에서 master node, worker node 확인


<br>

- `localhost:9870`에서 master node, worker node 확인


<br>