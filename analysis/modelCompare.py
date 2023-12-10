import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('analysis/model.csv')

plt.figure()
plt.plot(data['accuracy'], label="accuracy")
plt.plot(data['latency'], label="latency")
plt.legend()
plt.grid()
plt.show()