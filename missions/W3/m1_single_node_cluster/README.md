# Directory Hierarchy
```
├── Dockerfile
├── start-hadoop.sh
├── config/
    ├── hadoop-env.sh
    ├── core-site.xml
    ├── hdfs-site.xml
    ├── mapred-site.xml
    └── yarn-site.xml
```

# Build Image
```bash
(local)% docker build -t hadoop-single-node .
```

# Run Container
```bash
(local)% docker run -it -p 9870:9870 -p 8088:8088 -p 9864:9864 --name hadoop-single-node hadoop-single-node
```

# Working on HDFS
### Make Directory
```bash
(container)$ hdfs dfs -mkdir /user
(container)$ hdfs dfs -mkdir /user/hadoopuser
```
### Upload File
```bash
(container)$ echo "this is test file" >> test.txt
(container)$ hdfs dfs -put test.txt /user/hadoopuser
```
### Check Upload
```bash
(container)$ hdfs dfs -ls /user/hadoopuser
(container)$ hdfs dfs -cat /user/hadoopuser/test.txt
```
