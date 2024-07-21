
---

# ONE Click Test

## If You Only Want to Test, Not Customize, Follow the Instructions Below
You should execute the command from the directory where the script is located. Please follow the order below:

### Instructions:
```sh
python3 pdf_to_txt.py
./test_mapreduce.sh usr/local/hadoop namenode
```
Or you can run the one-click script `one_click.sh`.

## Announcement
* This task is performed in the container created in M2.
* The MapReduce files used in M2 are appropriately modified and used here.

## MapReduce Process

### Step 1: Create Mapper and Reducer Scripts (mapper.py, reducer.py)
The `input.txt` file is divided and processed in parallel on each node. The files required for processing are `mapper.py` and `reducer.py`.

In the MapReduce process, the input.txt file is split into chunks and each node processes these chunks by creating key-value pairs. Here, `mapper.py` is used. Each node returns pairs in the form of "word: count ~ key: value". The same key-value pairs are then sent to the reducer, which aggregates the values and outputs the result.

In this process, we are counting the occurrences of words, so we removed all non-alphabetic characters. This pre-processing step can either be done before generating the `input.txt` file or within the mapper process. Depending on the requirements, performance might vary. In this MapReduce process, the functionality is implemented within `mapper.py`.

### Step 2: Create input.txt
Generate the `input.txt` required for the MapReduce process. This task is performed in the `.../M3/` directory. The `pride_and_prejudice.pdf` file should be prepared in advance. The `pdf_to_txt.py` script extracts text from the `pride_and_prejudice.pdf` file and saves it as `mapreduce/input.txt`.

### Step 3: Modify wordcount.sh
Two new files, `mapper.py` and `reducer.py`, have been created and need to be copied to the container for use. The `wordcount.sh` script, which is copied into the container, needs to be modified as follows. The changes have already been applied.

- Add the following command to perform the MapReduce task in Hadoop:
```sh
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
-mapper mapper.py \
-reducer reducer.py \
-input /user/hadoop/input/input.txt \
-output /user/hadoop/output \
-file ./mapper.py \
-file ./reducer.py
```

- Add the command to copy `mapper.py` and `reducer.py`:
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

### Step 4: Run `test_mapreduce.sh`
Running this script will execute the MapReduce task on the namenode container.

## Result

### File in HDFS
You can check the result file with the following command:
```sh
hadoop fs -cat /user/hadoop/output/part-00000
```

### Words in Files
You can bring the result file to the container's local directory with the following command:
```sh
hadoop fs -get /user/hadoop/output/part-00000 /usr/local/hadoop/data/namenode/current
```

The output file is saved in the `.../result/` directory. The `result_to_csv.py` script converts the result to a CSV file and sorts it to display the final output.

```Markdown
Word,Count
to,4083
the,4046
of,3583
and,3377
her,2125
```
The top 5 most frequent words are shown above.

## Reference

### pride_and_prejudice.pdf

The file source:
- [Project Gutenberg](https://www.gutenberg.org)

Free E-books are provided here.

Download link:
- [Pride and Prejudice PDF](https://www.gutenberg.org/files/1342/old/pandp12p.pdf)

---
