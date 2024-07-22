
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

The input file is `All_Beauty.jsonl`. This file is not available on this GitHub repo but can be obtained from [amazon-github](https://amazon-reviews-2023.github.io/).

The input file is split into chunks and processed in parallel on each node using the `mapper.py` and `reducer.py` scripts. The mapper script generates key-value pairs, which are then aggregated by the reducer script.

In this process, we can obtain rows with product ID, the number of reviews, and the average rating.

* **`mapper.py`**: 
  In `mapper.py`, each line from the input stream is in the form of a JSON object. The values associated with the keys 'asin' and 'rating' are extracted to form a key-value pair in the format `"{asin}\t{rating}"`. The mapper outputs these key-value pairs, which are then shuffled and sorted by the Hadoop framework before being passed to the reducers.

* **`reducer.py`**:
  The reducer receives sorted key-value pairs. It increments the count for each 'asin' and accumulates the ratings. Finally, it computes the average rating by dividing the sum of the ratings by the count of the 'asin' occurrences and outputs this average.

### Step 2: Modify `wordcount.sh`

Two new files, `mapper.py` and `reducer.py`, need to be copied into the container. The `wordcount.sh` script, which is also copied into the container, should be modified as follows. These changes have already been applied:

- Add the following command to execute the MapReduce job in Hadoop:

```sh
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-mapper mapper.py \
-reducer reducer.py \
-input /user/hadoop/input/All_Beauty.jsonl \
-output /user/hadoop/output \
-file ./mapper.py \
-file ./reducer.py
```

- Add the commands to copy `mapper.py` and `reducer.py`:

```sh
# Copy files for MapReduce
copy_file All_Beauty.jsonl $HADOOP_HOME/mapreduce_test
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

### Amazon Product Review

Retrieve the result file to the local directory of the container with the following command:

```sh
hadoop fs -get /user/hadoop/output/part-00000 /usr/local/hadoop/data/namenode/current/result_M6
```

The output file will be saved in the `.../result/` directory.

Example output:

```Markdown
0005946468	1	5.00
0123034892	1	5.00
0124784577	3	4.33
0515059560	1	4.00
0615675026	1	2.00
...
```

Please check the result file for the complete details.

## Reference

### `All_Beauty.jsonl`

File source:
- [Amazon](https://amazon-reviews-2023.github.io/)

Download link:
- [All_Beauty.jsonl](https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_2023/raw/review_categories/All_Beauty.jsonl.gz)

---
