
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
from datetime import datetime
from IPython.display import display


# 로그 기록 함수
def log_progress(message, etl_path):
    # 시간 형식 정의
    timestamp_format = '%Y-%b-%d-%H:%M:%S'  # 년-월이름-일-시간-분-초 형식
    now = datetime.now()  # 현재 시간 가져오기
    timestamp = now.strftime(timestamp_format)  # 형식에 맞게 시간 문자열로 변환
    # 로그 파일에 기록
    with open(os.path.join(etl_path, 'etl_project_log.txt'), "a") as f:
        f.write(f"{timestamp}, {message}\n")

# 추출 (Extract) 함수
def extract(url, table_attribs, etl_path):
    log_progress('데이터 추출 시작', etl_path)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    df = pd.DataFrame(columns=table_attribs)

  # 적절한 테이블 선택
    table = soup.find('table', {'class': 'wikitable sortable sticky-header-multi static-row-numbers'})
    if table is None:
        raise ValueError("Unable to find the sortable table on the Wikipedia page.")


    # 테이블 파싱
    rows = table.find_all('tr')
    data = []

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

# 변환 (Transform) 함수
def transform(df, regions_path, etl_path):
    log_progress('데이터 변환 시작', etl_path)
    # GDP 값을 숫자로 변환
    df["GDP_USD_millions"] = df["GDP_USD_millions"].astype(float)
    df["GDP_USD_billions"] = df["GDP_USD_millions"].div(1000).round(2)  # 단위를 억 달러로 변환
    df.drop(columns=['GDP_USD_millions'], inplace=True)  # 원래 컬럼 삭제
    regions=pd.read_csv(regions_path)
    #df에 region 부여
    df = pd.merge(df, regions, on='Country', how='left') 

    log_progress('데이터 변환 완료', etl_path)
    return df


# 로드 (Load) 함수 - CSV 파일로 저장
def load_to_csv(df, csv_path, etl_path):
    log_progress('CSV 파일로 데이터 저장 시작', etl_path)
    df.to_csv(csv_path, index=False)  # CSV 파일로 저장
    log_progress('CSV 파일로 데이터 저장 완료', etl_path)

# JSON 파일로 로드하는 함수
def load_gdp_data(df, etl_path):
    log_progress('JSON 파일로 데이터 저장 시작', etl_path)
    # JSON 파일로 저장
    df.to_json(os.path.join(etl_path, 'Countries_by_GDP.json'), orient='records', lines=True)
    log_progress('JSON 파일로 데이터 저장 완료', etl_path)

# 메인 함수
def main():
    # 지정된 경로에 ETL 폴더 생성
    etl_path = '/Users/admin/Documents/GitHub/softeer_wiki/missions/w1/ETL'

    if not os.path.exists(etl_path):
        os.makedirs(etl_path)

    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
    regions_path = '/Users/admin/Documents/GitHub/softeer_wiki/missions/w1/region.csv'
    table_attribs = ["Country", "GDP_USD_millions"]
    csv_path = os.path.join(etl_path, 'Countries_by_GDP.csv')

    log_progress('ETL 프로세스 시작', etl_path)

    # 추출 단계
    df = extract(url, table_attribs, etl_path)
    load_gdp_data(df, etl_path)

    # 변환 단계
    df = transform(df, regions_path,etl_path)   
     # 로드 단계
    load_to_csv(df, csv_path, etl_path)
    top_5_mean = df.groupby('Region').apply(lambda x: x.nlargest(5, 'GDP_USD_billions')['GDP_USD_billions'].mean()).reset_index(name='Top5_Avg_GDP_USD_billions')
    top_5_mean_sorted = top_5_mean.sort_values(by='Top5_Avg_GDP_USD_billions', ascending=False)
    print('-' * 36)
    print("각 Region별로 top5 국가의 GDP 평균")
    print(top_5_mean_sorted)
    print('-' * 36)-
    print("GDP가 100B USD 이상인 국가들")
    log_progress("GDP가 100B USD 이상인 국가 출력",etl_path)
    df_filtered = df[df["GDP_USD_billions"] >= 100]
    df_filtered.index = df_filtered.index + 1   
    print(df_filtered)
    log_progress('ETL 프로세스 완료', etl_path)
    log_progress('-' * 36, etl_path)

if __name__ == "__main__":
    main()

 