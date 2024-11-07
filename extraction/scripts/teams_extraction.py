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


def extract_data(teams):
    teams_data = {}   
    for team in teams:  
        team_id = int(team["team"]["id"])
        if team_id not in teams_data: 
            teams_data[team_id] = {
                "team_id": int(team["team"].get("id")),
                "country": team["team"]["translations"]["countryName"].get("EN") if team["team"]["translations"].get("countryName") else None,
                "team": team["team"]["translations"]["displayOfficialName"].get("EN") if team["team"]["translations"].get("displayOfficialName") else None,
                "logo": team["team"].get("logoUrl")
            }    

    return list(teams_data.values())


def main(output_dir):   
    limit = 100
    offset = 0
    all_teams_data = []

    while True:
        teams = fetch_data(limit, offset)
        if not teams:
            break

        teams_data = extract_data(teams)
        all_teams_data.extend(teams_data)

        print(f"Offset: {offset}")
        offset += limit

    teams_df = pd.DataFrame(all_teams_data)
    teams_df.drop_duplicates("team_id", inplace=True)
    teams_df = teams_df.set_index("team_id")
    teams_df.to_csv(os.path.join('extraction','raw_data',output_dir,'teams_data.csv'))
    

if __name__ == "__main__":
    main()