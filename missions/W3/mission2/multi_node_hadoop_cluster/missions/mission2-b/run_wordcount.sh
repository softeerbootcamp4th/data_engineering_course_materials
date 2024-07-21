#!/bin/bash

# test the hadoop cluster by running wordcount
mkdir input
echo "Hello Docker" >input/file2.txt
echo "Hello Hadoop" >input/file1.txt

# create input directory on HDFS
hdfs dfs -mkdir -p /user/root/mission2-b/input

# put input files to HDFS
hdfs dfs -put ./input/* /user/root/mission2-b/input

# run wordcount 
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/sources/hadoop-mapreduce-examples-3.3.6-sources.jar org.apache.hadoop.examples.WordCount mission2-b/input mission2-b/output

# print the input files
echo -e "\ninput file1.txt:"
hdfs dfs -cat /user/root/input/file1.txt

echo -e "\ninput file2.txt:"
hdfs dfs -cat /user/root/input/file2.txt

# print the output of wordcount
echo -e "\nwordcount output:"
hdfs dfs -get /user/root/mission2-b/output/part-00000 ~/missions/mission2-b/output/
cat ~/missions/mission2-b/output/part-00000