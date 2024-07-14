import requests
from bs4 import BeautifulSoup
import pandas as pd
from IPython.display import display, Markdown
import logging
import json

#로그파일 만들기 
logging.basicConfig(
    filename='elt_project_log.txt', # 로그 파일 이름
    format='%(asctime)s, %(message)s', # 로그 형식
    datefmt='%Y-%b-%d-%H-%M-%S', # 날짜 표기 형식
    level=logging.INFO
    )

def web_scrapping(GDP_url):
    url = GDP_url
    r = requests.get(url)

    # 로그 기록, 추출
    logging.info('Extract Country-GDP table start')

    #나라 - GDP 데이터 추출하기
    soup = BeautifulSoup(r.content,'html.parser')
    data = soup.find_all('table',class_ = 'wikitable sortable sticky-header-multi static-row-numbers jquery-tablesorter'.split())
    lst = []
    logging.info('Transform Start : GDP')
    for table in data:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if cols:
                name  = cols[0].find('a')
                if name :
                    country = name.text.strip()
                    if len(cols)>1:
                        gdp_value = cols[1].text.strip().replace(',', '')  # 콤마 제거
                        
                    if len(cols)>3:
                        year = cols[2].text.strip()
                        if gdp_value == '—': 
                            year = '—'
                        lst.append((country,gdp_value,year))
                        
    #나라 - GDP 데이터프레임 
    df = pd.DataFrame(lst,columns = ['Country','GDP_M','Year']) #나라이름, gdp, 연도값을 저장한 lst을 데이터 프레임 생성
    logging.info('Extract Country-GDP table end')
    pd.set_option('display.max_rows', None)
    #print(df)
    return df

def transform(df):
    logging.info('Transform start')

    logging.info('Transform : Add colums about converting GDP value from millions to billions')

    #기존 GDP값을 밀리언 기준에서 빌리언 기준으로 변환하여 새로운 열에 추가(밀리언 값은 유지)
    df['GDP_M'] = pd.to_numeric(df['GDP_M'], errors='coerce')# 숫자로 변환
    df['GDP_B'] = df['GDP_M'] / 1000 # 새로운 열에 빌리언 값 저장
    df['GDP_B'] = df['GDP_B'].map(lambda x: f'{x:.2f}')  # 소수점 두 자리로 변환
    df['GDP_B'] = pd.to_numeric(df['GDP_B'], errors='coerce')
    df = df.sort_values(by='GDP_M', ascending=False)  # GDP 값 기준으로 내림차순 정렬

    logging.info('Transform : Get Country-Region Table from csv')

    # Contry_Region_Table.csv 읽어서 DataFrame으로 변환
    df_continent = pd.read_csv('Contry_Region_Table.csv')

    logging.info('Transform : Merge Contry-GDP_B and Country-Region Table')
    #대륙-나라-GDP-Year left join해서 데이터 프레임 합치기
    df_Total = pd.merge(df, df_continent, left_on='Country', right_on='Country', how='left')

    # JSON 딕셔너리에서 값 가져와서 다른 나라여서 못들어간 값 업데이트
    logging.info('Transform : Update the Exception (country name is different)')
    with open('add_country_region.json', 'r', encoding='utf-8') as json_file:
        country_region_dict = json.load(json_file)
    for country, region in country_region_dict.items():
        df_Total.loc[df_Total['Country'] == country, 'Region'] = region
    pd.set_option('display.max_rows', None)

    logging.info('Transform end')
    #print(df_Total)

    return df_Total

def load(df_Total):
    #GDP 데이터 프레임 json으로 저장하기
    logging.info('Load : saved json file')
    df_Total.to_json('Countries_by_GDP.json',orient = 'columns')

def Countries_gdp_over_100b():
    df_Total = pd.read_json('Countries_by_GDP.json')
    print(' ')
    print('#화면 출력 예제 1 : GDP가 100B USD이상이 되는 국가')
    filtered_df = df_Total[df_Total['GDP_B'].astype(float) >= 100] #GDP_B가 100B USD이상이 되는 국가만 출력
    print(filtered_df)

def Avg_gdp_top5_by_region():
    df_Total = pd.read_json('Countries_by_GDP.json')
    print(' ')
    print('#화면 출력 예제 2 : 각 Region별로 상위 5개 국가의 GDP 평균')
    region_top5_avg = df_Total.groupby('Region',group_keys=False).apply(lambda x: x.nlargest(5, 'GDP_B')['GDP_B'].mean()) #각 Region별로 상위 5개 국가의 GDP 평균 계산
    print(region_top5_avg)

if __name__ == '__main__':

    GDP_url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    
    e_result = web_scrapping(GDP_url)
    t_result = transform(e_result)
    load(t_result)
    Countries_gdp_over_100b()
    Avg_gdp_top5_by_region()

