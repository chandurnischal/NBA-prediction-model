import os
import mysql.connector as mc
import json
from tqdm import tqdm
import subprocess

with open("creds.json") as file:
    creds = json.load(file)

os.system("python processing/updateDB.py")

dumpFilePath = "data/latest_dump.sql"

cmd = "mysqldump --host={} --user={} --password={} {} > {}".format(
    creds["host"], creds["user"], creds["password"], creds["database"], dumpFilePath
)

try:
    subprocess.run(cmd, shell=True, check=True)
    print("Successfully created SQL dump")
except subprocess.CalledProcessError as e:
    print("Error executing dump")

with open("processing/clean.sql") as file:
    queries = file.readlines()


with open("processing/preprocess.sql") as file:
    preprocessQueries = file.readlines()

with mc.connect(**creds) as conn:
    cur = conn.cursor()
    conn.autocommit = True

    for query in tqdm(queries, desc="Cleaning Data", unit="query"):
        try:
            cur.execute(query)

        except:
            pass

    os.system("python processing/elo.py")
    os.system("python processing/efficiency.py")

    for query in tqdm(preprocessQueries, desc="Cleaning Data", unit="query"):
        try:
            cur.execute(query)
        except:
            pass
