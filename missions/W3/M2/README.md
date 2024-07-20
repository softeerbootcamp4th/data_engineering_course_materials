# INIT 

## Build initial hadoop cluster
* step 1 : run "build_and_run_hadoop_services.sh"
instruction | ./build_and_run_hadoop_services.sh

## Change Configuration
* step 1 : Modify the configuration files in "/change-config".
* step 2 : Add the directories that need to be included for configuration changes at the bottom of the "make_dir.sh" file.
<예시> 
''' xml
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///hadoop/dfs/name</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///hadoop/dfs/data</value>
'''

When changing as above, /hadoop/dfs/name and /hadoop/dfs/data paths must be added inside the container.

* step 3 : 변경 사항을 적용할 컨테이너를 apply_all.sh에 추가합니다
./configuration_modify.sh $HADOOP_HOME $CONTAINER_NAME $ROLE 오 같은 명령행을 추가합니다.

* step 4 : run "apply_all.sh"
instruction | ./apply_all.sh
변경사항이 적용됩니다.


## Verification
* step 1 : run "build-verify-scrips.py"
instruction | python3 run build-verify-scrips.py
it creates four .sh files for verify changed configuration
"verify_core-site_conf.sh", "verify_hdfs-site_conf.sh", "verify_mapred-site_conf.sh", "verify_yarn-site_conf.sh" 

The above four scripts are required to run configuration_verify.sh

* step 2 : run "configuration_verify.sh"
instruction : ./configuration_verify.sh <HADOOP_HOME> <CONTAINER_NAME>

## mapreduce
* just run test_mapreduce.sh
instruction : ./test_mapreduce.sh <HADOOP_HOME> <CONTAINER_NAME>

* if you want to test by using another mapreduce process
* chagene input.txt, wordcount.sh


## TEST
* if you only want to test, not customise then, just follow instructions below
instruction | ./build_and_run_hadoop_services.sh
instruction | ./apply_all.sh
instruction | python3 run build-verify-scrips.py
instruction : ./configuration_verify.sh usr/local/hadoop namenode
instruction : ./test_mapreduce.sh usr/local/hadoop namenode


## Troble Shooting
if you change dfs.datanode.data.dir property, then there is a possibility that you can get "java.io.IOException: Incompatible clusterIDs in /hadoop/dfs/data: namenode clusterID = CID-8ec62c1c-7b9a-413b-afa2-05dd41fc8f94; datanode clusterID = CID-79c89a70-9b81-4808-a954-d6d4d8c98c02"

This is because the directory with the changed settings already exists. you should remove the directory and run script again

''' xml
<property>
    <name>dfs.datanode.data.dir</name>
    <value>file:///usr/local/hadoop/data/datanode</value>
</property>
'''
