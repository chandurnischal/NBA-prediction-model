import sys
sys.path.append('extraction')
import extraction as e
import json
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from time import sleep
from random import randint
import subprocess

def pushToDatabase(data:pd.DataFrame, tablename, engine) -> None:
    try:
        data.to_sql(tablename, con=engine, if_exists="append", index=False)
    except:
        pass

def totalStats(player, team:e.Teams, year:int, engine) -> None:
    print("Extracting Total Stats...\n")
    regularPlayer = player[0].totalStats(year)
    sleep(randint(5, 10))
    playoffsPlayer = player[1].totalStats(year)
    sleep(randint(5, 10))
    regularTeam = team[0].totalStats(year)
    sleep(randint(5, 10))
    playoffsTeam = team[1].totalStats(year)
    sleep(randint(5, 10))

    pushToDatabase(regularPlayer, "player_total", engine)
    pushToDatabase(playoffsPlayer, "player_total", engine)
    pushToDatabase(regularTeam, "team_total", engine)
    pushToDatabase(playoffsTeam, "team_total", engine)

def perGameStats(player, team:e.Teams, year:int, engine) -> None:
    print("Extracting Per Game Stats...\n")
    regularPlayer = player[0].perGameStats(year)
    sleep(randint(5, 10))

    playoffsPlayer = player[1].perGameStats(year)
    sleep(randint(5, 10))

    regularTeam = team[0].perGameStats(year)
    sleep(randint(5, 10))

    playoffsTeam = team[1].perGameStats(year)
    sleep(randint(5, 10))

    pushToDatabase(regularPlayer, "player_per_game", engine)
    pushToDatabase(playoffsPlayer, "player_per_game", engine)
    pushToDatabase(regularTeam, "team_per_game", engine)
    pushToDatabase(playoffsTeam, "team_per_game", engine)

def perMinuteStats(player, year:int, engine) -> None:
    print("Extracting Per Minute Stats...\n")
    regularPlayer = player[0].perMinuteStats(year)
    sleep(randint(5, 10))

    playoffsPlayer = player[1].perMinuteStats(year)
    sleep(randint(5, 10))

    pushToDatabase(regularPlayer, "player_per_minute", engine)
    pushToDatabase(playoffsPlayer, "player_per_minute", engine)

def perPossessionStats(player, year:int, engine) -> None:
    print("Extracting Per Possession Stats...\n")
    regularPlayer = player[0].perPossessionStats(year)
    sleep(randint(5, 10))

    playoffsPlayer = player[1].perPossessionStats(year)
    sleep(randint(5, 10))

    regularTeam = team[0].perPossStats(year)
    sleep(randint(5, 10))

    playoffsTeam = team[1].perPossStats(year)
    sleep(randint(5, 10))

    pushToDatabase(regularPlayer, "player_per_possesion", engine)
    pushToDatabase(playoffsPlayer, "player_per_possession", engine)
    pushToDatabase(regularTeam, "team_per_possession", engine)
    pushToDatabase(playoffsTeam, "team_per_possession", engine)

def advancedStats(player, year:int, engine) -> None:
    print("Extracting Advanced Stats...\n")
    regularPlayer = player[0].advancedStats(year)
    sleep(randint(5, 10))
    playoffsPlayer = player[1].advancedStats(year)
    sleep(randint(5, 10))

    pushToDatabase(regularPlayer, "player_advanced", engine)
    pushToDatabase(playoffsPlayer, "player_advanced", engine)    

with open("creds.json") as file:
    creds = json.load(file)

engine = create_engine("mysql://{}:{}@{}/{}".format(creds["user"], creds["password"], creds["host"], creds["database"]))

games = e.Games()
currentYear = datetime.now().year + 1


player = e.Players("regular"), e.Players("playoffs")
team = e.Teams("regular"), e.Teams("playoffs")


print("Extracting Games schedule...\n")
currentSchedule = games.seasonSchedule(currentYear)
currentSchedule = currentSchedule[currentSchedule['VPoints'] != '']
pushToDatabase(currentSchedule, "games", engine)

# with open("data/latest.sql", 'w') as output:
#     c = subprocess.Popen(['mysqldump', '-u', creds['user'], '-p', creds['database']], stdout=output, stdin=creds['password'], shell=True)

print("Extracting playoffs schedule...\n")
games.playoffsDates((1980, currentYear)).to_sql("playoffs_dates", index = False, con=engine, if_exists = "replace")
sleep(randint(5, 10))

print("Extracting Conference Standings...\n")
pushToDatabase(team[0].conferenceStandings(currentYear), "conference_standings", engine)
sleep(randint(5, 10))

totalStats(player, team, currentYear, engine)
perGameStats(player, team, currentYear, engine)
perMinuteStats(player, currentYear, engine)
perPossessionStats(player, currentYear, engine)
advancedStats(player, currentYear, engine)