import json
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVR
import utils as u
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np
from datetime import datetime

with open("creds.json") as file:
    creds = json.load(file)

today = datetime.now()
year = today.year
season = year + 1


def classification(creds: dict):
    query = """
    select * from elo where is_regular=1
    """

    data = u.sqlTodf(query, creds)
    n = len(data.index)
    train = data[data["season"] <= year]
    test = data[data["season"] == season]

    features = ["home_elo", "home_per", "visitor_elo", "visitor_per"]
    label = ["home_victory"]

    trainX, trainY = np.array(train[features]), np.array(train[label]).reshape(-1)
    testX, testY = np.array(test[features]), np.array(test[label]).reshape(-1)

    model = LogisticRegression()
    # model = GaussianNB()
    # model = DecisionTreeClassifier(criterion='entropy')
    # model = SVR(kernel='sigmoid', C=1000)
    res = model.fit(trainX, trainY)

    prediction = model.predict(testX)
    accuracy = accuracy_score(testY, prediction)

    # print("Accuracy: \n", accuracy)
    # print("Classification Report:\n", classification_report(testY, prediction))
    # print("Confusion Matrix:\n", confusion_matrix(testY, prediction))
    # print()

    return model


def filterVector(vector, teamID):
    if not vector[vector["home_id"] == teamID].empty:
        return vector[["home_elo", "home_per"]]
    return vector[["visitor_elo", "visitor_per"]]


def getInputVectors(creds: dict, home_id: int, visitor_id: int, season: int):
    team1Query = """
    select date, home_id, home, home_elo, home_per, visitor_id, visitor, visitor_elo, visitor_per from elo where (home_id = {} or visitor_id = {}) and season={} order by date desc limit 1
    """.format(
        home_id, home_id, season
    )

    team2Query = """
    select home_id, home, home_elo, home_per, visitor_id, visitor, visitor_elo, visitor_per from elo where (home_id = {} or visitor_id = {}) and season={} order by date desc limit 1  
    """.format(
        visitor_id, visitor_id, season
    )

    team1, team2 = u.sqlTodf(team1Query, creds), u.sqlTodf(team2Query, creds)
    home = filterVector(team1, home_id).apply(pd.to_numeric, errors="coerce")
    visitor = filterVector(team2, visitor_id).apply(pd.to_numeric, errors="coerce")

    return pd.DataFrame(
        [home.iloc[0].to_list() + visitor.iloc[0].to_list()],
        columns=["home_elo", "home_per", "visitor_elo", "visitor_per"],
    )


def LogReg(home_id, visitor_id, season):
    input = getInputVectors(creds, home_id, visitor_id, season)
    model = classification(creds)
    probs = model.predict_proba(input.values)[0]

    return probs
