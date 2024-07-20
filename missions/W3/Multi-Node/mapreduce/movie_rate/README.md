# Hadoop Mapreduce Movie Rate

# 준비
hdfs에 `/user/hdoop/input` 파일이 없는 경우에만 실행한다.
```bash
./hdfs_init.sh
```

# 실행
```bash
bin/hdfs dfs -rm -r -f output_movie # output_movie가 있는 경우에 실행

./movie_rate.sh
```