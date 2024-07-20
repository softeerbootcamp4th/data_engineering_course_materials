#!/bin/bash

mkdir input
cd input
python3 ../download_amazon_reviews_2023.py 1
cd amazon-reviews-2023
mv *.jsonl ..
cd ..
rmdir amazon-reviews-2023
cd ..
bin/hdfs dfs -rm -r -f output-amazon
bin/hdfs dfs -mkdir input-amazon
bin/hdfs dfs -copyFromLocal input/*.jsonl input-amazon
bin/mapred streaming -file mapreduce/amazon_review/mapper.py \
                     -file mapreduce/amazon_review/reducer.py \
                     -input input-amazon/ -output output-amazon \
                     -mapper mapreduce/amazon_review/mapper.py \
                     -reducer mapreduce/amazon_review/reducer.py