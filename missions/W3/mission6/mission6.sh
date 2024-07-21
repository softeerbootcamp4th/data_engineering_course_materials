# If output dir is already exists, remove it.
hdfs dfs -rm -r /user/root/mission6/output

# Download amazone review dataset.
# ~/missions/mission6/download_csv.sh
hdfs dfs -mkdir -p /user/root/mission6/input
hdfs dfs -put missions/mission6/data/* /user/root/mission6/input/
hadoop jar /usr/local/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -file ~/missions/mission6/code/mapper.py -file ~/missions/mission6/code/reducer.py -mapper ~/missions/mission6/code/mapper.py -reducer ~/missions/mission6/code/reducer.py -input /user/root/mission6/input -output /user/root/mission6/output
hdfs dfs -get /user/root/mission6/output/part-00000 ~/missions/mission6/output/
cat ~/missions/mission6/output/part-00000