import pandas as pd
from scipy.stats import pointbiserialr
import json
import utils as u

with open("creds.json") as file:
    creds = json.load(file)

homeFeatures = [
    "home_elo",
    "home_per",
    "home_eff",
    "home_win_perc",
    "home_ppg",
    "home_pag",
    "hpoints",
]
visitorFeatures = [
    "visitor_elo",
    "visitor_per",
    "visitor_eff",
    "visitor_win_perc",
    "visitor_ppg",
    "visitor_pag",
    "vpoints",
]


features = homeFeatures + visitorFeatures

query = """
select * from elo where season=2024
"""

data = u.sqlTodf(query, creds).apply(pd.to_numeric, errors="ignore")

data["CategoricalColumn"] = pd.Categorical(data["home_victory"]).codes

rows = []

for feature in features:
    correlation_coefficient, p_value = pointbiserialr(
        data[feature], data["CategoricalColumn"]
    )
    rows.append([feature, correlation_coefficient, p_value])


corr = (
    pd.DataFrame(rows, columns=["feature", "correlation", "p_value"])
    .sort_values(by=["correlation"], ascending=False)
    .reset_index(drop=True)
)
corr.to_csv("analysis/correlation_data.csv", index=False)
