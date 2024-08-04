# W4M2
## 1. Intro
- 제출 파일 목록
    - README.md
    - W4M2.ipynb

## 2. Environment
### Spark Standalone Cluster with HDFS
- Docker를 이용하여 총 4개의 container로 spark stand-alone cluster를 구성하였다.
- Spark의 경우, spark-master, 두 개의 spark-worker, spark-history-server로 구성하였다.
- HDFS의 경우, spark-master node에서 namenode를, 나머지에서 datanode를 실행하였다.

### Spark Web UI
<img width="1704" alt="spark-master" src="https://github.com/user-attachments/assets/72d3ad11-dfbb-47ab-be58-9fe4b179ef3d">

### Hadoop Web UI
<img width="1170" alt="hadoop" src="https://github.com/user-attachments/assets/ca159063-fcea-4ca4-b6e0-6ab1588d25de">

## 3.Change User
- container 실행 시, default로 spark-user로 접속하므로,  hdfs 관련 권한을 가진 'hduser'로 user를 바꿔준다.
- 이후, hadoop path를 환경변수로 설정한다.
```
su -s /bin/bash hduser
cd
source path_setup.sh
```

## 4. Data Loading
- Local file system의 data들을 hdfs로 올린다.
- 이후, 모든 사용자가 hdfs 상의 데이터에 접근할 수 있도록 권한을 수정한다.
- spark의 연산 결과를 저장할 폴더를 만들고, 모든 사용자가 이용할 수 있도록 권한을 수정한다.
- 마지막으로, bash를 종료해 다시 spark-user로 돌아간다.

```
hdfs dfs -mkdir -p /user/hduser
hdfs dfs -put hdfs_data/ /user/hduser
hadoop fs -chmod 777 /user/hduser/hdfs_data
hdfs dfs -mkdir -p /user/spark_user/W4M2_output
hadoop fs -chmod 777 /user/spark_user/W4M2_output
exit
```

## 5. Run Jupyter
- Interactive한 데이터 분석을 위해, jupyter notebook을 이용한다.
- 그 결과를 W4M2.ipynb 파일로 함께 제출하였다.
- 실행 결과는 hdfs 상에 저장하였다.


## 6. Results
### Peak Hour Identification
- 평균적으로, 퇴근 시간대(18시 이후)에 높은 수요를 보인다.

<img width="594" alt="스크린샷 2024-08-04 오후 6 38 22" src="https://github.com/user-attachments/assets/6356356b-f1c3-40eb-9781-1b88b0e28040">

### Weather Condition Analysis
- 강우여부를 시간 단위로 반영하였을 때, 평균적으로 비가 올 때 수요가 1.5배 정도 증가함을 알 수 있다.

<img width="539" alt="스크린샷 2024-08-04 오후 6 38 06" src="https://github.com/user-attachments/assets/d0b3c4e2-9b77-4104-ace5-24687ff103b7">


## 6. Side Project (Demand Forecast for Wheelchair-Accessible Vehicles)
- WAV(Wheelchair-Accessible Vehicles)의 수요 예측을 위해, WAV의 수요에 어떤 특징이 있는지 확인하고자 함.
- 이를 위해, 전체 주행 데이터셋과 WAV 차량을 호출한 주행 데이터셋을 각각 시각화하여 비교함.
- 시간대별 평균 호출 수, 날짜별 호출량을 평일/주말로 구분하여 시각화 하였다.

### Average Number of Calls by Day
- 주황색: 평일
- 하늘색: 주말
- 전체 호출량을 보았을 때 평일과 주말에 수요에 큰 차이가 없지만, WAV 차량을 호출한 결과들만을 시각화했을 때는 주말보다 평일에 훨씬 높은 수요를 보인다는 것을 알 수 있다.
<img width="587" alt="스크린샷 2024-08-04 오후 6 37 27" src="https://github.com/user-attachments/assets/3a267180-2bbb-4def-beba-7522367ca1e6">

### Number of Calls by Time of Day
- 전체 호출과 WAV 차량의 호출 모두 평일보다 주말에 늦은 시간대의 차량 호출량이 높아진다.
<img width="572" alt="스크린샷 2024-08-04 오후 6 37 37" src="https://github.com/user-attachments/assets/dfd93363-4ef8-4653-88f2-62adfb30d73d">