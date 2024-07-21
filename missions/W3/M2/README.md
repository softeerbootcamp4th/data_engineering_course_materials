## ONE Click Test

### If You Only Want to Test, Not Customize, Follow the Instructions Below
You should execute the command from the directory where the script is located. please following the order!

Instructions:
```sh
./build_and_run_hadoop_services.sh
./apply_all.sh
python3 run build-verify-scripts.py
./configuration_verify.sh usr/local/hadoop namenode
./test_mapreduce.sh usr/local/hadoop namenode
```
Or you can run the one-click script `test.sh`.

## Build Hadoop Cluster

### Step 1: Run the `build_and_run_hadoop_services.sh` Script
Instruction:
```sh
./build_and_run_hadoop_services.sh
```

### Flow of Building and Running Hadoop Cluster

1. The `build_and_run_hadoop_services.sh` script builds four types of Docker images (for DataNode, NameNode, ResourceManager, and NodeManager).
2. It runs these images with Docker Compose, which should be set up before running `build_and_run_hadoop_services.sh`.
3. Each Dockerfile is created as follows:
    - Uses `ubuntu:22.04` as the base image.
    - Installs the necessary packages to run Hadoop.
    - Creates a user and sets environment variables.
    - Downloads and installs Hadoop.
    - Configures the SSH service.
    - Copies Hadoop configuration files from `local/workdir/config/`.
    - Copies the script for running Hadoop. This script is executed when the container starts and ends with the command `tail -f /dev/null` to keep the PID 1 process running, preventing the container from shutting down.
    - The Hadoop programs are basically daemon services.

## Change Configuration

### Step 1: Modify the Configuration Files
Modify the configuration files in `/change-config`.

### Step 2: Add Required Directories for Configuration Changes
Add the directories that need to be included for configuration changes at the bottom of the `make_dir.sh` file.
<Example>
```xml
<property>
    <name>dfs.namenode.name.dir</name>
    <value>file:///hadoop/dfs/name</value>
</property>
<property>
    <name>dfs.datanode.data.dir</name>
    <value>file:///hadoop/dfs/data</value>
</property>
```
When changing as above, `/hadoop/dfs/name` and `/hadoop/dfs/data` paths must be added inside the container.

### Step 3: Add the Container to `apply_all.sh`
Add a command line like:
```sh
./configuration_modify.sh $HADOOP_HOME $CONTAINER_NAME $ROLE
```

### Step 4: Run `apply_all.sh`
Instruction:
```sh
./apply_all.sh
```
As a result, the changes are applied.

## Verification

### Step 1: Run `build-verify-scripts.py`
Instruction:
```sh
python3 run build-verify-scripts.py
```
This creates four `.sh` files to verify the changed configuration: `verify_core-site_conf.sh`, `verify_hdfs-site_conf.sh`, `verify_mapred-site_conf.sh`, `verify_yarn-site_conf.sh`.

### Step 2: Run `configuration_verify.sh`
Instruction:
```sh
./configuration_verify.sh <HADOOP_HOME> <CONTAINER_NAME>
```

## MapReduce

### Just Run `test_mapreduce.sh`
Instruction:
```sh
./test_mapreduce.sh <HADOOP_HOME> <CONTAINER_NAME>
```
`wordcount.sh` is a one-click MapReduce test script executed in the container. It initializes the HDFS directory for MapReduce work.

* 참고사항 : HDFS instruction
- 디렉토리 생성, 파일 업로드, 파일 읽기

> 현재 작업 경로(”/usr/local/hadoop/data”)에서 파일을 생성합니다.
echo "apple banana grape" > localfile.txt

하둡 파일 시스템에 디렉토리를 생성합니다.
hdfs dfs -mkdir /user

/user 디렉토리에 localfile.txt 파일을 업로드합니다.
hdfs dfs -put localfile.txt /user

업로드 이후 하둡 파일 시스템의 루트에서부터 하위 디렉토리 정보를 확인합니다.
hdfs dfs -ls -R /

/user/localfile.txt 를 열어 내용을 확인합니다.
hdfs dfs -cat /user/locafile.txt

hdfs dfs -rm -r /user
hdfs dfs -rm -r /tmp
>

### If You Want to Test Using Another MapReduce Process
Change `input.txt`, `wordcount.sh`.


## Troubleshooting

If you change the `dfs.datanode.data.dir` property, there is a possibility that you can get:
```java
java.io.IOException: Incompatible clusterIDs in /hadoop/dfs/data: namenode clusterID = CID-8ec62c1c-7b9a-413b-afa2-05dd41fc8f94; datanode clusterID = CID-79c89a70-9b81-4808-a954-d6d4d8c98c02
```
This is because the directory with the changed settings already exists. You should remove the directory and run the script again.

* Example
```xml
<property>
    <name>dfs.datanode.data.dir</name>
    <value>file:///usr/local/hadoop/data/datanode</value>
</property>
```

---