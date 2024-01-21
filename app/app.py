import json
from datetime import datetime
from flask import Flask, render_template
import prediction as p
import time
from tqdm import tqdm
import warnings
import utils as u
import matplotlib.pyplot as plt

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
    start = time.perf_counter()

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
    select player_id, player, team_id, tm, pos, pts, ast, blk, trb, stl, mp from player_per_game where team_id in ({}, {}) and is_regular=1 and year = (select max(year) from player_per_game) order by per desc
    """.format(
        home_id, visitor_id
    )

    players = u.sqlTodf(playerQuery, creds)

    homePlayers = (
        players[players["team_id"] == int(home_id)].reset_index(drop=True).head(5)
    )

    visitorPlayers = (
        players[players["team_id"] == int(visitor_id)].reset_index(drop=True).head(5)
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
    winPerc = probs["YES"] * 100
    lossPerc = 100 - winPerc
    homeHistory = u.getTeamHistory(int(home_id), creds)[::-1]
    visitorHistory = u.getTeamHistory(int(visitor_id), creds)[::-1]

    end = time.perf_counter()

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
        winPerc=int(winPerc),
        lossPerc=int(lossPerc),
        homeHistory=homeHistory,
        visitorHistory=visitorHistory,
    )

@app.route('/summary')
def summary():
    start = time.perf_counter()
    yes, no = [], []
    hcolor, vcolor = [], []

    with open('app/today.json') as file:
        outcomes = json.load(file)
    
    for _, value in outcomes.items():
        home_id, visitor_id = int(value['home']['id']), int(value['visitor']['id'])
        outcome = {'YES': value['home']['prob'], 'NO': value['visitor']['prob']}
        c1, c2 = u.themeExtractor(home_id), u.themeExtractor(visitor_id)

        if (c1[0] - c2[0]) + (c1[1] - c2[1]) + (c1[2] - c2[2]) <= 50:
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
    end = time.perf_counter()
    latency = round(end - start, 2)
    app.logger.info('Latency: {}'.format(latency))

    return render_template("summary.html", date=formattedDate, data=data) 


@app.route("/team/<team_id>")
def team(team_id):
    teamQuery = """
    select * from team_per_game where year= (select max(year) from team_per_game where team_id = {}) and team_id={};    
    """.format(
        team_id, team_id
    )

    team = u.sqlTodf(teamQuery, creds)

    playerQuery = """
    select * from player_per_game where year=(select max(year) from team_total where team_id = {}) and team_id={} order by pts desc, g desc;
    """.format(
        team_id, team_id
    )

    player = u.sqlTodf(playerQuery, creds)

    leagueQuery = """
    select * from conference_standings where year = (select max(year) from conference_standings where team_id={})
    """.format(
        team_id
    )

    league = u.sqlTodf(leagueQuery, creds)

    region = league[league["team_id"] == int(team_id)]["conf"].iloc[0]

    conf = league[league["conf"] == region].reset_index(drop=True)

    if region == "W":
        note = "Western"
    else:
        note = "Eastern"

    league = league.sort_values(by="W%", ascending=False).reset_index(drop=True)
    leaguePos = league[league["team_id"] == int(team_id)].index[0]
    conf = conf.sort_values(by="W%", ascending=False).reset_index(drop=True)
    confPos = conf[conf["team_id"] == int(team_id)].index[0]
    teamRow = league[league["team_id"] == int(team_id)]

    return render_template(
        "team.html",
        team=team,
        player=player.head(10),
        note=note,
        leaguePos=leaguePos,
        confPos=confPos,
        teamRow=teamRow,
    )


@app.route("/conference")
def conference():
    conferenceQuery = """
    select * from conference_standings where year=(select max(year) from conference_standings)
    """

    conf = u.sqlTodf(conferenceQuery, creds)
    year = conf["Year"].iloc[0]
    east = conf[conf["conf"] == "E"].reset_index(drop=True)
    west = conf[conf["conf"] == "W"].reset_index(drop=True)

    east = east.sort_values(by="W%", ascending=False).reset_index(drop=True)
    west = west.sort_values(by="W%", ascending=False).reset_index(drop=True)

    return render_template("conference.html", east=east, west=west, year=year)


@app.route("/players")
def players():
    return render_template("players.html")


@app.route("/player/<player_id>")
def player(player_id):
    data, teams = u.getPlayerHistory(int(player_id), creds)

    data = data.sort_values(by=['Year'], ascending=False)

    regular, playoffs = data[data["is_regular"] == 1].reset_index(drop=True), data[
        data["is_regular"] == 0
    ].reset_index(drop=True)
    name = data["Player"].iloc[0]
    return render_template("player.html", name=name, teams=teams, regular=regular, playoffs=playoffs)


if __name__ == "__main__":
    app.run(debug=True)
