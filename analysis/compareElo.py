import json
import utils as u
import pandas as pd
import matplotlib.pyplot as plt


def getFranchiseElo(franchiseID:int, data:pd.DataFrame) -> list:
    elo = []

    for _, row in data.iterrows():
        if row['home_fid'] == franchiseID:
            elo.append(row['home_elo'])
        elif row['visitor_fid'] == franchiseID:
            elo.append(row['visitor_elo'])

    return elo

def plotFranchiseElo(franchiseID:int) -> None:

    with open("creds.json") as file:
        creds = json.load(file)

    query = '''
    select home_id, home_fid, home, visitor_id, visitor_fid, visitor, hpoints, vpoints, home_elo, visitor_elo, date from elo where (home_fid = {} or visitor_fid = {})
    '''.format(franchiseID, franchiseID)

    data = u.sqlTodf(query, creds)

    elo = getFranchiseElo(franchiseID, data)
    franchiseName = data[data['home_fid'] == franchiseID].iloc[-1]['home']
    plt.plot(data['date'], elo, label = franchiseName)

def compareFranchiseElos(franchisIDs:list) -> None:

    for franchiseID in franchisIDs:
        plotFranchiseElo(franchiseID)

    plt.title("Franchise Elo Comparison")
    plt.legend()
    plt.grid('--')
    plt.show()


def getTeamElo(teamID:int, data:pd.DataFrame) -> list:
    elo = []

    for _, row in data.iterrows():
        if row['home_fid'] == teamID:
            elo.append(row['home_elo'])
        elif row['visitor_fid'] == teamID:
            elo.append(row['visitor_elo'])

    return elo

def plotTeamElo(teamID:int) -> None:

    with open("creds.json") as file:
        creds = json.load(file)

    query = '''
    select home_id, home_fid, home, visitor_id, visitor_fid, visitor, hpoints, vpoints, home_elo, visitor_elo, date from elo where (home_fid = {} or visitor_fid = {})
    '''.format(teamID, teamID)

    data = u.sqlTodf(query, creds)

    elo = getFranchiseElo(teamID, data)
    teamName = data[data['home_id'] == teamID].iloc[-1]['home']
    plt.plot(data['date'], elo, label = teamName)

def compareTeamElos(teamIDS:list) -> None:
    for teamID in teamIDS:
        plotTeamElo(teamID)

    plt.title("Team Elo Comparison")
    plt.legend()
    plt.grid('--')
    plt.show()

ids = [24]
# compareTeamElos(ids)
compareFranchiseElos(ids)
