# /bin/bash

hdfs dfs -rm -r /user/root/mission4/output

hdfs dfs -mkdir -p /user/root/mission4/input
hdfs dfs -put missions/mission4/data/mission4.csv /user/root/mission4/input/mission4.csv
hadoop jar /usr/local/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -file ~/missions/mission4/code/mapper.py -file ~/missions/mission4/code/reducer.py -mapper ~/missions/mission4/code/mapper.py -reducer ~/missions/mission4/code/reducer.py -input /user/root/mission4/input -output /user/root/mission4/output
hdfs dfs -get /user/root/mission4/output/part-00000 ~/missions/mission4/output/
cat ~/missions/mission4/output/part-00000