#!/bin/bash

# hdfs dfs -rm -r /user
# hdfs dfs -rm -r /tmp

# hdfs dfs -mkdir -p /user/hadoop/input
# hdfs dfs -put input.txt /user/hadoop/input
# hdfs dfs -ls -R /

docker exec -it --user hadoop spark-master bash -c "
    hdfs dfs -rm -r /user
    hdfs dfs -rm -r /tmp

    hdfs dfs -mkdir -p /user/hadoop/input
    hdfs dfs -put input.txt /user/hadoop/input
    hdfs dfs -ls -R /
  "

docker cp "/Users/admin/Desktop/HMG_W2/missions/W5/M1/docker/untracked/TLC Tripdata Jan 2024.parquet" "spark-master:usr/local/spark/rdd/TLC_Tripdata_Jan_2024.parquet"
docker exec -it --user hadoop spark-master bash -c "
hdfs dfs -put "TLC_Tripdata_Jan_2024.parquet" /user/hadoop/input
"