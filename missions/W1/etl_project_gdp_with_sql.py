'''
etl_project_gdp_with_sql: 나라별 GDP 리스트를 위키피디아에서 가져오기
'''

import logging
import re
import sqlite3
import json

import requests
from bs4 import BeautifulSoup, Tag


# 나라별 GDP 위키피디아 URL
GDP_WIKI_URL = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'

# 대륙 이름과 위키피디아 내 대륙별 소속 나라 리스트가 포함된 챕터 id
REGION_TABLE_URLS = [
    ['Asia', 'States_of_Asia'],
    ['North_America', 'Definitions'],
    ['South_America', 'Countries_and_territories'],
    ['Europe', 'List_of_states_and_territories'],
    ['Africa', 'Territories_and_regions'],
    ['Oceania', 'Demographics'],
]


class Top5Mean:
    '''
    상위 5개의 평균을 구하는 SQLite 집계 함수
    '''
    def __init__(self):
        self.nums = []
    
    def step(self, value):
        self.nums.append(value)

    def finalize(self):
        self.nums.sort(reverse=True)

        return sum(self.nums[:5]) / 5.0


def extract_gdp_table(cur: sqlite3.Cursor) -> None:
    '''
    위키피디아에서 IMF가 조사한 GDP 테이블을 DB에 저장
    '''
    normalization_dict = {
        'DR Congo': 'Democratic Republic of the Congo',
        'Congo': 'Republic of the Congo',
        'Bahamas': 'The Bahamas',
        'Gambia': 'The Gambia',
    }

    cur.execute('''
                CREATE TABLE IF NOT EXISTS Countries_by_GDP (
                    Country varchar(255) PRIMARY KEY NOT NULL,
                    GDP_USD_billion float NOT NULL
                );
                ''')

    try:
        req_wiki_gdp = requests.get(GDP_WIKI_URL, timeout=10)
    except requests.exceptions.Timeout as e:
        raise e

    soup = BeautifulSoup(req_wiki_gdp.text, 'html.parser')

    gdp_table = soup.find(id='Table').parent \
                    .find_next_sibling('table').find_all('tr') # 'Table' 챕터에 들어있는 테이블 찾기

    for row in gdp_table[3:]: # <thead>에 있는 <tr>과 World 행을 제외
        row = row.get_text().split('\n')
        country, gdp = row[1:3]
        country = country[1:].strip()

        if country in normalization_dict:
            country = normalization_dict.get(country)

        if gdp == '—': # 공란 처리된 셀은 제외
            continue
        else:
            gdp = float(gdp.replace(',', ''))
            gdp = gdp / 1000  # million$ 단위에서 billion$ 단위로 변환
            gdp = round(gdp, 2)
        cur.execute('''
                    INSERT OR REPLACE INTO Countries_by_GDP (Country, GDP_USD_billion)
                    VALUES (?, ?);
                    ''',
                    (country, gdp))


def show_table(data: sqlite3.Cursor) -> None:
    '''
    쿼리 결과를 탭으로 구분된 테이블로 보여주기
    '''
    if data.description is None:
        return
    
    column_names = list(map(lambda column: column[0], data.description))
    print('\t'.join(column_names))

    for row in data:
        row = list(map(lambda cell: '(Null)' if cell is None else str(cell), row))
        print('\t'.join(row))
    print()


def load_to_json_on_disk(cur: sqlite3.Cursor) -> None:
    '''
    DB에 저장된 GDP 테이블을 json 형식으로 저장
    '''
    data = cur.execute('''
                       SELECT * FROM Countries_by_GDP
                       ORDER BY GDP_USD_billion DESC;
                       ''')
    
    countries_by_gdp_dict = dict()

    for country, gdp in data:
        countries_by_gdp_dict[country] = gdp
    
    with open('Countries_by_GDP.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(countries_by_gdp_dict))



def main() -> None:
    logging.basicConfig(
        filename='elt_project_log.txt',
        format='%(asctime)s, %(message)s',
        datefmt='%Y-%b-%d-%H-%M-%S',
        level=logging.INFO)
    
    conn = sqlite3.connect('World_Economies.db')
    cur = conn.cursor()

    conn.create_aggregate('top5mean', 1, Top5Mean) # 사용자 정의 집계 함수

    # ----- Data Extraction ----- #
    logging.info('Extracting GDP table from wikipedia ...')
    try:
        extract_gdp_table(cur)
        conn.commit()
    except requests.exceptions.Timeout as e:
        logging.error(e)
        return
    else:
        logging.info('Successfully extracted GDP table')
    # ----- Data Extraction ----- #

    # ----- Data Transformation ----- #
    logging.info('Transforming GDP table ...')
    data = cur.execute('''
                       SELECT * FROM Countries_by_GDP
                       WHERE GDP_USD_billion >= 100
                       ORDER BY GDP_USD_billion DESC;
                       ''')
    show_table(data)
    logging.info('Successfully transformed GDP table')

    logging.info('Transforming for Top 5 mean GDP by regions ...')
    data = cur.execute('''
                       SELECT c.Region, round(top5mean(g.GDP_USD_billion), 2) AS [Top 5 Mean GDP]
                       FROM Countries_by_GDP g
                       INNER JOIN Regions c On g.Country = c.Country
                       GROUP BY c.Region;
                       ''')
    show_table(data)
    logging.info('Successfully transformed Top 5 mean GDP table')
    # ----- Data Transformation ----- #

    # ----- Data Load ----- #
    logging.info('Loading GDP table to disk ...')
    try:
        load_to_json_on_disk(cur)
    except Exception as e:
        logging.error(e)
    else:
        logging.info('Successfully loaded GDP time')
    # ----- Data Load ----- #


if __name__ == '__main__':
    main()
