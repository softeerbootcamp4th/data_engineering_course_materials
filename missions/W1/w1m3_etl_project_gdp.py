import os
import sys
import sqlite3
from datetime import datetime

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


LOGGER_PATH = "etl_project_log.txt"
WIKI_URL = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
REGION_DF_PATH = "region_mp.csv"
JSON_PATH = "Countries_by_GDP.json"


class Logger:
    """Logger Class"""

    def __init__(self, log_file: str | os.PathLike) -> None:
        """__init__ Constructor

        Args:
            log_file (str | os.PathLike): _description_
        Returns:
            None
        """
        self.log_file = log_file

    def log(
        self,
        msg: str,
        level: str = "INFO"
    ) -> None:
        """Logging Function

        Args:
            msg (str): _description_
            level (str, optional): _description_. Defaults to "INFO".
        Returns:
            None
        """
        timestamp = datetime.now().strftime('%Y-%B-%d %H:%M:%S')
        with open(self.log_file, 'a') as f:
            line = f"{timestamp} - ({level}) - {msg}\n"
            f.write(line)
            print(line)


def extract(
    url: str,
    logger: Logger
) -> dict:
    """Extract Table Data from Wikipedia

    Args:
        url (str): Wikipedia URL
        logger (Logger): Logger
    Returns:
        data (dict): Extracted Data
    """
    logger.log(f"Extracting Start !!", "INFO")
    try:
        html = requests.get(url)
        soup = bs(html.content, 'html.parser')
        table = soup.find('table', {'class': 'wikitable'})
        data = {
            'Country': [],
            'GDP(US$MM)': [],
        }

        # Country: [other data]
        for i, row in enumerate(table.find_all('tr')):
            # Remove Title
            if i < 3:
                continue

            # Extract each column
            cols = [col.text.strip() for col in row.find_all(['th', 'td'])]
            data['Country'].append(cols[0])
            data['GDP(US$MM)'].append(cols[1])

        logger.log(f"Extracting Finished !!", "INFO")
        return data

    except Exception as e:
        logger.log("Extracting Failed", "ERROR")
        print(e)
        sys.exit(0)


def transform(
    json_data: dict,
    region_df_path: pd.DataFrame,
    logger: Logger,
) -> pd.DataFrame:
    """Transform Data

    Args:
        json_data (dict): JSON filepath
        region_df_path (pd.DataFrame): Region DataFrame filepath
        logger (Logger): Logger
    Returns:
        df (pd.DataFrame): DataFrame
    """

    logger.log("Transforming Start !!")
    try:
        df = pd.DataFrame(json_data)
        region_df = pd.read_csv(region_df_path)

        df['GDP_USD_B'] = df['GDP(US$MM)'].apply(
            lambda x: x.replace(',', '') if x != '—' else '0')
        df['GDP_USD_B'] = df['GDP_USD_B'].astype(float) / 1000
        df['GDP_USD_B'] = df['GDP_USD_B'].round(2)

        df = pd.merge(df, region_df, on='Country', how='left')
        logger.log("Transforming Finished !!")

        return df

    except Exception as e:
        logger.log("Transforming Failed", "ERROR")
        print(e)
        sys.exit(0)


def load(
    df: pd.DataFrame,
    json_path: str | os.PathLike,
    logger: Logger,
) -> None:
    """Save Transformed Data to JSON

    Args:
        df (pd.DataFrame): DataFrame
        json_path (str | os.PathLike): DataFrame filepath
        logger (Logger): Logger
    Returns:
        None
    """

    try:
        logger.log("Loading start !!", "INFO")
        df.to_json(json_path, orient='records')
        logger.log("Loading Finished !!", "INFO")

    except Exception as e:
        logger.log("Loading Failed", "ERROR")
        print(e)
        sys.exit(0)


def query_gdp_over_usd_100b(
    json_path: str | os.PathLike,
    logger: Logger,
) -> None:
    """Query GDP over USD 100B"""
    logger.log("Query GDP over USD 100B", "INFO")
    try:
        df = pd.read_json(json_path)
        conn = sqlite3.connect(':memory:')

        df.to_sql('gdp_data', conn, index=False, if_exists='replace')
        query = """
        SELECT
            Country,
            GDP_USD_B
        FROM 
            gdp_data
        WHERE 
            GDP_USD_B > 100
        ORDER BY
            GDP_USD_B DESC;
        """

        res_df = pd.read_sql_query(query, conn)
        print(res_df)
        conn.close()
        logger.log("Querying Finished !!", "INFO")

    except Exception as e:
        logger.log("Querying Failed", "ERROR")
        print(e)


def query_top5_mean_per_region(
    json_path: str | os.PathLike,
    logger: Logger,
) -> None:
    """Query top5 mean value of GDP per region"""
    logger.log("Querying top5 mean value of GDP per region", "INFO")

    try:
        df = pd.read_json(json_path)
        conn = sqlite3.connect(':memory:')

        df.to_sql('gdp_data', conn, index=False, if_exists='replace')
        query = """            
        WITH Top5 AS (
            SELECT 
                Country, 
                GDP_USD_B, 
                Region,
                ROW_NUMBER() OVER(PARTITION BY Region ORDER BY GDP_USD_B DESC) AS rnk
            FROM gdp_data
            WHERE GDP_USD_B IS NOT NULL
        )
        SELECT Region, AVG(GDP_USD_B) AS Top5_AVG_GDP 
        FROM Top5
        WHERE rnk <= 5
        GROUP BY Region
        ORDER BY Top5_AVG_GDP DESC;
        """

        res_df = pd.read_sql_query(query, conn)
        print(res_df)
        conn.close()
        logger.log("Querying Finished !!", "INFO")

    except Exception as e:
        logger.log("Querying Failed", "ERROR")
        print(e)


if __name__ == '__main__':
    logger = Logger(LOGGER_PATH)
    logger.log("ETL Process is Started", "INFO")

    extract_data = extract(WIKI_URL, logger)
    transform_data = transform(extract_data, REGION_DF_PATH, logger)
    load(transform_data, JSON_PATH, logger)
    query_gdp_over_usd_100b(JSON_PATH, logger)
    query_top5_mean_per_region(JSON_PATH, logger)

    logger.log("ETL Process is Finished", "INFO")
