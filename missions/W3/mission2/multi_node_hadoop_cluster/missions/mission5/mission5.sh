# If output dir is already exists, remove it.
hdfs dfs -rm -r /user/root/mission5/output

hdfs dfs -mkdir -p /user/root/mission5/input
hdfs dfs -put missions/mission5/data/mission5.csv /user/root/mission5/input/mission5.csv
hadoop jar /usr/local/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -file ~/missions/mission5/code/mapper.py -file ~/missions/mission5/code/reducer.py -mapper ~/missions/mission5/code/mapper.py -reducer ~/missions/mission5/code/reducer.py -input /user/root/mission5/input -output /user/root/mission5/output
hdfs dfs -get /user/root/mission5/output/part-00000 ~/missions/mission5/output/
cat ~/missions/mission5/output/part-00000