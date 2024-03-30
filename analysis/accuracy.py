import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

data = pd.read_excel("data/tracker.xlsx")
data = data[["date", "acc"]]
x = [i + 1 for i in data.index]
median = np.median(data['acc'])

lastIndex, lastElement = data.index[-1], data["acc"].iloc[-1]

sns.set_style('darkgrid')
plt.figure(figsize=(10, 7))
sns.lineplot(x=x, y=data['acc'])
plt.title("Cumulative Accuracy")
plt.xlabel("Matches")
plt.ylabel("Cumulative Accuracy")
plt.axhline(y=median, c = 'k')
plt.text(lastIndex, lastElement, "{}%".format(lastElement), ha="left", va="top")
plt.show()
