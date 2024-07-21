
## Sentiment Analysis using Hadoop MapReduce

### Overview
This project demonstrates the use of Apache Hadoop and MapReduce to analyze the sentiment of tweets using the 'Twitter Data from Sentiment140' dataset.

### Prerequisites
- Hadoop 3.3.3
- Python 3.8
- Docker

### Dataset
The dataset used is the 'Twitter Data from Sentiment140' which contains tweets classified into three sentiment categories:
- 0: Negative
- 2: Neutral 
- 4: Positive

### Steps

1. **Build Docker Image and Start Hadoop Cluster**

   ```bash
   docker build -t w3m4:latest . 
   docker-compose up -d   
   ```

2. **Upload Dataset to HDFS**

   ```bash
   docker cp ~/Desktop/w3m4/sentiment.csv master:/home/hduser/sentiment.csv
   docker exec -it master /bin/bash
   hdfs dfs -mkdir -p /user/hduser/projects
   hdfs dfs -put /home/hduser/sentiment.csv /user/hduser/projects/sentiment.csv
   hdfs dfs -ls /user/hduser/projects
   ```

3. **Run MapReduce Job**

   ```bash
   hadoop jar /home/hduser/hadoop-3.3.3/share/hadoop/tools/lib/hadoop-streaming-3.3.3.jar \
     -files /home/hduser/mapper.py,/home/hduser/reducer.py \
     -mapper 'python3 mapper.py' \
     -reducer 'python3 reducer.py' \
     -input /user/hduser/projects/sentiment.csv \
     -output /user/hduser/projects/output
   ```

4. **Check Output**

   ```bash
   hdfs dfs -cat /user/hduser/projects/output/part-00000
   ```

### Explanation of Mapper and Reducer
- **Mapper**: The mapper processes each tweet and classifies it as positive, negative, or neutral based on the sentiment value. It emits key-value pairs where the key is the sentiment category and the value is 1.
- **Reducer**: The reducer aggregates the counts for each sentiment category and outputs the total count for each category.

### Example Output
The output file should contain the counts for each sentiment category as follows:

```
negative   800000
positive   800000
```
