import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data = pd.read_excel('data/tracker.xlsx')
data = data[["Probability of Victory", "C", "I", "T", "Accuracy"]]
data = data.dropna()
n = len(data.index)

sns.set_style('darkgrid')


melted = pd.melt(data[["Probability of Victory", "C", "I"]], id_vars=['Probability of Victory'], var_name='Outcome', value_name='Value')

plt.figure(figsize=(15, 7))
sns.barplot(data=melted, x='Probability of Victory', y='Value', hue='Outcome')
plt.title('Probability of Victory vs C and I')
plt.xlabel('Probability of Victory')
plt.ylabel('Outcome')
plt.tight_layout()

plt.figure(figsize=(15, 7))
sns.barplot(data=data, x="Probability of Victory", y="Accuracy")
plt.title('Accuracy of Outcome')
plt.xlabel('Probability of Victory')
plt.ylabel('Accuracy')

for i in range(n):
    plt.text(x=data["Probability of Victory"].iloc[i], y=data["Accuracy"].iloc[i], s="{}%".format(data["Accuracy"].iloc[i]), ha="center", va = "bottom")

plt.show()

print(melted)