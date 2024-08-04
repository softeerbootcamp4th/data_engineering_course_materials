# HMG Softeer Spark Container

## Run Spark Cluster
```bash
# pwd => missions/W4/spark-softeer
docker compose up
```

## Submit a job to Spark
| Docker Container 외부에서 submit 한다면, driver 환경에 Python 버전이 3.10이여야 합니다.
```bash
docker exec spark-softeer-master-1 bin/spark-submit --files file --master spark://localhost:7077 client-application [args]

# example
docker exec spark-softeer-master-1 bin/spark-submit --files userdata/pg74102.txt --master spark://localhost:7077 userdata/wordcount.py

# output is stored in userdata/output_wordcount directory.
```