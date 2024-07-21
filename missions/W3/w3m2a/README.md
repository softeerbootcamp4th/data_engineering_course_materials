# Hadoop Docker Setup

This project provides a setup to run Apache Hadoop in Docker containers. This README file explains how to run the containers, perform HDFS operations, and execute cluster tasks.

## Project Components

1. **Dockerfile**: Contains instructions for building the Docker image.
2. **core-site.xml**: Hadoop core configuration file.
3. **hdfs-site.xml**: Hadoop HDFS configuration file.
4. **mapred-site.xml**: Hadoop MapReduce configuration file.
5. **yarn-site.xml**: Hadoop YARN configuration file.
6. **docker-entrypoint.sh**: Initializes and starts NameNode and DataNode services when the container starts.
7. **docker-compose.yml**: Defines Docker containers for NameNode and DataNode.


## Running the Containers

1. **Build and Start Containers**

   ```bash
   docker-compose up --build
   ```

   This command builds the image based on the Dockerfile and starts two containers for NameNode and DataNode using Docker Compose.

2. **Check Services**

   Ensure all Hadoop services (NameNode, DataNode, ResourceManager, NodeManager) are running inside the containers. Check running services with:

   ```bash
   docker exec -it master jps
   docker exec -it worker jps
   ```

   Example output:

   ```bash
   # From master container
   69 NameNode
   553 NodeManager
   204 ResourceManager
   748 Jps

   # From worker container
   17 DataNode
   521 Jps
   303 NodeManager
   ```

## HDFS Operations

1. **Create Directory in HDFS**

   Create a directory in HDFS from the master node:

   ```bash
   docker exec -it master hdfs dfs -mkdir /user/hduser/test
   ```

2. **Upload Files**

   Upload a file from the local filesystem to HDFS. For example, to upload the `mtcars` file:

   ```bash
   docker cp mtcars master:/home/hduser/
   docker exec -it master hdfs dfs -put /home/hduser/mtcars /user/hduser/test/
   ```

3. **View Files**

   View the uploaded file from HDFS:

   ```bash
   docker exec -it master hdfs dfs -ls /user/hduser/test/
   docker exec -it master hdfs dfs -cat /user/hduser/test/mtcars
   ```

## Cluster Tasks

1. **Run a MapReduce Job**

   Execute a sample MapReduce job on the Hadoop cluster. For example, run the WordCount example:

   1. **Run WordCount Example**

      ```bash
      docker exec -it master hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount /user/hduser/test/mtcars /user/hduser/test/output
      ```

   2. **Check Output**

      After the job completes, check the results:

      ```bash
      docker exec -it master hdfs dfs -ls /user/hduser/test/output
      docker exec -it master hdfs dfs -cat /user/hduser/test/output/part-r-00000
      ```
