import json
from collections import OrderedDict
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import os.path
from io import StringIO

URL = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
PATH = "assets/"
LOG_NAME = 'etl_project_log.txt'
JSON_NAME = "Countries_by_GDP.json"
REGION_INFO_NAME = 'region_infos.json'

def logger(msg: str):
    """_summary_

    Args:
        msg (str): msg for logging
    """
    with open(PATH+LOG_NAME, 'a') as f:
        time = datetime.now()
        time_str = f"{time.year}-{time.strftime("%B")}-{time.day:02d}-{time.hour:02d}-{time.second:02d}"
        f.write(time_str+', '+msg+'\n')
    return 
    
    
def extract()->pd.DataFrame:
    """_summary_
    Extract GDP info from "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    and save into json file.

    Returns:
        tables_df (raw data about GDP per country)
    """
    logger("Extracting Start.")
    
    # Get raw data
    response = requests.get(URL)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    raw_data = soup.select('table')

    # Transform raw data to pandas dataFrame
    table_df_list = pd.read_html(StringIO(str(raw_data)))
    tables_df = table_df_list[2]

    logger("Extracting Done")
    return tables_df


def transform(tables_df: pd.DataFrame)->pd.DataFrame: 
    """_summary_
    Transform raw data to target data. 
    1. Add region info
    2. Change GDP Unit (million dollars to billion dollars)
    3. Change '-' to np.nan in 'Forecast' column. 
    
    Args:
        tables_df (pd.DataFrame): raw data about GDP per country

    Returns:
        data (pd.DataFrame): transformed data.
    """
    logger("Transform Start.")
    
    df_country = tables_df['Country/Territory'].copy()
    
    # Convert '-' to np.nan and remove '[%]'. 
    df_IMF_Year =  tables_df['IMF[1][13]']['Year'].copy()
    is_num = np.array((df_IMF_Year.str.isnumeric()))
    not_num_idx = np.where(is_num==False)[0].tolist()
    for idx in not_num_idx:
        orig_data = df_IMF_Year[idx]
        if len(orig_data) != 1:
            df_IMF_Year[idx] = orig_data[-4:]
        else:
            df_IMF_Year[idx] = np.nan

    # Calc million to billion
    df_IMF_Forecast =  tables_df['IMF[1][13]']['Forecast'].copy()
    is_num = np.array((df_IMF_Forecast.str.isnumeric()))
    not_num_idx = np.where(is_num==False)[0].tolist()
    for idx in not_num_idx:
        orig_data = df_IMF_Forecast[idx]
        if len(orig_data) == 1:
            df_IMF_Forecast[idx] = np.nan
    df_IMF_Forecast = (pd.to_numeric(df_IMF_Forecast) / 1000).round(2)

    # Concat transformed data
    data = pd.concat([df_country, df_IMF_Year, df_IMF_Forecast], axis=1)
    data = data.sort_values(by=['Forecast', "Country/Territory"], ascending=[False, True])

    # Add column for region info
    with open(PATH+REGION_INFO_NAME, "r") as region_infos_json:
        continent_countries = json.load(region_infos_json)

    all_nations_list = list(data['Country/Territory'])
    regions = []
    
    for nation in all_nations_list:
        for key, value in continent_countries.items():
            find=0
            if nation in value:
                regions.append(key)
                find=1
                break
        if not find:
            regions.append("None")
    data['Region']=regions        
    logger("Transform Done.")
    return data


def load(data: pd.DataFrame):
    """_summary_
    Save transformed data in json file.
    
    Args:
        data (pd.DataFrame): transformed data
    """

    logger("Loading Start.")    
    
    # Save in json file.
    data.to_json(PATH+JSON_NAME, orient='columns')
    logger("Loading Done.")
    return


if __name__=="__main__":
    # init log file.
    if not os.path.isfile(PATH+LOG_NAME):
        f = open(PATH+LOG_NAME, 'w')
        f.close() 

    # Run ETL Process
    tables_df = extract()
    data = transform(tables_df)
    load(data)
    
    # Requirements 1
    over_100B_GDP_nations = data.loc[data.Forecast > 100]['Country/Territory']
    over_100B_GDP_nations_list = list(over_100B_GDP_nations)
    print("[Requirements 1] Over 100B GDP\n ", *over_100B_GDP_nations_list, sep=' ')
    
    # Requirements 2    
    region_names = ["Asia", "North America", "Europe", "South America", "Africa", "Oceania"]
    print("\n[Requirements 2] Average GDP of Top 5 Nations (Unit: Billion Dollars)")    
    for region_name in region_names:
        top5_avg_GDP = round(data.loc[data.Region==region_name].iloc[:5]['Forecast'].mean(), 2)
        print(f"{region_name}: {top5_avg_GDP}")
    
