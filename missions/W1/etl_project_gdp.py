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
    gdp_df['GDP_USD_billion'] = gdp_df['GDP'].apply(lambda x: None if x == '—' else int(x.replace(',','')) / 1000)
    gdp_df['Region'] = gdp_df['Country'].map(region_dict)
    gdp_df = gdp_df.drop('GDP', axis=1).sort_values(by='GDP_USD_billion', ascending=False, ignore_index=True)
    return gdp_df

@logger("Loading data in json file")
def load_in_json(df):
    df.to_json(json_path, orient='records', indent=4, force_ascii=False)


def get_avg_gdp_of_top_n_by_region(df, n: int):
    avg_df = pd.DataFrame(columns=('Region', 'Avg_GDP_USD_billion'))
    for region in df['Region'].unique():
        region_countries = df[df['Region'] == region]
        top_n_countries = region_countries.sort_values(by='GDP_USD_billion', ascending=False).iloc[:n]
        avg_gdp = top_n_countries['GDP_USD_billion'].mean()

        new_row = {'Region':region, 'Avg_GDP_USD_billion':avg_gdp}
        avg_df.loc[len(avg_df)] = new_row
    return avg_df

def print_data_frame(df):
    print(tabulate(df, headers='keys', tablefmt='psql', floatfmt=".2f"))


if __name__ == "__main__":
    gdp_list = extract_from_wikipedia()
    gdp_df = transform_to_dataframe(gdp_list)
    load_in_json(gdp_df)

    print("\n\n[ Countries whose GDP is upper than 100B USD ]")
    print_data_frame(gdp_df[gdp_df['GDP_USD_billion'] >= 100])

    print("\n\n[ Average GDP of top 5 countries by region ]")
    print_data_frame(get_avg_gdp_of_top_n_by_region(gdp_df, 5))