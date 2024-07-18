FROM ubuntu:jammy

# HDFS web 포트
EXPOSE 9870
# Resource Manager web 포트
EXPOSE 8088
# HDFS datanode 포트
EXPOSE 9864

# hadoop용 사용자 정보
ENV USERNAME=hdoop
ENV USERPASSWORD=hadoop

USER root

# apt update and install
RUN apt update -y && \
    apt upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt install openjdk-8-jdk ssh pdsh sudo -y

# hadoop용 사용자 생성
RUN useradd ${USERNAME} -m -s /bin/bash -p ${USERPASSWORD}
RUN echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER ${USERNAME}
WORKDIR /home/${USERNAME}

# ssh 인증키 등록
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
RUN cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
RUN chmod 0600 ~/.ssh/authorized_keys

# ssh 접속시 접속여부를 물어보는 과정 생략
RUN echo "Host *\n\
    StrictHostKeyChecking no" >> ~/.ssh/config
RUN chmod 400 ~/.ssh/config

# dumb-init
RUN sudo wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.5/dumb-init_1.2.5_aarch64
RUN sudo chmod +x /usr/local/bin/dumb-init

# hadoop 파일이 이미 로컬에 있는 경우 사용
# COPY hadoop-3.4.0-aarch64.tar.gz /home/${USERNAME}/
# hadoop 파일을 서버에서 가져오기
RUN wget https://dlcdn.apache.org/hadoop/common/hadoop-3.4.0/hadoop-3.4.0-aarch64.tar.gz

# hadoop 압축 파일 해제 및 세팅
RUN tar -xzvf hadoop-3.4.0-aarch64.tar.gz
RUN mv hadoop-3.4.0 hadoop
RUN rm hadoop-3.4.0-aarch64.tar.gz

# datanode와 namenode 저장소 세팅
RUN mkdir /home/${USERNAME}/dfs /home/${USERNAME}/dfs/name /home/${USERNAME}/dfs/data
VOLUME "/home/${USERNAME}/dfs"
RUN chown ${USERNAME}:${USERNAME} -R /home/${USERNAME}/dfs
RUN chmod u+rwx -R /home/${USERNAME}/dfs
RUN chmod o+rwx /home/${USERNAME}/dfs/data

WORKDIR /home/${USERNAME}/hadoop

# 환경변수 세팅
RUN echo "export JAVA_HOME=$(readlink -f $(which java) | sed 's/\/bin\/java//g')" >> etc/hadoop/hadoop-env.sh
RUN echo "export PDSH_RCMD_TYPE=ssh" >> etc/hadoop/hadoop-env.sh

# 하둡 config 파일 적용
ADD etc/hadoop/*.xml etc/hadoop

# 하둡 실행용 스크립트 파일
ADD ./scripts/*.sh /home/${USERNAME}/hadoop
RUN sudo chown ${USERNAME}:${USERNAME} ./*.sh
RUN chmod +rwx ./*.sh

# 하둡 초기화
RUN [ "./initialize.sh" ]
# 하둡 실행
CMD [ "dumb-init", "--", "./start.sh", "&&"]