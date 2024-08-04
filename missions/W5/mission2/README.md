# W5M2
## Intro
- 제출 파일 목록
    - README.md
    - W5M2.py
    - W5M2.ipynb

- jupyter notebook을 이용하여 작성한 코드를 python script로 다시 작성하였고, DAG를 포함한 README.md 파일을 함께 제출함.
- 작성한 코드를 application으로 실행하면, 17개의 Job으로 구성되며 각 Job의 DAG를 아래에 첨부함.
- 파이썬 script는 아래의 명령어로 실행할 수 있다.
```
spark-submit W5M2.py
```

## Environment
### Spark Standalone Cluster with HDFS
- Docker를 이용하여 총 4개의 container로 spark stand-alone cluster를 구성하였다.
- Spark의 경우, spark-master, 두 개의 spark-worker, spark-history-server로 구성하였다.
- HDFS의 경우, spark-master node에서 namenode를, 나머지에서 datanode를 실행하였다.


### Spark Config
```
spark = SparkSession.builder \
    .master('spark://spark-master:7077') \
    .appName('W5M2_script') \
    .config('spark.executor.memory', '6gb') \
    .config('spark.executor.cores', '5') \
    .getOrCreate()
```

### Spark Web UI
<img width="1704" alt="spark-master" src="https://github.com/user-attachments/assets/72d3ad11-dfbb-47ab-be58-9fe4b179ef3d">

### Hadoop Web UI
<img width="1170" alt="hadoop" src="https://github.com/user-attachments/assets/ca159063-fcea-4ca4-b6e0-6ab1588d25de">

## Optimization
- 최적화를 위해서는 큰 비용이 드는 연산을 줄여야 한다. Wide transform 연산들이 대표적으로 비용이 큰 연산들이고, 이를 줄이는 것이 stage의 수를 줄이는 것과 같다.
- 또 다른 방법은, 자주 사용하는 dataframe을 caching 해두는 것이다. 이를 통해 동일한 연산을 반복적으로 수행하는 것을 피할 수 있다.
- Spark Web UI에서, 기존의 연산결과를 이용하는 경우 DAG에서 회색으로 skipped라고 표현한다.

## Lazy Evaluation
- Spark에서, transformation은 action이 호출되기 전까지는 실제로 수행되지 않는다. 이를 laze evaluation이라 부른다.
- 그 예로, dataframe에서 존재하지 않는 Column을 select(transformation 연산 중 하나) 하더라도, action을 호출하기 전까지는 error가 발생하지 않는다.

## DAG
### All Jobs
<img width="1707" alt="jobs" src="https://github.com/user-attachments/assets/41083f9f-c984-4b08-a937-85825075bbdd">

### Job 0
<img width="209" alt="0" src="https://github.com/user-attachments/assets/1d695e6b-93fe-4b06-b317-e1637872c943">

### Job 1
<img width="226" alt="1" src="https://github.com/user-attachments/assets/105f7b3e-f004-4973-b999-9e13997a3d98">

### Job 2
<img width="226" alt="2" src="https://github.com/user-attachments/assets/29014fb7-7f2e-4d74-ab6f-79982ce92262">

### Job 3
<img width="227" alt="3" src="https://github.com/user-attachments/assets/0db3c153-bb3c-4b24-b92e-c491cff19054">

### Job 4
<img width="409" alt="4" src="https://github.com/user-attachments/assets/cc53c98c-5e41-4580-bcd2-35bed02899ba">

### Job 5
<img width="202" alt="5" src="https://github.com/user-attachments/assets/195de17a-1df9-45fb-8c01-fe1bdff61e03">

### Job 6
<img width="410" alt="6" src="https://github.com/user-attachments/assets/249de09d-9194-42c7-9e7b-17976cd96734">

### Job 7
<img width="202" alt="7" src="https://github.com/user-attachments/assets/f3f92727-fef0-4a8f-b652-ba2276a92a32">

### Job 8
<img width="202" alt="8" src="https://github.com/user-attachments/assets/ae4fc4ea-bcd9-4e85-a3bf-2a25069fff77">

### Job 9
<img width="202" alt="9" src="https://github.com/user-attachments/assets/d8d89cc1-6dd7-4505-afa0-46d09507928c">

### Job 10
<img width="409" alt="10" src="https://github.com/user-attachments/assets/8733e320-56d0-4281-85e1-553be2c2d794">

### Job 11
<img width="414" alt="11" src="https://github.com/user-attachments/assets/fb9b4109-74cc-4305-a523-abaf9af45ad8">

### Job 12
<img width="616" alt="12" src="https://github.com/user-attachments/assets/44238898-4d95-43e5-b71b-9219b5760eb4">

### Job 13
<img width="206" alt="13" src="https://github.com/user-attachments/assets/b869b214-cc9d-4727-8b12-444861c9f538">

### Job 14
<img width="409" alt="14" src="https://github.com/user-attachments/assets/3c297063-d1ee-44fd-93df-623e3f8bbcad">

### Job 15
<img width="417" alt="15" src="https://github.com/user-attachments/assets/bd118783-4d99-4802-a19f-f70e4526b5a6">

### Job 16
<img width="618" alt="16" src="https://github.com/user-attachments/assets/ea61a061-9179-42c9-ac8c-e73df0d0dcae">
