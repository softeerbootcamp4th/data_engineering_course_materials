#!/bin/bash

hdfs dfs -rm -r /user
hdfs dfs -rm -r /tmp

hdfs dfs -mkdir -p /user/hadoop/input
hdfs dfs -put input.txt /user/hadoop/input
hdfs dfs -ls -R /

# hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount /user/hadoop/input /user/hadoop/output

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-mapper mapper.py \
-reducer reducer.py \
-input /user/hadoop/input/input.txt \
-output /user/hadoop/output \
-file ./mapper.py \
-file ./reducer.py

hadoop fs -cat /user/hadoop/output/part-00000


