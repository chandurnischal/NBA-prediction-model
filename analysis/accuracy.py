import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

def plotLine(data:pd.DataFrame, n:int=-1):
    data = data.dropna(subset=["outcome"])
    length = len(data.index)
    if n != -1 or n >= length:
        data = data.tail(n)
    data = data[["date", "acc"]]
    x = [i + 1 for i in data.index]

    lastIndex, lastElement = data.index[-1], data["acc"].iloc[-1]

    sns.set_style('darkgrid')
    plt.figure(figsize=(10, 7))
    sns.lineplot(x=x, y=data['acc'])
    if n == -1 or n >= length:
        plt.title("Cumulative Accuracy")
    else:
        plt.title("Cumulative Accuracy (Last {} Games)".format(n))

    plt.xlabel("Matches")
    plt.ylabel("Cumulative Accuracy")
    plt.text(lastIndex, lastElement, "{}%".format(lastElement), ha="left", va="top")
    plt.show()

try:
    n = int(sys.argv[1])
    data = pd.read_excel("data/tracker.xlsx")
    plotLine(data, n)
except:
    data = pd.read_excel("data/tracker.xlsx")
    plotLine(data)
