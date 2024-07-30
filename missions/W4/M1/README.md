1. [x] The cluster should consist of one Spark master and two Spark worker nodes.
2. [x] The Spark Web UI should be accessible to monitor the job progress and cluster status.
3. [x] The Spark job should be able to read a dataset from a mounted volume or a specified input path.
4. [x] The job should perform a data transformation (e.g., estimating π) and write the results to a specified output
   path.
5. [x] The output should be correctly partitioned and saved in a format such as CSV or Parquet.
6. [x] Logs should be accessible to debug any issues with the Spark job or cluster setup.

## 스파크 구성

`docker compsoe up -d`

스파크 마스터 1개와 스파크 워커 2개가 실행됩니다.

## Web UI

http://localhost:8080에 들어가면 스파크 마스터의 WebUI를 볼 수 있다.

http://localhost:8081에 들어가면 스파크 워커의 WebUI를 볼 수 있다.

## Spark Job 실행

`spark_job.sh` 를 실행하면 pi.py exmaple을 실행해서 PI의 값을 계산한다.

실행 결과는 화면에 출력됩니다.

## 데이터 읽기, 저장

### CSV(pyspark)

`df.write.csv('foo.csv', header=True)`

`spark.read.csv('foo.csv', header=True).show()`

csv는 위 명령어로 읽고 쓸 수 있다.

`data = spark.read.csv("hdfs://localhost:19000/user/movies.csv", header="true", inferSchema="true")`

추가로 하둡이 설정되어 있다면 위와 같은 명령어로 hdfs에서 파일을 읽을 수 도 있다.

## 로그

`/opt/spark/works`

작업에 대한 로그는 위 경로에 있다.

`/opt/spark/logs`

노드들에 대한 로그는 위 경로에 있다.