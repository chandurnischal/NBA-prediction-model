import json
from sqlalchemy import create_engine
import extraction as e
from random import randint
from time import sleep
import pandas as pd
from tqdm import tqdm 


with open("creds.json") as file:
    creds = json.load(file)


engine = create_engine("mysql://{}:{}@{}/{}".format(creds["user"], creds["password"], creds["host"], creds["database"]))
player = e.Players("regular"), e.Players("playoffs")

team = e.Teams("regular"), e.Teams("playoffs")

games = e.Games()



years = creds["years"]


def playerTotalStats(year):
    
    output = []

    output.append(player[0].totalStats(year))

    sleep(randint(10, 20))

    output.append(player[1].totalStats(year))

    sleep(randint(10, 20))

    pd.concat(output).to_sql(name="player_total", index=False, con=engine, if_exists="append")


def playerPerGameStats(year):
    
    output = []

    output.append(player[0].perGameStats(year))

    sleep(randint(10, 20))

    output.append(player[1].perGameStats(year))

    sleep(randint(10, 20))

    pd.concat(output).to_sql(name="player_per_game", index=False, con=engine, if_exists="append")

def playerPerPossStats(year):
        
    output = []

    output.append(player[0].perPossessionStats(year))

    sleep(randint(10, 20))

    output.append(player[1].perPossessionStats(year))

    sleep(randint(10, 20))

    pd.concat(output).to_sql(name="player_per_possession", index=False, con=engine, if_exists="append")

def playerAdvancedStats(year):
        
    output = []

    output.append(player[0].advancedStats(year))

    sleep(randint(10, 20))

    output.append(player[1].advancedStats(year))

    sleep(randint(10, 20))

    pd.concat(output).to_sql(name="player_advanced", index=False, con=engine, if_exists="append")


def playerPerMinuteStats(year):

    output = []

    output.append(player[0].perMinuteStats(year))

    sleep(randint(10, 20))

    output.append(player[1].perMinuteStats(year))

    sleep(randint(10, 20))

    pd.concat(output).to_sql(name="player_per_minute", index=False, con=engine, if_exists="append")

def teamTotalStats(year):
        
    output = []

    output.append(team[0].totalStats(year))

    sleep(randint(10, 20))

    output.append(team[1].totalStats(year))

    sleep(randint(10, 20))

    pd.concat(output).to_sql(name="team_total", index=False, con=engine, if_exists="append")


def teamPerGameStats(year):
        
    output = []

    output.append(team[0].perGameStats(year))

    sleep(randint(10, 20))

    output.append(team[1].perGameStats(year))

    sleep(randint(10, 20))

    pd.concat(output).to_sql(name="team_per_game", index=False, con=engine, if_exists="append")

def teamPerPossessionStats(year):
    output = []

    output.append(team[0].perPossStats(year))

    sleep(randint(10, 20))

    output.append(team[1].perPossStats(year))

    sleep(randint(10, 20))

    pd.concat(output).to_sql(name="team_per_possession", index=False, con=engine, if_exists="append")



def gamesSchedule(year):
    games.seasonSchedule(year).to_sql(name="games", index=False, con=engine, if_exists="append")
    sleep(randint(10, 20))

for year in tqdm(range(*years)):
    try:
        playerTotalStats(year)

        playerPerGameStats(year)

        playerPerMinuteStats(year)

        playerPerPossStats(year)

        playerAdvancedStats(year)

        teamPerGameStats(year)

        teamPerPossessionStats(year)

        teamTotalStats(year)

        gamesSchedule(year)


    except Exception as e:
        print(year, e.__class__)