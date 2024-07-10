import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os
import time
import requests
from bs4 import BeautifulSoup
import json
from io import StringIO

# 설정 파일에서 데이터 로드
with open('/Users/admin/Desktop/Data_Engineering/W1/ETL/settings.json', 'r') as f:
    settings = json.load(f)

log_path = settings["log_path"]
region_data_json_path = settings["region_data_json_path"]
GDP_json_path = settings["GDP_json_path"]
db_path = settings["db_path"]
GDP_WIKIPEDIA_URL = settings["GDP_WIKIPEDIA_URL"]

# 로그 기록 함수
def log(message): # log message를 etl_project_log.txt 파일에 기록
    with open(log_path, 'a') as f:
        current_time = datetime.now().strftime('%Y-%b-%d %H:%M:%S')
        f.write(f"{current_time}, {message}\n") # 현재 날짜 및 시간, message를 write

def extract_data(url): # url에서 Data를 extraction
    log("Data extraction started") # Extract log 기록
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # 데이터프레임 리스트로 가져오기
    tables = pd.read_html(StringIO(str(soup)), match='Forecast')
    df = tables[0][['Country/Territory', 'IMF[1][13]']] # Table을 DataFrame에 담는다.
    log("Data extraction completed")
    return df

def transform_data(df): # Data 전처리 및 변환
    log("Data transformation started") # Transform log 기록
    df.columns = df.columns.droplevel() # 2중 column droplevel
    df = df.rename(columns={'Country/Territory': 'Country', 'Forecast': 'GDP_USD_billion'})
    df = (
        df[df['GDP_USD_billion'].apply(lambda x: x.isnumeric())]
        .astype({'GDP_USD_billion': 'float'})
        .query('Country != "World"')
        .sort_values('GDP_USD_billion', ascending=False)
        .reset_index(drop=True)
    )
    # Billion 단위로 변경
    df['GDP_USD_billion'] = (df['GDP_USD_billion'] / 1000).round(2)
    # 현재 날짜와 시간 추가
    df['Year'] = datetime.now().strftime("%Y-%b-%d %H:%M")
    
    with open(region_data_json_path) as country_json:
        Country_Region = json.load(country_json)
        df['Region'] = df['Country'].map(lambda x: next((continent for continent, countries in Country_Region.items() if x in countries), 'Other'))
    
    df.to_json(GDP_json_path, orient='records', lines=True)
    log("Data transformation completed")
    return df

def load_data(df, db_path): # Data를 DB에 Load
    log("Data load started") # Load log 기록
    
    # SQLite에 연결
    conn = sqlite3.connect(db_path)
    # 전체 데이터(Total_Countries_by_GDP) 저장
    df.to_sql('Total_Countries_by_GDP', conn, if_exists='append', index=False)
    
    conn.commit()
    conn.close()
    log("Data load completed")

def get_sql(query, db_name=db_path):
    try:
        with sqlite3.connect(db_name) as conn:
            cur = conn.cursor()
            cur.execute(query)
            return cur.fetchall()
    except Exception as e:
        print(e)

def get_OVER_100b():
    query = """
        SELECT * 
        FROM Total_Countries_by_GDP
        WHERE GDP_USD_billion >= 100
        """
    return get_sql(query, db_path)

def get_average_gdp_by_region():
    query = """
        SELECT Region, ROUND(AVG(GDP_USD_billion),2)
        FROM
            (
            SELECT Region, GDP_USD_billion, RANK() OVER (PARTITION BY Region ORDER BY GDP_USD_billion DESC) AS RANKING
            FROM Total_Countries_by_GDP
            )
        WHERE RANKING <= 5 AND Region IS NOT NULL
        GROUP BY Region
        """
    return get_sql(query, db_path)

def etl_process():
    log("ETL process started")
    df = extract_data(GDP_WIKIPEDIA_URL) # Extract process 실행
    df = transform_data(df) # Transform process 실행

    # 디렉토리가 존재하지 않는 경우 생성
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    load_data(df, db_path) # Load process 실행
    log("ETL process completed")

def wait_until_next_hour(): # 지금은 정각마다 DB에 저장하는 코드를 작성했다.
                            # 정각마다 DB에 잘 저장하는 것을 확인했으므로 주기를 분기 또는 반기 단위로 하여 GDP를 update하면 된다.
    now = datetime.now()
    # 다음 정각 계산
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    # 다음 정각까지의 시간을 계산하여 불필요한 Overhead가 발생하지 않게 sleep하도록 하였다.
    wait_seconds = (next_hour - now).total_seconds()
    time.sleep(wait_seconds)

def Print_get_100B():
    over_100b = get_OVER_100b()
    print("Countries with GDP over 100B:")
    for row in over_100b:
        print(row)

def Print_get_TOP5_by_region():
    avg_gdp_by_region = get_average_gdp_by_region()
    print("\nAverage GDP by region for top 5 countries:")
    for row in avg_gdp_by_region:
        print(row)

if __name__ == "__main__":
    # ETL 프로세스를 첫 실행
    etl_process()
    # 데이터베이스 쿼리 결과 출력
    Print_get_100B()
    Print_get_TOP5_by_region()
    
    # 정각마다 ETL 프로세스를 실행
    while True:
        wait_until_next_hour() # 다음 정각을 계산하고 남는 시간만큼 sleep한다.
        etl_process() # ETL process를 진행한다.
        # 데이터베이스 쿼리 결과 출력
        Print_get_100B()
        Print_get_TOP5_by_region()
