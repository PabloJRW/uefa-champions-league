import os
import requests
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

UEFA_API = os.getenv("UEFA_API")

response = requests.get(UEFA_API, headers=headers)

players = response.json()

players_list = []
for player in players:
    player_dict = {
        "id": player["player"]["id"],
        "playerName": player["player"]["internationalName"],
        "nationality": player["player"]["translations"]["countryName"]["EN"],
        "fieldPosition": player["player"]["translations"]["fieldPosition"]["EN"],
        #"position": player["player"]["detailedFieldPosition"],
       # "weight(kg)": str(player["player"]["weight"]),
       # "height(cm)": str(player["player"]["height"]),
        "age": player["player"]["age"],
        "team": player["team"]["internationalName"],
        "minutesPlayed": player["statistics"][0]["value"],
        "matchesAppareance": player["statistics"][1]["value"],
        "goals": player["statistics"][2]["value"],
        "assists": player["statistics"][3]["value"],
        "distanceCovered(km/h)": player["statistics"][4]["value"],
        "topSpeed": player["statistics"][5]["value"],
        }

    players_list.append(player_dict)

players_data = pd.DataFrame(players_list)
print(players_data)