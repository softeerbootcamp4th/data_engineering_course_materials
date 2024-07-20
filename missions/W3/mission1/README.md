### Mission 1

#### Bulild Image and Create Container
##### 1. Using Docker
- Build image.
```
docker build -t single_node_hadoop_cluster .
```

- Create Container
```
docker run --name single_node_hadoop_cluster -v hdfs-data:/home/hduser/hdfs-data/ -p 9864:9864 -p 9870:9870 -p 8088:8088 -p 9000:9000 --hostname localhost single_node_hadoop_cluster
```

#### 2. Using docker-compose
```
docker compose up -d
```

#### Attach to Docker Container
```
docker exec -it single_node_hadoop_cluster /bin/bash
```

#### Check Hadoop serivces
jps command를 이용하여 현재 실행 중인 hadoop service 확인
```
1475 ResourceManager
632 SecondaryNameNode
1800 NodeManager
250 NameNode
410 DataNode
1996 Jps
```

#### HDCFS HDFS Operations
- Create a directory in HDFS
```
hdfs dfs -mkdir /mission1
```

- Upload a file from the local file system to the directory in HDFS
```
echo "Hello, World!" >> ~/text_file.txt
hdfs dfs -put ~/text_file.txt /mission1/
```

- Retrieve the uploaded file from HDFS to the local file system.
```
mkdir ~/retrieve_dir
hdfs dfs -get /mission1/text_file.txt ~/retrieve_dir/
diff text_file.txt retrieve_dir/text_file.txt 
```

#### Stop and Restart Docker Container
- hdfs-site.xml 파일에서 namenode, datanode의 정보를 docker volume에 저장하도록 설정하였기 때문에, container의 종료 및 재실행에도 데이터가 유지된다.