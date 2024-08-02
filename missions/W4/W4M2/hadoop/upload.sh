#!/bin/bash

hadoop fs -mkdir -p /opt/hadoop/pi
hadoop fs -mkdir -p /opt/hadoop/taxi
hadoop fs -mkdir -p /opt/hadoop/weather

# 원본 디렉토리
SRC_DIR="/opt/hadoop/pi"

# HDFS 대상 디렉토리
DEST_DIR="/opt/hadoop/pi"

# .parquet 파일 목록 자동 생성
FILES=($(find "$SRC_DIR" -maxdepth 1 -type f -name "*.parquet"))

# 업로드 명령어 실행
for FILE in "${FILES[@]}"; do
  # HDFS로 업로드
  hadoop fs -put "$FILE" "$DEST_DIR"
done

hadoop fs -put "/opt/hadoop/pi/taxi_zone.csv" "/opt/hadoop/taxi/taxi_zone.csv"
hadoop fs -put "/opt/hadoop/pi/weather.csv" "/opt/hadoop/weather/weather.csv"