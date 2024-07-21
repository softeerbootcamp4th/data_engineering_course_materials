
---

## Test

To execute the MapReduce job, run the `test_mapreduce.sh` script with the following command:

```sh
./test_mapreduce.sh
```

## Announcement

* This task is executed within the container created in M2.
* The MapReduce files used in M2 have been appropriately modified and are utilized here.

## MapReduce Process

### Step 1: Create Mapper and Reducer Scripts (mapper.py, reducer.py)

The input file is `training.1600000.processed.noemoticon.csv`. This file is not available on GitHub but can be obtained from [Kaggle](https://www.kaggle.com/datasets/kazanova/sentiment140).

The input file is split into chunks and processed in parallel on each node using the `mapper.py` and `reducer.py` scripts. The mapper script generates key-value pairs, which are then aggregated by the reducer script.

In this process, we count the occurrences of sentiments.

* **`mapper.py`**: 
  In `mapper.py`, each line from the input stream is split by commas. The first field is checked to determine the sentiment. If the sentiment value is "0", it is labeled as "negative"; if "2", as "neutral"; and if "4", as "positive". Each sentiment is output as a key with a value of 1. The mapper outputs key-value pairs, which are then shuffled and sorted by the Hadoop framework before being passed to the reducers.

* **`reducer.py`**:
  The reducer receives sorted key-value pairs, where each key (sentiment) is processed along with all its associated values (counts). The reducer aggregates the counts for each sentiment and outputs the result.

### Step 2: Modify `wordcount.sh`

Two new files, `mapper.py` and `reducer.py`, need to be copied into the container. The `wordcount.sh` script, which is also copied into the container, should be modified as follows. These changes have already been applied:

- Add the following command to execute the MapReduce job in Hadoop:

```sh
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-mapper mapper.py \
-reducer reducer.py \
-input /user/hadoop/input/training.1600000.processed.noemoticon.csv \
-output /user/hadoop/output \
-file ./mapper.py \
-file ./reducer.py
```

- Add the commands to copy `mapper.py` and `reducer.py`:

```sh
# Copy files for MapReduce
copy_file input.txt $HADOOP_HOME/mapreduce_test
copy_file wordcount.sh $HADOOP_HOME/mapreduce_test
########## Add files here ##########
# copy_file <SOURCE_FILE> $HADOOP_HOME/mapreduce_test
copy_file mapper.py $HADOOP_HOME/mapreduce_test
copy_file reducer.py $HADOOP_HOME/mapreduce_test
# End ##################################
```

### Step 3: Run `test_mapreduce.sh`

Execute the script to run the MapReduce job on the namenode container.

## Result

### File in HDFS

To check the result file, use the following command:

```sh
hadoop fs -cat /user/hadoop/output/part-00000
```

### Sentiment Counts

Retrieve the result file to the local directory of the container with the following command:

```sh
hadoop fs -get /user/hadoop/output/part-00000 /usr/local/hadoop/data/namenode/current/result_M3
```

The output file will be saved in the `.../result/` directory.

Example output:

```Markdown
negative    800000
positive    800000
```

No neutral sentiment sentences are present.

## Reference

### `training.1600000.processed.noemoticon.csv`

File source:
- [Kaggle Dataset](https://www.kaggle.com/datasets/kazanova/sentiment140)

Download link:
- [Sentiment140 Dataset](https://www.kaggle.com/datasets/kazanova/sentiment140)

---
