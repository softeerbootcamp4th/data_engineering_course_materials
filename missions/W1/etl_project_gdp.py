'''
etl_project_gdp: 나라별 GDP 리스트를 위키피디아에서 가져오기
'''
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup


# 나라별 GDP 위키피디아 URL
GDP_WIKI_URL = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'


def extract_gdp_table() -> pd.DataFrame:
    '''
    위키피디아에서 IMF가 조사한 GDP 테이블을 pd.DataFrame 형으로 가져오기
    '''
    normalization_dict = {
        'DR Congo': 'Democratic Republic of the Congo',
        'Congo': 'Republic of the Congo',
        'Bahamas': 'The Bahamas',
        'Gambia': 'The Gambia',
    }

    try:
        req_wiki_gdp = requests.get(GDP_WIKI_URL, timeout=10)
    except requests.exceptions.Timeout as e:
        raise e

    soup = BeautifulSoup(req_wiki_gdp.text, 'html.parser')

    gdp_list = []
    gdp_table = soup.find(id='Table').parent \
                    .find_next_sibling('table').find_all('tr') # 'Table' 챕터에 들어있는 테이블 찾기

    for row in gdp_table[3:]: # <thead>에 있는 <tr>과 World 행을 제외
        row = row.get_text().split('\n')
        country, gdp = row[1:3]
        country = country[1:].strip()

        if country in normalization_dict:
            country = normalization_dict.get(country)

        if gdp == '—': # 공란 처리된 셀을 Null로 처리
            gdp = None
        else:
            gdp = float(gdp.replace(',', ''))
            gdp = gdp / 1000  # million$ 단위에서 billion$ 단위로 변환
            gdp = round(gdp, 2)
        gdp_list.append({'country': country, 'gdp': gdp})

    return pd.DataFrame(gdp_list).set_index('country')


def extract_region_table_from_csv(csvfile: str) -> pd.DataFrame:
    '''
    외부 csv 파일에서 region 테이블을 pd.DataFrame 형식으로 가져오기
    '''
    return pd.read_csv(csvfile, header=0).set_index('country')


def refine_null_sort_gdp(df: pd.DataFrame) -> pd.DataFrame:
    '''
    GDP 값이 NULL인 데이터 정제하고 GDP 기준으로 정렬
    '''
    df = df.dropna(subset=['gdp'])
    df = df.sort_values('gdp', ascending=False)

    return df


def transform_gdp_table_over_100b(df: pd.DataFrame) -> pd.DataFrame:
    '''
    GDP가 $100B 이상인 국가들을 내림차순으로 정렬
    '''
    return df[df['gdp'] >= 100].sort_values('gdp', ascending=False)


def get_top5_mean(df: pd.DataFrame) -> float:
    '''
    GDP 상위 5개 나라의 GDP 평균 계산하기
    '''
    top5_gdp_s = df['gdp'].sort_values(ascending=False).head(5)
    return top5_gdp_s.mean()


def transform_top_5_mean_gdp_by_region(gdp_df: pd.DataFrame,
                                       region_df: pd.DataFrame
                                       ) -> pd.DataFrame:
    '''
    대륙별로 GDP 상위 5개국의 평균을 계산
    '''
    top5_mean_s = gdp_df.join(region_df, on='country').groupby('region') \
                                                      .apply(lambda x: round(get_top5_mean(x), 2),
                                                             include_groups=False)
    
    return pd.DataFrame({'Top 5 mean GDP($Bilion)': top5_mean_s})


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


def main() -> None:
    logging.basicConfig(
        filename='elt_project_log.txt',
        format='%(asctime)s, %(message)s',
        datefmt='%Y-%b-%d-%H-%M-%S',
        level=logging.INFO)

    # ----- Data Extraction ----- #
    logging.info('Extracting GDP table from wikipedia ...')
    try:
        gdp_df = extract_gdp_table()
    except requests.exceptions.Timeout as e:
        logging.error(e)
        return
    else:
        logging.info('Successfully extracted GDP table')

    logging.info('Extracting Region table from csvfile ...')
    region_df = extract_region_table_from_csv('region.csv')
    logging.info('Successfully extracted Region table')
    # ----- Data Extraction ----- #

    # ----- Data Transformation ----- #
    logging.info('Transforming GDP table ...')
    gdp_df = refine_null_sort_gdp(gdp_df)
    show_table('GDP by countries more than $100B', 
               transform_gdp_table_over_100b(gdp_df))
    logging.info('Successfully transformed GDP table')

    logging.info('Transforming for Top 5 mean GDP by region ...')
    show_table('Top 5 mean GDP by region',
               transform_top_5_mean_gdp_by_region(gdp_df, region_df))
    logging.info('Successfully transformed Top 5 mean GDP table')
    # ----- Data Transformation ----- #

    # ----- Data Load ----- #
    logging.info('Loading GDP table to disk ...')
    try:
        gdp_df.to_json('Countries_by_GDP.json')
    except Exception as e:
        logging.error(e)
    else:
        logging.info('Successfully loaded GDP time')
    # ----- Data Load ----- #


if __name__ == '__main__':
    main()
