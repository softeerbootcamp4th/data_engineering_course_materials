# W4M1 - Building Apache Spark Standalone Cluster on Docker
## 1. Build & Run Spark Standalone Cluster
```
cd spark-spark-standalone-cluster
docker compose up
```

## 2. Run Spark Job & Check Result
```
docker exec -it spark-master /bin/bash
./mission1.sh
```

- The file mission1.sh consists of the following commands. After executing mission1.sh, an output file is created at /home/spark_user/pi_result.csv.

``` (mission1.sh)
#! /bin/bash
cd ~
spark-submit pi_modified.py
echo
echo
echo
echo "===== [result of pi_modified.py] ====="
cat pi_result.csv
```

(Result Example)
<img width="1254" alt="image" src="https://github.com/user-attachments/assets/00620f56-39eb-4d5e-aead-9a1317c0faac">
