from datetime import datetime, timedelta
import os
from time import perf_counter
import utils as u
import json


def updateDB():
    start = perf_counter()
    os.system("python processing/load.py")
    os.system("python processing/clean.py")

    print("Execution Time: {} minutes".format(round((perf_counter() - start) / 60, 1)))


yest = datetime.now() - timedelta(1)
yest = datetime.strftime(yest, "%Y-%m-%d")

with open("creds.json") as file:
    creds = json.load(file)

query = """
select * from games where date='{}' and vpoints != ''
""".format(
    yest
)

try:
    data = u.sqlTodf(query, creds)
    if data.empty:
        updateDB()
    else:
        print("Database up to date.")
except:
    updateDB()
