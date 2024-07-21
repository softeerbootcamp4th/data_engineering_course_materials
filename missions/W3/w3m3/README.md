
# Hadoop MapReduce Word Count Project

## Introduction
This project demonstrates a MapReduce program to count word occurrences in a text file using Apache Hadoop. The project includes uploading a text file to HDFS, running the MapReduce job using Python scripts for the mapper and reducer, and verifying the results.

## Prerequisites
- Apache Hadoop 3.3.3
- Python 3.8 or later
- A Hadoop cluster (single-node or multi-node)
- A text file (e.g., `romeo_text_file.txt`)

## Setup

### 1. Upload Text File to HDFS
Ensure Hadoop is correctly installed and configured on your cluster. Upload the text file to HDFS.

1. Create a directory in HDFS:
   ```bash
   hdfs dfs -mkdir -p /user/hduser/projects
   ```

2. Upload the text file to HDFS:
   ```bash
   hdfs dfs -put /home/hduser/romeo.txt /user/hduser/projects/romeo.txt
   ```
   Check the uploaded file:
   ```bash
   hdfs dfs -ls /user/hduser/projects
   ```

### 2. Mapper and Reducer Scripts
Create the `mapper.py` and `reducer.py` scripts in your working directory.

- **Mapper**: The mapper reads the input text file line by line, splits each line into words, and emits a key-value pair for each word with a count of 1.
- **Reducer**: The reducer reads the key-value pairs emitted by the mapper, aggregates the counts for each word, and emits the total count for each word.

### 3. Running the MapReduce Job
Run the MapReduce job using the following command:

```bash
hadoop jar /home/hduser/hadoop-3.3.3/share/hadoop/tools/lib/hadoop-streaming-3.3.3.jar \
  -files /home/hduser/mapper.py,/home/hduser/reducer.py \
  -mapper 'python3 mapper.py' \
  -reducer 'python3 reducer.py' \
  -input /user/hduser/projects/romeo.txt \
  -output /user/hduser/projects/output
```

### 4. Verifying the Results
Retrieve and view the output:

1. List the output directory:
   ```bash
   hdfs dfs -ls /user/hduser/projects/output
   ```

2. View the contents of the output file:
   ```bash
   hdfs dfs -cat /user/hduser/projects/output/part-00000
   ```

### Example Output
```
see     40
seeds   1
seeing  3
seek    4
seeking 1
seeks   1
seem    2
seeming 4
seems   2
seen    6
...
```

## E-book Information
- **Title**: *Romeo and Juliet*
- **Author**: William Shakespeare
- **Source**: Project Gutenberg (http://www.gutenberg.org/ebooks/1112)

