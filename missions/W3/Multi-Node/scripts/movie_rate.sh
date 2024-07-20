#!/bin/bash

mkdir input
cd input
wget https://files.grouplens.org/datasets/movielens/ml-20m.zip
unzip ml-20m.zip
cd ml-20m
mv ratings.csv ..
cd ..
rm ml-20m.zip
rm ml-20m/*
rmdir ml-20m
cd ..
bin/hdfs dfs -copyFromLocal input/ratings.csv input
bin/mapred streaming -file mapreduce/movie_rate/mapper.py \
                     -file mapreduce/movie_rate/reducer.py \
                     -input input/ratings.csv -output output-movie \
                     -mapper mapreduce/movie_rate/mapper.py \
                     -reducer mapreduce/movie_rate/reducer.py