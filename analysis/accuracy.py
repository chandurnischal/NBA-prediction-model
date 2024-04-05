import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

data = pd.read_excel("data/tracker.xlsx")
data = data.dropna(subset=["outcome"])
data = data[["date", "acc"]]
x = [i + 1 for i in data.index]

lastIndex, lastElement = data.index[-1], data["acc"].iloc[-1]

sns.set_style('darkgrid')
plt.figure(figsize=(10, 7))
sns.lineplot(x=x, y=data['acc'])
plt.title("Cumulative Accuracy")
plt.xlabel("Matches")
plt.ylabel("Cumulative Accuracy")
plt.text(lastIndex, lastElement, "{}%".format(lastElement), ha="left", va="top")
plt.show()
