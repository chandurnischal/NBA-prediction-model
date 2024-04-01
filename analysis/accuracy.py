import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

data = pd.read_excel("data/tracker.xlsx")
data = data[["date", "acc"]]
x = [i + 1 for i in data.index]
mean = np.mean(data['acc'])

lastIndex, lastElement = data.index[-1], data["acc"].iloc[-1]

sns.set_style('darkgrid')
plt.figure(figsize=(10, 7))
sns.lineplot(x=x, y=data['acc'])
plt.text(x=-25, y=mean, s='{}%'.format(round(mean, 1)), ha='left', va='bottom')
plt.title("Cumulative Accuracy")
plt.xlabel("Matches")
plt.ylabel("Cumulative Accuracy")
plt.axhline(y=mean, c = 'k')
plt.text(lastIndex, lastElement, "{}%".format(lastElement), ha="left", va="top")
plt.show()
