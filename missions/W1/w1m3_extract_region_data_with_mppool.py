import os
import time
from multiprocessing import Process, Pool

import requests
import pandas as pd

from bs4 import BeautifulSoup as bs


# for extract region data
gdp_country_url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
base_url = "https://en.wikipedia.org/wiki/"
region_df_path = 'region_mp.csv'


regions = {
    "Africa": "Africa", "East Africa": "Africa", "North Africa": "Africa", "Southern Africa": "Africa", "West Africa": "Africa", "Central Africa": "Africa",
    "Asia": "Asia", "Central Asia": "Asia", "East Asia": "Asia", "North Asia": "Asia", "South Asia": "Asia", "Southeast Asia": "Asia", "West Asia": "Asia",
    "Europe": "Europe", "Eastern Europe": "Europe", "Northern Europe": "Europe", "Southern Europe": "Europe", "Southeast Europe": "Europe", "Western Europe": "Europe",
    "Western Europe": "Europe", "Central Europe": "Europe", "North America": "America", "Caribbean": "America", "Central America": "America", "America": "America",
    "Oceania": "Oceania", "Australia": "Oceania", "Melanesia": "Oceania", "Micronesia": "Oceania", "Polynesia": "Oceania", "China": "Asia", 'British': 'Europe',
    'West Indies': "America", "France": "Europe", "Florida": "America", "Adriatic": "Europe", 'Southeast': "Europe"
}


def extract_country_from_url():
    # extract
    html = requests.get(gdp_country_url)
    soup = bs(html.content, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    data = {
        'Country': []
    }

    # Country/Territory: [other data]
    for i, row in enumerate(table.find_all('tr')):
        # Remove Title
        if i < 3:
            continue

        # Extract each column
        cols = [col.text.strip() for col in row.find_all(['th', 'td'])]
        data['Country'].append(cols[0])

    return data['Country']


def extract_region_with_multiprocess(
    country: str,
) -> str:
    try:
        country: str = country.replace(' ', '_')
        for aux_url in ['', '_(region)', '_(country)']:
            search_url = base_url + country + aux_url
            try:
                html = requests.get(search_url)
                soup = bs(html.content, 'html.parser')
                main_contents = soup.find(
                    'div', {'class': 'mw-content-ltr mw-parser-output'}
                )
                paragraphs = main_contents.find_all('p')
                if not paragraphs:
                    continue
                break
            except:
                continue

        for idx in range(1, 5):
            f_paragraph = paragraphs[idx].text.split('. ')
            if len(f_paragraph) < 2:
                continue

            # 본문일 때
            flag = False
            for paragraph in f_paragraph:
                for key, value in regions.items():
                    if key in paragraph:
                        return [country, value]
                if flag:
                    break

            if not flag:
                return [country, 'None']
            break

    except Exception as e:
        pass

    return [country, 'None']


# Processing time: 40 seconds
if __name__ == '__main__':
    s_time = time.time()
    countries = extract_country_from_url()

    processes = []
    with Pool(4) as pool:
        return_values = pool.map(
            extract_region_with_multiprocess,
            countries
        )
        country_to_region = dict(return_values)

    df = pd.DataFrame(data=country_to_region.items(),
                      columns=['Country', 'Region'])
    df.to_csv(region_df_path, index=False)
    e_time = time.time()
    print(f"Processing time: {e_time - s_time}")
