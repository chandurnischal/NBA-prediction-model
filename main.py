import sys
sys.path.append("extraction/extraction")
import extraction.extraction as e
import pandas as pd

team = e.Teams("regular"), e.Teams("playoffs")

dataList = []


dataList.append(team[0].totalStats(2023))

dataList.append(team[1].totalStats(2023))

data = pd.concat(dataList)

print(data)