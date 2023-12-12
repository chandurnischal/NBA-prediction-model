import json
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import utils as u
import numpy as np
from datetime import datetime

with open("creds.json") as file:
    creds = json.load(file)


def trainingFunction(creds, homeFeatures, visitorFeatures):
    query = """
    select * from elo where is_regular=1
    """

    data = u.sqlTodf(query, creds)
    train = data[data["season"] <= 2023].apply(pd.to_numeric, errors="ignore")

    features = homeFeatures + visitorFeatures
    label = ["home_victory"]

    trainX, trainY = np.array(train[features]), np.array(train[label]).reshape(-1)
    # scaler = StandardScaler()
    # trainX = scaler.fit_transform(trainX)

    # model = GaussianNB()
    model = LogisticRegression()
    # model = DecisionTreeClassifier(criterion="entropy", random_state=1001, max_depth=5)
    # model = KNeighborsClassifier(n_neighbors=8)
    # model = RandomForestClassifier(n_estimators=100, criterion="entropy", max_depth=5, random_state=1001)

    model.fit(trainX, trainY)

    return model


def getLatestFeature(teamID, homeFeatures, visitorFeatures) -> pd.DataFrame:
    query = """
    select * from elo where season={} and is_regular=1
    """.format(
        datetime.now().year + 1
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


def classify(home_id, visitor_id):
    home_id = int(home_id)
    visitor_id = int(visitor_id)
    homeFeatures = ["home_elo", "home_per", "home_eff", "home_win_perc"]
    visitorFeatures = ["visitor_elo", "visitor_per", "visitor_eff", "visitor_win_perc"]
    model = trainingFunction(creds, homeFeatures, visitorFeatures)
    instance = makeFeature(home_id, visitor_id, homeFeatures, visitorFeatures)
    probs = model.predict_proba(instance)[0]
    return {"NO": round(probs[0], 2), "YES": round(probs[1], 2)}
