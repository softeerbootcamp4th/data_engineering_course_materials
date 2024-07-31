# Hadoop Multi Node Cluster on Docker.

## 0. Ebook Download
```bash
python download_text.py
```

# 1. 컨테이너 생성
## 1.1. Docker-compose image를 build(mapper.py, reducer.py 포함한 Dockerfile)
```bash
docker-compose build
```
* Dockerfile, Docker-compose.yml이 있는 디렉토리에서 터미널이 입력

## 1.2. Docker container를 실행한다.
```bash
docker-compose up -d
```
* docke-compose file을 보고 포트 뚫고 컨테이너 실행한다.

## 1.3. 실행 중인 Docker를 확인한다.
```
docker ps
```

# 2. Mapreduce 확인
## 2.1. container 접속
```bash
docker exec -it hadoop-master /bin/bash
```
* hadoop-master : master container 이름

## 2.2. Hadoop 설정 파일 확인
```bash
ls -l /usr/local/hadoop/etc/hadoop/
```

## 2.3. 스크립트, py 파일 확인
```bash
ls -l /usr/local/bin/
```

## 2.5. mapreduce_example.txt 파일 확인
```bash
ls -l /home/hdfs/
```


# 3. Maprduce
## 3.1. hdfs로 접속
```bash
su - hdfs
```

## 3.2. Hadoop 마스터 노드에 접속하여 mapreduce_example.txt 파일을 HDFS에 업로드
```bash
hdfs dfs -mkdir -p /user/hdfs/input
hdfs dfs -put /home/hdfs/mapreduce_example.txt /user/hdfs/input/
```

## 3.3. hdfs에 잘 올라갔나 확인
```bash
hdfs dfs -ls /user/hdfs/input
```
### 3.3.1 Python이 설치되지 않았다면 설치
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip
sudo ln -s /usr/bin/python3 /usr/bin/python
```
### 3.3.2. 환경변수 설정
```bash
export HADOOP_STREAMING_OPTS="-D mapreduce.map.env='PYTHONUSERBASE=/usr/bin/python' -D mapreduce.reduce.env='PYTHONUSERBASE=/usr/bin/python'"
```
### 3.3.3. .py files HDFS에 업로드
```bash
hdfs dfs -put /usr/local/bin/mapper.py /user/hdfs/
hdfs dfs -put /usr/local/bin/reducer.py /user/hdfs/
```

### 3.3.3. 권한 설정
```bash
sudo chmod +x /usr/local/bin/mapper.py
sudo chmod +x /usr/local/bin/reducer.py
```

## 3.4. Word Count 작업
### 3.4.1 mapper.py test
```bash
cat /tmp/mapreduce_example.txt | python /usr/local/bin/mapper.py
```
### 3.4.2. reducer.py test
```bash
cat /tmp/mapreduce_example.txt | python /usr/local/bin/mapper.py | python /usr/local/bin/reducer.py
```
### 3.4.3. Hadoop Streaming Job을 실행
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -D mapreduce.job.user.classpath.first=true \
  -D stream.map.output.field.separator=\t \
  -D stream.reduce.input.field.separator=\t \
  -files /usr/local/bin/mapper.py,/usr/local/bin/reducer.py \
  -mapper "python3 /usr/local/bin/mapper.py" \
  -reducer "python3 /usr/local/bin/reducer.py" \
  -input /user/hdfs/input/mapreduce_example.txt \
  -output /user/hdfs/output
```

### 3.4.4. 결과 확인
```bash
hdfs dfs -cat /user/hdfs/output/part-00000
```
