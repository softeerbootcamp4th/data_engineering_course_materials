### Mission 2-a

#### Bulild Image and Create Containers
- Run Container
```
docker compose up -d .
```

- Attach to master node
```
docker exec -it hadoop-master /bin/bash
```

#### Run MapReduce Job
```
./run_wordcount.sh
```

#### Check Hadoop serivces
jps command를 이용하여 현재 실행 중인 hadoop service 확인
- Master Node
    - NameNode, SecondaryNameNode, ResourceNamager, NodeManager 실행

- Slave Node
    - DataNode, NodeManager 실행


#### Retrieve Containers & Check Data Persistency
```
docker-compose down
docker-compose up -d
```

localhost:9870 -> Utilities -> Browse the file system에서, 앞서 생성한 wordcount 결과 확인 가능 (/user/root/output)

#### Trouble Shooting
- dockerfile의 entry point에서 사용하는 shell script를 수정하다가 생긴 오류를 고치려고 많은 시간을 썼다.
- docker compose를 이용하면 알아서 이미지 빌드부터 컨테이너의 생성까지 해준다.
- 나는 dockerfile을 고치지 않았고, shell script만 고친 상태이니 docker compose를 이용해서 실행할 때 이미지를 다시 빌드하지 않는다.
- 그렇게 만들어진 container에는 당연히 shell script가 수정되어 있지 않다.
- 이걸 몰라서 2시간 정도를 날렸다~