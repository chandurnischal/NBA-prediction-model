import json
import utils as u
import pandas as pd
import matplotlib.pyplot as plt


def getTeamElo(teamID: int, data: pd.DataFrame) -> list:
    elo = []

    for _, row in data.iterrows():
        if row["home_fid"] == teamID:
            elo.append(row["home_elo"])
        elif row["visitor_fid"] == teamID:
            elo.append(row["visitor_elo"])

    return elo


def plotTeamElo(teamID: int) -> None:
    with open("creds.json") as file:
        creds = json.load(file)

    query = """
    select * from elo where (home_fid = {} or visitor_fid = {}) and season=2023 and is_regular=1
    """.format(
        teamID, teamID
    )

    data = u.sqlTodf(query, creds)

    elo = getTeamElo(teamID, data)
    teamName = data[data["home_id"] == teamID].iloc[-1]["home"]
    plt.plot(data["date"], elo, label=teamName)


def compareTeamElos(teamIDS: list) -> None:
    plt.figure(figsize=(15, 8))
    for teamID in teamIDS:
        plotTeamElo(teamID)

    plt.title("Team Elo Comparison Season 2023", fontdict={"size": 20})
    plt.legend()
    plt.axhline(y=1500, c="k")
    plt.xlabel('Date', fontdict={'size': 15})
    plt.ylabel('Elo', fontdict={'size': 15})
    plt.grid("--")
    # plt.show()
    plt.savefig('data/plots/elo.png')


ids = [6, 5, 12, 17]
# ids = [8, 6, 5, 16]
compareTeamElos(ids)