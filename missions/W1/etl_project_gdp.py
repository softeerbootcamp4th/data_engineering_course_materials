import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import json
import datetime
import os
import sqlite3


def log(text):
    now = datetime.datetime.now()
    now_date = now.strftime("%Y-%B-%d-%H-%M-%S")

    folder_path = os.path.join(os.getcwd(), "missions", "W1", "etl_process")
    file_path = os.path.join(folder_path, "etl_project_log.txt")

    with open(file_path, "a") as f:
        f.write(now_date + " " + text + "\n")


def extract():
    log("Extract start")
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # HTML에서 테이블을 DataFrame으로 읽어오기
    table = soup.find("table", class_="wikitable")
    df = pd.read_html(StringIO(str(table)))[0]  # 첫 번째 테이블만 가져오기

    # 컬럼 이름 설정
    df.columns = [
        "Country",
        "GDP_USD_million",
        "IMF_Year",
        "World_Bank_Estimate",
        "World_Bank_Year",
        "UN_Estimate",
        "UN_Year",
    ]
    df = df[["Country", "GDP_USD_million"]]
    json_data = df.to_json(orient="records")

    folder_path = os.path.join(os.getcwd(), "missions", "W1", "etl_process")
    file_path = os.path.join(folder_path, "Countries_by_GDP.json")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json_data)

    log("Extract end")
    return json_data


def preprocess_gdp(row):
    data = {}

    # 국가명 처리
    if pd.notna(row["Country"]):
        if row["Country"] != "World":
            data["Country"] = row["Country"]

    # GDP 처리
    if pd.notna(row["GDP_USD_million"]) and row["GDP_USD_million"] != "—":
        data["GDP_USD_billion"] = round(
            int(row["GDP_USD_million"].replace(",", "")) / 1000, 2
        )

    return pd.Series(data)


def transform(countries_by_gdp):
    log("Transform start")
    df = pd.read_json(countries_by_gdp, orient="records")
    df = df.apply(preprocess_gdp, axis=1)
    df = df.dropna(axis=0).reset_index(drop=True)

    json_file_path = "missions/W1/etl_process/Countries_by_Continent.json"
    with open(json_file_path, "r", encoding="utf-8") as f:
        countries_by_continent = json.load(f)

    region_map = {}
    for region, countries in countries_by_continent.items():
        for country in countries:
            region_map[country] = region
    df["Region"] = df["Country"].map(region_map)

    log("Transform end")
    return df


def load(transformed_gdp):
    log("Load start")
    db_path = "missions/W1/etl_process//World_Economies.db"
    conn = sqlite3.connect(db_path)
    transformed_gdp.to_sql("Countries_by_GDP", conn, index=False, if_exists="replace")
    conn.close()

    json_data = transformed_gdp.to_json(orient="records")

    folder_path = os.path.join(os.getcwd(), "missions", "W1", "etl_process")
    file_path = os.path.join(folder_path, "Countries_by_GDP_with_Region.json")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json_data)
    log("Load end")

# gdp 100B 이상인 국가 출력하기
def gdp_over_100B_print():
    log("print gdp over 100B country start")
    json_file_path = "missions/W1/etl_process/Countries_by_GDP_with_Region.json"
    with open(json_file_path, "r", encoding="utf-8") as f:
        countries_by_continent = json.load(f)
    for country in countries_by_continent:
        if country["GDP_USD_billion"] > 100:
            print(country["Country"])

    print(countries_by_continent)
    log("print gdp over 100B country end")


# 각 Region별 GDP TOP5 국가 평균 출력하기
def top5_each_region_mean_print():
    log("print top3 each region country mean start")
    json_file_path = "missions/W1/etl_process/Countries_by_GDP_with_Region.json"
    with open(json_file_path, "r", encoding="utf-8") as f:
        countries_by_continent = json.load(f)
    df = pd.DataFrame(countries_by_continent)

    top5_per_region = (
        df.groupby("Region")
        .apply(lambda x: x.nlargest(5, "GDP_USD_billion"))
        .reset_index(drop=True)
    )

    average_gdp_per_region = (
        top5_per_region.groupby("Region")["GDP_USD_billion"].mean().reset_index()
    )
    average_gdp_per_region["GDP_USD_billion"] = average_gdp_per_region[
        "GDP_USD_billion"
    ].round(2)

    print(average_gdp_per_region)
    log("print top3 each region country mean end")


# gdp 100B 이상인 국가 출력하기
def gdp_over_100B_print_sql():
    log("print gdp over 100B country start")
    db_path = "missions/W1/etl_process//World_Economies.db"
    conn = sqlite3.connect(db_path)
    sql = "SELECT Country FROM Countries_by_GDP WHERE GDP_USD_billion >= 100"
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        print(row)
    log("print gdp over 100B country end")


# 각 Region별 GDP TOP5 국가 평균 출력하기
def top5_each_region_mean_print_sql():
    db_path = "missions/W1/etl_process//World_Economies.db"
    conn = sqlite3.connect(db_path)
    sql = """        
        SELECT Region, ROUND(AVG(GDP_USD_billion), 2) AS Average_GDP
        FROM (
            SELECT Country, GDP_USD_billion, Region,
                ROW_NUMBER() OVER (PARTITION BY Region ORDER BY GDP_USD_billion DESC) AS rn
            FROM Countries_by_GDP
        )
        WHERE rn <= 5
        GROUP BY Region;
        """
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        print(row)


if __name__ == "__main__":
    countries_by_gdp = extract()
    transformed_gdp = transform(countries_by_gdp)
    load(transformed_gdp)
    gdp_over_100B_print()
    top5_each_region_mean_print()
