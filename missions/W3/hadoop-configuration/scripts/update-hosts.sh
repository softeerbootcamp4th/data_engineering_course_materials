#!/usr/bin/env bash

# 슬레이브 노드 목록
SLAVES=("hadoop-slave1" "hadoop-slave2")

HOST_NAME="${1:-hadoop-master}"
# hadoop-master의 IP 주소 가져오기
MASTER_IP=$(hostname -I | awk '{print $1}')
#echo $MASTER_IP

for SLAVE in "${SLAVES[@]}"; do
    sshpass -p "root" ssh -o StrictHostKeyChecking=no root@$SLAVE "echo '$MASTER_IP $HOST_NAME' >> /etc/hosts"
done

# 각 슬레이브 노드의 /etc/hosts 파일 업데이트
# /etc/hosts 파일에 추가
echo "$MASTER_IP $HOST_NAME" >> /etc/hosts