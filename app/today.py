import json
import utils as u
from prediction import classify
from datetime import datetime
from tqdm import tqdm

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
n = len(data.index)

outcomeDict = {}

winner, prob = [], []
for index, row in tqdm(data.iterrows(), total=n, desc="Predicting games", unit="game"):
    home_id, visitor_id = row["home_id"], row["visitor_id"]
    outcome = classify(home_id, visitor_id)
    outcomeDict[index] = {
        "home": {"id": home_id, "prob": outcome["YES"]},
        "visitor": {"id": visitor_id, "prob": outcome["NO"]},
    }
    if outcome["YES"] >= outcome["NO"]:
        winner.append(row["home"])
        prob.append(round(outcome["YES"] * 100))
    else:
        winner.append(row["visitor"])
        prob.append(round(outcome["NO"] * 100))


with open("app/today.json", "w") as file:
    outcomeJSON = json.dump(outcomeDict, file, indent=2)

data["date"] = todayDate
data["winner"] = winner
data["probability"] = prob

data[["date", "home", "visitor", "winner", "probability"]].to_csv(
    "data/today.csv", index=False
)
