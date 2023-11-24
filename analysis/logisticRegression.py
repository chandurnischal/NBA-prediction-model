import sys
sys.path.append('analysis/utils.py')
import analysis.utils as u
import json
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

with open("creds.json") as file:
    creds = json.load(file)

query = '''
select * from elo
'''
data = u.sqlTodf(query, creds)

win_per = {team: 0 for team in set(data['home']) | set(data['visitor'])}


home_win_list = []
visitor_win_list = []
 
for index, row in data.iterrows():
    home = row['home']
    visitor = row['visitor']

    home_win = win_per[home]
    away_win = win_per[visitor]

    W_home = 1 if row['mov'] > 0 else 0
    W_away = 1 - W_home   

    total_home_win = home_win + W_home
    total_away_win = away_win + W_away 

    home_per = total_home_win / (total_home_win + total_away_win)
    away_per = total_away_win / (total_home_win + total_away_win)

    win_per[home] = home_per
    win_per[visitor] = away_per

    home_win_list.append(home_per)
    visitor_win_list.append(away_per)

data['home_win_percentage'] = home_win_list
data['visitor_win_percentage'] = visitor_win_list


X = data[['home_elo', 'home_win_percentage', 'home_per', 'visitor_elo', 'visitor_win_percentage', 'visitor_per']]
y = data['home_victory']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 1001)

model = LogisticRegression()
model.fit(X_train, y_train)
prediction = model.predict(X_test)

print("Confusion: {}\n\n".format(confusion_matrix(y_test, prediction)))
print("Accuracy: {}\n\n".format(accuracy_score(y_test, prediction)))
print("\nClassification Report:\n", classification_report(y_test, prediction))