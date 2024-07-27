# Building Apache Spark Standalone Cluster on Docker

# 1. 컨테이너 생성
* Dockerfile : Spark 클러스터를 설정
* docker-compose.yml : Spark 클러스터를 설정
* entrypoint.sh : 각 컨테이너에서 실행될 명령어 스크립트
* spark-submit.sh : Spark 시작 스크립트
## 1.1. Docker image를 build한다.(Dockerfile, docker-compose.yml이 있는 path에서)
'''
docker-compose build
'''

## (선택) 같은 이름의 컨테이너를 지우고 싶다.
'''
docker-compose down
'''

## 1.2. Docker container를 실행한다.
'''
docker-compose up -d
'''

## 1.3. 실행 중인 Docker를 확인한다.
'''
docker ps
'''
# 2. Spark 작업 확인
## 2.1. spark-submit 스크립트 실행
'''
./spark-submit.sh
'''
*  spark-submit : 스크립트 파일 이름

## 2.2. Docker Container log 확인
'''
docker logs spark-master
'''
* spark-master: master container 이름
</br>

* 24/07/22 12:41:34 INFO SparkContext: Starting job: reduce at /opt/spark/pi.py:15

</br>

* 24/07/22 12:41:35 INFO DAGScheduler: Job 0 finished: reduce at /opt/spark/pi.py:15, took 1.216099 s

</br>

* 24/07/22 12:41:35 INFO DAGScheduler: Job 0 finished: reduce at /opt/spark/pi.py:15, took 1.216099 s

* Pi is ~~ 3.134060
* 파이를 성공적으로 근사했다.
