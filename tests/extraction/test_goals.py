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
    UEFA_API = f"https://compstats.uefa.com/v1/player-ranking?competitionId=1&limit={limit}&offset={offset}&optionalFields=PLAYER%2CTEAM&order=DESC&phase=TOURNAMENT&seasonYear=2025&stats=goals_scored_outside_penalty_area%2Cgoals%2Cgoals_scored_with_right%2Cgoals_scored_with_left%2Cgoals_scored_head%2Cgoals_scored_other%2Cgoals_scored_inside_penalty_area%2Cpenalty_scored%2Cmatches_appearance"
    response = requests.get(UEFA_API, headers=headers)
    response.raise_for_status()
    return response.json()


def extract_data(players):
    players_goals_data = []
    for player in players:  
        if player["team"]["internationalName"] in TEAMS_UCL_36: 
            goals_dict = {
                "id_player": player["player"].get("id"),
                "goals": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="goals"), None),
                "inside_area": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="goals_scored_inside_penalty_area"), None),
                "outside_area": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="goals_scored_outside_penalty_area"), None),   
                "right_foot": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="goals_scored_with_right"), None),
                "left_foot": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="goals_scored_with_left"), None),
                "head": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="goals_scored_head"), None),
                "other": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="goals_scored_other"), None),
                "penalties_scored": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="penalty_scored"), None),
            }
            players_goals_data.append(goals_dict)    

    return players_goals_data


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