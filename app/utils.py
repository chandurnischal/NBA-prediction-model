import mysql.connector as mc
import pandas as pd
from PIL import Image
from collections import Counter


def sqlTodf(query: str, creds: dict) -> pd.DataFrame:
    with mc.connect(**creds) as conn:
        cur = conn.cursor()

        cur.execute(query)
        column_names = [column[0] for column in cur.description]
        rows = cur.fetchall()

    data = pd.DataFrame(rows, columns=column_names)

    return data


def themeExtractor(teamID, common: int = 1):
    img = Image.open("app/static/logos/{}.png".format(teamID))
    img_rgb = img.convert("RGB")
    pixel_values = list(img_rgb.getdata())
    non_zero_pixel_values = [
        pixel
        for pixel in pixel_values
        if pixel != (0, 0, 0) and pixel != (255, 255, 255)
    ]

    color_counter = Counter(non_zero_pixel_values)
    themeExtractor = color_counter.most_common(2)[common - 1][0]

    return themeExtractor


def getTeamHistory(team_id: int, creds: dict) -> list:
    query = """
    select date, home_id, home, hpoints, visitor_id, visitor, vpoints, home_victory from elo where home_id = {} or visitor_id = {} order by date desc limit 10
    """.format(
        team_id, team_id
    )

    data = sqlTodf(creds=creds, query=query)
    w, l = "green", "red"
    colors = []

    for _, row in data.iterrows():
        if row["home_id"] == team_id:
            if row["home_victory"] == "YES":
                colors.append(w)
            else:
                colors.append(l)
        else:
            if row["home_victory"] == "NO":
                colors.append(w)
            else:
                colors.append(l)

    data["color"] = colors
    return colors


def getPlayerHistory(player_id: int, creds: dict) -> pd.DataFrame:
    query = """
    select * from (select * from player_per_game where player_id = {} order by year desc) a join (select max(year) as latest from player_per_game) b;
    """.format(
        player_id
    )

    data = sqlTodf(query, creds)
    data = data[~(data["Tm"] == "TOT")]

    teams = (
        data.groupby(by="team_id")
        .agg(start=("Year", "min"), end=("Year", "max"))
        .reset_index()
    )
    teams = teams.sort_values(by=["end"])
    teams["latest"] = data["latest"].iloc[0]
    return data, teams


def getTopEntity(data: pd.DataFrame, feature: str) -> pd.DataFrame:
    return data.sort_values(by=feature, ascending=False).reset_index(drop=True)


def getRank(data: pd.DataFrame, id: int, type: str) -> dict:
    keyList = ["PTS", "AST", "BLK", "TRB", "STL"]
    res = {
        "league": {key: None for key in keyList},
        "conference": {key: None for key in keyList},
    }

    c = data[data["{}_id".format(type)] == id]["conf"].iloc[0]
    confData = data[data["conf"] == c]

    for key in keyList:
        league = getTopEntity(data, key)
        conf = getTopEntity(confData, key)
        res["league"][key] = league[league["{}_id".format(type)] == id].index[0] + 1
        res["conference"][key] = conf[conf["{}_id".format(type)] == id].index[0] + 1
    return res


def getPlayerRank(player_id: int, creds: dict) -> dict:
    query = """
    select * from player_per_game where year=(select max(year) from player_per_game where player_id={});
    """.format(
        player_id
    )

    data = sqlTodf(query, creds)
    data["Tm"] = data.groupby("Player")["Tm"].transform("last")
    data['conf'] = data.groupby("Player")["conf"].transform("last")
    data = data.drop_duplicates(["Player"])

    return getRank(data, player_id, "player")


def getTeamRank(team_id: int, creds: dict) -> dict:
    query = """
    select * from team_per_game where year = (select max(year) from team_per_game where team_id={});
    """.format(
        team_id
    )

    data = sqlTodf(query, creds)

    return getRank(data, team_id, "team")
