# Hadoop Single Node Cluster with Docker

This README provides step-by-step instructions for building a Docker image, running the container, and performing HDFS operations on a single-node Hadoop cluster using Docker.

## Prerequisites

- Docker installed on your local machine
- Basic knowledge of Docker and HDFS

## Step 1: Prepare the Project Directory

Ensure you have the following files in your project directory:

1. **Dockerfile**: Contains instructions for building the Docker image.
2. **core-site.xml**: Hadoop core configuration file.
3. **hdfs-site.xml**: Hadoop HDFS configuration file.
4. **mapred-site.xml**: Hadoop MapReduce configuration file.
5. **yarn-site.xml**: Hadoop YARN configuration file.
6. **docker-entrypoint.sh**: Entry point script for the Docker container.

The Dockerfile is structured to:

- Use an Ubuntu base image.
- Install necessary packages such as Java, SSH, and Hadoop.
- Set environment variables for Hadoop.
- Create a Hadoop user.
- Copy configuration files into the container.
- Set up the entry point script and expose necessary ports.

## Step 2: Build the Docker Image

1. Open your terminal and navigate to the directory containing your Dockerfile and configuration files.
2. Build the Docker image using the following command:

    ```sh
    docker build -t hadoop-single-node .
    ```

## Step 3: Run the Docker Container

1. Run the Docker container using the following command:

    ```sh
    docker run -it -p 8088:8088 -p 8042:8042 -p 50070:50070 -p 50075:50075 -p 50010:50010 -p 50020:50020 -p 50090:50090 hadoop-single-node
    ```

2. Open a new terminal and verify that the container is running:

    ```sh
    docker ps
    ```

3. Access the container's shell:

    ```sh
    docker exec -it <container_id> /bin/bash
    ```

    Replace `<container_id>` with the actual container ID from the `docker ps` output.

## Step 4: Perform HDFS Operations

### 4.1 Create Directories in HDFS

Inside the container, create directories in HDFS:

```sh
hdfs dfs -mkdir -p /user/hduser/mission1

### 4.2 Upload Files to HDFS

Copy the local file to the Docker container
'''sh
docker cp ~/Desktop/Mission1/mtcars.csv <container_id>:/home/hduser/

Inside the container, upload the file to HDFS
'''sh
hdfs dfs -put /home/hduser/mtcars.csv /user/hduser/mission1/

### 4.3 Verify File Upload

List the files in the HDFS directory to verify the upload
'''sh
hdfs dfs -ls /user/hduser/mission1/

Display the contents of the uploaded file
'''sh
hdfs dfs -cat /user/hduser/mission1/mtcars.csv

### Step 5: Access HDFS Web UI

Open your web browser and go to the following URL to access the HDFS NameNode UI
http://localhost:50070

You should see the HDFS NameNode web interface, where you can browse the HDFS directories and files.