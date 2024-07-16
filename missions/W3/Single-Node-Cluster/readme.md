# Docker for Hadoop single node cluster

## Docker build image

```bash
docker build -t hadoop-single-node .
```

## Docker run container

```bash
docker run -d -p 9870:9870 -p 8088:8088 -p 9000:9000 -p 9864:9864 --name hadoop-single-node -v hadoop-volume:/hadoop/dfs hadoop-single-node
```

## Connect to Docker container

```bash
docker exec -it hadoop-single-node /bin/bash
```

# HDFS operation

## Creating directories

```bash
hdfs dfs -mkdir /w3/m1/
```

## Upload file from local to HDFS

```bash
hdfs dfs -put samplefile.txt /w3/m1/
```

## Check file

```bash
hdfs dfs -ls /w3/m1
```

## Retrieve from HDFS to local

```bash
hdfs dfs -get /w3m1/samplefile.txt /softeer/w3/samplefile_copy.txt
```
