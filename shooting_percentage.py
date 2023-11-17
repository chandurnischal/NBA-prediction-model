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
    select * from player_per_game order by year;
    '''

    cur.execute(query)
    
    column_names = [column[0] for column in cur.description]

    rows = cur.fetchall()

data = pd.DataFrame(rows, columns=column_names)


data['FGA_e'] = data['FGA'].replace(0,1)
data['FTA_e'] = data['FTA'].replace(0,1)
data['shooting_percenatge'] = data['PTS'].astype(float)/(data['FGA_e'].astype(float)*2*data['FTA_e'].astype(float)*2)


# offensive rating =  100*points/possession
#possession = FGA + 0.44*FTA + TOV
# data['TOV_e'] = data['TOV'].replace(0,0.001)

data['Offensive_rating'] = data['PTS'].astype(float) / ((data['FGA']).astype(float) + 0.44*data['FTA'].astype(float) + data['TOV'].astype(float))

data['EFF'] = data['PTS'].astype(float) + data['TRB'].astype(float) + data['AST'].astype(float) + data['STL'].astype(float) + data['BLK'].astype(float) - data['FGA'].astype(float) + data['FG'].astype(float) - data['FTA'].astype(float) + data['FT'].astype(float) - data['TOV'].astype(float)


data.to_csv('player_per_game_new.csv', index = False)

#dqv.apply(pd.to_numeric, errors = 'ignore')