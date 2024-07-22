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
- Docker compose 관련
    - docker compose를 이용하면 알아서 이미지 빌드부터 컨테이너의 생성까지 해준다.
    - dockerfile의 entry point에서 사용하는 shell script를 수정하다가 생긴 오류를 고치려고 많은 시간을 썼다.
    - 나는 dockerfile을 고치지 않았고, shell script만 고친 상태이니 docker compose를 이용해서 실행할 때 이미지를 다시 빌드하지 않는다.
    - 그렇게 만들어진 container에는 당연히 shell script가 수정되어 있지 않다.
    - 이걸 몰라서 2시간 정도를 날렸다~
- config를 바꾼 후, datanode를 다시 켜기 전에 (dfs.datanode.data.dir 설정에 해당하는) 기존의 data dir을 삭제해 주어야 한다. 
    - 새로운 config로 수정한 후 namenode, datanode를 다시 켜게 되면, resource manager에는 분명히 datanode가 2개 떠있는데, namenode(localhost:9870)에서 확인하면 datanode가 잡히지 않았다.
    - 새로운 config로 시작하는 namenode는 새로운 cluster ID를 갖게 되고, datanode와 namenode의 cluster id가 달라 통신이 되지 않는다고 이해했다.
    - 이 정보가 data dir 내부 파일(datanode/current/VERSION)에 저장되어 있어, 이를 삭제해 주어야 한다.
    - 그 후에 datanode를 실행하게 되면, 정상적으로 동작한다.