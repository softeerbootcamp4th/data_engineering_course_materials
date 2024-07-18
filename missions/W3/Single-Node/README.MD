# Hadoop Single Node Cluster

## Build the Docker image
```bash
docker build --tag docker-softeer:latest .
```

## Run Docker container
```bash
docker run -it -p 9870:9870 -p 8088:8088 -p 9864:9864 --hostname localhost --name hadoop hadoop-softeer:latest
```

## Retrieve the file
1. Connect to http://localhost:9870/ with a browser.
2. Click 'Utilities' in the navigation bar.
![](img/browse_directory_1.png)
3. Click 'Browse the file system' under 'Utilites'.
![](img/browse_directory_2.png)
4. You can see the file list of the root directory.
![](img/browse_directory_3.png)
5. If you want to go into a subdirectory, click the name of the subdirectory.
![](img/browse_directory_4.png)
6. You can see your current location here.
![](img/browse_directory_5.png)

## Create a new directory in HDFS
1. Click the folder button.
![](img/create_directory_1.png)
2. Type the name of the new directory in the input bar.
![](img/create_directory_2.png)
3. Click 'Create'
![](img/create_directory_3.png)

## Upload a file in HDFS
1. Click cloud button
![](img/upload_file_1.png)
2. Click 'Choose files' button
![](img/upload_file_2.png)
3. Select the file to upload
4. Click 'Upload' button
![](img/upload_file_3.png)