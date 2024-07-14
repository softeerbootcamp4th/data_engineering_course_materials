from bs4 import BeautifulSoup
import pandas as pd
import requests
import datetime


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
    

def open_json() -> pd.DataFrame:
    json_path = './Countries_by_GDP.json'
    df = pd.read_json(json_path)
    
    return df


"""
데이터프레임으로서 load한 내용을 요구사항에 맞게 정리하여 출력하는 함수
GDP가 100B USD를 초고화는 국가들을 출력
"""
def analyze_1(df):
    # 컬럼 이름 수정
    df.rename(columns={0: 'Nation', 1: 'GDP'}, inplace=True)
    
    # GDP가 100 이상인 행들을 추출
    filtered_df = df[df['GDP'].str.len()>=7][['Nation','GDP']]
    filtered_df = filtered_df.drop(0).reset_index(drop=True)
    
    # 분석을 위해 문자열 형태를 float형태로 변환
    filtered_df['GDP'] = filtered_df['GDP'].str.replace(',', '').astype(float)
    filtered_df['GDP'] = (filtered_df['GDP'] / 1000).round(2)
    
    # 분석 내용 출력
    print('\n[Nations with GDP exceeding 100B USD (Unit:Billion $)]')
    print(filtered_df)



"""
데이터프레임으로서 load한 내용을 요구사항에 맞게 정리하여 출력하는 함수
대륙별 상위 5개의 GDP 평균을 출력
"""
def analyze_2(df):
    # 미리 준비된 국가별 대륙 정보 "region.csv"
    df_nation_conti = pd.read_csv('region.csv')
    
    # 컬럼 이름 수정
    df.rename(columns={0: 'Nation', 1: 'GDP'}, inplace=True)
    
    # 0번째 row 제거
    df = df.drop(0).reset_index(drop=True)
    
    # 분석을 위해 문자열 형태를 float형태로 변환
    df['GDP'] = df['GDP'].str.replace(',', '').astype(float)
    df['GDP'] = (df['GDP'] / 1000).round(2)
    
    # 'GDP' 열의 값이 0 인 행을 제외
    df = df[df['GDP'] > 0]
    
    # 분석을 위해 df와 df_nation_conti를 left join
    df_joined = pd.merge(df, df_nation_conti, on='Nation', how='left')
    
    # df_joined에서 대륙 정보가 없는 국가 필터링
    df_joined['Continent'] = df_joined['Continent'].fillna('Unknown')
    df_unknown = df_joined[df_joined['Continent'] == 'Unknown']
    df_joined = df_joined[df_joined['Continent'] != 'Unknown']
    
    # 대륙별 상위 5개 국가 GDP 평균 추출
    top_5_gdp_per_continent = df_joined.sort_values(['Continent', 'GDP'], ascending=[True, False]).groupby('Continent').head(5)
    average_gdp_per_conitinent = top_5_gdp_per_continent.groupby('Continent')['GDP'].mean().round(2)
    
    # 대륙별 상위 5개 국가 GDP 평균 출력
    print('\n[Top 5 GDP averages in each region (Unit:Billion $)]')
    print(average_gdp_per_conitinent)
    

"""
* Deprecated *
국가,대륙 정보가 담긴 파일을 이용하여 딕셔너리 자료를 구성
중복되지 않는 대륙 정보를 사용하여 딕셔너리 자료를 구성
{키 = 대륙 : 값 = GDP 값 리스트} 
"""
def trans_region_data() -> tuple[dict, dict]:
    # 텍스트 파일 경로
    txt_file = 'region.csv'

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

######################################
## json -- open, dataframe -> print ##
######################################

#L : start load
log('L : start load')
nation_gdp_df = open_json()

#L : end load
log('L : end load')

# analze : there are two methods of analzation
analyze_1(nation_gdp_df)
analyze_2(nation_gdp_df)