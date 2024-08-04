# W5M1
## Intro
- 제출 파일 목록
    - README.md
    - W5M1.py
    - W5M1.ipynb

- jupyter notebook을 이용하여 작성한 코드를 python script로 다시 작성하였고, DAG를 포함한 README.md 파일을 함께 제출함.
- 작성한 코드를 application으로 실행하면, 17개의 Job으로 구성되며 각 Job의 DAG를 아래에 첨부함.
- 파이썬 script는 아래의 명령어로 실행할 수 있다.
```
spark-submit W5M1.py
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
    .appName('W5M1_script') \
    .config('spark.executor.memory', '6gb') \
    .config('spark.executor.cores', '5') \
    .getOrCreate()
```

### Spark Web UI
<img width="1704" alt="spark-master" src="https://github.com/user-attachments/assets/72d3ad11-dfbb-47ab-be58-9fe4b179ef3d">

### Hadoop Web UI
<img width="1170" alt="hadoop" src="https://github.com/user-attachments/assets/ca159063-fcea-4ca4-b6e0-6ab1588d25de">

## DAG
### All Jobs
<img width="1706" alt="Job" src="https://github.com/user-attachments/assets/63ec2cd2-d625-4dd5-a21b-595a934378a0">

### Job 0
<img width="256" alt="0" src="https://github.com/user-attachments/assets/57bad9aa-1137-4f92-8b41-4fb4198ab56e">

### Job 1
<img width="262" alt="1" src="https://github.com/user-attachments/assets/3155e3f5-51da-4bca-84b9-5e540a9bcda6">

### Job 2
<img width="263" alt="2" src="https://github.com/user-attachments/assets/f635a210-5675-4a87-8a12-83d692d6eda5">

### Job 3
<img width="260" alt="3" src="https://github.com/user-attachments/assets/91b6ebed-5ac1-4f5d-8641-26dcca19d9fc">

### Job 4
<img width="454" alt="4" src="https://github.com/user-attachments/assets/4a39ff3f-0793-4c12-b412-cb393c475f02">

### Job 5
<img width="449" alt="5" src="https://github.com/user-attachments/assets/59fa64ae-84b6-4c47-8d85-45115f284e8b">

### Job 6
<img width="449" alt="6" src="https://github.com/user-attachments/assets/55dbd93e-15ba-42b8-8ba3-ba7c80e27e08">

### Job 7
<img width="443" alt="7" src="https://github.com/user-attachments/assets/4b1c6e1c-5093-4003-a6cb-f75707b3cb55">

### Job 8
<img width="253" alt="8" src="https://github.com/user-attachments/assets/c1703166-8c87-4969-a78f-46fb0fb2e94c">

### Job 9
<img width="661" alt="9" src="https://github.com/user-attachments/assets/cca1e5d6-8f06-4f95-b4f0-45a80600a3d7">

### Job 10
<img width="664" alt="10" src="https://github.com/user-attachments/assets/7268f157-4a85-467a-826b-95ab190f97b2">

### Job 11
<img width="631" alt="11" src="https://github.com/user-attachments/assets/856faf08-97e9-41ca-80a5-1f11b489aeb0">

### Job 12
<img width="644" alt="12" src="https://github.com/user-attachments/assets/0c993d10-7561-4b67-8fee-ad946cb7650a">

### Job 13
<img width="635" alt="13" src="https://github.com/user-attachments/assets/e2324eec-dd0a-42c7-b746-68908e7b2c37">

### Job 14
<img width="639" alt="14" src="https://github.com/user-attachments/assets/b221653a-f047-402c-a702-87e7ac2a2594">

### Job 15
<img width="637" alt="15" src="https://github.com/user-attachments/assets/cd5968ae-5804-41d3-920d-8a2e9647e0be">

### Job 16
<img width="636" alt="16" src="https://github.com/user-attachments/assets/8e98b89a-1900-4c9a-ada3-c119306473e5">