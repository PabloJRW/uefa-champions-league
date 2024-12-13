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
    UEFA_API = f"https://compstats.uefa.com/v1/player-ranking?competitionId=1&limit={limit}&offset={offset}&optionalFields=PLAYER%2CTEAM&order=DESC&phase=TOURNAMENT&seasonYear=2025&stats=passes_accuracy%2Cpasses_attempted%2Cpasses_completed%2Ccross_accuracy%2Ccross_attempted%2Ccross_completed%2Cfree_kick%2Cmatches_appearance"
    response = requests.get(UEFA_API, headers=headers)
    response.raise_for_status()
    return response.json()


def extract_data(players):
    players_distribution_data = []
    for player in players:  
        if player["team"]["internationalName"] in TEAMS_UCL_36: 
            distribution_dict = {
                "id_player": player["player"].get("id"),
                "passing_accuracy(%)": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="passes_accuracy"), None),   
                "passes_attempted": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="passes_attempted"), None),
                "passes_completed": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="passes_completed"), None),
                "crossing_accuracy(%)": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="cross_accuracy"), None),
                "crosses_attempted": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="cross_attempted"), None),
                "crosses_completed": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="cross_completed"), None),
                "free_kick_taken": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="free_kick"), None),
                "matches_appearance": next((stat.get("value") for stat in player["statistics"] if stat.get("name")=="matches_appearance"), None),
            }
            players_distribution_data.append(distribution_dict)    

    return players_distribution_data

def main(output_dir):
    limit = 100
    offset = 0
    all_distribution_data = []

    while True:
        players = fetch_data(limit, offset)
        if not players:
            break

        distribution_data = extract_data(players)
        all_distribution_data.extend(distribution_data)

        offset += limit

    print(f"{len(all_distribution_data)} elements extracted.")
    distribution_df = pd.DataFrame(all_distribution_data).set_index("id_player")
    distribution_df.to_csv(os.path.join('extraction','data','raw',output_dir,'distribution_data.csv'))
    print("Data extracted!.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
        main(output_dir)
    else:
        print("Error: output_dir argument is missing.")