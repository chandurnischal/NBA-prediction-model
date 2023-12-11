import json
import pandas as pd
import numpy as np
import utils as u
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error

with open("creds.json") as file:
    creds = json.load(file)

homeFeatures = ["home_elo", "home_per", "home_eff", "home_win_perc"]
visitorFeatures = ["visitor_elo", "visitor_per", "visitor_eff", "visitor_win_perc"]
features = homeFeatures + visitorFeatures
label = "mov"

query = """
select * from elo where is_regular=1
"""

data = u.sqlTodf(query, creds).apply(pd.to_numeric, errors="ignore")

train = data[data["season"] <= 2023].apply(pd.to_numeric, errors="ignore")
test = data[data["season"] == 2024].apply(pd.to_numeric, errors="ignore")

trainX, trainY = np.array(train[features]), np.array(train[label]).reshape(-1)
testX, testY = np.array(test[features]), np.array(test[label]).reshape(-1)

polyFeatures = PolynomialFeatures(degree=1)
trainX = polyFeatures.fit_transform(trainX)
model = LinearRegression()
model.fit(trainX, trainY)
testX = polyFeatures.transform(testX)
prediction = model.predict(testX)
print("Mean Squared Error: ", mean_squared_error(testY, prediction))
