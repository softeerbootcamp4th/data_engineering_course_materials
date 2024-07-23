
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

The input file is `ratings.csv`. This file is not available on GitHub but can be obtained from [Grouplens Dataset](https://grouplens.org/datasets/movielens/20m/).

The input file is split into chunks and processed in parallel on each node using the `mapper.py` and `reducer.py` scripts. The mapper script generates key-value pairs, which are then aggregated by the reducer script.

In this process, we count the occurrences of sentiments.

* **`mapper.py`**: 
  In `mapper.py`, each line from the input stream is split by commas. From the fields `userId, movieId, rating, timestamp`, the `movieId` and `rating` are extracted and returned as a key-value pair. The mapper outputs these key-value pairs, which are then shuffled and sorted by the Hadoop framework before being passed to the reducers.

* **`reducer.py`**:
  The reducer receives sorted key-value pairs, where each key (movieId) is processed along with all its associated values (ratings). The reducer sums the ratings and counts the number of ratings for each `movieId`, then returns the `movieId` and the average rating.

### Step 2: Modify `wordcount.sh`

Two new files, `mapper.py` and `reducer.py`, need to be copied into the container. The `wordcount.sh` script, which is also copied into the container, should be modified as follows. These changes have already been applied:

- Add the following command to execute the MapReduce job in Hadoop:

```sh
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-mapper mapper.py \
-reducer reducer.py \
-input /user/hadoop/input/ratings.csv \
-output /user/hadoop/output \
-file ./mapper.py \
-file ./reducer.py
```

- Add the commands to copy `mapper.py` and `reducer.py`:

```sh
# Copy files for MapReduce
copy_file ratings.csv $HADOOP_HOME/mapreduce_test
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

### Average Rating of Movies

Retrieve the result file to the local directory of the container with the following command:

```sh
hadoop fs -get /user/hadoop/output/part-00000 /usr/local/hadoop/data/namenode/current/result_M5
```

The output file will be saved in the `.../result/` directory.

Example output:

```Markdown
1	3.921239561324077
10	3.430029305292191
100	3.22138517618469
1000	3.105911330049261
100003	3.6666666666666665
...
```

Please check the result file for the complete details.

## Reference

### `ratings.csv`

File source:
- [Grouplens Dataset](https://grouplens.org/datasets/movielens/20m/)

Download link:
- [MovieLens 20M Dataset](https://files.grouplens.org/datasets/movielens/ml-20m.zip)

---
