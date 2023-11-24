import os
import mysql.connector as mc
import json
from tqdm import tqdm 
from time import perf_counter
import subprocess

start = perf_counter()

with open("creds.json") as file:
    creds = json.load(file)

os.system("python processing/updateDB.py")

dumpFilePath = 'data/latest_dump.sql'

cmd = 'mysqldump --host={} --user={} --password={} {} > {}'.format(creds['host'], creds['user'], creds['password'], creds['database'], dumpFilePath)

try:
    subprocess.run(cmd, shell=True, check=True)
    print('Successfully created SQL dump')
except subprocess.CalledProcessError as e:
    print('Error executing dump')

with open('processing/clean.sql') as file:
    queries = file.readlines()


preprocessQueries = [
                    'create index home_idx on elo(home_id);', 
                    'create index visitor_idx on elo(visitor_id);', 
                    'create index team_idx on team_efficiency(team_id);', 
                    'alter table elo add column home_per decimal(10, 2);', 
                    'update elo a join team_efficiency b on a.home_id = b.team_id and a.season = b.year set a.home_per = b.per;', 
                    'alter table elo add column visitor_per decimal(10, 2);', 
                    'update elo a join team_efficiency b on a.visitor_id = b.team_id and a.season = b.year set a.visitor_per = b.per;',
                    'alter table elo add column home_victory int;',
                    'update elo set home_victory = 1 where mov > 0;',
                    'update elo set home_victory = 0 where mov < 0;'
                    ]

with mc.connect(**creds) as conn:
    cur = conn.cursor()
    conn.autocommit = True

    print("Cleaning data")

    for query in tqdm(queries):
        try:
            cur.execute(query)

        except:
            pass

    os.system("python processing/elo.py")
    os.system("python processing/efficiency.py")
    
    print("Processing data")

    for query in tqdm(preprocessQueries):
        try:
            cur.execute(query)
        except:
            pass

print("\nExecution Time: {}s".format(round(perf_counter() - start, 2)))