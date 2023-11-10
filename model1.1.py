import mysql.connector as mc
import pandas as pd
import numpy as np 

creds = {
    "host": "localhost", 
    "password": "Chatgpt132",
    "user": "root",
    "database": "nba"
}


with mc.connect(**creds) as conn:
    cur = conn.cursor()

    query = '''select * from games;'''

    cur.execute(query)

    column_names = [column[0] for column in cur.description]
    rows = cur.fetchall()

data = pd.DataFrame(rows, columns = column_names)
data.columns = [c.lower() for c in data.columns.to_list()]

elo_ratings = {team: 1500 for team in set(data['home']) | set(data['visitor'])}

elo_list = []
home_elo_list = []
visitor_elo_list = []

for index, row in data.iterrows():
    home = row['home']
    visitor = row['visitor']

    home_elo = elo_ratings[home]
    away_elo = elo_ratings[visitor]

    E_home = 1 / (1+ 10 ** ((away_elo - home_elo) / 400))
    E_away = 1 - E_home

    k = 20 * ((abs(row['mov']) + 3) ** 0.8) / (7.5 + 0.006 * (abs(home_elo - away_elo)))
    
    home_score = 1 if row['hpoints'] > row['vpoints'] else 0.5
    away_score = 1 - home_score
    
    new_home_elo = round(home_elo + k * (home_score - E_home), 2)
    new_away_elo = round(away_elo + k * (away_score - E_away), 2)

    elo_ratings[home] = new_home_elo
    elo_ratings[visitor] = new_away_elo
    
    home_elo_list.append(new_home_elo)
    visitor_elo_list.append(new_away_elo)

data['home_elo'] = home_elo_list
data['visitor_elo'] = visitor_elo_list

print(data)

