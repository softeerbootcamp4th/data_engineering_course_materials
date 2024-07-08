import pandas as pd
import requests

def get_continents() -> pd.DataFrame:
    """
    'https://restcountries.com/v3.1/all' API를 호출하고 받아온 데이터를 파싱하여 ['Region', 'Country'] 컬럼을 갖는 데이터프레임을 반환한다.
    """
    response = requests.get('https://restcountries.com/v3.1/all')
    data = response.json()
    countries = []
    for country in data:
        name = country.get('name', {}).get('common', 'N/A')
        region = country.get('region', 'N/A')
        countries.append({'Country': name, 'Region': region})
    return pd.DataFrame(countries)


def load_continents(df: pd.DataFrame, target='generated/continents.json'):
    """
    Region-Country 데이터프레임을 'generated/continents.json'로 저장한다.
    """
    df.to_json(target, force_ascii=False)


if __name__ == '__main__':
    df = get_continents()
    load_continents(df)

