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
    UEFA_API = f"https://compstats.uefa.com/v1/player-ranking?competitionId=1&limit={limit}&offset={offset}&optionalFields=PLAYER%2CTEAM&order=DESC&phase=TOURNAMENT&seasonYear=2025&stats=recovered_ball%2Ctackles%2Ctackles_won%2Ctackles_lost%2Cclearance_attempted%2Cmatches_appearance"
    response = requests.get(UEFA_API, headers=headers)
    response.raise_for_status()
    return response.json()


def extract_data(players):
    players_defending_data = []
    for player in players:  
        if player["team"]["internationalName"] in TEAMS_UCL_36: 
            defending_dict = {
                "id": player["player"].get("id"),
                "balls_recovered": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="recovered_ball"), None),   
                "tackles": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="tackles"), None),
                "tackles_won": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="tackles_won"), None),
                "tackles_lost": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="tackles_lost"), None),
                "clearance_attempted": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="clearance_attempted"), None),
            }
            players_defending_data.append(defending_dict)    

    return players_defending_data


def main():
    limit = 100
    offset = 0
    all_defending_data = []

    while True:
        players = fetch_data(limit, offset)
        if not players:
            break

        defending_data = extract_data(players)
        all_defending_data.extend(defending_data)

        print(f"Offset: {offset}")
        offset += limit

    print(f"{len(all_defending_data)} elements extracted.")
    defending_df = pd.DataFrame(all_defending_data)
    defending_df.to_csv(os.path.join('extraction','raw_data','players_defending_data.csv'))
    print("Data extracted!.")

if __name__ == "__main__":
    main()