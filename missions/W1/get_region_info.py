import json
from collections import OrderedDict
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import os.path
from io import StringIO

ASIA_URL='https://en.wikipedia.org/wiki/List_of_Asian_countries_by_GDP'
NORTH_AMERICA_URL='https://en.wikipedia.org/wiki/List_of_North_American_countries_by_GDP_(PPP)'
SOUTH_AMERICA_URL='https://en.wikipedia.org/wiki/List_of_South_American_countries_and_dependencies_by_GDP_(PPP)'
EUROPE_URL='https://en.wikipedia.org/wiki/List_of_sovereign_states_in_Europe_by_GDP_(PPP)'
OCEANIA_URL='https://en.wikipedia.org/wiki/List_of_Oceanian_countries_by_GDP'
AFRICA_URL='https://en.wikipedia.org/wiki/List_of_African_countries_by_GDP_(PPP)'
URLS = [ASIA_URL, NORTH_AMERICA_URL, SOUTH_AMERICA_URL, EUROPE_URL, OCEANIA_URL, AFRICA_URL]
PATH = "assets/"
REGION_INFO_NAME='region_infos.json'
TABLE_IDXS = [0, 0, 0, 1, 0, 0]

def etl_region_info():
    region_infos = dict()
    region_names = ["Asia", "North America", "South America", "Europe", "Oceania", "Africa"]


    for region_name, url, idx in zip(region_names, URLS, TABLE_IDXS):    
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        raw_data = soup.select('table')

        # Transform raw data to pandas dataFrame
        table_df_list = pd.read_html(StringIO(str(raw_data)))
        tables_df = table_df_list[idx]
        
        if region_name=='Oceania':
            region_infos[region_name] = list(tables_df['Location'])
        elif region_name=='Asia':
            country_series = tables_df[2:][1]
            asia_list = tables_df[2:][1].to_list()
            for idx, name in enumerate(asia_list):
                if name.find(" (SAR)") != -1:
                    asia_list[idx] = name.replace(' (SAR)', '')
            region_infos[region_name] = asia_list
        else:
            region_infos[region_name] = list(tables_df['Country'])        
                   
    with open(PATH+REGION_INFO_NAME, "w") as json_file:
        json.dump(region_infos, json_file)

    return

if __name__=="__main__":
    etl_region_info()