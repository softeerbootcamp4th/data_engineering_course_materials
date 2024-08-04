# NYC TLC Trip Record Analysis using Apache Spark

# 1. Dataset Download
```bash
python Download_parquet.py
```


# 1. 컨테이너 생성
## 1.1. docker-compose Build
```bash
docker-compose up --build -d
```

## 1.2. 실행 중인 Docker를 확인한다.
```bash
docker ps
```

# 2. Spark 작업 확인
## 2.1. spark-submit 스크립트 실행
* ./spark-submit.sh
     *  spark-submit : 스크립트 파일 이름

## 2.2. Docker Container log 확인
* docker logs spark-master
    * spark-master: master container 이름
</br>

* 24/07/22 12:41:34 INFO SparkContext: Starting job: reduce at /opt/spark/pi.py:15

</br>

* 24/07/22 12:41:35 INFO DAGScheduler: Job 0 finished: reduce at /opt/spark/pi.py:15, took 1.216099 s

</br>

* 24/07/22 12:41:35 INFO DAGScheduler: Job 0 finished: reduce at /opt/spark/pi.py:15, took 1.216099 s

* Pi is ~~ 3.134060
* 파이를 성공적으로 근사했다.
