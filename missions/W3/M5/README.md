### 데이터 준비

`docker cp ./mapper.py master-container:/`
`docker cp ./reducer.py master-container:/`
`docker cp ./ratings.csv master-container:/`

[링크](https://grouplens.org/datasets/movielens/20m/)에서 rating.csv를 다운로드


ratings.csv를 컨테이너에 넣고 hdfs에 저장

`hdfs dfs -put /ratings.csv /ratings.csv`

### Hadoop Streaming 작업 실행

다음 명령어로 MapReduce 작업을 실행합니다:

`mapred streaming -mapper mapper.py -reducer reducer.py -input /ratings.csv -output /output/average_ratings -file /mapper.py -file /reducer.py`

### 결과 확인

작업이 완료되면 다음 명령어로 결과를 확인할 수 있습니다:
`hdfs dfs -cat /output/average_ratings/part-*`

