#!/bin/bash

# HDFS 디렉토리 생성 및 파일 업로드
hdfs dfs -mkdir -p /user/hadoop/input
hdfs dfs -put /usr/local/hadoop/ebook.txt /user/hadoop/input/ebook.txt
# 기존 출력 디렉토리 삭제
hdfs dfs -rm -r /user/hadoop/output

# MapReduce 작업 실행
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files /usr/local/hadoop/mapper3.py,/usr/local/hadoop/reducer3.py \
  -mapper /usr/local/hadoop/mapper3.py \
  -reducer /usr/local/hadoop/reducer3.py \
  -input /user/hadoop/input/ebook.txt \
  -output /user/hadoop/output

# 결과 출력
hdfs dfs -cat /user/hadoop/output/part-00000
