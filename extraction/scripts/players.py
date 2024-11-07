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
            player_dict = {
                "id_player": player["player"].get("id"),
                "player_name": player["player"].get("internationalName"),
                "nationality": player["player"]["translations"]["countryName"].get("EN") if player["player"]["translations"].get("countryName") else None,
                "field_position": player["player"]["translations"]["fieldPosition"].get("EN") if player["player"]["translations"].get("fieldPosition") else None,
                "position": player["player"].get("detailedFieldPosition"),
                "weight(kg)": player["player"].get("weight"),
                "height(cm)": player["player"].get("height"),
                "age": player["player"].get("age"),
                "id_team": player["team"].get("id"),
                "player_image": player["player"].get("imageUrl")
            }
            players_data.append(player_dict)    

    return players_data


def main():
    limit = 100
    offset = 0
    all_players_data = []

    while True:
        players = fetch_data(limit, offset)
        if not players:
            break

        players_data = extract_data(players)
        all_players_data.extend(players_data)

        print(f"Offset: {offset}")
        offset += limit

    print(f"{len(all_players_data)} elements extracted.")
    players_df = pd.DataFrame(all_players_data, index="id_player")
    players_df.to_csv(os.path.join('extraction','raw_data','players_data.csv'))
    print("Data extracted!.")

if __name__ == "__main__":
    main()