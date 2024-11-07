import os
import requests
from dotenv import load_dotenv
import pandas as pd


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

TEAMS_UCL_36 = ['Aston villa','Liverpool','Man City','Monaco','Brest','Leverkusen','Inter','Sporting CP',
'Arsenal','Barcelona','B. Dortmund','Real Madrid','Benfica','Juventus','Lille','Feyenoord','Atalanta',
'Stuttgart','Paris','Celtic','Sparta Praha', 'GNK Dinamo','Bayern München','Girona','Milan','Club Brugge',
'Atleti','PSV','Bologna','Shakhtar','Leipzig','Sturm Graz','Crvena Zvezda','Salzburg','Young Boys','S. Bratislava']


def fetch_data(limit, offset):
    UEFA_API = f"https://compstats.uefa.com/v1/player-ranking?competitionId=1&limit={limit}&offset={offset}&optionalFields=PLAYER%2CTEAM&order=DESC&phase=TOURNAMENT&seasonYear=2025&stats=minutes_played_official%2Cmatches_appearance%2Cgoals%2Cassists%2Cdistance_covered%2Ctop_speed"
    response = requests.get(UEFA_API, headers=headers)
    response.raise_for_status()
    return response.json()


def extract_data(players):
    players_data = []
    for player in players:  
        if player["team"]["internationalName"] in TEAMS_UCL_36: 
            key_stats_dict = {
                "id_player": player["player"].get("id"),
                "distance_covered(km/h)": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="distance_covered"), None),
                "top_speed": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="top_speed"), None),
                "minutes_played": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="minutes_played_official"), None),
                "matches_appareance": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="matches_appearance"), None)
            }
            players_data.append(key_stats_dict)    
    return players_data


def main():
    limit = 20
    offset = 20
    key_stats_data = []

    players = fetch_data(limit, offset)
    key_stats_data = extract_data(players)

    print(f"{len(key_stats_data)} elements extracted.")
    key_stats_data_df = pd.DataFrame(key_stats_data)
    print(key_stats_data_df)


if __name__ == "__main__":
    main()