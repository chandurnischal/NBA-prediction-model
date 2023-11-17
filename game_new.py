import mysql.connector as mc
import pandas as pd
import numpy as np 
from sqlalchemy import create_engine

creds = {
    "host": "localhost", 
    "password": "Chatgpt132",
    "user": "root",
    "database": "nba"
}


with mc.connect(**creds) as conn:
    cur = conn.cursor()

    query = '''select * from games order by year(date)'''

    cur.execute(query)

    column_names = [column[0] for column in cur.description]
    rows = cur.fetchall()

data = pd.DataFrame(rows, columns = column_names)
data.columns = [c.lower() for c in data.columns.to_list()]

elo_ratings = {team: 1500 for team in set(data['home']) | set(data['visitor'])}

# elo_list = []
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
    
    home_score = 1 if row['hpoints'] > row['vpoints'] else 0
    away_score = 1 - home_score
    
    new_home_elo = round(home_elo + k * (home_score - E_home), 2)
    new_away_elo = round(away_elo + k * (away_score - E_away), 2)

    elo_ratings[home] = new_home_elo
    elo_ratings[visitor] = new_away_elo
    
    home_elo_list.append(new_home_elo)
    visitor_elo_list.append(new_away_elo)

data['home_elo'] = home_elo_list
data['visitor_elo'] = visitor_elo_list

# engine = create_engine('mysql://{}/{}@{}/{}'.format(creds['user'], creds['password'], creds['host'], creds['database']))

# data.to_sql(name = "games_elo", con = engine, index = False, if_exists = 'append')

win_per = {team: 0 for team in set(data['home']) | set(data['visitor'])}


home_win_list = []
visitor_win_list = []
 
for index, row in data.iterrows():
    home = row['home']
    visitor = row['visitor']

    home_win = win_per[home]
    away_win = win_per[visitor]

    W_home = 1 if row['mov'] > 0 else 0
    W_away = 1 - W_home   

    total_home_win = home_win + W_home
    total_away_win = away_win + W_away 

    home_per = total_home_win / (total_home_win + total_away_win)
    away_per = total_away_win / (total_home_win + total_away_win)

    win_per[home] = home_per
    win_per[visitor] = away_per

    home_win_list.append(home_per)
    visitor_win_list.append(away_per)

data['home_win_percentage'] = home_win_list
data['visitor_win_percentage'] = visitor_win_list

print(data)
