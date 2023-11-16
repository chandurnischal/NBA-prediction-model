import json
import pandas as pd
import utils as u

with open("./creds.json") as file:
    creds = json.load(file)

teamIDS = 2, 11
year = 2020


playerQuery = '''
select * from player_efficiency where team_id in ({}, {}) and year = {} and is_regular = 0 order by team_id, eff desc
'''.format(*teamIDS, year)

player = u.sqlTodf(playerQuery, creds)
columns = player.columns.to_list()
playerAverage = player.groupby('team_id').head(10)
playerAverage = playerAverage.groupby('team_id')['PER'].mean()

print(playerAverage)
