#!/bin/bash

hdfs dfs -rm -r /user
hdfs dfs -rm -r /tmp

hdfs dfs -mkdir -p /user/hadoop/input
hdfs dfs -put All_Beauty.jsonl /user/hadoop/input
hdfs dfs -ls -R /

# hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount /user/hadoop/input /user/hadoop/output

# hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
# -mapper mapper.py \
# -reducer reducer.py \
# -input /user/hadoop/input/asin2category.json \
# -output /user/hadoop/output \
# -D mapreduce.map.memory.mb=1024 \
# -D mapreduce.reduce.memory.mb=1024 \
# -file ./mapper.py \
# -file ./reducer.py

# hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
# -mapper mapper.py \
# -reducer reducer.py \
# -input /user/hadoop/input/asin2category.json \
# -output /user/hadoop/output \
# -file ./mapper.py \
# -file ./reducer.py

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-D mapreduce.input.fileinputformat.split.minsize=67108864 \
-D mapreduce.input.fileinputformat.split.maxsize=134217728 \
-D mapred.child.java.opts=-Xmx1024m \
-input /user/hadoop/input/All_Beauty.jsonl \
-output /user/hadoop/output \
-mapper mapper.py \
-reducer reducer.py \
-file ./mapper.py \
-file ./reducer.py




hadoop fs -cat /user/hadoop/output/part-00000
# hadoop fs -get /user/hadoop/output/part-00000 /usr/local/hadoop/data/namenode/current/result_M3


