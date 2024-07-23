#!/bin/bash

# 현재 디렉토리로 이동
echo $(pwd)
cd "$(dirname "$0")"

# pdf_to_text.py가 현재 디렉토리에 존재하는지 확인
if [ ! -f pdf_to_txt.py ]; then
  echo "Error: pdf_to_txt.py not found!"
  exit 1
fi

# pdf 파일을 text 파일로 변환
python3 pdf_to_txt.py

# test_mapreduce.sh 실행
cd mapreduce
./test_mapreduce.sh usr/local/hadoop namenode
cd ..
