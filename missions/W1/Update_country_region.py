import pandas as pd
import json
import requests
from io import StringIO
import yaml

# yaml Data config로 가져오기
with open('/Users/admin/Desktop/Data_Engineering/W1/ETL/path_url_settings.yaml', 'r') as file:
    config = yaml.safe_load(file)

# 저장하고 다음부터 load할 Region별 국가 Data JSON file
json_path = config['file_path']['region_data_json_path']
# Region을 Update할 URL
csv_url = config['URL']['REGION_UPDATE_URL']

# DataFrame 생성
response = requests.get(csv_url)
if response.status_code == 200:
    csv_data = response.content.decode('utf-8')
    df = pd.read_csv(StringIO(csv_data))
else:
    raise Exception(f"Failed to fetch CSV data: {response.status_code}")

# Region별 Country로 변환
Region_dict = df.groupby('Continent')['Country'].apply(list).to_dict()

# JSON file load
try:
    with open(json_path, 'r') as file:
        Region_data = json.load(file)
except FileNotFoundError:
    Region_data = {}

# New Data insert to JSON
Region_data.update(Region_dict)

# JSON file update
with open(json_path, 'w') as file:
    json.dump(Region_data, file, indent=4)