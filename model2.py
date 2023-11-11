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

    query = '''
    select * from games;
    '''
#where date between '2019-01-01' and '2022-01-01
    cur.execute(query)
    
    column_names = [column[0] for column in cur.description]

    rows = cur.fetchall()

data = pd.DataFrame(rows, columns=column_names)
data.columns = [c.lower() for c in data.columns.to_list()]



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


data.to_csv('winper_dataframe.csv', index = False)




    






