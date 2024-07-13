from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import sqlite3
import logging
import yaml


url = None
log_file = None
table_name = None
db_name = None
api_url = None
continents_path=None
logger = None


def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def init(file_path = 'resources/etl_only_config.yaml', mode = 'default'):
    global url, log_file, table_name, db_name, continents_path
    config = load_config(file_path)[mode]
    url = config['url']
    log_file = config['log_file_path']
    table_name = config['table_name']
    db_name = config['db_name']
    continents_path = config['continents_path']


def init_logger() -> logging.Logger:
    """
    로깅을 위한 logger를 초기화하여 반환한다.
    로그를 File에 출력하기 위한 핸들러를 추가하고 로그 레벨을 INFO로 설정한다.
    """
    global logger
    logger = logging.getLogger(__name__)
    # init_logger를 여러번 호출하는 경우 싱글톤 패턴을 따르는 loggin.getLogger에 같은 핸들러를 여러번 추가하여 하나의 로그가 여러번 찍히는 것을 방지
    if len(logger.handlers):  # 핸들러가 이미 존재하면 그대로 반환
        return logger
    logger.setLevel(logging.INFO)  # 로그 레벨 설정
    logger.addHandler(logging.FileHandler(log_file))
    return logger


def log_info(msg: str):
    """
    '[Year-Monthname-Day-Hour-Minute-Second], <message>' 형식으로 로그를 출력한다.
    """
    now = datetime.now()  # 현재 날짜와 시간 가져오기
    formatted_date = now.strftime('[%Y-%B-%d-%H-%M-%S], ')  # 원하는 포맷으로 변환
    logger.info(formatted_date + msg)


def create_table():
    command = f'CREATE TABLE {table_name} (index INTEGER, Country INTEGER, GDP_USD_billion REAL, Region VARCHAR(100));'
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(command)
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()


def exec_query(query: str) -> pd.DataFrame:
    try:
        with sqlite3.connect(db_name) as conn:
            result = pd.read_sql(query, conn)
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()
    return result


def extract() -> list:
    """
    bs4 라이브러리를 통해 위키피디아 페이지를 스크래핑, 국가별 GDP 테이블을 가져온다.
    테이블에서 국가 이름과 IMF에서 산정한 GDP(단위: Million) 쌍을 하나씩 읽어 data에 담아 반환한다.

    예)
        ['United States', '28,781,083']
        ['China', '18,532,633']
        ['Germany', '4,591,100']
        ['Japan', '4,110,452']
                 ...
    """
    log_info("Starting Extract Task: Initiating data extraction from the source.")
    data = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.select("table",
                             {"class": "wikitable sortable sticky-header-multi static-row-numbers jquery-tablesorter"})

        table_body = tables[2].find('tbody')
        rows = table_body.find_all('tr')
        for row in rows[3:]:
            tds = row.find_all('td')
            country = tds[0].find('a').text
            gdp = tds[1].text
            data.append([country, gdp])
    else:
        print(response.status_code)
        return data
    log_info("Completed Extract Task: Data extraction from the source completed successfully.")
    return data


def read_continents() -> pd.DataFrame:
    """
    'generated/continents.json' 파일에서 Region-Country 데이터프레임을 읽는다.
    """
    df = pd.read_json(continents_path)
    return df


def fill_continents(country_gdp: pd.DataFrame, region_country: pd.DataFrame) -> pd.DataFrame:
    """
    country-gdp로 구성된 데이터프레임과 region-country로 구성된 데이터프레임을 병합해 country-gdp-region 데이터프레임을 만든다.
    어떤 region에도 속하지 않는 country의 region은 'N/A'로 채우고, 어떤 country도 속하지 않는 region은 결과에 포함하지 않는다.
    """
    df_merged = pd.merge(country_gdp, region_country, on='Country', how='left')
    df_merged['Region'] = df_merged['Region'].fillna('N/A')
    return df_merged


def transform(data: list) -> pd.DataFrame:
    """
    extract 과정에서 뽑운 데이터를 통해 Country-GDP_USD_billion의 데이터프레임을 만들어 반환한다.
    GDP의 내림차순으로 정렬하며, Million 단위의 값을 Billion(소수 둘째자리)로 변환한다.
    """
    log_info("Starting Transform Task: Initiating data transformation process.")

    region_country = read_continents()

    country_gdp = pd.DataFrame(data, columns=['Country', 'GDP'])
    country_gdp['GDP_USD_billion'] = [round(int(e.replace(',', '')) / 1000, 2) if e.replace(',', '').isdigit() else 0 for e in
                             country_gdp['GDP']]  # 0 or None
    del country_gdp['GDP']
    country_gdp.sort_values(by='GDP_USD_billion', ascending=False, inplace=True)

    # 두 데이터프레임을 병합하여 region-country-gdp 데이터프레임을 만든다.
    df_merged = fill_continents(country_gdp, region_country)

    log_info("Completed Transform Task: Data transformation process completed successfully.")
    return df_merged


def load(df: pd.DataFrame):
    """
    완성된 데이터프레임을 받아 target 데이터베이스 {table_name} 테이블에 행으로 삽입한다.
    """
    log_info("Starting Load Task: Initiating data loading into the target system.")
    try:
        with sqlite3.connect(db_name) as conn:
            df.to_sql(table_name, conn, if_exists='replace')  # 기존에 데이터는 어떻게 처리해야할까?
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()
    log_info("Completed Load Task: Data loading into the target system completed successfully.")


def show_over(condition: int):
    """
    GDP(Billion Dollar)가 condition 이상인 항목을 조회한다.
    """
    query = f'SELECT * FROM {table_name} WHERE GDP_USD_billion >= {condition}'
    df = exec_query(query)
    df.reindex(columns=['index', 'Country', 'GDP_USD_billion', 'Region'])
    print(df[df[df.columns[2]] >= condition].set_index('Country'))


def show_topn_mean_region(n: int):
    """
    ['Region', 'AVG_GDP_USD_billion'] 조회 'Region'을 기준으로 그룹화하고, 개별 그룹에서 GDP 상위 n개 항목의 평균을 조회한다.
    """
    query = f"""
                SELECT Region, ROUND(AVG(GDP_USD_billion), 2) AS AVG_GDP_USD_billion
                FROM (
                    SELECT *, ROW_NUMBER() OVER (
                        PARTITION BY Region
                        ORDER BY GDP_USD_billion DESC
                    ) gdp_rank
                    FROM {table_name}
                )
                WHERE gdp_rank <= {n}
                GROUP BY Region
                ORDER BY 2 DESC;
            """
    result = exec_query(query)
    print(result)


def execute():
    # 위키피디아 List_of_countries_by_GDP의 표, IMF에서 정리한 국가-GDP 항목을 파싱하여 2차원 리스트로 반환한다.
    data = extract()
    # [[<Index>, <Country>, <GDP>, <Region>] ... ] 배열의 data를 받아, GDP 단위 변경(M->B), 정렬을 수행한 결과를 반환한다.
    df_merged = transform(data)
    # 테이블에 데이터 저장
    load(df_merged)


if __name__ == '__main__':
    # Init Configuration
    init()
    # 로거 초기화
    init_logger()
    # 테이블 생성
    create_table()
    # ETL 프로세스
    execute()
    # 1. 인수(condition(Billion USD Dollar)) 이상의 항목만을 조회한다.
    show_over(100)
    # 2. 각 레코드를 Region별로 묶어, 그룹별 GDP 상위 5개 항목의 평균을 출력한다.
    show_topn_mean_region(5)

