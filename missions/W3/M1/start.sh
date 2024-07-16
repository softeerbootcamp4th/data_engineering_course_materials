# run sshd
mkdir -p /run/sshd
/usr/sbin/sshd

# current라는 폴더가 있다면 포맷해야대
if [ -d "/tmp/hadoop-root/dfs/name/current" ]; then
  echo "NameNode is already formatted."
# 비어있다면 포맷을 진행
else
  echo "Format NameNode."
  /hadoop-3.3.6/bin/hdfs namenode -format
fi
# run namenode, yarn
./hadoop-3.3.6/sbin/start-dfs.sh
./hadoop-3.3.6/sbin/start-yarn.sh

# 무한 루프를 추가하여 컨테이너가 종료되지 않게 함
while true; do
  sleep 3600
done