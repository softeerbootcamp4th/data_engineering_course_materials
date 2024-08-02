# download.py
import requests
import pandas as pd
import os


# 저장할 폴더 경로
save_folder = "/opt/hadoop/pi"
os.makedirs(save_folder, exist_ok=True)  # 폴더가 없으면 생성

# 데이터 종류 및 기간 설정
categories = ["yellow_tripdata", "green_tripdata", "fhv_tripdata", "fhvhv_tripdata"]
months = (
    pd.date_range(start="2022-07-01", end="2022-07-01", freq="MS")
    .strftime("%Y-%m")
    .tolist()
)


# URL을 생성하여 데이터를 다운로드 및 저장
base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/"
for category in categories:
    for month in months:
        file_name = f"{category}_{month}.parquet"
        url = f"{base_url}{file_name}"
        file_path = os.path.join(save_folder, file_name)

        # 데이터 다운로드
        response = requests.get(url)

        # 응답 상태 코드 확인
        if response.status_code == 200:
            # 파일을 로컬 폴더에 저장
            with open(file_path, "wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to retrieve the data from {url}")
