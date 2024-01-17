import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("data/tracker.xlsx")
data = data[["date", "acc"]]
x = [i + 1 for i in data.index]

lastIndex, lastElement = data.index[-1], data["acc"].iloc[-1]

plt.figure(figsize=(10, 7))
plt.plot(x, data["acc"])
plt.title("Cumulative Accuracy")
plt.xlabel("Matches")
plt.ylabel("Cumulative Accuracy")
plt.text(lastIndex, lastElement, "{}%".format(lastElement), ha="left", va="top")
plt.show()
