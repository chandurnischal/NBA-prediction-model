import json
import utils as u
import pandas as pd
import matplotlib.pyplot as plt


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


with open("creds.json") as file:
    creds = json.load(file)

query = """
select a.*, b.team_win_perc from (select * from player_total where year=2023 and Pos = 'PG' and MP > 500) a join (select team_id, `W%` as team_win_perc from conference_standings where year=2023) as b on a.team_id = b.team_id order by a.PTS desc, a.MP desc
"""


data = u.sqlTodf(query, creds)
data.columns = [column.lower() for column in data.columns]
data = data.apply(pd.to_numeric, errors="ignore")
data["PER"] = PER(data)

print(
    data[["pts", "g", "ast", "blk", "trb", "stl", "mp", "PER", "team_win_perc"]].corr(
        method="pearson"
    )["team_win_perc"]
)

data = data[["player", "tm", "PER", "team_win_perc"]]

print(data.head(5), data.tail(5), sep="\n\n")
