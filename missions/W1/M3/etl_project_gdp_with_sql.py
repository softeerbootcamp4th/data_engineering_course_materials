import collections
import json
import logging
import sqlite3

import pandas as pd
import requests
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser

collections.Callable = collections.abc.Callable
logger = logging.getLogger(__name__)
logging.basicConfig(filename='etl_project_log.txt', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s,%(message)s', datefmt='%Y-%B-%d-%H-%M-%S')


def extract():
    logging.debug("extracting GDP from wikipedia")
    # get wikipedia page
    html = requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29').text
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


def load(imf_gdp_with_region, db_name='World_Economies.db', table_name='Countries_by_GDP'):
    def create_sqlite_database(db_name):
        conn = None
        try:
            conn = sqlite3.connect(db_name)
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    logging.debug("loading GDP to db start")
    create_sqlite_database(db_name='World_Economies.db')
    with sqlite3.connect(db_name) as con:
        imf_gdp_with_region.to_sql(table_name, con, if_exists='replace', index_label='Rank')
    logging.debug("loading GDP in db done")
    return True


def get_countries_gdp_more_than_100b(db_name='World_Economies.db'):
    query = """
        SELECT * FROM Countries_by_GDP WHERE GDP_USD_billion >= 100
        """
    return sql_get(query)


def get_average_gdp_for_region(db_name='World_Economies.db'):
    query = """
        SELECT Region, ROUND(AVG(GDP_USD_billion),2) FROM
        (
            SELECT
                Region,
                GDP_USD_billion,
                RANK() OVER (PARTITION BY Region ORDER BY GDP_USD_billion DESC) AS RANKING
            FROM Countries_by_GDP
        )
        WHERE RANKING <= 5 AND Region IS NOT NULL
        GROUP BY Region
        """
    return sql_get(query)


def sql_get(query, db_name='World_Economies.db'):
    logging.debug("executing query {}".format(query))
    try:
        with sqlite3.connect(db_name) as conn:
            cur = conn.cursor()
            cur.execute(query)
            logging.debug("executed query done")
            return cur.fetchall()
    except sqlite3.Error as e:
        logging.debug("failed query")
        logging.debug(e)
        print(e)
        return []


if __name__ == '__main__':
    gdp_frame = extract()
    imf_gdp_with_region = transform(gdp_frame)
    load(imf_gdp_with_region)
    print(get_countries_gdp_more_than_100b())
    print(get_average_gdp_for_region())
