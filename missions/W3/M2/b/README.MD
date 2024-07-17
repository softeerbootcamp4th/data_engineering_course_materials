## Modifying configs

W3M2a에서 클러스터를 구축한것을 전제로 설정값들을 변경, 적용.
`modify_config.py ./config`를 실행하면 ./config 디렉토리 내의 설정값들을
적용하고 클러스터를 재시작해서 적용된다.

## 요구 사항

1. [X] The script should accept the path to the Hadoop configuration directory as an argument.
2. [X] It should back up the original configuration files before making any changes.
3. [X] The script should modify the specified settings in the XML files to the given values.
4. [X] Restart the Hadoop services.

## Verifying configs
`verify.py`를 실행하면 verify 절차가 진행된다.

## 요구 사항
1. [X] The script should confirm the default file system name is set correctly by running a relevant Hadoop command and parsing the output.
2. [X] It should create a test file in HDFS and check its replication factor to verify the change.
3. [X] The script should run a simple MapReduce job and ensure it uses the YARN framework.
4. [X] It should query YARN ResourceManager to verify the total available memory for YARN.
5. [X] The script should verify the temporary directory, buffer size, block size, NameNode directory, JobTracker, sort memory buffer size, ResourceManager hostname, NodeManager memory allocation, and container minimum allocation.
6. [X] Query the Hadoop configuration to check the modified settings.
7. [X] Print the results, indicating whether each setting matches the expected value.
8. [X] Create a test file in HDFS and verify the replication factor.

# TODO 
modify_config.py는 한 번 실행하고 두번은 못함..