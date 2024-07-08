import collections
import json
import logging

import pandas as pd
import requests
import yaml
from box import Box
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser
from pandasql import sqldf

collections.Callable = collections.abc.Callable
logger = logging.getLogger(__name__)
logging.basicConfig(filename='etl_project_log.txt', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s,%(message)s', datefmt='%Y-%B-%d-%H-%M-%S')

with open('config.yaml', 'r') as f:
    config_yaml = yaml.load(f, Loader=yaml.FullLoader)
    print(config_yaml)
    config = Box(config_yaml)


def extract():
    logging.debug("extracting GDP from wikipedia")
    # get wikipedia page
    html = requests.get(config.GDP_WIKIPEDIA_URL).text
    soup = BeautifulSoup(html, 'html.parser')
    # find gdp table tag from page
    gdp_table = soup.find("table", attrs={"class": "wikitable sortable sticky-header-multi static-row-numbers"})
    # make table using table tag
    parsed = parser.make2d(gdp_table)
    # filter table
    filtered_table = filter_table(parsed)
    # make dataframe from table
    gdp_frame = pd.DataFrame(filtered_table[2:], columns=[filtered_table[0], filtered_table[1]])
    # export imf table
    imf_gdp = gdp_frame[['Country/Territory', 'IMF']]
    logging.debug("extracted GDP from wikipedia done")
    return imf_gdp


def filter_table(parsed):
    for i, row in enumerate(parsed):
        for j, word in enumerate(row):
            parsed[i][j] = remove_nested_parens(word).replace(',', '')
    return parsed


def remove_nested_parens(input_str):
    result = ''
    paren_level = 0
    for ch in input_str:
        if ch == '[':
            paren_level += 1
        elif (ch == ']') and paren_level:
            paren_level -= 1
        elif not paren_level:
            result += ch
    return result


def transform(imf_gdp):
    logging.debug("transforming step start")
    # drop unnecessary multi-column
    imf_gdp.columns = imf_gdp.columns.droplevel()
    imf_gdp = imf_gdp.rename(columns={'Country/Territory': 'Country', 'Forecast': 'GDP_USD_billion'})
    imf_gdp = (
        imf_gdp[imf_gdp['GDP_USD_billion'].apply(lambda x: x.isnumeric())]
        .astype({'GDP_USD_billion': 'float'})
        .astype({'Year': 'int64'})
        .query('Country != "World"')
        .sort_values('GDP_USD_billion', ascending=False)
        .reset_index(drop=True)
    )
    imf_gdp['GDP_USD_billion'] = imf_gdp['GDP_USD_billion'] / 1000
    imf_gdp = imf_gdp.round({'GDP_USD_billion': 2})

    region_column = get_region_column(imf_gdp)
    imf_gdp_with_region = pd.merge(imf_gdp, region_column,
                                   how='right', right_index=True, left_index=True)
    logging.debug("transforming step done")
    return imf_gdp_with_region


def get_region_column(imf_gdp):
    region = []
    with open('country_region.json') as json_file:
        country_region = json.load(json_file)
        for row in imf_gdp.iterrows():
            country = row[1]['Country']
            if country in country_region:
                region.append(country_region[country])
            else:
                region.append(None)
                logging.debug("region for {} not found".format(country))
    return pd.DataFrame(region, columns=['Region'])


def load(imf_gdp_with_region):
    logging.debug("loading GDP in json start")
    imf_gdp_with_region.to_json(config.LOAD_FILE_DESTINATION)
    logging.debug("loading GDP in json done")


def get_countries_gdp_more_than_100b(db_name=config.LOAD_FILE_DESTINATION):
    gdp = pd.read_json(db_name)
    return sqldf("SELECT * FROM gdp WHERE GDP_USD_billion >= 100")


def get_average_gdp_for_region(db_name=config.LOAD_FILE_DESTINATION):
    gdp = pd.read_json(db_name)
    return sqldf("""
        SELECT Region, ROUND(AVG(GDP_USD_billion),2) FROM
        (
            SELECT
                Region,
                GDP_USD_billion,
                RANK() OVER (PARTITION BY Region ORDER BY GDP_USD_billion DESC) AS RANKING
            FROM gdp
        )
        WHERE RANKING <= 5 AND Region IS NOT NULL
        GROUP BY Region
        """)


if __name__ == '__main__':
    gdp_frame = extract()
    imf_gdp_with_region = transform(gdp_frame)
    load(imf_gdp_with_region)
    print(get_countries_gdp_more_than_100b())
    print(get_average_gdp_for_region())
