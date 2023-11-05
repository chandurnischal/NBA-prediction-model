import mysql.connector as mc
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

creds = {
    "host": "localhost", 
    "password": "ChatGPT132!",
    "user": "root",
    "database": "nba_r"
}


with mc.connect(**creds) as conn:
    cur = conn.cursor()

    query = '''
    select team_id, fg, year from team_per_game order by year, team_id;
    '''

    cur.execute(query)
    
    column_names = [column[0] for column in cur.description]

    rows = cur.fetchall()

data = pd.DataFrame(rows, columns=column_names)
# print(data)
# sumFG = data.groupby("team_id")
# print(sumFG)

mask = (data['year'] <= 2021)
training_data = data[mask]
print('training data is \n')
print(training_data)

testing_data = data[data['year'] > 2021]
print('testing data is \n')
print(testing_data)
