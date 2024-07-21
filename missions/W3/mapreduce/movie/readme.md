# Data Download

[link](https://grouplens.org/datasets/movielens/20m/)

- From zipfile, use ratings file

# Copy Code and Data to Docker Container

```bash
docker cp mapper.py hadoop-master:usr/local/hadoop/mapreduce/movie
docker cp reducer.py  hadoop-master:usr/local/hadoop/mapreduce/movie
docker cp ratings.csv hadoop-master:usr/local/hadoop/mapreduce/movie/input
```

```bash
chmod 777 mapper.py reducer.py
```

# Upload to HDFS

```bash
hdfs dfs -put ratings.csv /mapreduce/movie/input
```

# MapReduce

## Run

```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
    -input /mapreduce/movie/input/ratings.csv \
    -output /mapreduce/movie/output \
    -mapper /usr/local/hadoop/mapreduce/movie/mapper.py \
    -reducer /usr/local/hadoop/mapreduce/movie/reducer.py \
    -file /usr/local/hadoop/mapreduce/movie/mapper.py \
    -file /usr/local/hadoop/mapreduce/movie/reducer.py
```

## Check

```bash
hdfs dfs -cat /mapreduce/movie/output/part-00000
```

# To Local File

```bash
hdfs dfs -get /mapreduce/movie/output/part-00000 /usr/local/hadoop/mapreduce/movie/output
```
