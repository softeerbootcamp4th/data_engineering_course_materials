import pandas as pd
import requests
import datetime
import sqlite3
import json
from bs4 import BeautifulSoup


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
위키에서 국가별 GDP를 스크롤하여 리스트로 반환하는 함수
[[국가, GDP], [국가, GDP], ...] 형태
첫번째 행은 [모든 국가, GDP 총합]
"""
def scroll_wiki() -> list:
    # 데이터 저장을 위한 리스트 초기화
    table_data = [] 
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    response = requests.get(url)
    
    # 요청이 성공했는지 확인
    if response.status_code == 200:
        
        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find_all('table')
        tbody = table[2].find('tbody')
        rows = tbody.find_all('tr')
    
        # 각 행의 데이터를 리스트 형태로 추출
        for row in rows:
            cells = row.find_all('td')[:2]
            if not cells:
                continue
            cell_values = [cell.get_text(strip=True) for cell in cells]
            if cell_values[1] == '\u2014':
                cell_values[1] = '-1'
            table_data.append(cell_values)
            
    # 요청 실패시 메시지 출력
    else:
        print("Failed to retrieve the web page")
    
    return table_data


"""
list 자료를 입력받아 json 파일로 내보내는 함수
"""
def list_to_json(_list) -> None:
    df = pd.DataFrame(_list)
    json_data = df.to_json(orient='records')
    
    with open('Countries_by_GDP.json', 'w') as f:
        f.write(json_data)
    

"""
json 파일을 열어 DB에 테이블을 생성하는 함수
"""
def open_json():
    json_path = './Countries_by_GDP.json'
    with open(json_path, 'r') as file:
        data_list = json.load(file)
    
    with sqlite3.connect('World_Economies.db') as conn:
        cur = conn.cursor()
        cur.execute(
                '''
                CREATE TABLE IF NOT EXISTS Countries_by_GDP (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Country TEXT UNIQUE,
                GDP_USD_billion INT
                )
                '''
        )
        
        for item in data_list:
            if item['0'] == 'World':
                continue
            try:
                cur.execute(
                    '''
                    INSERT INTO Countries_by_GDP (Country, GDP_USD_billion) VALUES (?, ?)
                    ''',
                    (item['0'], int(item['1'].replace(',','')))
                )
            except sqlite3.IntegrityError as e:
                print(e)
                break
        conn.commit()


"""
국가,대륙 정보를 가지고 있는 region.txt 파일을 얼어
국가,대륙 정보를 가지고 있는 테이블 CONTINENT를 생성한 후
GDP, CONTINENT 테이블을 LEFT JOIN한 테이블 GDP_CONTI을 생성하는 함수
"""
def create_nation_conti_table():
    txt_file = './region.txt'
    nation_conti_list = []
    with open(txt_file, mode='r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # 줄 바꿈 문자 제거
            if line:
                nation, continent = line.split(',')
                nation_conti_list.append((nation, continent))
    
    with sqlite3.connect('World_Economies.db') as conn:
        cur = conn.cursor()
        cur.execute(
                '''
                CREATE TABLE IF NOT EXISTS CONTINENT (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nation TEXT UNIQUE,
                continent TEXT
                )
                '''
        )
        
        for item in nation_conti_list:
            try:
                cur.execute(
                    '''
                    INSERT INTO CONTINENT (nation, continent) VALUES (?, ?)
                    ''',
                    (item[0], item[1])
                )
            except sqlite3.IntegrityError as e:
                print(e)
                break
            
        cur.execute(
                """
                CREATE TABLE IF NOT EXISTS NATION_CONTI  (
                nation TEXT PRIMARY KEY,
                gdp INTEGER,
                continent TEXT
                );
                """
        )
        
        conn.commit()
        try:
            cur.execute(
                    """
                    INSERT INTO NATION_CONTI (nation, gdp, continent)
                    SELECT
                        Countries_by_GDP.Country,
                        Countries_by_GDP.GDP_USD_billion,
                        CONTINENT.continent
                    FROM
                        Countries_by_GDP
                    LEFT JOIN
                        CONTINENT ON Countries_by_GDP.Country = CONTINENT.nation;
                    """
            )
        except:
            print()
            
        conn.commit()
        
        
"""
데이터프레임으로서 load한 내용을 요구사항에 맞게 정리하여 출력하는 함수
"""
def analyze():
    nation_gdp_list = execute_sql(
    """
    SELECT *
    FROM Countries_by_GDP
    WHERE GDP_USD_billion >= 100000
    """
    )

    region_average_list = execute_sql(
    """
    WITH RankedGDP AS (
        SELECT
            nation,
            continent,
            gdp,
            ROW_NUMBER() OVER (PARTITION BY continent ORDER BY gdp DESC) AS row_num
        FROM
            NATION_CONTI
    )
    SELECT
        continent,
        AVG(gdp) AS average_top_5_gdp
    FROM
        RankedGDP
    WHERE
        row_num <= 5
    GROUP BY
        continent;
    """
    )
    
    print('\n[Nations with GDP exceeding 100B USD (Unit:Billion $)]')
    for item in nation_gdp_list:
        
        float_gdp = item[2] / 1000
        print(f'{item[0]:<4}{item[1]:<25}{float_gdp:<12.2f}')
        
    print('\n[Top 5 GDP averages in each region (Unit:Billion $)]')
    for item in region_average_list:
        if not item[0]:
            continue
        float_gdp = item[1] / 1000
        print(f'{item[0]:15} : {float_gdp:.2f}')
        

"""
국가,대륙 정보가 담긴 파일을 이용하여 딕셔너리 자료를 구성
중복되지 않는 대륙 정보를 사용하여 딕셔너리 자료를 구성
{키 = 대륙 : 값 = GDP 값 리스트} 
"""
def trans_region_data() -> tuple[dict, dict]:
    # 텍스트 파일 경로
    txt_file = 'region.txt'

    # 빈 dictionary 생성
    nation_continent_dict = dict()
    continent_set = set()

    # 텍스트 파일 읽기
    with open(txt_file, mode='r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # 줄 바꿈 문자 제거
            if line:
                nation, continent = line.split(',')
                nation_continent_dict[nation] = continent
                continent_set.add(continent)
                
    continent_GDP_dict = {item : [] for item in continent_set}

    return nation_continent_dict, continent_GDP_dict
    

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
    

################################
## wiki -- scraping --> jason ##
################################

#E : start extract
log('E : start extract')
gdp_list = scroll_wiki()

#E : end extract
log('E : end extract')

#T : start transform (list -> json)
log('T : start transform (list -> json)')
list_to_json(gdp_list)

#T : end transform (list -> json)
log('T : end transform (list -> json)')

####################################
## json -- open, put data into db ##
####################################
 
#L : start load
log('L : start load')
create_nation_conti_table()
open_json()

# #L : end load
log('L : end load')

#######################################################
## db -- analyze by using sql query and print result ##
#######################################################
analyze()
