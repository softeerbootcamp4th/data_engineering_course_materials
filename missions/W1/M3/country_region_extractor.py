import collections
import json

import pandas as pd
import requests
import yaml
from box import Box
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser

collections.Callable = collections.abc.Callable
with open('config.yaml', 'r') as f:
    config_yaml = yaml.load(f, Loader=yaml.FullLoader)
    print(config_yaml)
    config = Box(config_yaml)

target_url = [(
    config.AFRICA_COUNTRY_URL, "Africa"
), (
    config.SOUTH_AMERICA_COUNTRY_URL, "South America"
), (
    config.NORTH_AMERICA_COUNTRY_URL, "North America"
), (
    config.ASIA_COUNTRY_URL, "Asia"
), (
    config.EUROPE_COUNTRY_URL, "Europe"
), (
    config.OCEANIA_COUNTRY_URL, "Oceania"
)]


def get_table(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    table = parser.make2d(soup.find("table"))
    return pd.DataFrame(table[1:], columns=[table[0]])


if __name__ == '__main__':
    country_region = {
        "Hong Kong": "Asia"
    }
    for url, region in target_url:
        df = get_table(url)
        for row in df.filter(regex='(Country)|(Location)').iterrows():
            if row[1].iloc[0] in country_region.keys():
                print(row[1].iloc[0], " already exists ", country_region[row[1].iloc[0]], "current : ", region)
            else:
                country_region[row[1].iloc[0]] = region
    with open("country_region.json", "w") as json_file:
        json.dump(country_region, json_file)
