import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import os
import sqlite3
from datetime import datetime
from IPython.display import display

def log_progress(message, etl_path):
    """
    로그 기록 함수
    """
    timestamp_format = '%Y-%b-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(os.path.join(etl_path, 'etl_project_log.txt'), "a") as f:
        f.write(f"{timestamp}, {message}\n")

def extract(url, table_attribs, etl_path):
    """
    데이터 추출 함수
    """
    log_progress('데이터 추출 시작', etl_path)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    df = pd.DataFrame(columns=table_attribs)

    # 적절한 테이블 선택
    table = soup.find('table', {'class': 'wikitable sortable sticky-header-multi static-row-numbers'})
    
    # 테이블 모든 행 추출 
    rows = table.find_all('tr')
    data = []

    # 각 행의 데이터를 파싱
    for row in rows[3:]:   
        cols = row.find_all('td')
        if len(cols) < 3:
            continue  
        country = cols[0].text.strip()
        gdp_text = cols[1].text.strip()
        gdp = re.sub(r'\[.*?\]', '', gdp_text).replace(',', '')
        try:
            gdp = float(gdp)
        except ValueError:
            continue
        data.append([country, gdp])

    # 데이터프레임 생성
    df = pd.DataFrame(data, columns=table_attribs)
    log_progress('데이터 추출 완료', etl_path)
    return df

def transform(df, regions_path, etl_path):
    """
    데이터 변환 함수
    """
    log_progress('데이터 변환 시작', etl_path)
    
    # GDP 값을 숫자로 변환 및 단위를 억 달러로 변환
    df["GDP_USD_millions"] = df["GDP_USD_millions"].astype(float)
    df["GDP_USD_billions"] = df["GDP_USD_millions"].div(1000).round(2)
    df.drop(columns=['GDP_USD_millions'], inplace=True)

    # Region 데이터 병합
    regions = pd.read_csv(regions_path)
    df = pd.merge(df, regions, on='Country', how='left')

    log_progress('데이터 변환 완료', etl_path)
    return df

def load_to_csv(df, csv_path, etl_path):
    """
    데이터 로드 함수 (CSV)
    """
    log_progress('CSV 파일로 데이터 저장 시작', etl_path)
    df.to_csv(csv_path, index=False)
    log_progress('CSV 파일로 데이터 저장 완료', etl_path)

def load_gdp_data_to_json(df, filename, etl_path):
    """
    데이터 로드 함수 (JSON)
    """
    log_progress('데이터를 JSON 파일로 저장 시작', etl_path)
    df.to_json(filename, orient='records', lines=True, force_ascii=False)
    log_progress('데이터를 JSON 파일로 저장 완료', etl_path)

def run_query(query_statement, db_name, etl_path):
    """
    쿼리 실행 함수
    """
    log_progress(f"쿼리 실행: {query_statement}", etl_path)
    conn = sqlite3.connect(db_name)
    df = pd.read_sql_query(query_statement, conn)
    conn.close()
    display(df)

def create_and_insert_table(df, db_name, table_name, etl_path):
    """
    테이블 생성 및 데이터 삽입 함수
    """
    log_progress(f"{table_name} 테이블 생성 및 데이터 삽입 시작", etl_path)
    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    log_progress(f"{table_name} 테이블 생성 및 데이터 삽입 완료", etl_path)

def analyze_data(df,db_name, table_name,etl_path):
    """
    각 Region별로 top5 국가의 GDP 평균 계산
    GDP가 100B USD 이상인 국가 산출
    """
    top_5_mean = df.groupby('Region').apply(lambda x: x.nlargest(5, 'GDP_USD_billions')['GDP_USD_billions'].mean()).reset_index(name='Top5_Avg_GDP_USD_billions')
    top_5_mean_sorted = top_5_mean.sort_values(by='Top5_Avg_GDP_USD_billions', ascending=False)

    print('-' * 36)
    print("각 Region별로 top5 국가의 GDP 평균")
    display(top_5_mean_sorted)
    
    print('-' * 36)
    print("GDP가 100B USD 이상인 국가들")
    query_statement = f"SELECT * from {table_name} WHERE GDP_USD_billions >= 100"
    run_query(query_statement,db_name,etl_path)


def etl_process():
    """
    ETLA 프로세스 실행 함수
    """
    etl_path = '/Users/admin/Documents/GitHub/softeer_wiki/missions/w1/ETL'
    if not os.path.exists(etl_path):
        os.makedirs(etl_path)
    db_name = os.path.join(etl_path, 'World_Economies.db')
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
    table_attribs = ["Country", "GDP_USD_millions"]
    table_name = 'Countries_by_GDP'
    regions_path = 'https://raw.githubusercontent.com/ssangmin-junior/softeer_wiki/main/missions/w1/ETL/region.csv'
    csv_path = os.path.join(etl_path, 'Countries_by_GDP.csv')
    json_path = os.path.join(etl_path, 'Countries_by_GDP.json')
    log_progress('ETL 프로세스 시작', etl_path)

    # 데이터 추출
    df = extract(url, table_attribs, etl_path)
    load_gdp_data_to_json(df, json_path, etl_path)

    # 데이터 변환
    df = transform(df, regions_path, etl_path)
    
    # 테이블 생성 및 데이터 삽입
    create_and_insert_table(df, db_name, table_name, etl_path)
 
    # 데이터 Analyze
    analyze_data(df,db_name, table_name,etl_path)

    # 데이터 로드
    load_to_csv(df, csv_path, etl_path)

    log_progress('ETL 프로세스 완료', etl_path)
    log_progress('------------------------------------------', etl_path)

if __name__ == "__main__":
    etl_process()
