import mysql.connector as mc
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

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

col_label = ['team_id', 'FG_avg']

training_data = data[data['year'] <= 2021]
training_data = training_data.drop(['year'], axis=1)
training_data = training_data.groupby('team_id')['fg'].mean().to_frame()
print('training data is \n')
print(training_data)


testing_data = data[data['year'] > 2021]
testing_data = testing_data.drop(['year'], axis=1)
testing_data = testing_data.groupby('team_id')['fg'].mean().to_frame
print('testing data is \n')
print(testing_data)


