#!/bin/bash

mkdir input
cd input
cp /hadoop/mapreduce/twitter_analysis/training.1600000.processed.noemoticon.csv .
cd ..
bin/hdfs dfs -copyFromLocal input/training.1600000.processed.noemoticon.csv input
bin/mapred streaming -file mapreduce/twitter_analysis/mapper.py \
                     -file mapreduce/twitter_analysis/reducer.py \
                     -input input -output output-twitter \
                     -mapper mapreduce/twitter_analysis/mapper.py \
                     -reducer mapreduce/twitter_analysis/reducer.py