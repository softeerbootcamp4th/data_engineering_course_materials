'''
elt_project_region: Wikipedia에서 나라별 region 정보를 가져와 csv 파일로 저장하는 프로젝트
'''
import logging
import re
import sqlite3

import requests
import pandas as pd
from bs4 import BeautifulSoup, Tag


# 대륙 이름과 위키피디아 내 대륙별 소속 나라 리스트가 포함된 챕터 id
REGION_TABLE_URLS = [
    ['Asia', 'States_of_Asia'],
    ['North_America', 'Definitions'],
    ['South_America', 'Countries_and_territories'],
    ['Europe', 'List_of_states_and_territories'],
    ['Africa', 'Territories_and_regions'],
    ['Oceania', 'Demographics'],
]


def extract_from_html_table(table_tag: Tag, region: str) -> list[dict[str, str]]:
    '''
    파싱된 테이블에서 나라 리스트를 가져와 (나라, 대륙) 쌍 데이터를 가져오기
    '''
    output_list = []

    tr_elements = table_tag.find_all('tr')

    for tr in tr_elements:
        row = tr.text.split('\n')
        if row[1].strip() != '': # 테이블 내 그룹 표기(예: 동유럽, 서유럽, 북유럽)를 나타내는 행 제거
            continue
        country = re.sub(r'\[.+\]|\ ?\(.+\)|\*', r'', row[5]) # 첨자와 속령 표기 제거
        output_list.append({'country': country, 'region': region})

    return output_list


def extract_region_table() -> pd.DataFrame:
    '''
    위키피디아에서 대륙별 나라 리스트를 가져와 pd.DataFrame 형에 모두 모아 가져오기
    '''
    region_pairs = []

    for region, section_id in REGION_TABLE_URLS:
        wiki_url = 'https://en.wikipedia.org/wiki/' + region # 대륙별 위키 페이지 주소
        try:
            req = requests.get(wiki_url, timeout=10)
        except requests.exceptions.Timeout as e:
            raise e

        soup = BeautifulSoup(req.text, 'html.parser')

        # 나라 리스트가 포함된 챕터에서 테이블 가져오기
        table = soup.find(id=section_id).parent.find_next_sibling('table')
        # 유럽의 경우, 나라 리스트는 두번째 테이블에 존재
        if region == 'Europe':
            table = table.next_sibling.next_sibling

        pairs = extract_from_html_table(table, region)
        region_pairs.extend(pairs)

        # 아시아와 유럽은 UN이 인정하지 않은 국가 리스트가 별도로 존재
        if region in ['Asia', 'Europe']:
            table = table.next_sibling.next_sibling.next_sibling.next_sibling
            pairs = extract_from_html_table(table, region)
            region_pairs.extend(pairs)

    return pd.DataFrame(region_pairs).set_index('country')


def load_region_table_to_db(df: pd.DataFrame) -> None:
    '''
    대륙별 나라 리스트를 DB에 저장
    '''
    conn = sqlite3.connect('World_Economies.db')
    cur = conn.cursor()


    cur.execute('''
                SELECT EXISTS (
                    SELECT name FROM sqlite_schema
                    WHERE type='table' AND name='Regions'
                );
                ''')
    res = cur.fetchone()[0]
    if res == 0:
        cur.execute('''
                    CREATE TABLE Regions (
                        Country varchar(255) NOT NULL,
                        Region varchar(255) NOT NULL
                    );
                    ''')

        for country, row_s in df.iterrows():
            cur.execute('''
                        INSERT INTO Regions (Country, Region)
                        VALUES (?, ?);
                        ''',
                        (country, row_s['region']))

    conn.commit()
    conn.close()


def main() -> None:
    logging.basicConfig(
        filename='elt_project_log.txt',
        format='%(asctime)s, %(message)s',
        datefmt='%Y-%b-%d-%H-%M-%S',
        level=logging.INFO)

    logging.info('Extracting Region table from wikipedia ...')
    try:
        region_df = extract_region_table()
    except requests.exceptions.Timeout as e:
        logging.error(e)
        return
    else:
        logging.info('Successfully extracted Region table')

    logging.info('Loading Region table to disk ...')
    try:
        region_df.to_csv('region.csv', header=True)
        load_region_table_to_db(region_df)
    except Exception as e:
        logging.error(e)
    else:
        logging.info('Successfully loaded Region table')


if __name__ == '__main__':
    main()
