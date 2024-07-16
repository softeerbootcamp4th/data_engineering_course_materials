## Building the Docker image

`docker build . -t hadoop`

Dockerfile이 있는 디렉토리에서 위 명령어를 사용하여 도커 이미지를 빌드합니다.

## Running the container
docker-compose.yaml이 있는 디렉토리에서 hadoop-data 디렉토리를 만들고, 그 안에 namenode, datanode 라는
디렉토리를 생성합니다.

`docker compose up -d`

docker-compose.yaml 파일이 있는 디렉토리에서 위 명령어를 사용하여 도커 컨테이너를 실행합니다.

`docker-compose up -d`

OS나 버전에 따라 위 명령어를 사용 해야 할 수 도 있습니다.
이 때, 빌드한 이미지의 tag는 hadoop 이어야 합니다.


## Performing HDFS operations

`docker exec -it hadoop-container sh`

도커 컨테이너가 정상적으로 구동됐다면 위 명령어를 통해 컨테이너에 접속 합니다.
컨테이너 이름은 hadoop-container 입니다.

`hdfs dfs -mkdir -p /user/root`

root라는 이름의 유저의 hdfs 디렉토리를 생성합니다.

`echo hihihi >> hi.txt`

hi.txt라는 파일을 만듭니다. 

`hdfs dfs -put hi.txt /user/root`

hi.txt라는 파일의 hdfs의 /user/root 에 업로드합니다. 

`hdfs dfs -get /user/root/hi.txt hi_copy.txt`

hdfs의 /user/root에 있는 hi.txt 파일을 로컬에 hi_copy.txt 파일로 다운로드 합니다.
## Access the HDFS web interface

hdfs 웹 UI : http://localhost:9870/

클러스터 상태 : http://localhost:808/