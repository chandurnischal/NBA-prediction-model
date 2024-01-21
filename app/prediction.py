import json
import pandas as pd
from sklearn.linear_model import LogisticRegression
import utils as u
import numpy as np
from datetime import datetime
import requests
import joblib

with open("creds.json") as file:
    creds = json.load(file)


def trainingFunction(creds, features):
    query = """
    select * from elo
    """

    data = u.sqlTodf(query, creds)
    train = data.apply(pd.to_numeric, errors="ignore")

    label = ["home_victory"]

    trainX, trainY = np.array(train[features]), np.array(train[label]).reshape(-1)

    model = LogisticRegression()
    model.fit(trainX, trainY)

    return model


def getLatestFeature(teamID, homeFeatures, visitorFeatures) -> pd.DataFrame:
    currentSeason = datetime.now().year + 1

    url = """https://www.basketball-reference.com/leagues/NBA_{}.html""".format(
        currentSeason
    )

    r = requests.get(url)

    if r.status_code != 200:
        currentSeason = currentSeason - 1

    query = """
    select * from elo where season={}
    """.format(
        currentSeason
    )

    data = u.sqlTodf(query, creds)
    data["date"] = pd.to_datetime(data["date"])
    team_games = data[(data["home_id"] == teamID) | (data["visitor_id"] == teamID)]
    latest_game = team_games.loc[team_games["date"].idxmax()]
    if latest_game["home_id"] == teamID:
        points_scored = latest_game[homeFeatures]
    else:
        points_scored = latest_game[visitorFeatures]
    return points_scored


def makeFeature(home_id: int, visitor_id: int, homeFeatures, visitorFeatures):
    home = pd.DataFrame(
        [getLatestFeature(home_id, homeFeatures, visitorFeatures)]
    ).apply(pd.to_numeric, errors="ignore")
    home.columns = homeFeatures
    visitor = pd.DataFrame(
        [getLatestFeature(visitor_id, homeFeatures, visitorFeatures)]
    ).apply(pd.to_numeric, errors="ignore")
    visitor.columns = visitorFeatures
    return np.array([home.values.tolist()[0] + visitor.values.tolist()[0]])


def classifySlow(home_id, visitor_id):
    home_id = int(home_id)
    visitor_id = int(visitor_id)
    homeFeatures = ["home_elo", "home_per", "home_eff", "home_win_perc"]
    visitorFeatures = ["visitor_elo", "visitor_per", "visitor_eff", "visitor_win_perc"]
    model = trainingFunction(creds, homeFeatures, visitorFeatures)
    instance = makeFeature(home_id, visitor_id, homeFeatures, visitorFeatures)
    probs = model.predict_proba(instance)[0]
    return {"NO": round(probs[0], 2), "YES": round(probs[1], 2)}


def classify(home_id, visitor_id):
    home_id = int(home_id)
    visitor_id = int(visitor_id)

    features = ["elo", "per", "eff", "win_perc"]
    homeFeatures = ["home_{}".format(feature) for feature in features]
    visitorFeatures = ["visitor_{}".format(feature) for feature in features]

    instance = makeFeature(home_id, visitor_id, homeFeatures, visitorFeatures)
    params = joblib.load("app/weights.joblib")
    weights = params["weights"]
    intercept = params["intercept"]

    predictions = np.dot(instance, weights[0]) + intercept
    probs = 1 / (1 + np.exp(-predictions))
    yes = round(probs[0], 2)
    no = 1 - yes
    return {"YES": round(yes, 2), "NO": round(no, 2)}
