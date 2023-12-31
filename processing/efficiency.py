import json
from sqlalchemy import create_engine
import mysql.connector as mc
import pandas as pd

with open("creds.json") as file:
    creds = json.load(file)


"""
(PTS + REB + AST + STL + BLK - Missed FG - Missed FT - TO) / GP
"""


def EFF(row) -> float:
    return (
        row["pts"]
        + row["trb"]
        + row["ast"]
        + row["stl"]
        + row["blk"]
        - (row["fga"] - row["fg"])
        - (row["fta"] - row["ft"])
        - row["tov"]
    ) / row["g"]


"""
PER = (FGM x 85.910 + Steals x 53.897 + 3PTM x 51.757 + FTM x 46.845 + Blocks x 39.190 + Offensive_Reb x 39.190 + Assists x 34.677 + Defensive_Reb x 14.707 — Foul x 17.174 — FT_Miss x 20.091 — FG_Miss x 39.190 — TO x 53.897) x (1 / Minutes)
"""


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


with mc.connect(**creds) as conn:
    cur = conn.cursor()

    query = """
    select * from team_total order by year
    """

    cur.execute(query)
    column_names = [column[0] for column in cur.description]
    rows = cur.fetchall()

    data = pd.DataFrame(rows, columns=column_names)
    data.columns = [column.lower() for column in data.columns]

    data["per"] = PER(data)
    data["eff"] = EFF(data)

    from sqlalchemy import create_engine

    engine = create_engine(
        "mysql+mysqlconnector://{}:{}@{}/{}".format(
            creds["user"], creds["password"], creds["host"], creds["database"]
        )
    )
    data.to_sql(name="team_efficiency", index=False, con=engine, if_exists="replace")
