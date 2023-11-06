import mysql.connector as mc
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

creds = {
    "host": "localhost", 
    "password": "ChatGPT132!",
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
# print(data)


# def total_home_win_percentage(x):
#     N = 40
#     home_wins = 0
#     home_losses = 0
#     total = 0
#     for i in range(N):
#         HomeGames = data[(data["home_id"] == int(x)) & (data["visitor_id"] == i+1) & data["visitor_id"] != data['home_id']]

#         # total += len(HomeGames)
#         home_wins += len(HomeGames[HomeGames["home_victory"] == 1])
#         home_losses += len(HomeGames[HomeGames["home_victory"] == 0])
#     home_win_percentage = home_wins / (home_wins + home_losses)
#     return home_win_percentage

# y = input("Enter home team ID:")
# home_team_adv = total_home_win_percentage(y)
# print(home_team_adv)


def home_win_vs_vistor(a,b):
    HomeGames = data[(data["home_id"] == int(a)) & (data["visitor_id"] == int(b))]
    HomeW = len(HomeGames[HomeGames["home_victory"] == 1])
    HomeL = len(HomeGames[HomeGames["home_victory"] == 0])
    print(HomeW, HomeL)
    home_adv = HomeW / (HomeL + HomeW)
    return home_adv

a = input('Enter home team ID: \n')
b = input('Enter vistor team ID: \n')
home_team_adv = home_win_vs_vistor(a,b)
print(home_team_adv)


# HomeGames = data[(data["home_id"] == int(a)) & (data["visitor_id"] == int(b))]
# HomeW = len(HomeGames[HomeGames["home_victory"] == 1])
# HomeL = len(HomeGames[HomeGames["home_victory"] == 0])
# print(HomeW, HomeL)