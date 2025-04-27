# services/f1_scraper.py

import requests
import pandas as pd

def scrape_f1_standings():
    url = "http://ergast.com/api/f1/2024/driverStandings.json"
    response = requests.get(url)
    data = response.json()

    standings_list = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

    data_rows = []
    for driver_info in standings_list:
        position = driver_info['position']
        driver_name = f"{driver_info['Driver']['givenName']} {driver_info['Driver']['familyName']}"
        team = driver_info['Constructors'][0]['name']
        points = driver_info['points']
        data_rows.append([position, driver_name, team, points])

    df = pd.DataFrame(data_rows, columns=["Position", "Driver", "Team", "Points"])
    return df
