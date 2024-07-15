import requests
from bs4 import BeautifulSoup
import os
import json


def countries_by_continent():
    url = "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_by_continent"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find_all("table", {"class": "sortable"})
    africa_rows = table[0].find_all("tr")
    asia_rows = table[1].find_all("tr")
    europe_rows = table[2].find_all("tr")
    north_america_rows = table[3].find_all("tr")
    oceania_rows = table[4].find_all("tr")
    south_america_rows = table[5].find_all("tr")

    africa = each_continent(africa_rows[3:])
    asia = each_continent(asia_rows[3:])
    europe = each_continent(europe_rows[3:])
    north_america = each_continent(north_america_rows[3:])
    oceania = each_continent(oceania_rows[3:])
    south_america = each_continent(south_america_rows[3:])

    json_data = {
        "Africa": africa,
        "Asia": asia,
        "Europe": europe,
        "North America": north_america,
        "Oceania": oceania,
        "South America": south_america,
    }

    region_map = {
        "South Korea": "Asia",
        "DR Congo": "Africa",
        "Congo": "Africa",
        "Bahamas": "North America",
        "Gambia": "Africa",
    }

    for country, region in region_map.items():
        json_data[region].append(country)

    folder_path = os.path.join(os.getcwd(), "missions", "W1", "etl_process")
    file_path = os.path.join(folder_path, "Countries_by_Continent.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


def each_continent(rows):
    data = []
    for row in rows:
        cols = row.find_all("td")
        if cols and cols[0].find("a"):
            country = cols[0].find("a").text.strip()
            data.append(country)
    return data


countries_by_continent()
