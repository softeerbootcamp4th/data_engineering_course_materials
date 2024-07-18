import pandas as pd
import requests
import datetime
import sqlite3
import json
from bs4 import BeautifulSoup


"""
datatime library를 통해 현재 시각을 적절한 포맷의 문자열로 반환하는 함수
"""    
def get_cur_time():
    # 현재 시각을 얻기
    now = datetime.datetime.now()
    # 원하는 포맷으로 변환
    formatted_now = now.strftime('%Y-%B-%d-%H-%M-%S')
    return formatted_now


"""
현재 시각과 입력받은 메시지를 로그 파일에 기록하는 함수
"""
def log(process : str) -> None:
    filename = 'etl_project_log.txt'
    cur_time = get_cur_time()
    log_string = ','.join([cur_time, process])    
    
    with open(filename, 'a+') as file:
        # 파일에 쓸 콘텐츠 추가
        file.write(log_string + '\n')
        
        
"""
sqlite3 를 통해 sql 쿼리를 수행하여 조회한 내용을 반환하는 함수
"""
def execute_sql(sql_text) -> list[any]:
    with sqlite3.connect('World_Economies.db') as conn:
        cur = conn.cursor()
        cur.execute(sql_text)
        rows = cur.fetchall()
        return rows
            

"""
위키에서 국가별 GDP를 스크롤하여 데이터프레임으로 반환하는 함수
"""
def scroll_wiki() -> pd.DataFrame:
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    response = requests.get(url)
    
    # 요청이 성공했는지 확인
    if response.status_code == 200:
        
        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find_all('table')
        tbody = table[2].find('tbody')
        rows = tbody.find_all('tr')
        
        # 행의 개수를 파악하여 빈 데이터프레임 생성
        num_rows = len(rows)
        df = pd.DataFrame(index=range(num_rows), columns=['Country', 'GDP (million)'])

        # 각 행의 데이터를 데이터프레임에 추가
        row_index = 0
        for row in rows:
            cells = row.find_all('td')[:2]
            if not cells:
                continue
            cell_values = [cell.get_text(strip=True) for cell in cells]
            if cell_values[1] == '\u2014':
                cell_values[1] = '-1'
            # 데이터프레임에 행 추가
            df.loc[row_index] = cell_values
            row_index += 1
        
        # 실제 데이터가 들어간 부분만 추출
        df = df.iloc[:row_index]
        
        return df
    else:
        # 요청이 실패한 경우 빈 데이터프레임 반환
        return pd.DataFrame()


"""
데이터프레임을 json 파일로 내보내는 함수
"""
def df_to_json(df : pd.DataFrame) -> None:
    json_data = df.to_json(orient='records')
    
    with open('Countries_by_GDP.json', 'w') as f:
        f.write(json_data)    


"""
json 파일을 열어 데이터프레임으로 반환하는 함수
"""
def json_to_df(json_path: str) -> pd.DataFrame:
    df = pd.read_json(json_path)
    return df


"""
DB에서 대륙 정보를 가져오는 함수 (다른 절차를 통해 이미 만들어진 데이터)
"""
def get_continent_data(db_path: str) -> pd.DataFrame:
    # SQLite 데이터베이스에 연결
    conn = sqlite3.connect(db_path)
    
    # SQL 쿼리를 사용하여 데이터 가져오기
    query = "SELECT * FROM CONTINENT"
    df = pd.read_sql_query(query, conn)
    
    # 데이터베이스 연결 종료
    conn.close()
    
    if df.empty:
        log('No data found in the CONTINENT table.')
    
    return df


"""
트랜스폼 함수
필요한 데이터가 있는지 확인(이전 프로세스, 준비된 데이터)
필요한 데이터가 있으면 transform 수행
"""
def transform() -> pd.DataFrame:
    db_path = 'World_Economies.db'
    df_continent_world = get_continent_data(db_path=db_path)    
    df_continent_world.columns = ['id','Country', 'Continent']
    
    json_path = './Countries_by_GDP.json'
    df_countries_by_GDP = json_to_df(json_path)
    df_countries_by_GDP.columns = ['Country', 'GDP_USD_million']
    
    if df_continent_world.empty or df_countries_by_GDP.empty:
        log('No data found in the CONTINENT or Countries_by_GDP table.')
        return
    
    # df_merged.column : Country, GDP_USD_million, Continent
    df_merged = pd.merge(df_countries_by_GDP, df_continent_world[['Country', 'Continent']], on='Country', how='left')
    
    # GDP_USD_million을 쉼표 제거 후 숫자로 변환하고 GDP_USD_billion으로 변환
    df_merged['GDP_USD_billion'] = df_merged['GDP_USD_million'].apply(
        lambda x: (pd.to_numeric(x.replace(',', ''), errors='coerce') / 1000).round(2) if pd.notna(x) else None
    )
    
    # 필요 없는 컬럼 삭제
    df_merged = df_merged.drop(columns=['GDP_USD_million'])
    
    # 컬럼 순서 재배치
    df_merged = df_merged[['Country', 'GDP_USD_billion', 'Continent']]
    return df_merged

    
"""
데이터베이스에 데이터를 적재하는 함수
"""
def load_to_db(df: pd.DataFrame):
    db_path = 'World_Economies.db'
    
    # SQLite 데이터베이스에 연결 및 데이터 삽입
    with sqlite3.connect(db_path) as conn:
        # 데이터프레임을 'NATION_CONTI' 테이블에 삽입
        df.to_sql('NATION_CONTI', conn, if_exists='replace', index=False)
        
        # Check if the table exists in the database
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='NATION_CONTI'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            log("NATION_CONTI table exists in the database.")
        else:
            log("NATION_CONTI table does not exist in the database.")
    
    # 로그 메시지 출력
    log('Data inserted into NATION_CONTI table.')
    

"""
데이터베이스에 SQL 쿼리를 실행하고 결과를 DataFrame으로 반환하는 함수
"""
def query_database(query: str, db_path: str) -> pd.DataFrame:
    """Execute a SQL query and return the results as a DataFrame."""
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)        
   
        
"""
데이터베이스에서 GDP가 1000B 이상인 국가를 조회하는 함수
"""
def analyze_gdp_exceeding_1000B():
    db_path = 'World_Economies.db'
    
    # Query for nations with GDP exceeding 1000 billion USD
    nation_gdp_query = """
    SELECT Country, GDP_USD_billion
    FROM NATION_CONTI
    WHERE GDP_USD_billion >= 1000
    """
    nation_gdp_df = query_database(nation_gdp_query, db_path)
    nation_gdp_df = nation_gdp_df.iloc[1:]
    
    # Print nations with GDP exceeding 1000 billion USD
    print('\n[Nations with GDP exceeding 1000B USD (Unit: Billion $)]')
    print(nation_gdp_df)
    
    
"""
데이터베이스에서 대륙별 상위 5개 국가의 GDP 평균을 계산하는 함수
"""
def analyze_top_5_GDP_average():
    db_path = 'World_Economies.db'
    
    # Query for the top 5 GDP averages in each continent
    region_average_query = """
    WITH RankedGDP AS (
        SELECT
            Country,
            GDP_USD_billion,
            Continent,
            ROW_NUMBER() OVER (PARTITION BY Continent ORDER BY GDP_USD_billion DESC) AS row_num
        FROM
            NATION_CONTI
    )
    SELECT
        Continent,
        AVG(GDP_USD_billion) AS average_top_5_gdp
    FROM
        RankedGDP
    WHERE
        row_num <= 5
    GROUP BY
        Continent;
    """
    
    region_average_df = query_database(region_average_query, db_path)
    region_average_df = region_average_df.iloc[1:]
        
    # Print top 5 GDP averages in each region
    print('\n[Top 5 GDP averages in each region (Unit: Billion $)]')
    print(region_average_df)
    

###############################
## wiki -- scraping --> json ##
###############################

#E : start extract
log('E : start extract')
scrolled_dataframe = scroll_wiki()
df_to_json(scrolled_dataframe)

#E : end extract
log('E : end extract')


#########################################
## input data    : scrolled data(json) ##
## reserved data : CONTINENT(DB TABLE) ##
#########################################

#T : start transform 
log('T : start transform')
df_transformed = transform() # scrolled data(df) 를 받아도 되지만, json으로 저장하였으므로 transform에서는 input으로서 json을 받아 처리함

#T : end transform 
log('T : end transform')


################################
## load transfored data to DB ##
################################
 
#L : start load
log('L : start load')
load_to_db(df_transformed)

#L : end load
log('L : end load')

#######################################################
## db -- analyze by using sql query and print result ##
#######################################################
analyze_gdp_exceeding_1000B()
analyze_top_5_GDP_average()