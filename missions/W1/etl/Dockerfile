# 베이스 이미지로 Python 3.9 사용
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /etl

# 현재 디렉토리의 파일들을 컨테이너의 작업 디렉토리로 복사
COPY . /etl

# 필요한 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# Python 스크립트 실행
CMD ["python", "etl_project_gdp_with_sql.py"]
