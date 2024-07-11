# 베이스 이미지 선택
FROM python:3.12

# 작업 디렉토리 설정
WORKDIR /usr/src/wh_M5

# 현재 디렉토리의 파일들을 컨테이너의 작업 디렉토리로 복사
COPY . /usr/src/wh_M5

# 필요한 시스템 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# Jupyter Notebook이 실행될 포트 설정
EXPOSE 8888

# Jupyter Notebook 실행
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
