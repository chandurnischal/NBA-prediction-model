from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
import joblib
import utils as u
import json 

def trainModel(creds, features):
    query = """
    select * from elo
    """

    data = u.sqlTodf(query, creds)
    train = data.apply(pd.to_numeric, errors="ignore")

    features = ['home_{}'.format(feature) for feature in features] + ['visitor_{}'.format(feature) for feature in features]
    
    label = ["home_victory"]

    trainX, trainY = np.array(train[features]), np.array(train[label]).reshape(-1)
    
    model = LogisticRegression()

    model.fit(trainX, trainY)
    params = {'weights': model.coef_, "intercept": model.intercept_}
    joblib.dump(params, 'app/weights.joblib')

    return None

with open('creds.json') as file:
    creds = json.load(file)

print('Training model...')
features = ["elo", "per", "eff", "win_perc"]
trainModel(creds, features)