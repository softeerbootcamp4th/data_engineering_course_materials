# E-Book Download

[The Great Gatsby](https://www.gutenberg.org/ebooks/64317)

# File Copy to Container

```bash
docker cp mapper.py hadoop-master:usr/local/mapreduce/wordcount
docker cp reducer.py hadoop-master:usr/local/mapreduce/wordcount
docker cp The_Great_Gatsby.txt hadoop-master:usr/local/mapreduce/wordcount/input/
```

```bash
chmod 777 /usr/local/mapreduce/wordcount/mapper.py
chmod 777 /usr/local/mapreduce/wordcount/reducer.py
```

# File Copy to HDFS

```bash
hdfs dfs -put /usr/local/mapreduce/wordcount/input/The_Great_Gatsby.txt /mapreduce/wordcount/input
```

# MapReduce

## Run

```bash
hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
    -input /mapreduce/wordcount/input/The_Great_Gatsby.txt \
    -output /mapreduce/wordcount/output \
    -mapper /usr/local/mapreduce/wordcount/mapper.py \
    -reducer /usr/local/mapreduce/wordcount/reducer.py \
    -file /usr/local/mapreduce/wordcount/mapper.py \
    -file /usr/local/mapreduce/wordcount/reducer.py
```

## File Check

```bash
hdfs dfs -cat /mapreduce/wordcount/output/part-00000
```

# File get to Container

```bash
hdfs dfs -get /mapreduce/wordcount/output/part-00000 /usr/local/mapreduce/wordcount/output
```
