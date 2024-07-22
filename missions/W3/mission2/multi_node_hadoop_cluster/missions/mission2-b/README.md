### Mission 2-b

#### Modify Config
``` (모든 hadoop container에서 실행. - namenode, datanode1, datanode2)
./mission/mission2-b/script_config_modify.sh
```


#### Verify Config
```
./mission/mission2-b/script_verify.sh
```

#### Trouble Shooting
- config를 바꾼 후, datanode를 다시 켜기 전에 (dfs.datanode.data.dir 설정에 해당하는) 기존의 data dir을 삭제해 주어야 한다. 
    - 새로운 config로 수정한 후 namenode, datanode를 다시 켜게 되면, resource manager에는 분명히 datanode가 2개 떠있는데, namenode(localhost:9870)에서 확인하면 datanode가 잡히지 않았다.
    - 새로운 config로 시작하는 namenode는 새로운 cluster ID를 갖게 되고, datanode와 namenode의 cluster id가 달라 통신이 되지 않는다고 이해했다.
    - 이 정보가 data dir 내부 파일(datanode/current/VERSION)에 저장되어 있어, 이를 삭제해 주어야 한다.
    - 그 후에 datanode를 실행하게 되면, 정상적으로 동작한다.