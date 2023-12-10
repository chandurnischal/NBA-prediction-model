import json
import pandas as pd
import utils as u
import numpy as np
import matplotlib.pyplot as plt

def getElo(teamID:int, data:pd.DataFrame) -> dict:
    data = data[(data['home_id'] == teamID) | (data['visitor_id'] == teamID)]

    elo = dict()

    for _, row in data.iterrows():
        if row['home_id'] == teamID:
            elo[row['date']] = row['home_elo']
        if row['visitor_id'] == teamID:
            elo[row['date']] = row['visitor_elo']

    return elo

with open('creds.json') as file:
    creds = json.load(file)

query = '''
select date, home_id, home, visitor_id, visitor, home_elo, visitor_elo from elo
'''

data = u.sqlTodf(query, creds)

teamIDs = [7, 4, 11, 2]
teamNames = [data[data['home_id'] == teamID].iloc[0]['home'] for teamID in teamIDs]

elos = [getElo(teamID, data) for teamID in teamIDs]

plt.figure()

for i, elo in enumerate(elos):
    plt.plot(elo.keys(), elo.values(), label = teamNames[i])

plt.legend()
plt.grid()
plt.show()