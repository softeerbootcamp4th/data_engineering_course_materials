## Single Node Cluster Hadoop/HDFS In Docker

### Functional Requirement

- Docker Images
    - ~~Docker 이미지는 모든 기능을 갖춘 Hadoop 마스터 및 워커 노드를 캡슐화해야 합니다.~~
    - ~~Docker 컨테이너가 실행되면 모든 필수 Hadoop 서비스가 자동으로 시작됩니다.~~
    - ~~컨테이너는 마스터와 워커 노드 간의 통신을 원활하게 하기 위해 동일한 Docker 네트워크에 연결할 수 있어야 합니다.~~
- HDFS Operations
    - ~~사용자는 마스터 노드에서 HDFS와 상호작용할 수 있어야 합니다.~~
    - ~~사용자는 디렉토리를 생성하고, 파일을 업로드하고, HDFS에서 파일을 검색할 수 있어야 합니다.~~
    - ~~HDFS 웹 인터페이스는 호스트 머신에서 접근하여 파일 시스템을 모니터링할 수 있어야 합니다.~~
- Cluster Operations
    - ~~Hadoop 클러스터는 분산 저장 및 처리를 위해 작업자 노드를 인식하고 활용해야 합니다.~~
    - ~~YARN RM은 워커 노드에서 실행되는 NodeManager에 작업을 분산해야 합니다.~~
    - ~~클러스터는 분산 처리를 시연하면서 샘플 MapReduce 작업을 성공적으로 실행할 수 있어야 합니다.~~
- Persistance
    - ~~Docker 컨테이너 내의 Hadoop 데이터 디렉토리는 컨테이너가 다시 시작되기 전에도 데이터를 유지하도록 구성되어야 합니다.~~
    - ~~컨테이너가 중지되었다가 다시 시작되더라도 HDFS에 저장된 데이터가 손상되지 않도록 합니다.~~

### Docker Image

- Docker Image의 경우, 이전 과제였던 Single_Node_Cluster에서 사용했던 Dockerfile을 일부 수정해서 활용했으며, Master와 Slave Node를 한 번에 RUN/DOWN 하여 관리하고자, Docker-Compose를 활용했습니다.
- Dockerfile을 Build할 때, Worker Nodes (Slave Nodes)를 선언해주기 위해서는 내가 실행시킬 Worker Node만큼 추가해줘야했습니다.
    
    ⇒ worker의 정보가 들어있는 file을 `$HADOOP_HOME/etc/hadoop` 경로에 추가하여 생성
    
- Docker 내부에서 Container끼리 통신할 수 있게하기위해 ssh 접근 권한을 변경했습니다.
- Docker 실습을 진행하면서 한 가지 불편했던 부분은, 빌드 후 Dockerfile을 수정해서 재빌드하면 수정되지 않는다는 것이다. 이를 해결하기 위해서는 생성했던 Container/Image를 삭제해야한다. 해당 과정을 간편하게 수행할 수 있도록 `Makefile`을 활용했다.
    
    > make clean ⇒ 실행 중이던 파일들(Image, Volume, Cache)를 삭제할 수 있도록 파일 구성


### Docker Compose

- Master / Slave Node를 각각 다른 Container로 생성하여 실행시켜야하는 상황에서, 각각의 Container를 `docker run ~` 해서 사용하기에는 불편한 부분이 존재한다. 이러한 불편함을 줄여줄 수 있는 것이 docker compose이다.
    
    > 예를 들어, docker run -p 8000:8000 -v <volume_path> <image_name> ~~~ 이렇게 수행해야 하는 여러가지 param들을 docker compose에서 한번에 관리가 가능하다.
    > 
- 동시에 실행되는 Container를 한 번에 관리하기위해 docker compose 사용
- Master / Slave 비율을 1:3으로 설정했으며, Replication ratio를 2로 설정하여 로컬에서 하나의 데이터를 삽입할 때, 세 개의 Slave Node중 두 노드에 저장되는지를 확인하고자 함.
- 본 실습에서도 컨테이너 종료 후 재시작 / 삭제 후 재실행을 진행할 때, 실습했던 정보가 남아있도록 하기 위해 `volume` 설정을 해줬다.

    
### Hadoop 설정 파일

- core-site.xml
    - 기존에는 defaultFS를 localhost(0.0.0.0):9000으로 설정했지만, Multi-node clustering 실습에서는 MasterNode에 접속하도록 해당 부분을 수정했습니다.
    - Client는 MasterNode에게 요청하는 것이 맞기 때문에, [localhost](http://localhost) 역할을 해야하는 것 같습니다.
- hdfs-site.yml
    - hdfs 관련 config를 지정하는 파일이며, 해당 파일을 수정해가며 데이터 복원을 위해 필요한 기능인 replication의 원리를 알게 되었습니다.
    - 처음에는 Slave Node 2, replication 2로 설정했기에, local에서 file을 올려도 두 Slave node에 모두 저장되는 현상을 확인했습니다.
    - 이를 보다 정확하게 해결해보고자, Slave Node 3, replication 2로 설정하여 실험을 해본 결과, 의도했던 대로 Slave 1, 2, 3 중 2개의 Slave Node에만 저장되는 것을 확인했습니다.
        
        ![스크린샷 2024-07-17 오후 5.42.35.png](https://github.com/user-attachments/assets/50baf87a-6db0-403c-ab5b-488989367834)
        
- mapred-site.xml (mapreduce)
    - MapReduce 관련 config를 지정하는 파일이며, 해당 파일을 수정해가며 MapReduce 과정을 이해하기 위해 노력했습니다.
    - map의 job을 10으로 설정하여 MapReduce 작업을 수행할 경우, 10개의 부분 파일로 분할된 작업들이 master를 포함한 4개의 Node에서 분산하여 처리하는 결과를 확인했다.
        
        ![스크린샷 2024-07-17 오후 4.19.34.png](https://github.com/user-attachments/assets/0d91d956-25ea-4fb9-9156-615789d2d031)
        
    - reduce의 job을 2로 설정할 경우, MapReduce 작업이 종료된 후 두 개의 Part(tition) 파일이 생성되며, 각 파티션마다 다른 결과가 저장되는 것을 확인할 수 있다.
        
        ![스크린샷 2024-07-17 오후 5.39.38.png](https://github.com/user-attachments/assets/aa1c31d1-a0d7-40b5-80c0-9ed97f4173fa)
        

### Hadoop 상호작용 / MapReduce 실습

- Docker Container 접속
    
    > 실행 중인 Docker container에 접속하여 내부에서 `hdfs dfs` ~ 명령어를 통해  상호작용 진행
    > 
- 디렉토리 생성 및 파일 업로드
    
    ```bash
    hdfs dfs -mkdir /test # make directory
    hdfs dfs -put text.txt /test # push to $hdfs_root/test
    ```
    
    - word count에 필요한 text 파일은 [Link](https://github.com/nivdul/spark-in-practice-scala/blob/master/data/wordcount.txt)에서 다운로드 함.
- MapReduce 실습
    
    ```bash
    hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount /test /output
    ```

- 결과 확인
    ```bash
    # reduce의 job을 2개로 설정했기 때문에
    hdfs dfs -cat /output/part-r-00000 / hdfs dfs -cat /output/part-r-00001
    ```


### Reference Link

- word count text link: https://github.com/nivdul/spark-in-practice-scala/blob/master/data/wordcount.txt
- Hadoop Multi-Node Cluster Link: https://www.tutorialspoint.com/hadoop/hadoop_multi_node_cluster.htm
- Hadoop Multi-Node Cluster Link: https://medium.com/@jootorres_11979/how-to-set-up-a-hadoop-3-2-1-multi-node-cluster-on-ubuntu-18-04-2-nodes-567ca44a3b12