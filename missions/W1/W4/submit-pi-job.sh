#!/bin/bash

echo "Submitting Spark job..."
# 스파크 작업 제출
docker exec -it spark-master /usr/local/spark/bin/spark-submit \
    --master spark://spark-master:7077 \
    /usr/local/spark/work-dir/pi.py

# 결과 파일 경로 설정
echo "Fetching result file path from container..."
result_file=$(docker exec -it spark-master bash -c 'ls /usr/local/spark/work-dir/montecarlo_result_*.csv | tail -n 1 | tr -d "\r" | tr -d "\n"')

# 결과 파일이 존재하는지 확인
if [ -z "$result_file" ]; then
    echo "Result file not found in container"
    exit 1
fi

local_result_path="./$(basename $result_file)"

echo "Copying result file to host..."
# 결과 파일을 호스트로 복사
docker cp spark-master:$result_file $local_result_path

# 결과 파일 확인
if [ -f $local_result_path ]; then
    echo "Result file saved at $local_result_path"
    cat $local_result_path
else
    echo "Result file not found on host"
    exit 1
fi
