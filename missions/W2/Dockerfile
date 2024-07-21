# 사용할 베이스 이미지를 지정
FROM --platform=linux/amd64 ubuntu:latest

# 필요한 패키지를 설치
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv

# 작업 디렉토리를 설정
WORKDIR /app

# 가상 환경을 생성하고 활성화
RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# 로컬의 파일들을 컨테이너의 작업 디렉토리로 복사
COPY . /app

# 필요한 Python 패키지를 가상 환경에 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install jupyter

# 주피터 노트북 실행
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]