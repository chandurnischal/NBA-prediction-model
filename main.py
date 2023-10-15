import pandas as pd
import sys
sys.path.append("extraction/extraction.py")
import extraction.extraction as e
sys.path.append("processing/processing")
import processing.processing as p


games = e.Games()


with open("error.txt", "w", encoding='utf-8') as file:

    for year in range(1980, 2024):
        try:
            schedule = games.seasonSchedule(year)   
            schedule.to_csv("data\\games\\{}_schedule.csv".format(year), index=False)
        except Exception as e:
            file.write("{},{}\n".format(year, e.__class__))

