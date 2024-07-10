import pandas as pd
import json
import requests
from io import StringIO

# setting
json_path = '/Users/admin/Desktop/Data_Engineering/W1/ETL/continent_countries.json'
csv_url = 'https://raw.githubusercontent.com/jefftune/pycountry-convert/master/data/Continents_to_CountryNames.csv'

# CSV file to DataFrame
response = requests.get(csv_url)
if response.status_code == 200:
    csv_data = response.content.decode('utf-8')
    df = pd.read_csv(StringIO(csv_data))
else:
    raise Exception(f"Failed to fetch CSV data: {response.status_code}")

# DataFrame을 대륙별 국가로 변환
continent_dict = df.groupby('Continent')['Country'].apply(list).to_dict()

# load JSON
try:
    with open(json_path, 'r') as file:
        continent_data = json.load(file)
except FileNotFoundError:
    continent_data = {}

# new data insert to JSON
continent_data.update(continent_dict)

# JSON file update
with open(json_path, 'w') as file:
    json.dump(continent_data, file, indent=4)
