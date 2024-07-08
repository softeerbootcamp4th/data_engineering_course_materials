import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import os
import sqlite3
from datetime import datetime
from IPython.display import display

# 로그 기록 함수
def log_message(message):
    """
    로그 메시지를 etl_project_log.txt 파일에 기록
    """
    # 현재 시간과 메시지를 로그 형식으로 저장
    timestamp = datetime.now().strftime('%Y-%B-%d-%H-%M-%S')
    log_entry = f"{timestamp}, {message}\n"
    with open("etl_project_log.txt", "a") as log_file:
        log_file.write(log_entry)

# 데이터 추출 함수
def fetch_gdp_data():
    """
    Wikipedia에서 IMF 데이터를 스크랩하여 국가별 GDP 데이터를 반환합니다.
    """
    log_message("데이터 추출 시작") 
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
    response = requests.get(url) 
    
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable sticky-header-multi static-row-numbers'})

    if table is None:
        log_message("Wikipedia 페이지에서 테이블을 찾을 수 없음")
        raise ValueError("Wikipedia 페이지에서 테이블을 찾을 수 없음")

    rows = table.find_all('tr')
    data = []

    # 각 행의 데이터를 파싱
    for row in rows[3:]: 
        cols = row.find_all('td')
        if len(cols) < 3:
            continue 
            
        country = cols[0].text.strip()
        gdp_text = cols[1].text.strip()
        data.append([country, gdp_text]) 

    log_message("데이터 추출 완료")
    return data 

# 데이터 변환 함수
def transform_gdp_data(data):
    """
    추출한 데이터를 변환하여 DataFrame으로 반환합니다.
    """
    log_message("데이터 변환 시작")
    
    transformed_data = []
    for row in data:
        country, gdp_text = row
        gdp = re.sub(r'\[.*?\]', '', gdp_text).replace(',', '') 
        
        try:
            gdp = float(gdp)
        except ValueError:
            continue 
        
        transformed_data.append([country, gdp])

    df = pd.DataFrame(transformed_data, columns=['Country', 'GDP (Millions of USD)'])

    # GDP를 1B USD로 변환 및 소수점 2자리까지 표시
    df['GDP (Billions of USD)'] = df['GDP (Millions of USD)'] / 1000
    df = df[['Country', 'GDP (Billions of USD)']]
    df['GDP (Billions of USD)'] = df['GDP (Billions of USD)'].round(2)

    # GDP가 높은 순서대로 정렬
    df_sorted = df.sort_values(by='GDP (Billions of USD)', ascending=False)
    
    log_message("데이터 변환 완료")
    return df_sorted

# 데이터 로드 함수 (JSON)
def load_gdp_data(df, filename='Countries_by_GDP.json'):
    """
    변환된 데이터를 JSON 파일로 저장합니다.
    """
    log_message("데이터를 JSON 파일로 저장 시작")
    
    # 데이터프레임을 JSON 파일로 저장
    df.to_json(filename, orient='records', lines=True, force_ascii=False)
   
    log_message("데이터를 JSON 파일로 저장 완료")

# 데이터 로드 함수 (SQLite)
def load_gdp_data_to_sqlite(df, db_filename='World_Economies.db'):
    """
    변환된 데이터를 SQLite 데이터베이스에 저장합니다.
    """
    log_message("데이터를 SQLite 데이터베이스에 저장 시작")

    # SQLite 데이터베이스에 연결
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Countries_by_GDP (
        Country TEXT PRIMARY KEY,
        GDP_USD_billion REAL
    )
    ''')

    # 데이터프레임의 각 행을 반복하면서 데이터를 삽입
    for _, row in df.iterrows():
        cursor.execute('''
        INSERT OR REPLACE INTO Countries_by_GDP (Country, GDP_USD_billion)
        VALUES (?, ?)
        ''', (row['Country'], row['GDP (Billions of USD)']))
    
    conn.commit()
    conn.close()
    
    log_message("데이터를 SQLite 데이터베이스에 저장 완료")

# SQL 쿼리 실행 함수
def execute_sql_query(query, db_filename='World_Economies.db'):
    """
    주어진 SQL 쿼리를 실행하고 결과를 반환합니다.
    """
    conn = sqlite3.connect(db_filename)
    df = pd.read_sql_query(query, conn)
    
    conn.close()
    return df

# ETL 프로세스 실행 함수
def etl_process():
    """
    ETL 프로세스를 실행합니다.
    """
    log_message("ETL 프로세스 시작")
    
    # 데이터 추출
    data = fetch_gdp_data()
    
    # 데이터 변환
    df_sorted = transform_gdp_data(data)
    
    # 데이터 로드 (JSON)
    load_gdp_data(df_sorted)
    
    # 데이터 로드 (SQLite)
    load_gdp_data_to_sqlite(df_sorted) 
    
    # GDP가 100B USD 이상인 국가 출력
    print("GDP가 100B USD 이상인 국가들")
    log_message("GDP가 100B USD 이상인 국가 출력")
    
    query = """
    SELECT * 
    FROM Countries_by_GDP 
    WHERE GDP_USD_billion >= 100
    """
    df_filtered = execute_sql_query(query)
    df_filtered.index = df_filtered.index + 1   
    display(df_filtered)

    
    # 각 Region별로 top5 국가의 GDP 평균 출력
    log_message("각 Region별로 top5 국가의 GDP 평균 출력")
    print('-' * 36)
    print("각 Region별로 top5 국가의 GDP 평균")

    df = pd.read_csv('region.csv')
    df = df[['Country', 'GDP_USD_billions', 'Region']] 
    
    conn = sqlite3.connect(':memory:')
    df.to_sql('region', conn, index=False, if_exists='replace')

    query = """
    WITH RankedCountries AS (
        SELECT 
            Country, 
            Region, 
            GDP_USD_billions,
            ROW_NUMBER() OVER (PARTITION BY Region ORDER BY GDP_USD_billions DESC) as rank
        FROM region
    )
    SELECT Region, AVG(GDP_USD_billions) as avg_gdp
    FROM RankedCountries
    WHERE rank <= 5
    GROUP BY Region
    """

    df_region = pd.read_sql_query(query, conn)
    df_region = df_region.sort_values(by=['Region', 'avg_gdp'], ascending=[True, False])   
    df_region.index = df_region.index + 1   
    display(df_region)
    
    log_message("ETL 프로세스 완료")

# ETL 프로세스 실행
if __name__ == "__main__":
    etl_process()