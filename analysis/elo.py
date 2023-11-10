import pandas as pd
import json
import utils as u


with open("creds.json") as file:
    creds = json.load(file)


query = '''
select home_id, home, visitor_id, visitor, hpoints, vpoints, mov from games where year(date) >= 2010;
'''

data = u.sqlTodf(query, creds)
data.columns = [c.lower() for c in data.columns.to_list()]


elo_ratings = {team: 1500 for team in set(data['home']) | set(data['visitor'])}


elo_list = []
homeEloList = []
visitorEloList = []

for index, row in data.iterrows():
    home = row['home']
    visitor = row['visitor']
    home_elo = elo_ratings[home]
    away_elo = elo_ratings[visitor]

    expected_home_win = 1 / (1 + 10**((away_elo - home_elo) / 400))
    expected_away_win = 1 / (1 + 10**((home_elo - away_elo) / 400))

    k = 20 * ((abs(row['mov']) + 3) ** 0.8) / (7.5 + 0.006 * (abs(home_elo - away_elo)))
    home_score = 1 if row['hpoints'] > row['vpoints'] else 0.5
    away_score = 1 - home_score
    new_home_elo = round(home_elo + k * (home_score - expected_home_win), 2)
    new_away_elo = round(away_elo + k * (away_score - expected_away_win), 2)

    elo_ratings[home] = new_home_elo
    elo_ratings[visitor] = new_away_elo
    homeEloList.append(new_home_elo)
    visitorEloList.append(new_away_elo)

data['home_elo'] = homeEloList
data['visitor_elo'] = visitorEloList

print(data)
