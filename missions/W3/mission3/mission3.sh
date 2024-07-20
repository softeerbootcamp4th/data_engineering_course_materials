# /bin/bash

hdfs dfs -mkdir -p /user/root/mission3/input
hdfs dfs -put missions/mission3/data/Egmont.txt /user/root/mission3/input/Egmont.txt
hadoop jar /usr/local/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -file ~/missions/mission3/code/mapper.py -file ~/missions/mission3/code/reducer.py -mapper ~/missions/mission3/code/mapper.py -reducer ~/missions/mission3/code/reducer.py -input /user/root/mission3/input -output /user/root/mission3/output
hdfs dfs -get /user/root/mission3/output/part-00000 ~/missions/mission3/output/
cat ~/missions/mission3/output/part-00000