'''
etl_project_gdp: 나라별 GDP 리스트를 위키피디아에서 가져오기
'''
import logging
from typing import Optional

import requests
import pandas as pd
from bs4 import BeautifulSoup


# 나라별 GDP 위키피디아 URL
GDP_WIKI_URL = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'

# 국가명 간소 표기와 정식 표기
COUNTRY_NAME_NORMALIZATION_DICT = {
    'DR Congo': 'Democratic Republic of the Congo',
    'Congo': 'Republic of the Congo',
    'Bahamas': 'The Bahamas',
    'Gambia': 'The Gambia',
}


def normalize_country_name(country: str) -> str:
    '''
    간소 표기된 국가명을 정식 명칭으로 변환
    '''
    if country in COUNTRY_NAME_NORMALIZATION_DICT:
        country = COUNTRY_NAME_NORMALIZATION_DICT.get(country)

    return country


def cast_float_or_null(value_str: str) -> float | None:
    '''
    string값을 float로 변환 후 million 단위를 billion 단위로 변환
    값이 '-'인 경우 NULL로 변환
    '''
    if value_str == '—': # 공란 처리된 셀을 Null로 처리
        value = None
    else:
        value = float(value_str.replace(',', ''))
        value = value / 1000  # million$ 단위에서 billion$ 단위로 변환
        value = round(value, 2)
    
    return value


def get_top5_mean(df: pd.DataFrame) -> float:
    '''
    GDP 상위 5개 나라의 GDP 평균 계산하기
    '''
    top5_gdp_s = df['gdp'].sort_values(ascending=False).head(5).mean()
    return top5_gdp_s


def get_gdp_table_from_web() -> pd.DataFrame | None:
    '''
    위키피디아에서 IMF가 조사한 GDP 테이블을 pd.DataFrame 형으로 가져오기
    '''
    logging.info('Extracting GDP table from wikipedia ...')

    try:
        req_wiki_gdp = requests.get(GDP_WIKI_URL, timeout=10)
    except requests.exceptions.Timeout as e:
        logging.error(e, ": 웹페이지에서 정보를 가져오는데 실패하였습니다.")
        return None

    soup = BeautifulSoup(req_wiki_gdp.text, 'html.parser')

    gdp_list = []
    gdp_table = soup.find(id='Table').parent \
                    .find_next_sibling('table').find_all('tr') # 'Table' 챕터에 들어있는 테이블 찾기

    gdp_table = gdp_table[3:]
    for row in gdp_table[3:]: # <thead>에 있는 <tr>과 World 행을 제외
        row = row.get_text().split('\n')
        country, gdp = row[1:3]
        country = country[1:].strip()

        country = normalize_country_name(country)

        gdp_list.append({'country': country, 'gdp': gdp})

    gdp_df = pd.DataFrame(gdp_list).set_index('country')

    logging.info('Successfully extracted GDP table')

    return gdp_df


def get_region_table_from_csv(csvfile: str) -> pd.DataFrame | None:
    '''
    외부 csv 파일에서 region 테이블을 pd.DataFrame 형식으로 가져오기
    '''
    logging.info('Extracting Region table from csvfile ...')

    try:
        region_df = pd.read_csv(csvfile, header=0)
    except FileNotFoundError:
        logging.error('%s이(가) 존재하지 않습니다.', csvfile)
        return None
    except Exception as e:
        logging.error('다음과 같은 이유로 파일을 불러올 수 없습니다. %s', e)
        return None

    region_df = region_df.set_index('country')

    logging.info('Successfully extracted Region table')

    return region_df


def preprocessing_gdp_table(gdp_df: pd.DataFrame) -> pd.DataFrame:
    '''
    GDP 테이블을 가공할 수 있도록 전처리
    - string으로 들어온 gdp 값을 float 또는 NULL로 변환
    - gdp 값이 NULL인 행을 제거
    - gdp 값을 기준으로 내림차순 정렬
    '''
    logging.info('Preprocessing GDP table ...')

    gdp_df = gdp_df.map(cast_float_or_null)
    gdp_df = gdp_df.dropna(subset=['gdp']) # GDP가 NULL인 국가 데이터 제거
    gdp_df = gdp_df.sort_values('gdp', ascending=False)

    logging.info('Successfully preprocessed GDP table')

    return gdp_df


def get_gdp_over_100b(df: pd.DataFrame) -> pd.DataFrame:
    '''
    GDP가 $100B 이상인 국가들을 내림차순으로 정렬
    '''
    logging.info('Transforming GDP table ...')

    df = df[df['gdp'] >= 100].sort_values('gdp', ascending=False)

    logging.info('Successfully transformed GDP table')

    return df


def get_top_5_mean_gdp_by_region(gdp_df: pd.DataFrame,
                                       region_df: pd.DataFrame
                                       ) -> pd.DataFrame:
    '''
    대륙별로 GDP 상위 5개국의 평균을 계산
    '''
    logging.info('Transforming for Top 5 mean GDP by region ...')

    top5_mean_s = gdp_df.join(region_df, on='country').groupby('region') \
                                                      .apply(lambda x: round(get_top5_mean(x), 2),
                                                             include_groups=False)
    top5_mean_df = pd.DataFrame({'Top 5 mean GDP($Bilion)': top5_mean_s})

    logging.info('Successfully transformed Top 5 mean GDP table')

    return top5_mean_df


def show_table(title: str, df: pd.DataFrame) -> None:
    '''
    pd.DataFrame을 CLI 화면에 표시
    '''
    print(title)
    print(df.index.name, end='\t')
    for column in df.columns:
        print(column, end='\t')
    print()

    for index, row in df.iterrows():
        print(index, end='\t')
        print('\t'.join(map(str, row.values)))
    print()


def save_as_json(gdp_df: pd.DataFrame) -> None:
    '''
    GDP 테이블을 json 파일로 저장합니다.
    '''
    logging.info('Loading GDP table to disk ...')
    try:
        gdp_df.to_json('Countries_by_GDP.json')
    except Exception as e:
        logging.error('다음과 같은 이유로 저장할 수 없습니다: %s', e)
    else:
        logging.info('Successfully loaded GDP time')


def extract() -> tuple[pd.DataFrame, pd.DataFrame]:
    '''
    GDP 테이블과 Region 테이블을 각 Data Source로 부터 가져옵니다.
    '''
    gdp_df = get_gdp_table_from_web()
    region_df = get_region_table_from_csv('region.csv')

    return gdp_df, region_df


def transform(gdp_df: Optional[pd.DataFrame], region_df: Optional[pd.DataFrame]
              ) -> tuple[pd.DataFrame, pd.DataFrame]:
    '''
    가져온 GDP 데이블과 Region 테이블을 통해 두가지 방식으로 변환한다.
    - GDP가 $100B 이상이고 내림차순으로 정렬된 국가 테이블
    - 각 대륙(Region)별 GDP 상위 5위까지의 평균 GDP 테이블
    '''

    if gdp_df is None or region_df is None:
        print("ERROR: Can't get GDP or region data.")
        return None, None

    gdp_df = preprocessing_gdp_table(gdp_df)

    gdp_over_100b_df = get_gdp_over_100b(gdp_df)
    top5_gdp_mean_df = get_top_5_mean_gdp_by_region(gdp_df, region_df)

    return gdp_over_100b_df, top5_gdp_mean_df
    

def load(gdp_df: Optional[pd.DataFrame],
         gdp_over_100b_df: Optional[pd.DataFrame], 
         top5_gdp_mean_df: Optional[pd.DataFrame]
         ) -> None:
    '''
    가공한 두 테이블(gdp_over_100b_df, top5_gdp_mean_df)을 출력하고
    GDP 테이블을 디스크에 저장한다.
    '''
    if ( gdp_df is None 
        or gdp_over_100b_df is None
        or top5_gdp_mean_df is None ):
        print("ERROR: Din't get GDP over $100B table.")
        return

    show_table('GDP by countries more than $100B', gdp_over_100b_df)
    show_table('Top 5 mean GDP by region', top5_gdp_mean_df)

    save_as_json(gdp_df)


def main() -> None:
    logging.basicConfig(
        filename='elt_project_log.txt',
        format='%(asctime)s, %(message)s',
        datefmt='%Y-%b-%d-%H-%M-%S',
        level=logging.INFO)

    gdp_df, region_df = extract()
    gdp_over_100b_df, top5_gdp_mean_df = transform(gdp_df, region_df)
    load(gdp_df, gdp_over_100b_df, top5_gdp_mean_df)


if __name__ == '__main__':
    main()
