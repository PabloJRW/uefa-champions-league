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
    UEFA_API = f"https://compstats.uefa.com/v1/player-ranking?competitionId=1&limit={limit}&offset={offset}&optionalFields=PLAYER%2CTEAM&order=DESC&phase=TOURNAMENT&seasonYear=2025&stats=saves%2Cgoals_conceded%2Csaves_on_penalty%2Cclean_sheet%2Cpunches%2Cmatches_appearance"
    response = requests.get(UEFA_API, headers=headers)
    response.raise_for_status()
    return response.json()


def extract_data(players):
    players_goalkeeping_data = []
    for player in players:  
        if player["team"]["internationalName"] in TEAMS_UCL_36: 
            goalkeep_dict = {
                "id_player": player["player"].get("id"),
                "saves": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="saves"), None),
                "goals_conceded": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="goals_conceded"), None),
                "saves_on_penalty": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="saves_on_penalty"), None),
                "clean_sheets": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="clean_sheet"), None),
                "punches_made": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="punches"), None),   
            }
            players_goalkeeping_data.append(goalkeep_dict)    

    return players_goalkeeping_data


def main():
    limit = 100
    offset = 0
    all_goalkeeping_data = []

    while True:
        players = fetch_data(limit, offset)
        if not players:
            break

        players_data = extract_data(players)
        all_goalkeeping_data.extend(players_data)

        print(f"Offset: {offset}")
        offset += limit

    print(f"{len(all_goalkeeping_data)} elements extracted.")
    goalkeeping_df = pd.DataFrame(all_goalkeeping_data)
    goalkeeping_df.to_csv(os.path.join('extraction','raw_data','goalkeeping_data.csv'))
    print("Data extracted!.")


if __name__ == "__main__":
    main()