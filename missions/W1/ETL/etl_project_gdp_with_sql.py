import re
import os
import requests
from enum import Enum
from io import StringIO
from datetime import datetime

import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.gdp_url = os.getenv('GDP_URL')
        self.region_url = os.getenv('REGION_URL')
        self.db_path = os.getenv('DB_PATH')
        self.table_name = os.getenv('TABLE_NAME')
        self.log_path = os.getenv('LOG_PATH')

config = Config()

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"

def logging(message: str, level: LogLevel) -> None:
    current_time = datetime.now().strftime("%Y-%B-%d-%H-%M-%S")
    log = f"[{level.value}]: {current_time}, {message}"
    with open(config.log_path, "a") as log_file:
        log_file.write(f"{log}\n")

class SQLExecutor:
    def __init__(self, database, table=None):
        self.database = database
        self.table = table
        self._ensure_database_exists()
        if table:
            self.create_table()

    def _ensure_database_exists(self):
        if not os.path.exists(self.database):
            open(self.database, 'w').close()

    def create_table(self):
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Country TEXT NOT NULL,
            GDP_USD_billion REAL NOT NULL,
            Region TEXT NOT NULL,
            Year INTEGER NOT NULL
        )
        """
        self.run_sql(create_table_query)

    """ 
    query에서 주석 제거
    """
    def strip_sql_comments(self, query):
        # (--) 제거
        query = re.sub(r'--.*', '', query)
        # (/* */) 제거, flags=re.DOTALL으로 \n도 .에 포함되도록
        query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
        return query

    def run_sql(self, query, data=None):
        try:
            cleaned_query = self.strip_sql_comments(query).strip()
            
            with sqlite3.connect(self.database) as conn:
                cur = conn.cursor()

                if data:
                    cur.executemany(cleaned_query, data)
                else:
                    cur.execute(cleaned_query)

                query_type = cleaned_query.split()[0].upper()

                if query_type in ['SELECT', 'WITH']:
                    return cur.fetchall()
                elif query_type in ['INSERT', 'UPDATE', 'DELETE', 'CREATE']:
                    conn.commit()
                    return cur.lastrowid if query_type == 'INSERT' else cur.rowcount
                else:
                    print("Unsupported query type")
                    return None
        except sqlite3.Error as e:
            raise Exception(f"Error during SQL execution: {e}")

def extract_gdp_data(url: str) -> pd.DataFrame:
    logging("Starting extraction", LogLevel.INFO)

    try: 
        response = requests.get(url)

        # HTTP 응답 코드가 400 이상인 경우 HTTPError 예외를 발생
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, "lxml")
        gdp_table = soup.find("table", "wikitable")

        table_df_list= pd.read_html(StringIO(str(gdp_table)))
        gdp_df = table_df_list[0]

        selected_columns = [
            ("Country/Territory", "Country/Territory"),
            ("IMF[1][13]", "Forecast"),
            ("IMF[1][13]", "Year")
        ]
        gdp_df = gdp_df[selected_columns]

        logging("Extraction finished successfully", LogLevel.INFO)
        return gdp_df 
    except Exception as e:
        logging(f"Error during extraction: {e}", LogLevel.ERROR)
        raise Exception("Error during extraction")
    
def get_region_info() -> pd.DataFrame:
    try:
        response = requests.get(config.region_url)
        regions_json = response.json()

        data = [{"Country": item["name"]["common"], "Region": item["region"]} for item in regions_json]
        region_df = pd.DataFrame(data)
        # 예외처리
        region_df.replace({"Czechia": "Czech Republic", "Republic of the Congo": "Congo", "Timor-Leste": "East Timor"}, inplace=True)
        return region_df
    except Exception as e:
        raise Exception("Error during region info extraction")

def transform_gdp_data(gdp_df: pd.DataFrame) -> pd.DataFrame:
    logging("Starting transformation", LogLevel.INFO)

    try:
        # 열 이름 변경
        gdp_df.columns = ["Country", "GDP", "Year"]

        # World 제거
        gdp_df = gdp_df[gdp_df["Country"] != "World"]

        # 결측값 제거
        gdp_df = gdp_df[(gdp_df["GDP"] != "—") & (gdp_df["Year"] != "—")]

        # 연도에 같이 있는 주석 제거
        gdp_df["Year"] = gdp_df["Year"].apply(lambda x: re.sub(r"\[\w+ \d+\]", "", x).strip())

        # GDP, Year  변환
        gdp_df["GDP"] = round(gdp_df["GDP"].astype(float) / 1000, 2)
        gdp_df["Year"] = gdp_df["Year"].astype(int)

        # Region 정보 추가
        region_df = get_region_info()
        gdp_region_df = pd.merge(left=gdp_df, right=region_df, on="Country", how="left")
        
        # GDP 기준으로 내림차순 정렬
        gdp_region_df.sort_values(by=["GDP"], ascending=False, inplace=True)

        logging("Transformation finished successfully", LogLevel.INFO)
        return gdp_region_df
    except Exception as e:
        logging(f"Error during transformation: {e}", LogLevel.ERROR)
        raise Exception("Error during transformation")

def load_gdp_data(gdp_df: pd.DataFrame, db_path: str, table_name: str):
    logging("Starting load", LogLevel.INFO)

    try: 
        executor = SQLExecutor(database=db_path, table=table_name)

        insert_query = f"""INSERT INTO {table_name} (Country, GDP_USD_billion, Region, Year) VALUES (?, ?, ?, ?)"""
        data = gdp_df[['Country', 'GDP', 'Region', 'Year']].values.tolist()
        executor.run_sql(insert_query, data)

        logging("Load finished successfully", LogLevel.INFO)
    except Exception as e:
        logging(f"Error during load: {e}", LogLevel.ERROR)
        raise Exception("Error during load")

def get_country_upper_n(db_path: str, table_name: str, n: int) -> list[str]:
    executor = SQLExecutor(database=db_path)

    query = f"""SELECT Country 
                FROM {table_name} 
                WHERE GDP_USD_billion >= {n}"""

    result = executor.run_sql(query)
    return result

def topN_mean_gdp_by_region(db_path: str, table_name: str, n: int) -> dict:
    executor = SQLExecutor(database=db_path)

    query = f"""WITH Ranked_{table_name} AS (
                    SELECT *
                        , RANK() OVER(PARTITION BY Region ORDER BY GDP_USD_billion DESC) AS Rank_Per_Region
                    FROM {table_name}
                )
                SELECT Region
                    , ROUND(AVG(GDP_USD_billion), 2) AS Mean_GDP
                FROM Ranked_{table_name}
                WHERE Rank_Per_Region <= {n}
                GROUP BY Region
                ORDER BY Mean_GDP DESC
            """

    result = executor.run_sql(query)
    return result

def run() -> None:
    print("GDP가 100B USD이상이 되는 국가: ")
    print(get_country_upper_n(config.db_path, config.table_name, 100))
    print()
    print("각 Region별로 top5 국가의 GDP 평균: ")
    print(topN_mean_gdp_by_region(config.db_path, config.table_name, 5))


def ETL(url: str, db_path: str, table_name: str) -> None:
    gdp_df = extract_gdp_data(url)
    transformed_gdp_df = transform_gdp_data(gdp_df)
    load_gdp_data(transformed_gdp_df, db_path, table_name)

if __name__ == "__main__":
    ETL(config.gdp_url, config.db_path, config.table_name)

    run()