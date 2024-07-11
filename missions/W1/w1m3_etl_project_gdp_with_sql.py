import os
import sys
import json
import sqlite3
from datetime import datetime

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


LOGGER_PATH = "etl_project_log.txt"
WIKI_URL = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
REGION_DF_PATH = "region_mp.csv"
DB_PATH = "Countries_by_GDP.db"


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
            line = f"{timestamp} - {level} - {msg}\n"
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
        json_path (json_data): JSON filepath
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
    db_path: str | os.PathLike,
    logger: Logger,
) -> None:
    """Save Transformed Data to DB Table

    Args:
        df (pd.DataFrame): DataFrame
        db_path (str | os.PathLike): Database filepath
        logger (Logger): Logger
    Returns:
        None
    """
    logger.log("Loading Start !!")
    if os.path.exists(db_path):
        os.remove(db_path)

    # Create Database
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE WorldEconomies (
            Country TEXT PRIMARY KEY,
            GDP FLOAT,
            Region TEXT
        )            
    """)
    conn.commit()

    # INSERT data into Database(world_economies)
    for _, row in df.iterrows():
        conn.execute(
            "INSERT INTO WorldEconomies VALUES (?, ?, ?)",
            (row['Country'], row['GDP_USD_B'], row['Region'])
        )
    conn.commit()
    conn.close()
    logger.log("Logging Finished !!")


def query_gdp_over_usd_100b(
    db_path: str | os.PathLike,
    logger: Logger,
) -> None:
    """Query GDP over USD 100B"""
    logger.log("Query GDP over USD 100B", "INFO")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * 
        FROM WorldEconomies
        WHERE GDP >= 100
        ORDER BY GDP DESC;
    """)

    print("Countries with GDP over 100 billion USD with SQL:")
    for row in cursor.fetchall():
        print(row)

    logger.log("Querying Finished !!", "INFO")
    conn.close()


def query_top5_mean_per_region(
    db_path: str | os.PathLike,
    logger: Logger,
) -> None:
    """Query top5 mean value of GDP per region"""
    logger.log("Querying top5 mean value of GDP per region", "INFO")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        WITH Top5 AS (
            SELECT 
                Country, 
                GDP, 
                Region,
                ROW_NUMBER() OVER(PARTITION BY Region ORDER BY GDP DESC) AS rnk
            FROM WorldEconomies
            WHERE GDP IS NOT NULL
        )
        SELECT Region, AVG(GDP) AS Top5_AVG_GDP 
        FROM Top5
        WHERE rnk <= 5
        GROUP BY Region
        ORDER BY Top5_AVG_GDP DESC;
    """)

    print("\nAverage GDP of top 5 countries in each region:")
    for row in cursor.fetchall():
        print(row)

    logger.log("Querying Finished !!", "INFO")
    conn.close()


if __name__ == '__main__':
    logger = Logger(LOGGER_PATH)
    logger.log("ETL Process is Started", "INFO")

    extract_data = extract(WIKI_URL, logger)
    transform_data = transform(extract_data, REGION_DF_PATH, logger)
    load(transform_data, DB_PATH, logger)
    query_gdp_over_usd_100b(DB_PATH, logger)
    query_top5_mean_per_region(DB_PATH, logger)

    logger.log("ETL Process is Finished", "INFO")
