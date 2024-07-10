########## ETL PROJECT GDP


# import field
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
import os

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
    # billion 단위로 수정
    gdp_df['GDP'] = (gdp_df['GDP']/1000).round(2)
    region_df = pd.read_csv('Region.csv')
    # region 정보 left outer join
    gdp_region_df = pd.merge(gdp_df, region_df, on = 'Country', how = 'left')
    
    return gdp_region_df


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
# json으로 저장
def load(gdp_region_df):
    # 파일 이름
    filename = 'gdp_region.json'
    filename = get_unique_filename(filename)
    gdp_region_df.to_json(filename, orient = 'records', lines=True)


if __name__ == "__main__":

    ### E
    log_message("E start !")
    gdp_df = extract()
    log_message("E finished !")

    ### T
    log_message("T start !")
    gdp_region_df = transform(gdp_df)
    log_message("T finished !")

    ### L
    log_message("L start !")
    load(gdp_region_df)
    log_message("L finished !")

    # Load 했으니까 다시 불러와야 하나 ... ?
    # 근데 같은 코드스페이스에 이미 올라와있으니까 ... 이거 쓰자 ... ㅋㅋ!

    ### A(?)
    # GDP 100B 넘는 나라들
    print('----- Countries whose GDP is over 100B -----')
    print(gdp_df[gdp_df['GDP'] >= 100])

    # Top 5
    print('----- Top 5 Countries by continental region -----')
    top5s = gdp_region_df.groupby('Continental Region').apply(lambda x: x.nlargest(5, 'GDP')).reset_index(drop=True)
    print(top5s[['Country','GDP','Continental Region']])