import os
import requests
from dotenv import load_dotenv

load_dotenv()

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}

UEFA_API = os.getenv("UEFA_API")

response = requests.get(UEFA_API, headers=headers)

players = response.json()

for player in players:
    print(player["player"]["internationalName"])
    print(player["player"]["translations"]["countryName"]["EN"])
    print(player["player"]["translations"]["fieldPosition"]["EN"])
    print(player["player"]["translations"]["nationalFieldPosition"]["EN"])
    print(f"Team: {player["team"]["internationalName"]}")
    print(f"Minutes playerd: {player["statistics"][0]["value"]}")
    print(f"Matches appearance: {player["statistics"][1]["value"]}")
    print(f"Goals: {player["statistics"][2]["value"]}")
    print(f"Assists: {player["statistics"][3]["value"]}")
    print(f"Distance covered: {player["statistics"][4]["value"]}")
    print(f"Top speed: {player["statistics"][5]["value"]}")
    print()