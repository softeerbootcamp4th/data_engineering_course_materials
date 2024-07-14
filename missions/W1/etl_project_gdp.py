import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from tabulate import tabulate
from datetime import datetime

log_path = 'etl_project_log.txt'
gdp_data_url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
json_path = 'Countries_by_GDP.json'
countries_by_region_path = "countries_by_region.csv"

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
def extract_from_wikipedia() -> pd.DataFrame:
    gdp_df = pd.DataFrame()
    try:
        page = requests.get(gdp_data_url)
        soup = bs(page.text, "html.parser")
        rows = soup.select('table.wikitable > tbody > tr')
        for count,row in enumerate(rows):
            items = row.select('td')
            if count >= 3:
                new_row = pd.DataFrame({'Country': [items[0].text], 'GDP': [items[1].text]})
                gdp_df = pd.concat([gdp_df, new_row] ,ignore_index=True)
    except Exception as e:
        write_log("Extracting Failed")
        print(e)
        exit(1)

    return gdp_df

@logger("Transforming gdp data")
def transform_to_dataframe(gdp_df: pd.DataFrame) -> pd.DataFrame:
    region_df = pd.read_csv(countries_by_region_path, skiprows=[0])
    region_dict = {row['Entity']:row['Continent'] for _,row in region_df.iterrows()}

    gdp_df['Country'] = gdp_df['Country'].str.strip()
    gdp_df['GDP_USD_billion'] = pd.to_numeric(gdp_df['GDP'].str.replace(',',''), errors='coerce') / 1000
    gdp_df['Region'] = gdp_df['Country'].map(region_dict)
    gdp_df = gdp_df.drop('GDP', axis=1).sort_values(by='GDP_USD_billion', ascending=False, ignore_index=True)
    return gdp_df

@logger("Loading data in json file")
def load_in_json(df: pd.DataFrame) -> None:
    df.to_json(json_path, orient='records', indent=4, force_ascii=False)


def get_avg_gdp_of_top_n_by_region(df: pd.DataFrame, n=5) -> pd.DataFrame:
    avg_df = (df.groupby('Region')
              .apply(lambda x: x.nlargest(5, 'GDP_USD_billion')['GDP_USD_billion'].mean(), include_groups=False)
              .reset_index(name='Average_GDP_USB_billion'))
    return avg_df

def print_data_frame(df: pd.DataFrame):
    print(tabulate(df, headers='keys', tablefmt='psql', floatfmt=".2f"))


if __name__ == "__main__":
    gdp_df = extract_from_wikipedia()
    gdp_df_transformed = transform_to_dataframe(gdp_df)
    load_in_json(gdp_df_transformed)

    print("\n\n[ Countries whose GDP is upper than 100B USD ]")
    print_data_frame(gdp_df_transformed[gdp_df_transformed['GDP_USD_billion'] >= 100])

    print("\n\n[ Average GDP of top 5 countries by region ]")
    print_data_frame(get_avg_gdp_of_top_n_by_region(gdp_df_transformed, 5))