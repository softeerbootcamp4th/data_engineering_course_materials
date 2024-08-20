# Amazon Linux 2 기반 이미지 선택
FROM amazonlinux:2

# 작업 디렉토리 설정
WORKDIR /usr/src/wh_M5

# 필요한 패키지 설치
RUN yum update -y \
    && amazon-linux-extras enable java-openjdk11 \
    && yum install -y java-11-amazon-corretto-headless \
    && amazon-linux-extras enable python3.8 \
    && yum install -y python3.8 python3-pip \
    && yum clean all

# 환경 변수 설정
ENV JAVA_HOME /usr/lib/jvm/java-11-amazon-corretto
ENV PATH $JAVA_HOME/bin:$PATH

# 심볼릭 링크를 통해 python3 명령어로 Python 3.8 사용
RUN if [ ! -e /usr/bin/python3 ]; then ln -s /usr/bin/python3.8 /usr/bin/python3; fi


# 현재 디렉토리의 파일들을 컨테이너의 작업 디렉토리로 복사
COPY . /usr/src/wh_M5

# 필요한 Python 패키지 설치
RUN pip3 install --no-cache-dir -r requirements.txt

# Jupyter Notebook이 실행될 포트 설정
EXPOSE 8888

# Jupyter Notebook 실행
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
