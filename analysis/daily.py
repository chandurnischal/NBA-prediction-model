import pandas as pd
import matplotlib.pyplot as plt


days = 15
data = pd.read_excel("data/tracker.xlsx")[["date", "daily"]]
data["date"] = pd.to_datetime(data["date"])
dates = data["date"].value_counts(sort=False)
data = data.dropna().reset_index(drop=True)
mean = data["daily"].mean()

data = data.head(days)

n = len(data.index)

plt.bar(data["date"], data["daily"])

for i in range(n):
    plt.text(
        data["date"].iloc[i],
        data["daily"].iloc[i] / 2,
        dates[data["date"].iloc[i]],
        va="bottom",
        ha="center",
    )
    plt.text(
        data["date"].iloc[i],
        data["daily"].iloc[i],
        "{}%".format(data["daily"].iloc[i]),
        va="bottom",
        ha="center",
    )

plt.title("Daily Predictions (Last 15 days)".format(days))
plt.ylabel("Accuracy")
plt.xlabel("Date")
plt.axhline(mean, c="k")
plt.grid(linestyle="--")
plt.show()
