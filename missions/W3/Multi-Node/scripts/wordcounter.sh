#!/bin/bash

mkdir input
cd input
wget https://www.gutenberg.org/cache/epub/20417/pg20417.txt
wget https://www.gutenberg.org/cache/epub/5000/pg5000.txt
wget https://www.gutenberg.org/cache/epub/4300/pg4300.txt
cd ..
bin/hdfs dfs -copyFromLocal input/*.txt input
bin/mapred streaming -file mapreduce/wordcounter/mapper.py \
                     -file mapreduce/wordcounter/reducer.py \
                     -input input -output output-guten \
                     -mapper mapreduce/wordcounter/mapper.py \
                     -reducer mapreduce/wordcounter/reducer.py