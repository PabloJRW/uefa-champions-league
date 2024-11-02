import os
import requests
from dotenv import load_dotenv
import pandas as pd


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

offset = 10
TEAMS_UCL_36 = ['Aston villa','Liverpool','Man City','Monaco','Brest','Leverkusen','Inter','Sporting CP',
'Arsenal','Barcelona','B. Dortmund','Real Madrid','Benfica','Juventus','Lille','Feyenoord','Atalanta',
'Stuttgart','Paris','Celtic','Sparta Praha', 'GNK Dinamo','Bayern München','Girona','Milan','Club Brugge',
'Atleti','PSV','Bologna','Shakhtar','Leipzig','Sturm Graz','Crvena Zvezda','Salzburg','Young Boys','S. Bratislava']


def fetch_data(offset):
    UEFA_API = f"https://compstats.uefa.com/v1/player-ranking?competitionId=1&limit=10&offset={offset}&optionalFields=PLAYER%2CTEAM&order=DESC&phase=TOURNAMENT&seasonYear=2025&stats=minutes_played_official%2Cmatches_appearance%2Cgoals%2Cassists%2Cdistance_covered%2Ctop_speed"
    response = requests.get(UEFA_API, headers=headers)
    response.raise_for_status()
    return response.json()


def extract_data(players):
    players_list = []
    
    for player in players:  
        if player["team"]["internationalName"] in TEAMS_UCL_36: 
            player_dict = {
                "id": player["player"]["id"],
                "player_name": player["player"]["internationalName"],
                "nationality": player["player"]["translations"]["countryName"]["EN"],
                "field_position": player["player"]["translations"]["fieldPosition"]["EN"],
                "position": player["player"].get("detailedFieldPosition"),
                "weight(kg)": player["player"].get("weight"),
                "height(cm)": player["player"].get("height"),
                "age": player["player"]["age"],
                "team_id": player["team"]["id"],
                "minutes_played": player["statistics"][0]["value"],
                "matches_appareance": player["statistics"][1]["value"],
                "goals": player["statistics"][2]["value"],
                "assists": player["statistics"][3]["value"],
                "distance_covered(km/h)": player["statistics"][4]["value"],
                "top_speed": player["statistics"][5]["value"],
                "player_image": player["player"]["imageUrl"]
            }
            players_list.append(player_dict)    

    return players_list

def main():
    offset = 10
    all_players = []
    all_teams = {}

    while True:
        # Obtener datos de jugadores desde la API
        players = fetch_data(offset)

        for player in players:
            
            # Si no hay jugadores, finalizamos la extracción
            if not player:
                print("No hay más datos para extraer.")
                break
            
            # Extraer y procesar datos
            players_data = extract_data(players)
            all_players.extend(players_data)
            

        # Incrementar el offset para la siguiente página
        offset += offset

        # Convertir a DataFrames si es necesario
        df_players = pd.DataFrame(all_players)


    # Aquí puedes cargar los DataFrames en una base de datos o guardarlos como archivos
    print("Extracción completa. Total de jugadores:", len(df_players))
        

if __name__ == "__main__":
    main()