import json
import utils as u
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm 

def PER(row) -> float:
    return (
        row["fg"] * 85.91
        + row["stl"] * 53.897
        + row["3p"] * 51.757
        + row["ft"] * 46.845
        + row["blk"] * 39.19
        + row["orb"] * 39.19
        + row["ast"] * 34.677
        + row["drb"] * 14.707
        - row["pf"] * 17.174
        - (row["fta"] - row["ft"]) * 20.091
        - (row["fga"] - row["fg"]) * 39.190
        - row["tov"] * 53.897
    ) * (1 / row["mp"])

def plotPER(playerID):

    query = '''
    select * from player_total where player_id = {} and is_regular=1 order by year
    '''.format(playerID)

    data = u.sqlTodf(query, creds).apply(pd.to_numeric, errors="ignore")
    data.columns = [column.lower() for column in data.columns]

    name = data[data['player_id'] == playerID]['player'].iloc[0].replace('*', '')

    startYear = data['year'].min()
    endYear = data['year'].max()


    data['per'] = PER(data)

    plt.figure(figsize=(15, 8))
    plt.title('Player Efficiency Rating of {} ({}-{})'.format(name, startYear, endYear), fontdict={"size": 20})
    plt.xlabel('Year', fontdict={'size': 15})
    plt.ylabel('Player Efficiency Rating', fontdict={'size': 15})

    plt.grid(linestyle='--')
    plt.plot(data['year'], data['per'])
    plt.xticks(data['year'])
    plt.savefig('data/plots/{}.png'.format(playerID))
    plt.show()

with open('creds.json') as file:
    creds = json.load(file)

playerIDS = [222, 100, 125, 569, 177, 692, 420, 324, 475, 405, 2238]

# playerIDS = [222]


for playerID in tqdm(playerIDS):
    plotPER(playerID)

