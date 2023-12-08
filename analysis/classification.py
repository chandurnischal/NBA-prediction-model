import json
import pandas as pd
from sklearn.naive_bayes import GaussianNB
import utils as u
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np
from sklearn.model_selection import train_test_split
from datetime import datetime

with open("creds.json") as file:
    creds = json.load(file)

def classify(creds:dict):
    query = """
    select * from elo where is_regular=1
    """

    data = u.sqlTodf(query, creds)
    # train = data[data["season"] <= 2023].apply(pd.to_numeric, errors="ignore")
    # test = data[data["season"] == 2024].apply(pd.to_numeric, errors="ignore")

    train, test = train_test_split(data, test_size=0.2, random_state=1001)

    features = ["home_elo", "home_per", "home_eff", "visitor_elo", "visitor_per", "visitor_eff"]
    label = ["home_victory"]

    trainX, trainY = np.array(train[features]), np.array(train[label]).reshape(-1)
    testX, testY = np.array(test[features]), np.array(test[label]).reshape(-1)

    model = GaussianNB()
    res = model.fit(trainX, trainY)

    prediction = model.predict(testX)
    accuracy = accuracy_score(testY, prediction)

    print("Accuracy: \n", accuracy)
    print("Classification Report:\n", classification_report(testY, prediction))
    print("Confusion Matrix:\n", confusion_matrix(testY, prediction))

    return model

def getLatestFeature(teamID:int) -> pd.DataFrame:

    query = '''
    select * from elo where season={}
    '''.format(datetime.now().year + 1)

    data = u.sqlTodf(query, creds)
    data['date'] = pd.to_datetime(data['date'])
    team_games = data[(data['home_id'] == teamID) | (data['visitor_id'] == teamID)]
    latest_game = team_games.loc[team_games['date'].idxmax()]
    if latest_game['home_id'] == teamID:
        points_scored = latest_game[['home_per', 'home_eff', 'home_elo']]
    else:
        points_scored = latest_game[['visitor_per', 'visitor_eff', 'visitor_elo']]
    return points_scored

def makeFeature(home_id:int, visitor_id:int):
    home_features = pd.DataFrame([getLatestFeature(home_id)]).apply(pd.to_numeric, errors="ignore")
    home_features.columns = ['home_per', 'home_eff', 'home_elo']
    visitor_features = pd.DataFrame([getLatestFeature(visitor_id)]).apply(pd.to_numeric, errors="ignore")
    visitor_features.columns = ['visitor_per', 'visitor_eff', 'visitor_elo']
    return np.array([home_features.values.tolist()[0] + visitor_features.values.tolist()[0]])

home_id, visitor_id = 11, 2
model = classify(creds)
instance = makeFeature(home_id, visitor_id)
print(model.predict(instance))