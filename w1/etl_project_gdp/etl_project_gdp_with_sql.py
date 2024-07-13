########## ETL PROJECT GDP WITH SQL

# ------------ 2024.7.13 transform 모듈 수정됨 !

# import field
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
import os
import sqlite3

### Logger
# 로그 파일 => etl_project_log.txt
def log_message(message):
    if not 'etl_project_log.txt' in os.listdir():
        with open('etl_project_log.txt', 'w') as f:
            f.write("ETL Project Log\n")
            f.write("=" * 20 + "\n")
    with open('etl_project_log.txt', 'a') as f:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{current_time} - {message}\n")

### E ! 
# 추출"만" -> 사람이 인식하는 테이블 형태로 반환
# 전처리됨 !
def extract():
    # 페이지 요청
    response = requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29')
    # html 파싱
    soup = BeautifulSoup(response.content, 'html.parser')
    # 테이블 찾기
    gdp_table = soup.find('table', {'class': 'wikitable'})
    # 테이블 행으로 파싱
    rows = gdp_table.find_all('tr')
    
    ### gdp_df 만들기
    
    countries = []
    gdps = []
    years = []

    for row in rows[3:]:
        eles = row.find_all('td')  # td태그 달린 애들 중 [0][1]만 쓸 것임 !
        # 나라 추가
        country = eles[0].text.strip()
        countries.append(country)
        # gdp, 연도 추가
        # - 가 있음 ! => 적절한 처리(아래)
        if eles[1].text.strip().replace(',', '') != '—':
            gdp_forecast = int(eles[1].text.strip().replace(',', ''))
            gdps.append(gdp_forecast)
            year = int(eles[2].text.strip()[-4:])
            years.append(year)
        else:  # 측정이 안됐을 경우
            gdps.append(np.nan)
            years.append(np.nan)

    # 데이터프레임 생성
    gdp_df = pd.DataFrame(
        {
            'Country': countries,
            'GDP': gdps,
            'Year': years
        }
    )

    return gdp_df


### Transform
# GDP 단위 수정 + Region 정보 merge된 df 반환
def transform(gdp_df):
    ###### 수정 필요 !
    # billion 단위로 수정
    # gdp_df['GDP'] = (gdp_df['GDP']/1000).round(2)
    # 컬럼 이름 바꾸기
    # gdp_df = gdp_df.rename(columns={'GDP': 'GDP_USD_BILLION'})
    ###### => 단위 처리가 다 안된 상태에서  데이터가 중간에 꼬이거나 오류가 발생하면 단위가 M인지 B인지 모르는 상황이 생길 수도 있다 !
    ###### -> 새로운 컬럼을 만들고, 거기에 추가 변환 결과를 저장 !

    # GDP_USD_BILLION 컬럼 추가 !
    gdp_df['GDP_USD_BILLION'] = (gdp_df['GDP']/1000).round(2)
    
    # sql버전에서는 그냥 단위만 수정해서 보내주자 
    # A 과정에서 쿼리로 한번에 할 것! 
    
    return gdp_df


### 저장할 파일의 이름 결정 함수
# 혹시 이름이 있으면 _1, _2 ... 이런식으로
# 저장할 이름을 반환
# filename은 이름.확장자
# 디렉터리는 현재 디렉터리 기준
def get_unique_filename(filename): 
    # 없으면 그냥 이름 그대로 쓰자
    if not os.path.exists(filename):
        return filename
    else: # 있으면
        base, ext = os.path.splitext(filename)
        counter = 1
        new_filename = f"{base}_{counter}{ext}"
        while os.path.exists(new_filename): # 있으면 카운터 계속 올리기
            counter += 1
            new_filename = f"{base}_{counter}{ext}"
        return new_filename


### Load 
# DB에 테이블로 저장
def load(gdp_df):
    conn = sqlite3.connect('World_Economies.db')
    gdp_df.to_sql('Countries_by_GDP',conn, if_exists='replace', index=False)
    conn.close()

if __name__ == "__main__":

    conn = sqlite3.connect('World_Economies.db')

    ### E
    log_message("E start !")
    gdp_df = extract()
    log_message("E finished !")

    ### T
    log_message("T start !")
    gdp_df = transform(gdp_df)
    log_message("T finished !")

    ### L
    log_message("L start !")
    load(gdp_df)
    log_message("L finished !")

    # Load 했으니까 다시 불러와야 하나 ... ?
    # 근데 같은 코드스페이스에 이미 올라와있으니까 ... 이거 쓰자 ... ㅋㅋ!


    ### A(?)
    # GDP 100B 넘는 나라들
    print('----- Countries whose GDP is over 100B -----')
    query = """
    SELECT * 
    FROM Countries_by_GDP
    WHERE GDP_USD_BILLION >= 100;
    """
    countries_gdp_over_100 = pd.read_sql_query(query, conn)
    print(countries_gdp_over_100)

    ### 지역 별 TOP 5 출력
    print('-----Top 5 Countries by continental region-----')
    query = """
    SELECT COUNTRY, GDP_USD_BILLION, REGION, RANK 
    FROM (
        SELECT COUNTRY, GDP_USD_BILLION, REGION, ROW_NUMBER() OVER (PARTITION BY REGION ORDER BY GDP_USD_BILLION) AS RANK
        FROM (
            SELECT L.Country AS COUNTRY, L.GDP_USD_BILLION AS GDP_USD_BILLION, R."Continental Region" AS REGION
            FROM Countries_by_GDP L
            LEFT OUTER JOIN Region R
            ON L.Country = R.Country
        )
    ) WHERE RANK <= 5;
    """
    top5s = pd.read_sql_query(query, conn)
    print(top5s)

    conn.close()