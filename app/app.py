import json
from datetime import datetime
from flask import Flask, render_template
import prediction as p
import time
from tqdm import tqdm
import warnings
import utils as u

warnings.filterwarnings("ignore")

today = datetime.now()
todayDate = today.strftime("%Y-%m-%d")

with open("creds.json") as file:
    creds = json.load(file)

query = """
select home_id, home, visitor_id, visitor from games where date = '{}'
""".format(
    todayDate
)

data = u.sqlTodf(query, creds).astype(str)

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

    logos = u.sqlTodf(logoQuery, creds)

    teamQuery = """
    select * from conference_standings where team_id in ({}, {}) and year = (select max(year) from conference_standings) order by (team_id = {}) desc, team_id;
    """.format(
        home_id, visitor_id, home_id
    )

    team = u.sqlTodf(teamQuery, creds).reset_index()

    home_team, visitor_team = (
        logos[logos["ID"] == int(home_id)]["Team"].iloc[0],
        logos[logos["ID"] == int(visitor_id)]["Team"].iloc[0],
    )

    playerQuery = """
    select player, team_id, tm, pos, pts, ast, blk, trb, stl, mp from player_per_game where team_id in ({}, {}) and is_regular=1 and year = (select max(year) from player_per_game) order by per desc
    """.format(
        home_id, visitor_id
    )

    players = u.sqlTodf(playerQuery, creds)

    homePlayers = (
        players[players["team_id"] == int(home_id)].reset_index(drop=True).head(7)
    )

    visitorPlayers = (
        players[players["team_id"] == int(visitor_id)].reset_index(drop=True).head(7)
    )

    arenaQuery = """
    select arena from games where home_id = {} order by date desc limit 1
    """.format(
        home_id
    )

    arena = u.sqlTodf(arenaQuery, creds).iloc[0].values[0]

    c1, c2 = u.themeExtractor(home_id), u.themeExtractor(visitor_id)

    if (c1[0] - c2[0]) + (c1[1] - c2[1]) + (c1[2] - c2[2]) <= 50:
        c1 = u.themeExtractor(home_id, 2)

    if c1 == (255, 255, 255):
        c1 = u.themeExtractor(home_id, 2)

    if c2 == (255, 255, 255):
        c2 = u.themeExtractor(visitor_id, 2)

    color1 = "rgb({}, {}, {})".format(c1[0], c1[1], c1[2])
    color2 = "rgb({}, {}, {})".format(c2[0], c2[1], c2[2])

    probs = p.classify(home_id, visitor_id)

    homeHistory = u.getTeamHistory(int(home_id), creds)[::-1]
    visitorHistory = u.getTeamHistory(int(visitor_id), creds)[::-1]

    end = time.time()

    latency = round(end - start, 2)

    app.logger.info("Latency: {}s".format(latency))

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
        winPerc=int(probs["YES"] * 100),
        lossPerc=int((1 - probs["YES"]) * 100),
        homeHistory = homeHistory,
        visitorHistory = visitorHistory
    )


@app.route("/summary")
def summary():
    n = len(data.index)

    yes, no = [], []
    hcolor, vcolor = [], []

    for _, row in tqdm(data.iterrows(), total=n, desc="Processing games", unit="game"):
        home_id, visitor_id = row["home_id"], row["visitor_id"]
        outcome = p.classify(home_id, visitor_id)
        c1, c2 = u.themeExtractor(home_id), u.themeExtractor(visitor_id)

        if (c1[0] - c2[0]) + (c1[1] - c2[1]) + (c1[2] - c2[2]) <= 20:
            c1 = u.themeExtractor(home_id, 2)

        if c1 == (255, 255, 255):
            c1 = u.themeExtractor(home_id, 2)

        if c2 == (255, 255, 255):
            c2 = u.themeExtractor(visitor_id, 2)

        color1 = "rgb({}, {}, {})".format(c1[0], c1[1], c1[2])
        color2 = "rgb({}, {}, {})".format(c2[0], c2[1], c2[2])
        hcolor.append(color1)
        vcolor.append(color2)

        yes.append(round(outcome["YES"] * 100))
        no.append(round(outcome["NO"] * 100))

    data["hcolor"] = hcolor
    data["vcolor"] = vcolor
    data["YES"] = yes
    data["NO"] = no

    return render_template("summary.html", date=formattedDate, data=data)


if __name__ == "__main__":
    app.run(debug=True)
