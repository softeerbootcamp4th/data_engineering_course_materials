## HADOOP 구성 파일 이해

### Funtional Requirements

- core-site.xml
    - ~~Change fs.defaultFS to hdfs://namenode:9000.~~
    - ~~Change hadoop.tmp.dir to /hadoop/tmp.~~
    - ~~Change io.file.buffer.size to 131072.~~
- hdfs-site.xml
    - ~~Change dfs.replication to 2.Change dfs.~~
    - ~~blocksize to 134217728 (128 MB).~~
    - ~~Change dfs.namenode.name.~~
    - ~~dir to /hadoop/dfs/name.~~
- mapred-site.xml
    - ~~Change mapreduce.framework.name to yarn.~~
    - ~~Change mapreduce.jobhistory.address to namenode:10020.~~
    - ~~Change mapreduce.task.io.sort.mb to 256.~~
- yarn-site.xml
    - ~~Change yarn.resourcemanager.hostname to resourcemanager.~~
    - ~~Change yarn.nodemanager.resource.memory-mb to 8192.~~
    - ~~Change yarn.scheduler.minimum-allocation-mb to 1024.~~

### 과제 수행 방법

- 프로그래밍 요구사항에 맞게, Python / Shell script를 활용하여 실습코드를 작성했습니다.
- `modify_config.py`에서는 기존 *-site.xml에 담겨있는 config를 *.bak 확장자로 백업을 진행한 후, 기존 *-site.xml에 2b 과제에서 요구하는 config값으로 변경하는 과정을 수행합니다.
- `rollback.sh`는 과제에서 요구한 사항은 아니지만, 과제 수행방법외 추가로 backup file을 활용하여 기존 config로 돌아오는 과정을 수행합니다.
- `Hadoop getcong -confKey`를 통해 Hadoop Cluster와 상호작용하며 Config 값들을 가져오고 확인하는 작업을 진행하는  `verify_config.sh` 코드를 작성했습니다.

### Modify_config

- python script를 활용하여 코드를 작성했으며, xml 데이터의 구조를 파싱하여 값을 변경할 수 있는 라이브러리인 xml.etree.ElementTree를 활용했습니다.
- 기존 *-site.xml에 담겨있는 config를 *.bak 확장자로 백업을 진행한 후, 기존 *-site.xml에 2b 과제에서 요구하는 config값으로 변경하는 과정을 수행하도록 코드를 작성했습니다.
- 직접 변경된 파일을 확인하는 방법과, verify_config.sh를 확인하는 방법을 통해 변경 여부를 확인이 가능합니다.
    
    ```bash
    python3 modify_config.py
    ```

### Verify_config

- shell script를 활용하여 코드를 작성했으며, `hdfs getconf ~` 를 통해 Hadoop Cluster와 상호작용하며 현재 실행중인 컨테이너 내 Hadoop의 config를 확인했습니다.

    ```bash
    bash verify_config.sh
    ```

### rollback_config

- 본 실습에서 초기 config로 돌아가는 코드를 추가로 작성했습니다.    

    ```bash
    bash rollback_config.sh
    ```