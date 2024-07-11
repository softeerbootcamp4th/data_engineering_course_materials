from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging
from datetime import datetime


"""
로깅을 위한 logger를 초기화하여 반환한다.
로그를 File에 출력하기 위한 핸들러를 추가하고 로그 레벨을 INFO로 설정한다. 
"""
def init_logger(log_file):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)  # 로그 레벨 설정
    logger.addHandler(logging.FileHandler(log_file))
    return logger


url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
db_file = 'generated/Countries_by_GDP.json'
log_file = 'generated/etl_project_log.txt'
continents_data = 'resources/continents-according-to-our-world-in-data.csv'

logger = init_logger(log_file)

"""
'[Year-Monthname-Day-Hour-Minute-Second], <message>' 형식으로 로그를 출력한다.
"""
def log_info(msg):
    now = datetime.now() # 현재 날짜와 시간 가져오기
    formatted_date = now.strftime('[%Y-%B-%d-%H-%M-%S], ') # 원하는 포맷으로 변환
    logger.info(formatted_date + msg)


"""
'https://restcountries.com/v3.1/all' API를 호출하고 받아온 데이터를 파싱하여 ['Region', 'Country'] 컬럼을 갖는 데이터프레임을 반환한다.
"""
def read_continents():
    response = requests.get('https://restcountries.com/v3.1/all')
    data = response.json()
    countries = []
    for country in data:
        name = country.get('name', {}).get('common', 'N/A')
        region = country.get('region', 'N/A')
        countries.append({'Country': name, 'Region': region})
    return pd.DataFrame(countries)


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
def extract():
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
            country=tds[0].find('a').text
            gdp = tds[1].text
            data.append([country, gdp])
    else:
        print(response.status_code)
        return data
    log_info("Completed Extract Task: Data extraction from the source completed successfully.")
    return data


"""
extract 과정에서 뽑운 데이터를 통해 Country-GDP(1B USD)의 데이터프레임을 만들어 반환한다.
GDP의 내림차순으로 정렬하며, Million 단위의 값을 Billion(소수 둘째자리)로 변환한다. 
"""
def transform(data):
    log_info("Starting Transform Task: Initiating data transformation process.")

    df = pd.DataFrame(data, columns=['Country', 'GDP'])
    df['GDP(1B USD)'] = [round(int(e.replace(',', '')) / 1000, 2) if e.replace(',', '').isdigit() else 0 for e in df['GDP']] # 0 or None
    del df['GDP']
    result = df.sort_values(by='GDP(1B USD)', ascending=False)
    log_info("Completed Transform Task: Data transformation process completed successfully.")
    return result


"""
완성된 데이터프레임을 받아 target 위치에 json 포맷으로 저장한다.
"""
def load(df, target):
    log_info("Starting Load Task: Initiating data loading into the target system.")
    df.to_json(target, orient="records")
    log_info("Completed Load Task: Data loading into the target system completed successfully.")


"""
GDP(Billion Dollar)가 condition 이상인 항목을 출력한다.
"""
def show_over(df, condition):
    result = df[df['GDP(1B USD)'] >= condition]
    result.set_index(df.columns[0], inplace=True)
    print(result)


"""
country-gdp로 구성된 데이터프레임과 region-country로 구성된 데이터프레임을 병합해 country-gdp-region 데이터프레임을 만든다.
어떤 region에도 속하지 않는 country의 region은 'N/A'로 채우고,
어떤 country도 속하지 않는 region은 결과에 포함하지 않는다.
"""
def fill_continents(country_gdp, region_country):
    df_merged = pd.merge(country_gdp, region_country, on='Country', how='left')
    df_merged['Region'] = df_merged['Region'].fillna('N/A')
    return df_merged


"""
['Region', 'Country', 'GDP(1B USD)'] 컬럼으로 구성된 데이터프레임을 받아
'Region'을 기준으로 그룹화하고, 개별 그룹에서 GDP 상위 n개 항목을 출력한다. 
"""
def show_topn_region(df_merged, n):
    result = (df_merged.set_index('Country')
              .groupby(by='Region')
              .apply(lambda x: x.nlargest(n, ['GDP(1B USD)']), include_groups=False))
    print(result)


"""
['Region', 'Country', 'GDP(1B USD)'] 컬럼으로 구성된 데이터프레임을 받아
'Region'을 기준으로 그룹화하고, 개별 그룹에서 GDP 상위 n개 항목의 평균을 출력한다. 
"""
def show_topn_mean_region(df_merged, n):
    result = (df_merged.set_index('Country')
              .groupby(by='Region')
              .apply(lambda x: x.nlargest(n, ['GDP(1B USD)']), include_groups=False)
              .groupby(by='Region')['GDP(1B USD)']
              .mean())
    print(result.sort_values(ascending=False))


def execute(n, target):
    # 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'의 표에서 IMF에서 정리한 국가-GDP 항목을 파싱하여 2차원 리스트로 반환한다.
    data = extract()
    # [[<Country>, <GDP>] ... ] 배열의 data를 받아, GDP 단위 변경(M->B), 정렬을 수행한 결과를 반환한다.
    country_gdp = transform(data)
    # target 위치에 country-gdp 쌍으로 이뤄진 데이터프레임을 json 포맷으로 저장한다.
    load(country_gdp, target)
    # 두번쨰 인수(condition(Billion USD Dollar)) 이상의 항목만을 출력한다.
    show_over(country_gdp, 100)
    # 'https://restcountries.com/v3.1/all' API를 호출하고 받아온 데이터를 파싱하여 ['Region', 'Country'] 컬럼을 갖는 데이터프레임을 반환한다.
    region_country = read_continents()
    # 두 데이터프레임을 병합하여 region-country-gdp 데이터프레임을 만든다.
    df_merged = fill_continents(country_gdp, region_country)
    # region-country-gdp 데이터프레임의 각 레코드를 Region별로 묶어, 그룹별 GDP 상위 5개 항목을 출력한다.
    show_topn_mean_region(df_merged, 5)
    # show_topn_region(df_merged, 5)


if __name__ == '__main__':
    execute(5, db_file)

