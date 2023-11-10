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

    cur.execute(query)
    
    column_names = [column[0] for column in cur.description]

    rows = cur.fetchall()

data = pd.DataFrame(rows, columns=column_names)


#elo 
elo_ratings = {team: 1500 for team in set(data['home']) | set(data['visitor'])}

elo_list = []
home_elo = []
visitor_elo = []

for index, row in data.iterrows():

    E_home = 1/(1+10 ** ((away_elo - home_elo)/400))
    E_away = 1 - E_home

    S_home = 1 if home_score > away_score else 0

    k = 20 * ((abs(rows['mov'])))

    elo_change_home = k*(home_result - E_home)



