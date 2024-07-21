#!/bin/bash


##### 컨테이너 내부로 ebook, mapper, reducer 복사

# ebook 컨테이너 내부로 복사
docker cp The_Southern_Literary_Messenger.txt hadoop-master:/temp

# mapper, reducer 컨테이너 내부로 복사
docker cp ebook_mapper.py hadoop-master:/temp/ebook_mapper.py 
docker cp ebook_reducer.py hadoop-master:/temp/ebook_reducer.py


##### HDFS에 ebook 옮기기

# hdfs에 ebook directory 생성
docker exec -it hadoop-master hdfs dfs -mkdir -p /ebook_dir

# 해당 디렉토리로 ebook 옮기기
docker exec -it hadoop-master hdfs dfs -put /temp/The_Southern_Literary_Messenger.txt /ebook_dir


##### MapReduce 작업 실행
# ebook_output 디렉토리는 생성됨
docker exec -it hadoop-master hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -input /ebook_dir/The_Southern_Literary_Messenger.txt \
  -output /ebook_output \
  -mapper ebook_mapper.py \
  -reducer ebook_reducer.py \
  -file /temp/ebook_mapper.py \
  -file /temp/ebook_reducer.py


##### 호스트 머신으로 결과 가져오기

# 컨테이너 로컬 파일 시스템의 /temp의 소유권을 hadoopuser로 변경
docker exec -it hadoop-master sudo chown hadoopuser:hadoopuser temp

# HDFS의 ebook_output 디렉토리를 컨테이너의 로컬 디렉토리로 가져옴
docker exec -it hadoop-master hdfs dfs -get /ebook_output /temp

# 결과를 호스트 머신(Mac)의 현재 폴더로 가져옴
docker cp hadoop-master:/temp/ebook_output .