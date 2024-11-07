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
    UEFA_API = f"https://compstats.uefa.com/v1/player-ranking?competitionId=1&limit={limit}&offset={offset}&optionalFields=PLAYER%2CTEAM&order=DESC&phase=TOURNAMENT&seasonYear=2025&stats=attempts_on_target%2Cattempts%2Cattempts_off_target%2Cattempts_blocked%2Cmatches_appearance"
    response = requests.get(UEFA_API, headers=headers)
    response.raise_for_status()
    return response.json()


def extract_data(players):
    players_attempts_data = []
    for player in players:  
        if player["team"]["internationalName"] in TEAMS_UCL_36: 
            goals_dict = {
                "id_player": player["player"].get("id"),
                "total_attempts": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="attempts"), None),
                "attempts_on_target": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="attempts_on_target"), None),
                "attempts_off_target": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="attempts_off_target"), None),   
                "blocked": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="attempts_blocked"), None),
            }
            players_attempts_data.append(goals_dict)    

    return players_attempts_data


def main():
    limit = 20
    offset = 0
    all_attempts_data = []

    players = fetch_data(limit, offset)
    all_attempts_data = extract_data(players)

    print(f"{len(all_attempts_data)} elements extracted.")
    players_df = pd.DataFrame(all_attempts_data)
    print(players_df)


if __name__ == "__main__":
    main()