# Hadoop Mapreduce Twitter Sentiment Analysis
# 준비
hdfs에 `/user/hdoop/input` 파일이 없는 경우에만 실행한다.
```bash
./hdfs_init.sh
```

# 실행
/hadoop/mapreduce/twitter_analysis에 `training.1600000.processed.noemoticon.csv` 파일을 추가 후 실행
```bash
bin/hdfs dfs -rm -r -f output_twitter # output_twitter가 있는 경우에 실행

./twitter_analysis.sh
```