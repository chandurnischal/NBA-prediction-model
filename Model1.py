import mysql.connector as mc
import pandas as pd
import numpy as np
import math

creds = {
    "host": "localhost", 
    "password": "Chatgpt132",
    "user": "root",
    "database": "nba"
}


with mc.connect(**creds) as conn:
    cur = conn.cursor()

    query = '''
    select * from games;
    '''

    cur.execute(query)
    
    column_names = [column[0] for column in cur.description]

    rows = cur.fetchall()

data = pd.DataFrame(rows, columns=column_names)
data.columns = [c.lower() for c in data.columns.to_list()]

#elo 
elo_ratings = {team: 1500 for team in set(data['home']) | set(data['visitor'])}

elo_list = []
home_elo_list = []
visitor_elo_list = []

for index, row in data.iterrows():
    home = row['home']
    visitor = row['visitor']
    home_elo = elo_ratings[home]
    away_elo = elo_ratings[visitor]

    E_home = 1 / (1 + 10 ** ((away_elo - home_elo) / 400))
    E_away = 1 - E_home

    k = 20 * ((abs(row['mov']) + 3) ** 0.8) / (7.5 +0.006 * (abs(home_elo - away_elo)))

    S_home = 1 if row['hpoints'] > row['vpoints'] else 0.5
    S_away = 1 - S_home

    home_elo_new = round(k * (S_home - E_home + home_elo), 2)
    away_elo_new = round(k * (S_away - E_away + away_elo), 2)

    elo_ratings[home] = home_elo_new
    elo_ratings[visitor] = away_elo_new

    home_elo_list.append(home_elo_new)
    visitor_elo_list.append(away_elo_new)

data['home_elo'] = home_elo_list
data['visitor_elo'] = visitor_elo_list

print(data)






    
    
    
    
    

    




