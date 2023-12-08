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

    print("Cleaning data")

    for query in tqdm(queries):
        try:
            cur.execute(query)

        except:
            pass

    print("Calculating Elo")
    os.system("python processing/elo.py")
    print("Calculating Efficiency")
    os.system("python processing/efficiency.py")

    print("Processing data")

    for query in tqdm(preprocessQueries):
        try:
            cur.execute(query)
        except:
            pass
