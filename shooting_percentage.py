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
print(data)



