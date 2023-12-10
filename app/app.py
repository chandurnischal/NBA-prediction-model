import mysql.connector as mc
import json
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, render_template
from PIL import Image
from collections import Counter
import prediction as p
import time

def themeExtractor(teamID, common:int = 1):
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


def sqlTodf(query: str, creds: dict) -> pd.DataFrame:
    with mc.connect(**creds) as conn:
        cur = conn.cursor()

        cur.execute(query)
        column_names = [column[0] for column in cur.description]
        rows = cur.fetchall()

    data = pd.DataFrame(rows, columns=column_names)

    return data


today = datetime.now() + timedelta(1)
todayDate = today.strftime("%Y-%m-%d")
year = today.year + 1

with open("creds.json") as file:
    creds = json.load(file)

query = """
select home_id, home, visitor_id, visitor from games where date = '{}'
""".format(
    todayDate
)

data = sqlTodf(query, creds).astype(str)

app = Flask(__name__)

formattedDate = datetime.now().strftime("%d %B %Y")

@app.route("/")
def today():
    return render_template(
        "index.html", columns=data.columns, df=data, date=formattedDate
    )


@app.route("/game/<home_id>/<visitor_id>")
def game(home_id, visitor_id):
    start = time.time()

    logoQuery = """
    select * from abbrev where id in ({}, {})
    """.format(
        home_id, visitor_id
    )

    logos = sqlTodf(logoQuery, creds)

    teamQuery = """
    select * from conference_standings where team_id in ({}, {}) and year = (select max(year) from conference_standings)
    """.format(
        home_id, visitor_id
    )

    team = sqlTodf(teamQuery, creds).reset_index()

    home_team, visitor_team = (
        logos[logos["ID"] == int(home_id)]["Team"].iloc[0],
        logos[logos["ID"] == int(visitor_id)]["Team"].iloc[0],
    )

    playerQuery = """
    select player, team_id, tm, pos, pts, ast, blk, trb, stl, mp from player_per_game where team_id in ({}, {}) and is_regular=1 and year = (select max(year) from player_per_game) order by pts desc
    """.format(
        home_id, visitor_id
    )

    players = sqlTodf(playerQuery, creds)

    homePlayers = (
        players[players["team_id"] == int(home_id)].reset_index(drop=True).head(5)
    )

    visitorPlayers = (
        players[players["team_id"] == int(visitor_id)].reset_index(drop=True).head(5)
    )

    arenaQuery = '''
    select arena from games where home_id = {} order by date desc limit 1
    '''.format(home_id)

    arena = sqlTodf(arenaQuery, creds).iloc[0].values[0]

    c1, c2 = themeExtractor(home_id), themeExtractor(visitor_id)

    if (c1[0] - c2[0]) + (c1[1] - c2[1]) + (c1[2] - c2[2]) <= 10:
        c1 = themeExtractor(home_id, 2)

    if c1 == (255,255, 255):
        c1 = themeExtractor(home_id, 2)

    if c2 == (255, 255, 255):
        c2 = themeExtractor(visitor_id, 2)

    color1 = "rgb({}, {}, {})".format(c1[0], c1[1], c1[2])
    color2 = "rgb({}, {}, {})".format(c2[0], c2[1], c2[2])

    probs = p.classify(home_id, visitor_id)

    end = time.time()

    latency = end - start

    app.logger.info('Latency: {}s'.format(latency))

    return render_template(
        "game.html",
        home_id=home_id,
        visitor_id=visitor_id,
        home_team=home_team,
        visitor_team=visitor_team,
        arena=arena,
        team=team,
        home_players=homePlayers,
        visitor_players=visitorPlayers,
        date=formattedDate,
        color1=color1,
        color2=color2,
        winPerc=int(probs['YES'] * 100),
        lossPerc=int(probs['NO'] * 100),
    )


if __name__ == "__main__":
    app.run(debug=True)
