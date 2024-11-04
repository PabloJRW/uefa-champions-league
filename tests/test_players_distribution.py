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
    UEFA_API = f"https://compstats.uefa.com/v1/player-ranking?competitionId=1&limit={limit}&offset={offset}&optionalFields=PLAYER%2CTEAM&order=DESC&phase=TOURNAMENT&seasonYear=2025&stats=passes_accuracy%2Cpasses_attempted%2Cpasses_completed%2Ccross_accuracy%2Ccross_attempted%2Ccross_completed%2Cfree_kick%2Cmatches_appearance"
    response = requests.get(UEFA_API, headers=headers)
    response.raise_for_status()
    return response.json()


def extract_data(players):
    players_distribution_data = []
    
    for player in players:  
        if player["team"]["internationalName"] in TEAMS_UCL_36: 
            distribution_dict = {
                "id": player["player"].get("id"),
                "passes_accuracy": player["statistics"][0]["value"],   
                "passes_attempted": player["statistics"][1]["value"],
                "passes_completed": player["statistics"][2]["value"],
                "cross_accuracy": player["statistics"][3]["value"],
                "cross_attempted": player["statistics"][4]["value"],
                "cross_completed": player["statistics"][5]["value"],
                "free_kick": player["statistics"][6]["value"],
                "matches_appearance": player["statistics"][7]["value"],
            }
            players_distribution_data.append(distribution_dict)    

    return players_distribution_data


def main():
    limit = 20
    offset = 20
    all_players_data = []

    players = fetch_data(limit, offset)
    all_players_data = extract_data(players)

    print(f"{len(all_players_data)} elements extracted.")
    players_df = pd.DataFrame(all_players_data)
    print(players_df)

if __name__ == "__main__":
    main()