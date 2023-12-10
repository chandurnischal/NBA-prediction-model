import json
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
import utils as u
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

def classifier(features, label):


    query = """
    select * from elo where is_regular=1
    """

    data = u.sqlTodf(query, creds).apply(pd.to_numeric, errors="ignore")

    train = data[data["season"] <= 2023].apply(pd.to_numeric, errors="ignore")
    test = data[data["season"] == 2024].apply(pd.to_numeric, errors="ignore")

    trainX, trainY = np.array(train[features]), np.array(train[label]).reshape(-1)
    testX, testY = np.array(test[features]), np.array(test[label]).reshape(-1)
    # scaler = StandardScaler()
    # trainX = scaler.fit_transform(trainX)
    # testX = scaler.fit_transform(testX)


    # model = GaussianNB()
    model = LogisticRegression()
    # model = DecisionTreeClassifier(criterion="entropy", random_state=1001, max_depth=5)
    # model = KNeighborsClassifier(n_neighbors=6)
    # model = RandomForestClassifier(n_estimators=100, criterion="entropy", max_depth=5, random_state=1001)

    model.fit(trainX, trainY)
    prediction = model.predict(testX)
    classficationReport = classification_report(testY, prediction, output_dict=True)
    return classficationReport

with open("creds.json") as file:
    creds = json.load(file)

homeFeatures = ['home_elo', 'home_per', 'home_eff', 'home_win_perc']
visitorFeatures = ['visitor_elo', 'visitor_per', 'visitor_eff', 'visitor_win_perc']
features = homeFeatures + visitorFeatures
report = classifier(features, "home_victory")

output = {'accuracy': report['accuracy']}
output.update(report['weighted avg'])

for o in output:
    print(o, ": ", output[o])