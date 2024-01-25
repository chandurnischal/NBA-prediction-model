import sys

sys.path.append("extraction")
import extraction as e
import json
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import requests


def pushToDatabase(data: pd.DataFrame, tablename, engine) -> None:
    try:
        data.to_sql(tablename, con=engine, if_exists="append", index=False)
    except:
        pass


def totalStats(player, team: e.Teams, year: int, engine) -> None:
    print("Extracting Total Stats...")
    regularPlayer = player[0].totalStats(year)

    playoffsPlayer = player[1].totalStats(year)

    regularTeam = team[0].totalStats(year)

    playoffsTeam = team[1].totalStats(year)

    pushToDatabase(regularPlayer, "player_total", engine)
    pushToDatabase(playoffsPlayer, "player_total", engine)
    pushToDatabase(regularTeam, "team_total", engine)
    pushToDatabase(playoffsTeam, "team_total", engine)


def perGameStats(player, team: e.Teams, year: int, engine) -> None:
    print("Extracting Per Game Stats...")
    regularPlayer = player[0].perGameStats(year)

    playoffsPlayer = player[1].perGameStats(year)

    regularTeam = team[0].perGameStats(year)

    playoffsTeam = team[1].perGameStats(year)

    pushToDatabase(regularPlayer, "player_per_game", engine)
    pushToDatabase(playoffsPlayer, "player_per_game", engine)
    pushToDatabase(regularTeam, "team_per_game", engine)
    pushToDatabase(playoffsTeam, "team_per_game", engine)


def perMinuteStats(player, year: int, engine) -> None:
    print("Extracting Per Minute Stats...")
    regularPlayer = player[0].perMinuteStats(year)

    playoffsPlayer = player[1].perMinuteStats(year)

    pushToDatabase(regularPlayer, "player_per_minute", engine)
    pushToDatabase(playoffsPlayer, "player_per_minute", engine)


def perPossessionStats(player, year: int, engine) -> None:
    print("Extracting Per Possession Stats...")
    regularPlayer = player[0].perPossessionStats(year)

    playoffsPlayer = player[1].perPossessionStats(year)

    regularTeam = team[0].perPossStats(year)

    playoffsTeam = team[1].perPossStats(year)

    pushToDatabase(regularPlayer, "player_per_possession", engine)
    pushToDatabase(playoffsPlayer, "player_per_possession", engine)
    pushToDatabase(regularTeam, "team_per_possession", engine)
    pushToDatabase(playoffsTeam, "team_per_possession", engine)


def advancedStats(player, year: int, engine) -> None:
    print("Extracting Advanced Stats...")
    regularPlayer = player[0].advancedStats(year)

    playoffsPlayer = player[1].advancedStats(year)

    pushToDatabase(regularPlayer, "player_advanced", engine)
    pushToDatabase(playoffsPlayer, "player_advanced", engine)


with open("creds.json") as file:
    creds = json.load(file)

engine = create_engine(
    "mysql+mysqlconnector://{}:{}@{}/{}".format(
        creds["user"], creds["password"], creds["host"], creds["database"]
    )
)

games = e.Games()
currentSeason = datetime.now().year + 1

url = """https://www.basketball-reference.com/leagues/NBA_{}.html""".format(
    currentSeason
)

r = requests.get(url)

if r.status_code != 200:
    currentSeason = currentSeason - 1


player = e.Players("regular"), e.Players("playoffs")
team = e.Teams("regular"), e.Teams("playoffs")


currentSchedule = games.seasonSchedule(currentSeason)
pushToDatabase(currentSchedule, "games", engine)

print("Extracting Playoffs schedule...")
games.playoffsDates((1980, currentSeason)).to_sql(
    "playoffs_dates", index=False, con=engine, if_exists="replace"
)


print("Extracting Conference Standings...")
pushToDatabase(
    team[0].conferenceStandings(currentSeason), "conference_standings", engine
)


totalStats(player, team, currentSeason, engine)
perGameStats(player, team, currentSeason, engine)
perMinuteStats(player, currentSeason, engine)
perPossessionStats(player, currentSeason, engine)
advancedStats(player, currentSeason, engine)
