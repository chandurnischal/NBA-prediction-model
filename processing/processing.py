import pandas as pd
import os
import numpy as np

def findExtension(folderPath: str, extension: str) -> list:
    files = [os.path.join(root, filename) 
                for root, _, filenames in os.walk(folderPath) 
                    for filename in filenames if filename.endswith(extension)]

    return files

def removeHyphen(data:pd.DataFrame) -> pd.DataFrame:
    columns = data.columns.to_list()

    for column in columns:
        try:
            data[column] = data[column].str.replace("—", "")
            data[column] = data[column].str.replace("*", "")
            data[column] = data[column].astype(float)
        except:
            pass
    return data

def getNickNamesPerYear(year:int) -> dict:

    filePath = ".\\data\\teams\\regular\\teamVteam.csv"
    
    data = pd.read_csv(filePath)
    data = data[data["Year"] == year].dropna(axis=1, how='all')
    del data["Year"]
    n = len(data.index)
    res = dict()
    for i in range(n):
        series = data.iloc[i]
        res[series["Team"]] = series[series.isna()].index.to_list()[0]
        
    return res

def getAllNickNames() -> dict:
    res = dict()
    for year in range(1980, 2024):
        res.update(getNickNamesPerYear(year))

    return res