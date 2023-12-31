import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel('data/tracker.xlsx')
data = data[['date', 'outcome']]
# data['date'] = pd.to_datetime(data['date'], errors='raise')
dailies = data.groupby(['date', 'outcome']).size().unstack()

dailies['acc'] = round(dailies['C'] * 100 / (dailies['C'] + dailies['I']), 2)
mean = dailies['acc'].mean()

print(dailies)

plt.title('Daily Accuracy')
plt.xlabel('Date')
plt.ylabel('Accuracy')
plt.axhline(mean, c='k', label='Mean', linestyle='--')
plt.plot(dailies.index, dailies['acc'])
plt.grid(linestyle='--')
plt.show()