# Hadoop Single Node Cluster on Docker.

# 1. 컨테이너 생성
## 1.1. Docker image를 build한다.(Dockerfile, docker-compose.yml이 있는 path에서)
* docker-compose build

## 1.2. Docker container를 실행한다.
* docker-compose up -d

## 1.3. 실행 중인 Docker를 확인한다.
* docker ps

# 2. HDFS에 파일 업로드
## 2.1. 컨테이너 접속
* docker exec -it single-node-hadoop /bin/bash
     *  single-node-hadoop : 컨테이너 이름

## 2.2. HDFS 디렉토리 생성 (컨데이너에서 입력)
* hdfs dfs -mkdir -p /w3/m1/
     * /w3/m1/: 디렉토리 생성 경로

## 2.3. local에서 HDFS로 파일 업로드
* hdfs dfs -put root/hello-hadoop.txt /w3/m1/
     * root/hello-hadoop.txt: local에서의 파일 경로
     * /w3/m1/: 업로드 할 HDFS 경로

## 2.4.1. HDFS 업로드 확인
* hdfs dfs -ls /w3/m1/

## 2.4.2 Hadoop UI에서 확인
* http://localhost:9870 에 접속
     * 1. Utilities
     * 2. Browse the file system
     * 3. /w3/m1: 디렉토리 경로로 이동
* HDFS에 파일이 잘 업로드된 것을 확인할 수 있다.

## 2.4.3. 터미널에서 파일 확인
* hdfs dfs -cat /w3/m1/hello-hadoop.txt

# 3. HDFS에서 컨테이너 local에 다시 파일 다운로드
## 3.1. 컨테이너에 다운로드하고 싶은 경로 생성
* mkdir -p /local/path/to
     * /local/path/to: 다운로드하고 싶은 local 경로
## 3.2. HDFS에서 local로 파일 다운로드
* hdfs dfs -get /w3/m1/hello-hadoop.txt /local/path/to/hello-hadoop.txt
     * /w3/m1/hello-hadoop.txt: HDFS에서의 경로
     * /local/path/to/hello-hadoop.txt: local의 경로 및 파일 이름
## 3.3. local path 확인
* ls -l /local/path/to/hello-hadoop.txt
* cat /local/path/to/hello-hadoop.txt

# 4. local에서 내 로컬 노트북으로 저장 (현재 내 로컬 노트북 터미널)
* docker cp single-node-hadoop:/local/path/to/hello-hadoop.txt /Users/admin/Desktop/Data_Engineering/W3/W3M1/realrealreal_final_hadoop/Download_example/hadoop_text.txt
     * /local/path/to/hello-hadoop.txt: Docker Container에서의 file path
     * /Users/admin/Desktop/Data_Engineering/W3/W3M1/realrealreal_final_hadoop/Download_example/hadoop_text.txt: 저장하고 싶은 내 노트북에서의 file path

# 5. HDFS에서 바로 내 로털 노트북으로 저장할 수 없을까?
## 5.1. curl pakage install 후 사용
* curl -L -o /Users/admin/Desktop/Data_Engineering/W3/W3M1/realrealreal_final_hadoop/Download_example/hadoop_text.txt "http://localhost:9870/webhdfs/v1/w3/m1/hello-hadoop.txt?op=OPEN"

## 5.2. 하지만 오류가 발생했다.
* curl -v -L -o /Users/admin/Desktop/Data_Engineering/W3/W3M1/realrealreal_final_hadoop/Download_example/hadoop_text.txt "http://localhost:9870/webhdfs/v1/w3/m1/hello-hadoop.txt?op=OPEN"
     * -v 옵션으로 디버깅해보자
* HDFS Namenode가 HTTP 307 리다이렉트 응답을 반환
* URL이 내부 호스트 이름(d98441460b60)을 포함하고 있는데 외부에서 접근할 수 없어서 실패했었다.

## 5.3. 리다이렉트된 URL에서 내부 호스트 이름을 명시적으로 적어주자.
* curl -L -o /Users/admin/Desktop/Data_Engineering/W3/W3M1/realrealreal_final_hadoop/Download_example/hadoop_text.txt "http://localhost:9864/webhdfs/v1/w3/m1/hello-hadoop.txt?op=OPEN&namenoderpcaddress=localhost:9000&offset=0"
* 다운로드 성공