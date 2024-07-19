# Put File on Container

```bash
docker cp mapper.py hadoop-master:usr/local/mapreduce/twitter
docker cp reducer.py  hadoop-master:usr/local/mapreduce/twitter
docker cp twitter_sentiment.csv hadoop-master:usr/local/mapreduce/twitter/input
```

```bash
chmod 777 mapper.py reducer.py
```

# Put File on HDFS

```bash
hdfs dfs -put twitter_sentiment.csv /mapreduce/twitter/input
```

# MapReduce

## Run

```bash
hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
    -input /mapreduce/twitter/input/twitter_sentiment.csv \
    -output /mapreduce/twitter/output \
    -mapper /usr/local/mapreduce/twitter/mapper.py \
    -reducer /usr/local/mapreduce/twitter/reducer.py \
    -file /usr/local/mapreduce/twitter/mapper.py \
    -file /usr/local/mapreduce/twitter/reducer.py
```

## Check

```bash
hdfs dfs -cat /mapreduce/twitter/output/part-00000
```

![result](./imgs/result.png)

# Move Result to Local

```bash
hdfs dfs -get /mapreduce/twitter/output/part-00000 /usr/local/mapreduce/twitter/output
```
