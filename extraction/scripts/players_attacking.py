import os
import sys
import requests
import pandas as pd


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}


TEAMS_UCL_36 = ['Aston villa','Liverpool','Man City','Monaco','Brest','Leverkusen','Inter','Sporting CP',
'Arsenal','Barcelona','B. Dortmund','Real Madrid','Benfica','Juventus','Lille','Feyenoord','Atalanta',
'Stuttgart','Paris','Celtic','Sparta Praha', 'GNK Dinamo','Bayern München','Girona','Milan','Club Brugge',
'Atleti','PSV','Bologna','Shakhtar','Leipzig','Sturm Graz','Crvena Zvezda','Salzburg','Young Boys','S. Bratislava']


def fetch_data(limit, offset):
    UEFA_API = f"https://compstats.uefa.com/v1/player-ranking?competitionId=1&limit={limit}&offset={offset}&optionalFields=PLAYER%2CTEAM&order=DESC&phase=TOURNAMENT&seasonYear=2025&stats=assists%2Ccorners%2Coffsides%2Cdribbling%2Cmatches_appearance"
    response = requests.get(UEFA_API, headers=headers)
    response.raise_for_status()
    return response.json()


def extract_data(players):
    players_attacking_data = []
    for player in players:  
        if player["team"]["internationalName"] in TEAMS_UCL_36: 
            goals_dict = {
                "id_player": player["player"].get("id"),
                "assists": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="assists"), None),
                "corners_taken": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="corners"), None),
                "offsides": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="offsides"), None),
                "dribbles": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="dribbling"), None),   
            }
            players_attacking_data.append(goals_dict)    

    return players_attacking_data


def main(output_dir):
    limit = 100
    offset = 0
    all_attacking_data = []

    while True:
        players = fetch_data(limit, offset)
        if not players:
            break

        attacking_data = extract_data(players)
        all_attacking_data.extend(attacking_data)

        offset += limit

    print(f"{len(all_attacking_data)} elements extracted.")
    attacking_df = pd.DataFrame(all_attacking_data).set_index("id_player")
    attacking_df.to_csv(os.path.join('extraction','data','raw',output_dir,'attacking_data.csv'))
    print("Data extracted!.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
        main(output_dir)
    else:
        print("Error: output_dir argument is missing.")