import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from tabulate import tabulate
from datetime import datetime
import sqlite3

log_path = 'etl_project_log.txt'
gdp_data_url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
countries_by_region_path = "countries_by_region.csv"
db_path = 'World_Economies.db'
table_name = 'Countries_by_GDP'

class SqlRunner:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.create_connection()

    def create_connection(self):
        self.con = None
        try:
            self.con = sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            write_log(f"CREATE CONNECTION ERROR {e}")

    # run any sql query. But not return selected items
    def run_sql(self, sql: str, commit=False) -> None:
        try:
            cur = self.con.cursor()
            cur.execute(sql)
            if commit:
                self.con.commit()
        except sqlite3.Error as e:
            write_log(f"SQL ERROR: {e}")

    # insert or replace data into table
    def insert_data(self, table: str, df: pd.DataFrame) -> None:
        try:
            sql = f"""
                INSERT OR REPLACE INTO {table}(Country, GDP_USD_billion, Region)
                VALUES(?, ?, ?);
            """
            data = [tuple(x) for x in df[['Country', 'GDP', 'Region']].to_numpy()]
            cur = self.con.cursor()
            cur.executemany(sql, data)
            self.con.commit()
        except sqlite3.Error as e:
            write_log(f"SQL INSERT ERROR: {e}")
    
    # use when execute select query. returns selected items
    def select_data(self, select_sql: str) -> list:
        data = []
        try:
            cur = self.con.cursor()
            cur.execute(select_sql)
            data = cur.fetchall()
        except sqlite3.Error as e:
            write_log(f"SQL SELECT ERROR: {e}")
        finally:
            return data


# log message
def write_log(msg: str):
    timestamp = datetime.now().strftime("[%Y-%B-%d-%H-%M-%S] ")
    with open(log_path, 'a+') as f:
        f.write(timestamp + msg.strip() + '\n')

# decorator for logging
def logger(msg: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            write_log(f"{msg} started.")
            result = func(*args, **kwargs)
            write_log(f"{msg} finished.")
            return result
        return wrapper
    return decorator


@logger("Extracting raw GDP data from Wikipedia")
def extract_from_wikipedia() -> list:
    gdp_list = []
    try:
        page = requests.get(gdp_data_url)
        soup = bs(page.text, "html.parser")
        rows = soup.select('table.wikitable > tbody > tr')
        for count,row in enumerate(rows):
            items = row.select('td')
            if count >= 3:
                gdp_list.append((items[0].text, items[1].text))
    except Exception as e:
        write_log("Extracting Failed")
        print(e)
        exit(1)

    return gdp_list

@logger("Transforming gdp data")
def transform_to_dataframe(gdp_list: list) -> pd.DataFrame:
    region_df = pd.read_csv(countries_by_region_path, skiprows=[0])
    region_dict = {row['Entity']:row['Continent'] for _,row in region_df.iterrows()}

    gdp_df = pd.DataFrame(gdp_list, columns=('Country', 'GDP'))
    gdp_df['Country'] = gdp_df['Country'].apply(lambda x: x.strip())
    gdp_df['GDP'] = gdp_df['GDP'].apply(lambda x: None if x == '—' else int(x.replace(',','')) / 1000)
    gdp_df['Region'] = gdp_df['Region'] = gdp_df['Country'].map(region_dict)
    gdp_df = gdp_df.sort_values(by='GDP', ascending=False, ignore_index=True)
    return gdp_df

@logger("Loading data in json file")
def load_in_db(gdp_df: pd.DataFrame) -> None:
    gdp_db = SqlRunner(db_path)
    sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            Country text PRIMARY KEY,
            GDP_USD_billion real,
            Region text
        );
    """
    gdp_db.run_sql(sql)
    gdp_db.insert_data(table_name, gdp_df)
    return gdp_db

def get_gdp_upper_100_db() -> list:
    gdp_db = SqlRunner(db_path)
    sql = f"""
        SELECT * FROM {table_name}
        WHERE GDP_USD_billion >= 100
        ORDER BY GDP`_USD_billion DESC
    """
    gdp_upper_100_list = gdp_db.select_data(sql)
    return gdp_upper_100_list

def get_avg_gdp_of_top_n_by_region(n=5) -> list:
    gdp_db = SqlRunner(db_path)
    sql = f"""
        WITH RankedCountries AS (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY Region ORDER BY GDP_USD_billion DESC) as rank
            FROM {table_name}
        )
        SELECT Region, AVG(GDP_USD_billion) as Average_GDP
        FROM RankedCountries
        WHERE rank <= {n}
        GROUP BY Region
        ORDER BY Average_GDP DESC;
    """
    avg_gdp_list = gdp_db.select_data(sql)
    return avg_gdp_list

def print_data(data: list, header='keys') -> None:
    print(tabulate(data, headers=header, tablefmt='psql', floatfmt=".2f"))


if __name__ == "__main__":
    gdp_list = extract_from_wikipedia()
    gdp_df = transform_to_dataframe(gdp_list)
    load_in_db(gdp_df)

    gdp_upper_100_list = get_gdp_upper_100_db()
    print("\n\n[ Countries whose GDP is upper than 100B USD ]")
    print_data(gdp_upper_100_list, header=('Country', 'GDP_USD_billion', 'Region'))

    avg_gdp_list = get_avg_gdp_of_top_n_by_region(n=5)
    print("\n\n[ Average GDP of top 5 countries by region ]")
    print_data(avg_gdp_list, header=('Region', 'Avg_GDP_USD_billion'))